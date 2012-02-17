import os
import time
from urllib import quote_plus

from pyramid.httpexceptions import HTTPSeeOther
from pyramid.renderers import render_to_response
from pyramid.security import authenticated_userid
from pyramid.security import forget
from pyramid.security import remember

import transaction

from webob.exc import HTTPFound

from poulda.models import DBSession
from poulda.models import Upload
from poulda.utils import check_enabled
from poulda.utils import check_password
from poulda.utils import copy_to_file
from poulda.utils import get_file_from_request
from poulda.utils import TemplateAPI


@check_enabled
def home(request, failed=False):
    api = TemplateAPI(request, step='home')
    # If the user is already logged in, proceed to the upload form
    # directly.
    if api.login:
        return upload_form(request)
    needs_login = request.GET.get('needs_login')
    next = request.GET.get('next') or \
        request.POST.get('next') or \
        request.route_url('upload_form')
    return render_to_response('templates/home.pt',
                              {'api': api, 'next': next,
                               'failed': failed, 'needs_login': needs_login})


@check_enabled
def upload_form(request):
    api = TemplateAPI(request, step='upload')
    settings = request.registry.settings
    if settings.get('poulda.nginx_upload_progress', 'false') != 'true':
        u = Upload()
        u.state = u'starting'
        session = DBSession()
        session.add(u)
        session.flush()  # set 'u.id'
        file_id = repr(u.id)
    else:
        file_id = repr(time.time())
    return render_to_response('templates/upload.pt',
                              {'api': api, 'file_id': file_id})


@check_enabled
def upload(request):
    """View used when support for Nginx Upload Progress module has
    been disabled.

    This view includes 3 steps:

    1. We change the "state" column in the upload table so that our
       AJAX-called 'progress' view sees that the upload has started
       and that the temporary file can be stat'ed.

    2. We copy the data from the POST request to a temporary
       file. This step is long, obviously, as we copy data as we
       receive it from the browser. While we are copying data, the
       browser will call the 'progress' view to update a progress bar.

    3. Once the file has been copied, we rename it to its final
       filename and redirect the browser to the success page.
    """
    # We pass the 'file_id' in the query string as a GET parameter. If
    # we read it from the POSTed data, WebOb would read all POSTed
    # data, which has various features and traps (like setting the
    # "Content-Length" header to 0) that we do not need since we are
    # going to read the data ourselves anyway.
    file_id = request.GET['X-Progress-ID']
    input_file, file_size, filename = get_file_from_request(request)
    session = DBSession()
    u = session.query(Upload).filter_by(id=file_id).one()
    upload_dir = request.registry.settings['poulda.upload_dir']
    user_id = authenticated_userid(request)
    # We use a temporary path to detect unfinished uploads (post
    # mortem, not in the application itself).
    path = os.path.join(upload_dir, '_'.join((user_id, file_id)))
    u.tmp_path = path
    u.started = int(time.time())
    u.size = file_size
    u.state = u'uploading'
    session.flush()
    # We need to commit the transaction so that changes to the Upload
    # object can be seen by the other threads (which will serve the
    # 'progress' JSON view called by the upload page).
    transaction.commit()
    with open(path, 'w') as output:
        # We must read only 'file_size' bytes from the 'input_file',
        # not all of it since it also contains the MIME boundary.
        copy_to_file(input_file, file_size, output)
    final_path = filename[1 + filename.rfind(os.sep):]
    final_path = os.path.join(upload_dir, final_path)
    os.rename(path, final_path)
    session = DBSession()
    u = session.query(Upload).filter_by(id=file_id).one()
    u.state = u'done'
    u.final_path = unicode(final_path, 'utf-8')
    return HTTPFound(location='success')


@check_enabled
def upload_with_nginx_upload_progress(request):
    """View used when Nginx Upload Progress module is enabled.

    When the Nginx Upload Progress module is used, we get to the WSGI
    application (and thus to this view) only when the file has been
    completely written to disk by Nginx. So here we merely copy it to
    the final upload directory and that is all.
    """
    input_file, file_size, filename = get_file_from_request(request)
    upload_dir = request.registry.settings['poulda.upload_dir']
    path = os.path.join(upload_dir, filename)
    with open(path, 'w') as output:
        # We must read only 'file_size' bytes from the 'input_file',
        # not all of it since it also contains the MIME boundary.
        copy_to_file(input_file, file_size, output)
    return HTTPFound(location='success')


@check_enabled
def success(request):
    api = TemplateAPI(request, step='success')
    return render_to_response('templates/success.pt', {'api': api})


@check_enabled
def progress(request):
    """View used only when the Nginx Upload Progress support has been
    disabled.

    When the Nginx Upload Progress support is enabled, this view is
    never called at all, since the Nginx module takes care of
    returning progress information.
    """
    file_id = request.GET['X-Progress-ID']
    session = DBSession()
    u = session.query(Upload).filter_by(id=file_id).one()
    data = {'state': u.state}
    if u.state == 'uploading':
        if not os.path.exists(u.tmp_path):
            # The temporary file has not been created yet or it has
            # already been renamed. We return 0 in both case, the
            # front-end code will know what to do.
            received = 0
        else:
            received = os.stat(u.tmp_path).st_size
        data.update({'size': u.size, 'received': received})
    return data


@check_enabled
def login(request):
    next = request.GET.get('next') or \
        request.POST.get('next') or \
        quote_plus(request.get('HTTP_REFERER') or request.route.url('home'))
    login = request.POST.get('login', '')
    password = request.POST.get('password', '')
    if not check_password(request.registry.settings, login, password):
        return home(request, failed=True)
    headers = remember(request, login)
    return HTTPSeeOther(location=next, headers=headers)


def logout(request):
    headers = forget(request)
    return HTTPSeeOther(location=request.application_url, headers=headers)


def forbidden(request):
    url = request.route_url('home',
                            _query={'next': request.url, 'needs_login': '1'})
    return HTTPSeeOther(location=url)
