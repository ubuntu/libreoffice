# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-

import snapcraft
from snapcraft.plugins import autotools
import logging
import os.path


# Set up Google API keys, see http://www.chromium.org/developers/how-tos/api-keys .
# Note: these are for Ubuntu use ONLY. For your own distribution,
# please get your own set of keys.
# Permission to add API keys, from Paweł Hajdan, To chad.miller@canonical.com
# msgid: CAADNaOFSFoch68NM1SGpCTRXqmspyKQgUPUtsF7SGRsRXiHZcg@mail.gmail.com
# reused from chromium-browser 48.0.2564.82-0ubuntu1.1222
GOOGLEAPI_APIKEY_UBUNTU = 'AIzaSyAQfxPJiounkhOjODEO5ZieffeBv6yft2Q'
GOOGLEAPI_CLIENTID_UBUNTU = '424119844901.apps.googleusercontent.com'
GOOGLEAPI_CLIENTSECRET_UBUNTU = 'AIienwDlGIIsHoKnNHmWGXyJ'

CONFFLAGS = [
	'--disable-ccache',
	'--disable-coinmp',
	'--disable-dconf',
	'--disable-dependency-tracking',
	'--disable-evolution2',
	'--disable-firebird-sdbc',
	'--disable-gltf',
	'--disable-gstreamer-0-10',
	'--disable-kde4',
	'--disable-online-update',
	'--enable-dbus',
	'--enable-eot',
	'--enable-ext-mariadb-connector',
	'--enable-ext-wiki-publisher',
	'--enable-extension-integration',
	'--enable-gstreamer-1-0',
	'--enable-hardlink-deliver',
	'--enable-mergelibs',
	'--enable-release-build',
	'--enable-scripting-beanshell',
	'--enable-scripting-javascript',
	'--with-alloc=system',
	'--with-build-version=libreoffice-5.2.0.0.beta2-snap1',
	'--with-gdrive-client-id=$(GOOGLEAPI_CLIENTID_UBUNTU)',
	'--with-gdrive-client-secret=$(GOOGLEAPI_CLIENTSECRET_UBUNTU)',
	'--with-system-libexttextcat',
	'--with-system-openldap',
	'--with-system-nss',
	'--with-theme=galaxy hicontrast oxygen tango sifr breeze elementary human',
	'--with-vendor=Canonical, Ltd.',
	'--disable-postgresql-sdbc',
	'--with-help']

LANGS = [ 
    'en-US',
    'af',
    'am',
    'ar',
    'as',
    'ast',
    'be',
    'bg',
    'bn',
    'br',
    'bs',
    'ca',
    'ca-valencia',
    'cs',
    'cy',
    'da',
    'de',
    'dz',
    'el',
    'en-GB',
    'en-ZA',
    'eo',
    'es',
    'et',
    'eu',
    'fa',
    'fi',
    'fr',
    'ga',
    'gd',
    'gl',
    'gu',
    'gug',
    'he',
    'hi',
    'hr',
    'hu',
    'id',
    'is',
    'it',
    'ja',
    'ka',
    'kk',
    'km',
    'ko',
    'kmr-Latn',
    'lt',
    'lv',
    'mk',
    'mn',
    'ml',
    'mr',
    'nb',
    'ne',
    'nl',
    'nn',
    'nr',
    'nso',
    'oc',
    'om',
    'or',
    'pa-IN',
    'pl',
    'pt',
    'pt-BR',
    'ro',
    'ru',
    'rw',
    'si',
    'sk',
    'sl',
    'sr',
    'ss',
    'st',
    'sv',
    'ta',
    'te',
    'tg',
    'th',
    'tn',
    'tr',
    'ts',
    'ug',
    'uk',
    'uz',
    've',
    'vi',
    'xh',
    'zh-CN',
    'zh-TW',
    'zu']

#	--enable-symbols \

class LibreOfficePlugin(autotools.AutotoolsPlugin):
    logger = logging.getLogger('snapcraft')
    def fetch(self):
        LibreOfficePlugin.logger.info('preparing dot/graphwiz')
        self.run(['sudo', 'dot', '-c'])
        #self.run(['pwd'])
        #self.run(['pwd'], '.')
        #self.run(['pwd'], './build/build')
        LibreOfficePlugin.logger.info('getting core repo')
        # TODO: basic clone can be down by default plugin
        #git clone --depth 1 -vb libreoffice-5.2.0.0.beta2 https://github.com/LibreOffice/core.git $(BUILDDIR) || true
        self.run(['git', 'clone',
            '--depth=1',
            '-v',
            '--branch=libreoffice-5.2.0.0.beta2',
            '/home/bjoern/checkouts/libreoffice',
            os.path.join(self.builddir, 'build')])
        self.run(
            ['git', '-C', os.path.join(self.builddir, 'build'), 'clean', '-dfx'])
        LibreOfficePlugin.logger.info('configuring for fetch')
        self.run(
            ['./autogen.sh'] + CONFFLAGS + ['--with-lang=' + ' '.join(LANGS)],
            os.path.join(self.builddir, 'build'))
        LibreOfficePlugin.logger.info('fetching additional source')
        self.run(
            ['make', 'fetch'],
            os.path.join(self.builddir, 'build'))
    def build(self):
        self.fetch()
        super(autotools.AutotoolsPlugin, self).build()

        # run boostrap before autotools build
        #self.run(['/bin/false'])

        # the plugins hooks are not idemnpotent, where they should be.
        # so we need to answer that calling the autotools plugins won't
        # retrigger BasePlugin build() which erase the directory.
        # However the issue with this hack is that other parts from this
        # project will be impacted if they are instantiated after this
        # method is ran, which is unlikely, but still possible.
        # https://bugs.launchpad.net/snapcraft/+bug/1595964.
        #snapcraft.BasePlugin.build = lambda self: None
        #super().build()


# vim:set shiftwidth=4 softtabstop=4 expandtab
