"""Define our own locale negotiator that looks at the browser
preferences.
"""


def locale_negotiator(request):
    """Return a locale name by looking at the ``Accept-Language`` HTTP
    header.
    """
    settings = request.registry.settings
    available_languages = settings['pyramid.available_languages'].split()
    return request.accept_language.best_match(available_languages)
