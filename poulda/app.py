from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPForbidden
from pyramid.security import NO_PERMISSION_REQUIRED

from poulda.auth import AuthorizationPolicy
from poulda.auth import PERMISSION_UPLOAD


def make_app(global_config, **settings):
    """Return the WSGI application."""
    nginx_upload_progress = settings.get(
        'poulda.nginx_upload_progress', 'false').lower() == 'true'
    if not nginx_upload_progress:
        from poulda.models import initialize_db
        initialize_db(settings['poulda.db_url'])
    config = Configurator(settings=settings)

    # Authentication and authorization policies
    auth_policy = AuthTktAuthenticationPolicy(settings['poulda.secret'])
    config.set_authentication_policy(auth_policy)
    authz_policy = AuthorizationPolicy()
    config.set_authorization_policy(authz_policy)

    # Views
    config.set_default_permission(PERMISSION_UPLOAD)
    config.add_static_view('static', 'static')
    config.add_route('home', '/')
    config.add_view('poulda.views.home',
                    route_name='home',
                    permission=NO_PERMISSION_REQUIRED)
    config.add_route('upload_form', '/upload', request_method='GET')
    config.add_view('poulda.views.upload_form', route_name='upload_form')
    config.add_route('upload', '/upload', request_method='POST')
    if nginx_upload_progress:
        upload_view = 'poulda.views.upload_with_nginx_upload_progress'
    else:
        upload_view = 'poulda.views.upload'
    config.add_view(upload_view, route_name='upload')
    if not nginx_upload_progress:
        # We need this view only if Nginx Upload Progress has been
        # disabled.
        config.add_route('progress', '/progress')
        config.add_view('poulda.views.progress', route_name='progress',
                        renderer='json')
    config.add_route('success', '/success')
    config.add_view('poulda.views.success', route_name='success')
    config.add_route('login', '/login', request_method='POST')
    config.add_view('poulda.views.login', route_name='login',
                    permission=NO_PERMISSION_REQUIRED)
    config.add_route('logout', '/logout')
    config.add_view('poulda.views.logout', route_name='logout')
    config.add_view('poulda.views.forbidden', context=HTTPForbidden,
                    permission=NO_PERMISSION_REQUIRED)

    # Internationalization
    config.add_translation_dirs('poulda:locale')
    config.set_locale_negotiator('poulda.i18n.locale_negotiator')

    return config.make_wsgi_app()
