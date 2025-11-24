# deo_events/cms_apps.py
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import gettext_lazy as _

class EventApphook(CMSApp):
    app_name = "events"
    name = _("Digital Event Organizer")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["events.urls"]

apphook_pool.register(EventApphook)
