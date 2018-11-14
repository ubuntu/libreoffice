#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Write a java settings file for libreoffice, if it does not exist yet.
# Without such a file, libreoffice can locate the JRE embedded in the snap,
# but it will not use it by default, and the user has to open the settings UI
# to explicitly select the JRE.

import base64
import os
import os.path
import re
import subprocess
import sys


if __name__ == '__main__':
    snap = os.environ["SNAP"]
    snap_arch = os.environ["SNAP_ARCH"]
    snap_user_data = os.environ["SNAP_USER_DATA"]
    lo_config_dir = os.path.join(snap_user_data, ".config", "libreoffice",
                                 "4", "user", "config")
    javasettings_arch = {"i386": "x86", "amd64": "X86_64"}.get(snap_arch)
    javasettings_filename = \
        "javasettings_Linux_{}.xml".format(javasettings_arch)
    javasettings_filepath = os.path.join(lo_config_dir, javasettings_filename)

    marker_revision = 1 # bump when the contents of the file need to change
    marker_filename = ".snap_javasettings_writer.{}".format(marker_revision)
    marker_file = os.path.join(lo_config_dir, marker_filename)
    if os.path.isfile(marker_file):
        # The java settings file already exists and is up-to-date, do nothing.
        sys.exit()

    if not os.path.exists(lo_config_dir):
        os.makedirs(lo_config_dir)

    jre = "{}/usr/lib/jvm/java-11-openjdk-{}".format(snap, snap_arch)
    jvm = "{}/lib".format(jre)

    java_location = "file://{}".format(jre)

    java_output = subprocess.getoutput("{}/bin/java -version".format(jre))
    java_version = re.match('openjdk version "(?P<version>[\d\._]+)"',
                            java_output).group("version")

    # Vendor data is a base64-encoded utf-16 string containing the path to the
    # JVM shared library, and a LD_LIBRARY_PATH to locate java libraries
    # (similar to the output of the javaldx executable).
    vendor_data = []
    vendor_data.append("file://{}/server/libjvm.so".format(jvm))
    paths = [os.path.normpath(os.path.join(jvm, snap_arch, i))
             for i in ("client", "server", "native_threads", "")]
    vendor_data.append(":".join(paths))
    vendor_data.append("")
    vendor_data = "\n".join(vendor_data)
    vendor_data = vendor_data.encode("utf-16")[2:]  # remove BOM
    vendor_data = base64.b16encode(vendor_data).decode()

    template = """<?xml version="1.0" encoding="UTF-8"?>
<java xmlns="http://openoffice.org/2004/java/framework/1.0"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <javaInfo xsi:nil="false" vendorUpdate="2013-05-02" autoSelect="false">
    <vendor>Oracle Corporation</vendor>
    <location>{javaLocation}</location>
    <version>{javaVersion}</version>
    <features>0</features>
    <requirements>1</requirements>
    <vendorData>{vendorData}</vendorData>
  </javaInfo>
  <enabled xsi:nil="true"/>
</java>"""
    javasettings = template.format(javaLocation=java_location,
                                   javaVersion=java_version,
                                   vendorData=vendor_data)
    with open(javasettings_filepath, "w") as f:
        f.write(javasettings)

    open(marker_file, "w").close()
