THISDIR := $(realpath $(dir $(firstword $(MAKEFILE_LIST))))
all:
	echo $(THISDIR)
	env
	cp $(THISDIR)/final_FixNss.mk build/solenv/gbuild/extensions/
	#cd build && ./autogen.sh --enable-python=system --disable-liblangtag --disable-collada --disable-coinmp --enable-verbose --disable-ccache --disable-postgresql-sdbc --without-doxygen --without-system-libs --with-system-nss --enable-debug --disable-fetch-external CPPFLAGS="$(CPPFLAGS) -I$(realpath $(THISDIR)/../../../stage/usr/include/libxml2/)" CFLAGS="$(CFLAGS) -I$(realpath $(THISDIR)/../../../stage/usr/include/libxml2/)"
	cd build && ./autogen.sh --enable-python=system --disable-liblangtag --disable-collada --disable-coinmp --enable-verbose --disable-ccache --disable-postgresql-sdbc --without-doxygen --without-system-libs --with-system-nss --enable-debug --disable-fetch-external
	#cd build && make verbose=T -k build-nocheck
	#cd build && make verbose=T build-nocheck
	#cd build && (make tools.all || true) && make && make check && make subsequentcheck
	cd build && (make -k || true)
	echo SECOND RUN
	cd build && (make -k || true)
	echo CHECKRUN
	cd build && make check
	

install:
	cd build && make install DESTDIR=$(shell readlink -f ../install)

# vim: set noet sw=4 ts=4:
