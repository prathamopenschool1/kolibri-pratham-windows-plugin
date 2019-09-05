from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic.base import TemplateView, View

from kolibri.content.models import ChannelMetadata, ContentNode


class ContentPermalinkRedirect(View):

    def get(self, request, *args, **kwargs):

        # extract the GET parameters
        channel_id = request.GET.get("channel_id")
        node_id = request.GET.get("node_id")
        content_id = request.GET.get("content_id")

        try:  # first, try to get the node by the unique node_id
            node = ContentNode.objects.get(id=node_id)
        except ContentNode.DoesNotExist as e:  # if it isn't found, fall back to looking for the content_id in the channel
            node = ContentNode.objects.filter(channel_id=channel_id, content_id=content_id).first()
            if not node:  # if it's still not found, see if we can find anything with the content_id across any channel
                node = ContentNode.objects.filter(content_id=content_id).first()

        # build up the target topic/content page URL
        if node:
            if not node.parent:
                kind_slug = ""
            elif node.kind == "topic":
                kind_slug = "t/"
            else:
                kind_slug = "c/"
            return HttpResponseRedirect(reverse('kolibri:learnplugin:learn') + "#/topics/" + kind_slug + node.id)
        else:
            raise Http404


class ThinCommonCartridgeManifestView(TemplateView):

    template_name = "ims/ccthin/manifest.xml"

    def get_context_data(self, **kwargs):
        context = super(ThinCommonCartridgeManifestView, self).get_context_data(**kwargs)
        context["nodes"] = self.get_toplevel_nodes(root_node_id=self.request.GET.get("root", "").split("_")[-1])
        rootlevel = context["nodes"][0].level
        context["maxlevel"] = int(self.request.GET.get("levels", "1000")) + rootlevel
        context["resources"] = context["nodes"].get_descendants(include_self=True).filter(available=True, level__lt=context["maxlevel"])
        context["baseurl"] = self.request.build_absolute_uri("/").rstrip("/")
        return context

    def get_toplevel_nodes(self, root_node_id):
        if not root_node_id:
            return ContentNode.objects.filter(parent=None)
        else:
            try:
                return ContentNode.objects.get(id=root_node_id).get_children()
            except ContentNode.DoesNotExist as e:
                raise Http404("Root node with id '{}' not found!".format(root_node_id))
