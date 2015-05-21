##Broken, Abandoned, and Forgotten Code, Part 3

This code corresponds with [part 5](http://shadow-file.blogspot.com) of the Broken, Abandoned, and Forgotten Code series. In part 5 I demonstrate how to use the Bowcaster exploit development framework to generate a stand-in for the unidentified 58 byte header in the Netgear R6200 firmware image. Using Bowcaster's pattern generator, it's easy to find the offsets of values that get parsed out when the firmware image is being validated by the router.

This update adds `buildfw.py` as well as a number of supporting classes. The `buildfw.py` program concatenates kernel and filesystem images and prepends a TRX header and the 58-byte stand-in mystery header.

I don't provide the kernel and filesystem components from a stock firmware, so you will need to get these on your own. You may get them by using `dd` to extract them from a stock firmware:

     $ dd if=R6200-V1.0.0.28_1.0.24.chk of=squashfs.bin skip=1328446 bs=1
     $ dd if=R6200-V1.0.0.28_1.0.24.chk of=kernel.lzma skip=86 bs=1 count=1328360

You can identify the offsets and sizes of the kernel and filesystem components using binwalk.

Then you can generate a firmware image or find the offset into the 58-byte header of a given pattern.

####Note: This program does not generate a working firmware image. It is for debugging and analyzing as described in Part 5 of the Broken, Abandoned series.

Command synopsis:

    Usage: buildfw.py {output file | find= } [input file 1 [input file 2,...]]

    Generate a Netgear R6200 firmware image from individual parts.
    Concatenate one or more firmware components (kernel, filesystem, etc.)
    and prepend a proprietary 58 byte header and a TRX header.

    Arguments:
      output file   	Final firmware image file
      find=<pattern>	Locate the offset of <pattern> in the stand-in
                    	58-byte header.
                    	<pattern> may be a string or integer. If an integer,
                    	it must be specified in hexadecimal,
                    	prepended with "0x", and big endian encoded.
      input file 1 [2,...]
                    	Input files to concatenate.

    Examples:
      buildfw.py firmware.chk kernel.lzma squashfs.bin
      buildfw.py find=0x62374162 kernel.lzma squashfs.bin
      buildfw.py find=b7Ab kernel.lzma squashfs.bin
