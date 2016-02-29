THISDIR := $(realpath $(dir $(firstword $(MAKEFILE_LIST))))
BUILDDIR := $(THISDIR)/build

CONFFLAGS := --enable-python=system --disable-liblangtag --disable-collada --disable-coinmp --enable-verbose --disable-ccache --disable-postgresql-sdbc --without-doxygen --without-system-libs --with-system-nss --disable-odk

.fetch:
	echo "executing step: $@"
	echo "SNAP: getting source"
	git clone -vb libreoffice-5.0.4.2 https://github.com/LibreOffice/core.git $(BUILDDIR) || true
	cd $(BUILDDIR) && git clean -dfx
	echo "SNAP: configuring"
	cd $(BUILDDIR) && ./autogen.sh $(CONFFLAGS)
	echo "SNAP: fetching"
	cd $(BUILDDIR) && make fetch
	touch $@
	
all: .fetch
	echo "executing step: $@"
	echo "SNAP: cleaning up"
	cd $(BUILDDIR) && make clean || true
	echo "SNAP: patching source"
	cp $(THISDIR)/final_FixNss.mk $(BUILDDIR)/solenv/gbuild/extensions/
	echo "SNAP: configuring"
	cd $(BUILDDIR) && ./autogen.sh --disable-fetch-external $(CONFFLAGS)
	echo "SNAP: building"
	cd $(BUILDDIR) && make
	echo "SNAP: running checks"
	cd $(BUILDDIR) && make check

install:
	echo "executing step: $@"
	cp -a $(shell readlink -f ../../../stage)/* $(shell readlink -f ../install)
	cd $(BUILDDIR) && make install DESTDIR=$(shell readlink -f ../install)


.PHONY: all install
.DEFAULT_GOAL: all

# vim: set noet sw=4 ts=4:
