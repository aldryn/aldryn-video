# -*- coding: utf-8 -*-

import re
from urllib import urlencode
from urlparse import parse_qs, urlparse, urlunparse

import micawber
from micawber.exceptions import ProviderNotFoundException, ProviderException

providers = micawber.bootstrap_basic()


IFRAME_SRC_REGEX = 'src="([^"]+)"'


def build_html_iframe(response, **params):
    html = response.get('html')
    data_url = response.get('player_url')
    if html and data_url:
        # What follows is a pretty nasty looking "hack"
        # oEmbed hss not implemented some parameters
        # and so for these we need to add them manually to the iframe.
        parsed_data_url = urlparse(data_url)
        url_parts = list(parsed_data_url)
        params.update(parse_qs(parsed_data_url.query))
        url_parts[4] = urlencode(params, True)
        new_url = 'src="%s" ' % urlunparse(url_parts)
        html = re.sub(IFRAME_SRC_REGEX, new_url, html)
    return html


def get_player_url(response):
    html = response.get('html', '')
    return re.search(IFRAME_SRC_REGEX, html)


def get_embed_code(**kwargs):
    try:
        data = providers.request(**kwargs)
    except (ProviderNotFoundException, ProviderException) as e:
        raise Exception(e.message)
    else:
        return data
