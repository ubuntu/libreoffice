THISDIR := $(realpath $(dir $(firstword $(MAKEFILE_LIST))))
all:
	env
	cp $(THISDIR)/final_FixNss.mk build/solenv/gbuild/extensions/
	cd build && ./autogen.sh --enable-python=system --disable-liblangtag --disable-collada --disable-coinmp --enable-verbose --disable-ccache --disable-postgresql-sdbc --without-doxygen --without-system-libs --with-system-nss --enable-debug
	#cd build && make verbose=T -k build-nocheck
	#cd build && make verbose=T build-nocheck
	cd build && make verbose=T
	

install:
	cd build && make install DESTDIR=$(shell readlink -f ../install)

# vim: set noet sw=4 ts=4:
