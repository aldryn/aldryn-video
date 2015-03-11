============
Aldryn Video
============

Plugin allows to embed videos from YouTube or Vimeo.


Installation
============

Aldryn Platform Users
---------------------

Choose a site you want to install the add-on to from the dashboard. Then go to ``Apps -> Install app`` and click ``Install`` next to ``Video`` app.

Redeploy the site.

Manuall Installation
--------------------

::

    pip install aldryn-video

Add ``aldryn_video`` to ``INSTALLED_APPS``.

Configure ``aldryn-boilerplates`` (https://pypi.python.org/pypi/aldryn-boilerplates/).

To use the old templates, set ``ALDRYN_BOILERPLATE_NAME='legacy'``.
To use https://github.com/aldryn/aldryn-boilerplate-standard (recommended, will be renamed to
``aldryn-boilerplate-bootstrap3``) set ``ALDRYN_BOILERPLATE_NAME='bootstrap3'``.
