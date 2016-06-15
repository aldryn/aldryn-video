============
Aldryn Video
============

Aldryn Video provides an elegant way to embed videos in your django CMS sites.

A number of video hosting providers are supported, including:

* Vimeo
* YouTube

(any provider that uses the `oEmbed specification <http://oembed.com>`_ should be supported).

The plugin also provides access to various control and sizing parameters for embedded video.


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

Credits
-------

Video file type icon by dreamxis, http://dreamxis.themex.net/,
under Creative Commons Attribution license.
