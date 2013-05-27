# -*- coding: utf-8 -*-

import micawber
from micawber.exceptions import ProviderNotFoundException, ProviderException

providers = micawber.bootstrap_basic()


def get_embed_code(**kwargs):
    try:
        data = providers.request(**kwargs)
    except (ProviderNotFoundException, ProviderException) as e:
        raise Exception(e.message)
    if data.get('type') != 'video':
        raise Exception('This must be an url for a video. '
                        'The "%(type)s" type is not supported.' % {'type': data.get('type')})
    return data['html']
