##Broken, Abandoned, and Forgotten Code, Part 9

This code corresponds with [part 9](http://shadow-file.blogspot.com/2015/06/abandoned-part-09.html) of the Broken, Abandoned, and Forgotten Code series. In this part we fill in enough of the ambit header to satisfy ``upnpd``'s loose validation and allow the firmware to be written to flash. The ``janky_ambit_header.py`` module has been updated with the necessary header fields to accomplish this.

You may wish to simply test with a <4MB blob of random data to avoid crashing ``upnpd``.

Alternatively, you can try using an actual kernel and filesystem, but an image over 4MB will result in a crash due to a bug in ``upnpd``.


#####Note: This program does not generate a working firmware image. It is for debugging and analyzing as described in the Broken, Abandoned series.

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
