import cgi

from pyramid.i18n import get_localizer
from pyramid.i18n import TranslationStringFactory
from pyramid.renderers import get_renderer
from pyramid.response import Response
from pyramid.security import authenticated_userid


_ = TranslationStringFactory('poulda')


BUFFER_SIZE = 8192


def get_file_from_request(request):
    """Return the input file, its size and its filename.

    ``cgi.FieldStorage`` reads the whole file. We do not want
    that. Since we know that there is only one file, we read only the
    beginning of the request body to determine the size and the
    filename of the file.
    """
    file_size = int(request.headers['Content-Length'])
    input_file = request['wsgi.input']
    line = input_file.readline()  # First MIME type boundary (file_id)
    file_size -= len(line)
    line = input_file.readline()  # Headers
    file_size -= len(line)
    line = input_file.readline()  # Blank line
    file_size -= len(line)
    line = input_file.readline()  # Value
    file_size -= len(line)
    line = input_file.readline()  # Second MIME type boundary (file)
    boundary_length = len(line)
    file_size -= boundary_length
    line = input_file.readline()  # Headers
    file_size -= len(line)
    filename = cgi.parse_header(line)[1]['filename']
    line = input_file.readline()  # Headers (continued)
    file_size -= len(line)
    line = input_file.readline()  # Blank line
    file_size -= len(line)
    if line.strip():  # pragma: no cover
        raise ValueError('Oups, I expected a blank line, here. '
                         'Got the following instead: %s' % line)
    file_size -= len('\r\n\r\n') + boundary_length
    return input_file, file_size, filename


class TemplateAPI(object):
    """A set of information provided to any template."""

    def __init__(self, request, step):
        self.request = request
        self.layout = get_renderer('templates/layout.pt').implementation()
        self.login = authenticated_userid(request)
        self.step = step

    def route_url(self, path, **kwargs):
        return self.request.route_url(path, **kwargs)

    def static_url(self, path):
        if ':' not in path:
            path = 'poulda:static/%s' % path
        return self.request.static_url(path)


def check_enabled(view):
    """A decorator that will shortcut the decorated view and return a
    simplified HTTP response page if the service is disabled.
    """
    def wrapper(request, *args, **kwargs):
        enabled = request.registry.settings['poulda.enabled'].lower() == 'true'
        if not enabled:
            localizer = get_localizer(request)
            msg = localizer.translate(_(u'This service has been disabled.'))
            return Response(msg)
        return view(request, *args, **kwargs)
    return wrapper


def copy_to_file(input_file, length, output):
    """Copy the first ``length`` bytes from ``input_file`` to
    ``output``.

    ``output`` should be an open stream. It will not be closed by this
    function.
    """
    q, r = divmod(length, BUFFER_SIZE)
    buffers = [BUFFER_SIZE] * q + [r]
    while buffers:
        chunk = input_file.read(buffers.pop(0))
        if not chunk:
            # We will get there only if the content length (advertised
            # by the browser) is larger than the effective length of
            # the file, which should not happen.
            break
        output.write(chunk)
        output.flush()


def check_password(settings, user, password):
    """Return whether the given credentials correspond to one of the
    configured accounts.
    """
    for account in settings.get('poulda.accounts', '').split():
        if account.split(':') == [user, password]:
            return True
    return False
