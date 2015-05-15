# -*- coding: utf-8 -*-

import os
import base64
import mimetypes


def get_path_url(path, relative=False):
    """ Returns an absolute or relative path url given a path
    """
    if relative:
        return os.path.relpath(path)
    else:
        return 'file://%s' % os.path.abspath(path)


def encode_image_from_url(url, source_path):
    if not url or url.startswith('data:') or url.startswith('file://'):
        return False

    if (url.startswith('http://') or url.startswith('https://')):
        return False

    real_path = url if os.path.isabs(url) else os.path.join(source_path, url)

    if not os.path.exists(real_path):
        print('%s was not found, skipping' % url)

        return False

    mime_type, encoding = mimetypes.guess_type(real_path)

    if not mime_type:
        print('Unrecognized mime type for %s, skipping' % url)

        return False

    try:
        with open(real_path, 'rb') as image_file:
            image_contents = image_file.read()
            encoded_image = base64.b64encode(image_contents)
    except IOError:
        return False

    return u"data:%s;base64,%s" % (mime_type, encoded_image.decode())
