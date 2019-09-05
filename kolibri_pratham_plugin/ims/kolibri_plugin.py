from __future__ import absolute_import, print_function, unicode_literals
from kolibri.core.webpack import hooks as webpack_hooks
from kolibri.plugins.base import KolibriPluginBase
from . import urls


class IMSPlugin(KolibriPluginBase):

    def url_module(self):
        return urls

    def url_slug(self):
        return "^ims/"
