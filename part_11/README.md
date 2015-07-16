##Broken, Abandoned, and Forgotten Code, Part 11

This code corresponds with [part 11](http://shadow-file.blogspot.com) of the Broken, Abandoned, and Forgotten Code series. In this part we add one more field to the ambit header that ``upnpd``'s does not check but the CFE bootloader does. If the TRX image checksum at offset 16 is not set, the CFE will halt and the router is effectively bricked. The ``janky_ambit_header.py`` module has been updated to reflect this.

Also, in part 11, we shrink the SquashFS filesystem down so that the resulting firmware image is <4MB. You should be able to generate a minimal firmware that you can test against a physical router.

Command synopsis:

    Usage: build_janky_fw.py {output file | find= } [input file 1 [input file 2,...]]

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
