# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-

import snapcraft
from snapcraft.plugins import autotools
import logging
import os.path
import os


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
#	'--disable-dependency-tracking',
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
#	'--enable-hardlink-deliver',
	'--enable-mergelibs',
	'--enable-release-build',
	'--enable-scripting-beanshell',
	'--enable-scripting-javascript',
	'--with-alloc=system',
	'--with-build-version=libreoffice-5.3.1.2-snap1',
	'--with-gdrive-client-id=$(GOOGLEAPI_CLIENTID_UBUNTU)',
	'--with-gdrive-client-secret=$(GOOGLEAPI_CLIENTSECRET_UBUNTU)',
	'--with-system-libexttextcat',
	'--with-system-openldap',
	'--with-system-nss',
	'--with-theme=galaxy hicontrast oxygen tango sifr breeze elementary',
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

# smaller langset to reduce snap size for now
LANGS = [ 
    'en-US',
    'de',
    'es',
    'fr',
    'it',
    'pt',
    'pt-BR']

#	--enable-symbols \

class LibreOfficePlugin(autotools.AutotoolsPlugin):
    logger = logging.getLogger('snapcraft')
    def pull(self):
        super().pull()
    def build(self):
        LibreOfficePlugin.logger.info('preparing dot/graphwiz')
#        self.run(['sudo', 'dot', '-c'])
        LibreOfficePlugin.logger.info('getting core repo')
        # TODO: basic clone can be down by default plugin
        # https://github.com/LibreOffice/core.git
        self.run(['git', 'clone',
            '--depth=1',
            '-v',
            '--branch=libreoffice-5.3.1.2',
            'https://github.com/LibreOffice/core.git',
            os.path.join(self.builddir, 'build')])
        self.run(
            ['git', '-C', os.path.join(self.builddir, 'build'), 'clean', '-dfx'])
        LibreOfficePlugin.logger.info('configuring for fetch')
        self.run(
            ['./autogen.sh'] + CONFFLAGS + ['--with-lang=' + ' '.join(LANGS)],
            os.path.join(self.builddir, 'build'))
        LibreOfficePlugin.logger.info('applying vendor patches from %s ' % os.path.join(self.builddir, '..' , 'src' ,'patches'))
        for patch in os.walk(os.path.join(self.builddir, '..', 'src', 'patches')).__next__()[2]:
            patchpath = os.path.join(self.builddir, '..', 'src', 'patches', patch)
            LibreOfficePlugin.logger.info('applying %s from %s' % (patch, patchpath))
            self.run(
                ['git', 'am', patchpath],
                os.path.join(self.builddir, 'build'))
        LibreOfficePlugin.logger.info('fetching additional source')
        self.run(
            ['make', 'fetch'],
            os.path.join(self.builddir, 'build'))
#    def build(self):
        LibreOfficePlugin.logger.info('configuring non-l10n')
        self.run(
            ['./autogen.sh'] + CONFFLAGS + ['--disable-fetch-external'],
            os.path.join(self.builddir, 'build'))
        LibreOfficePlugin.logger.info('cleaning up')
        self.run(
            ['make', 'clean'],
            os.path.join(self.builddir, 'build'))
        LibreOfficePlugin.logger.info('building externals')
        self.run(
            ['make', 'external.all'],
            os.path.join(self.builddir, 'build'))
        LibreOfficePlugin.logger.info('building non-l10n')
        self.run(
            ['make', 'build-nocheck'],
            os.path.join(self.builddir, 'build'))
        self.run(
            ['rm', '-rf', os.path.join(self.builddir, 'build', 'workdir', 'SrsPartTarget')],
            os.path.join(self.builddir, 'build'))
        self.run(
            ['rm', '-rf', os.path.join(self.builddir, 'build', 'workdir', 'SrsTarget')],
            os.path.join(self.builddir, 'build'))
#        for lang in [l for l in LANGS if l != 'en-US']:
#            LibreOfficePlugin.logger.info('configuring for l10n: %s' % lang)
#            self.run(
#                ['./autogen.sh'] + CONFFLAGS + ['--with-lang=%s' % lang],
#                os.path.join(self.builddir, 'build'))
#            self.run(
#                ['make', 'build-nocheck', 'verbose=T'],
#                os.path.join(self.builddir, 'build'))
#            self.run(
#                ['rm', '-rf', os.path.join(self.builddir, 'build', 'workdir', 'SrsPartTarget')],
#                os.path.join(self.builddir, 'build'))
#            self.run(
#                ['rm', '-rf', os.path.join(self.builddir, 'build', 'workdir', 'SrsTarget')],
#                os.path.join(self.builddir, 'build'))
        LibreOfficePlugin.logger.info('configuring for full l10n')
        self.run(
            ['./autogen.sh'] + CONFFLAGS + ['--with-lang=' + ' '.join(LANGS)],
            os.path.join(self.builddir, 'build'))
        LibreOfficePlugin.logger.info('run tests')
        self.run(
            ['make', 'build-nocheck'],
            os.path.join(self.builddir, 'build'))
        self.run(
            ['make', 'check'],
            os.path.join(self.builddir, 'build'))
        self.run(
            ['make', 'install', 'DESTDIR=' + self.installdir],
            os.path.join(self.builddir, 'build'))

# vim:set shiftwidth=4 softtabstop=4 expandtab
