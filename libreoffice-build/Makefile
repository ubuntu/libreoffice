THISDIR := $(realpath $(dir $(firstword $(MAKEFILE_LIST))))
all:
	echo "SNAP: environment"
	env
	echo "SNAP: patching source"
	cp $(THISDIR)/final_FixNss.mk build/solenv/gbuild/extensions/
	echo "SNAP: configuring"
	cd build && ./autogen.sh --enable-python=system --disable-liblangtag --disable-collada --disable-coinmp --enable-verbose --disable-ccache --disable-postgresql-sdbc --without-doxygen --without-system-libs --with-system-nss --disable-fetch-external --disable-odk
	echo "SNAP: building"
	cd build && make
	echo "SNAP: running checks"
	cd build && make check

install:
	cp -a $(shell readlink -f ../../../stage)/* $(shell readlink -f ../install)
	cd build && make install DESTDIR=$(shell readlink -f ../install)

# vim: set noet sw=4 ts=4:
