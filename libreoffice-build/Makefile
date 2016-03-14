THISDIR := $(realpath $(dir $(firstword $(MAKEFILE_LIST))))
BUILDDIR := $(THISDIR)/build

# Set up Google API keys, see http://www.chromium.org/developers/how-tos/api-keys .
# Note: these are for Ubuntu use ONLY. For your own distribution,
# please get your own set of keys.
# Permission to add API keys, from Paweł Hajdan, To chad.miller@canonical.com
# msgid: CAADNaOFSFoch68NM1SGpCTRXqmspyKQgUPUtsF7SGRsRXiHZcg@mail.gmail.com
# reused from chromium-browser 48.0.2564.82-0ubuntu1.1222
GOOGLEAPI_APIKEY_UBUNTU := AIzaSyAQfxPJiounkhOjODEO5ZieffeBv6yft2Q
GOOGLEAPI_CLIENTID_UBUNTU := 424119844901.apps.googleusercontent.com
GOOGLEAPI_CLIENTSECRET_UBUNTU := AIienwDlGIIsHoKnNHmWGXyJ

CONFFLAGS := \
	--disable-ccache \
	--disable-coinmp \
	--disable-dconf \
	--disable-dependency-tracking \
	--disable-evolution2 \
	--disable-firebird-sdbc \
	--disable-gltf \
	--disable-gstreamer-0-10 \
	--disable-kde4 \
	--disable-online-update \
	--enable-dbus \
	--enable-eot \
	--enable-ext-mariadb-connector \
	--enable-ext-wiki-publisher \
	--enable-extension-integration \
	--enable-gstreamer-1-0 \
	--enable-hardlink-deliver \
	--enable-mergelibs \
	--enable-release-build \
	--enable-scripting-beanshell \
	--enable-scripting-javascript \
	--enable-symbols \
	--with-alloc=system \
	--with-build-version='5.1.1.3-snap2' \
	--with-gdrive-client-id=$(GOOGLEAPI_CLIENTID_UBUNTU) \
	--with-gdrive-client-secret=$(GOOGLEAPI_CLIENTSECRET_UBUNTU) \
	--with-lang="en-US af am ar as ast be bg bn br bs ca ca-valencia cs cy da de dz el en-GB en-ZA eo es et eu fa fi fr ga gd gl gu gug he hi hr hu id is it ja ka kk km ko kmr-Latn lt lv mk mn ml mr nb ne nl nn nr nso oc om or pa-IN pl pt pt-BR ro ru rw si sk sl sr ss st sv ta te tg th tn tr ts ug uk uz ve vi xh zh-CN zh-TW zu" \
	--with-system-libexttextcat \
	--with-theme="galaxy hicontrast oxygen tango sifr breeze elementary human" \
	--with-vendor='Canonical, Ltd.' \
	--disable-postgresql-sdbc \

CONFFLAGS_HELP := $(CONFFLAGS) --with-help --with-parallelism=1

#see lp#1549691 -- fetching source cannot be done with default snapcraft tooling
.fetch:
	echo "executing step: $@"
	echo "SNAP: getting source"
	git clone -vb libreoffice-5.1.1.3 https://github.com/LibreOffice/core.git $(BUILDDIR) || true
	cd $(BUILDDIR) && git clean -dfx
	echo "SNAP: configuring"
	cd $(BUILDDIR) && ./autogen.sh $(CONFFLAGS_HELP)
	echo "SNAP: fetching"
	cd $(BUILDDIR) && make fetch
	touch $@
	
all: .fetch
	echo "executing step: $@"
	echo "SNAP: cleaning up"
	cd $(BUILDDIR) && make clean || true
	echo "SNAP: patching source"
	# lp#1548232: snapcraft messes with include paths in unhealthy ways
	cp $(THISDIR)/final_FixNss.mk $(BUILDDIR)/solenv/gbuild/extensions/
	echo "SNAP: configuring without help"
	cd $(BUILDDIR) && ./autogen.sh --disable-fetch-external $(CONFFLAGS)
	echo "SNAP: building without help"
	cd $(BUILDDIR) && make verbose=t
	echo "SNAP: configuring with help"
	cd $(BUILDDIR) && ./autogen.sh --disable-fetch-external $(CONFFLAGS_HELP)
	echo "SNAP: building without help"
	cd $(BUILDDIR) && make verbose=t
	echo "SNAP: running checks"
	cd $(BUILDDIR) && make check || true # lets not abort, it took a while to get here -- instead check the logs.

install:
	echo "executing step: $@"
	# lp#1548376: manually copy files from snap-packages to install, so that the will be part of the snap
	cp -a $(shell readlink -f ../../../stage)/* $(shell readlink -f ../install) | true
	cd $(BUILDDIR) && make install DESTDIR=$(shell readlink -f ../install)


.PHONY: all install
.DEFAULT_GOAL: all

# vim: set noet sw=4 ts=4:
