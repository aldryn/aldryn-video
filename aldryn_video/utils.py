# -*- coding: utf-8 -*-

import re
from urllib import urlencode
from urlparse import parse_qs, urlparse, urlunparse

import micawber
from micawber.exceptions import ProviderNotFoundException, ProviderException

providers = micawber.bootstrap_basic()


IFRAME_SRC_REGEX = 'src="([^"]+)"'

# List of parameters not supported by oEmbed
UNSUPPORTED_PARAMS = ['autoplay', 'loop']


def get_embed_code(**kwargs):
    try:
        data = providers.request(**kwargs)
    except (ProviderNotFoundException, ProviderException) as e:
        raise Exception(e.message)
    if data.get('type') != 'video':
        raise Exception('This must be an url for a video. '
                        'The "%(type)s" type is not supported.' % {'type': data.get('type')})

    html = data['html']
    if any(param in kwargs for param in UNSUPPORTED_PARAMS):
        data_url = re.search(IFRAME_SRC_REGEX, html)
        if data_url:
            # What follows is a pretty nasty looking "hack"
            # oEmbed hss not implemented some parameters
            # and so for these we need to add them manually to the iframe.
            parsed_data_url = urlparse(data_url.groups()[0])
            url_parts = list(parsed_data_url)
            query = parse_qs(parsed_data_url.query)
            for param in UNSUPPORTED_PARAMS:
                value = kwargs.get(param)
                if value and param not in query:
                    query[param] = value
            else:
                url_parts[4] = urlencode(query, True)
                new_url = 'src="%s" ' % urlunparse(url_parts)
                html = re.sub(IFRAME_SRC_REGEX, new_url, html)
    return html
