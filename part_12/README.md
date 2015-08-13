##Broken, Abandoned, and Forgotten Code, Part 12

This code corresponds with [part 12](http://shadow-file.blogspot.coml) of the Broken, Abandoned, and Forgotten Code series. In this part we pad the ambit header with a fake ``malloc_chunk.size=0`` field to avoid crashing when the wrong pointer is passed to free().


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

With this update, assuming you've generated a working, minimized firmware, you should be able to exploit the SetFirmware vulnerability, and flash your firmware image to the router:

``./setfirmware.py <stage_1_firmware.bin>``