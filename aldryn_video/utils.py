# -*- coding: utf-8 -*-
from urllib import urlencode
from urlparse import parse_qs, urlparse, urlunparse

from bs4 import BeautifulSoup

import micawber
from micawber.exceptions import ProviderNotFoundException, ProviderException

providers = micawber.bootstrap_basic()


def build_html_iframe(response, url_params=None, iframe_attrs=None):
    html = response.get('html', '')
    data_url = response.get('player_url')

    if url_params is None:
        url_params = {}

    if iframe_attrs is None:
        iframe_attrs = {}

    if html and data_url:
        # What follows is a pretty nasty looking "hack"
        # oEmbed hss not implemented some parameters
        # and so for these we need to add them manually to the iframe.
        player_url = urlparse(data_url)
        url_params.update(parse_qs(player_url.query))
        url_parts = list(player_url)
        url_parts[4] = urlencode(url_params, True)
        html = BeautifulSoup(html).iframe
        html['src'] = urlunparse(url_parts)
        for key, value in iframe_attrs.iteritems():
            if value:
                html[key] = value
    return unicode(html)


def get_player_url(response):
    html = BeautifulSoup(markup=response.get('html', ''))
    if html.iframe:
        return html.iframe.attrs['src']
    return None


def get_embed_code(**kwargs):
    try:
        data = providers.request(**kwargs)
    except (ProviderNotFoundException, ProviderException) as e:
        raise Exception(e.message)
    else:
        return data
