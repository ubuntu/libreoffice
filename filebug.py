#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# File a bug against the libreoffice source package on Launchpad with relevant
# information extracted from the environment, and a 'snap' tag. This is
# similar to the ubuntu-bug command on a classic system.

from email.generator import BytesGenerator
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO
import os
import subprocess
from urllib.parse import urlencode
from urllib.request import build_opener, HTTPSHandler, Request


LAUNCHPAD = 'launchpad.net'
ENV = [
    'DESKTOP_SESSION',
    'GTK_MODULES',
    'HOME',
    'LANG',
    'LC_MONETARY',
    'LC_NAME',
    'LC_NUMERIC',
    'LC_TIME',
    'LD_LIBRARY_PATH',
    'PATH',
    'SNAP',
    'SNAP_ARCH',
    'SNAP_COMMON',
    'SNAP_DATA',
    'SNAP_LIBRARY_PATH',
    'SNAP_NAME',
    'SNAP_REEXEC',
    'SNAP_REVISION',
    'SNAP_USER_COMMON',
    'SNAP_USER_DATA',
    'SNAP_VERSION',
    'TEMPDIR',
    'TMPDIR',
    'XDG_CONFIG_DIRS',
    'XDG_CURRENT_DESKTOP',
    'XDG_DATA_DIRS',
    'XDG_RUNTIME_DIR',
    'XDG_SESSION_DESKTOP',
    'XDG_SESSION_TYPE'
]


if __name__ == '__main__':
    lsb_release = ''
    with open('/etc/lsb-release', 'r') as f:
        lsb_release = f.read()
    env = ['{}={}'.format(k, v) for k, v in os.environ.items() if k in ENV]
    env.sort()
    text = lsb_release + '\n' + '\n'.join(env)
    attachment = MIMEText(text, _charset='UTF-8')
    attachment.add_header('Content-Disposition', 'inline')
    message = MIMEMultipart()
    message.add_header('Tags', 'snap')
    message.attach(attachment)
    blob = message.as_string().encode('UTF-8')
    url = 'https://{}/+storeblob'.format(LAUNCHPAD)
    data = MIMEMultipart()
    submit = MIMEText('1')
    submit.add_header('Content-Disposition', 'form-data; name="FORM_SUBMIT"')
    data.attach(submit)
    form_blob = MIMEBase('application', 'octet-stream')
    form_blob.add_header('Content-Disposition',
                         'form-data; name="field.blob"; filename="x"')
    form_blob.set_payload(blob.decode('ascii'))
    data.attach(form_blob)
    data_flat = BytesIO()
    gen = BytesGenerator(data_flat, mangle_from_=False)
    gen.flatten(data)
    request = Request(url, data_flat.getvalue())
    request.add_header('Content-Type',
                       'multipart/form-data; boundary=' + data.get_boundary())
    opener = build_opener(HTTPSHandler)
    result = opener.open(request)
    handle = result.info().get('X-Launchpad-Blob-Token')
    summary = '[snap] SUMMARY HERE'.encode('UTF-8')
    params = urlencode({'field.title': summary})
    filebug_url = 'https://bugs.{}/ubuntu/+source/libreoffice/+filebug/{}?{}'
    subprocess.run(["xdg-open", filebug_url.format(LAUNCHPAD, handle, params)])
