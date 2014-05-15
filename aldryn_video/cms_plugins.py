# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from aldryn_video import models


class OEmbedVideoPlugin(CMSPluginBase):

    render_template = 'aldryn_video/video.html'
    name = _('Video')
    model = models.OEmbedVideoPlugin

    fieldsets = (
        (None,
         {'fields': ['url']},
        ),
        (_('Advanced Options'),
         {'fields': [
             ('width', 'height'),
             ('iframe_width', 'iframe_height'),
             'auto_play',
             'loop_video',
             'custom_params'
         ]}
        )
    )

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context

plugin_pool.register_plugin(OEmbedVideoPlugin)
