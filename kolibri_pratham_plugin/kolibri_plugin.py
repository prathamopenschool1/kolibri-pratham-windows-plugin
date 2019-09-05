from __future__ import absolute_import, print_function, unicode_literals
from kolibri.plugins.base import KolibriPluginBase

class PrathamPlugin(KolibriPluginBase):
    def url_module(self):
        from . import urls
        return urls

    def url_slug(self):
        return "^pratham/"
