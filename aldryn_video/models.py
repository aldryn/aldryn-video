# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from json_field import JSONField

from aldryn_video.utils import build_html_iframe, get_embed_code, get_player_url


class OEmbedVideoPlugin(CMSPlugin):
    ALLOWED_MEDIA_TYPES = ['video']

    url = models.URLField(_('URL'), max_length=100)
    width = models.IntegerField(_('Width'), null=True, blank=True)
    height = models.IntegerField(_('Height'), null=True, blank=True)
    auto_play = models.BooleanField(_('auto play'), default=False)
    loop_video = models.BooleanField(_('loop'), help_text=_('when true, the video repeats itself when over.'), default=False)
    # cached oembed data
    oembed_data = JSONField(null=True)

    def __unicode__(self):
        return self.url

    def get_oembed_params(self):
        extra = {}
        if self.width:
            extra['maxwidth'] = self.width
        if self.height:
            extra['maxheight'] = self.height
        if self.auto_play:
            extra['autoplay'] = 1
        if self.loop_video:
            extra['loop'] = 1
        return extra

    @property
    def html(self):
        if not hasattr(self, '_html'):
            params = self.get_oembed_params()
            self._html = build_html_iframe(self.oembed_data, **params)
        return self._html

    def clean(self):
        params = self.get_oembed_params()
        try:
            data = get_embed_code(url=self.url, **params)
        except Exception as e:
            raise ValidationError(e.message)
        else:
            media_type = data.get('type')
            if media_type not in self.ALLOWED_MEDIA_TYPES:
                raise ValidationError('This must be an url for a video. The "%(type)s" type is not supported.' % dict(type=media_type))

        player_url = get_player_url(data)
        if player_url:
            data['player_url'] = player_url.groups()[0]
        self.oembed_data = data
