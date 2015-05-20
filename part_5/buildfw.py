#!/usr/bin/env python

from firmware_headers import trx
from firmware_headers.mystery_header import MysteryHeader
from bowcaster.common.support import Logging
import sys

class FirmwareImage(object):
    
    def __init__(self,input_files,logger=None):
        if not logger:
            logger=Logging(max_level=Logging.DEBUG)
        self.logger=logger
        
        trx_img=trx.TrxImage(input_files,trx.LittleEndian,logger=logger)
        header=MysteryHeader(str(trx_img),logger=logger)
        
        self.trx_img=trx_img
        self.header=header
    
    def find_offset(self,value):
        return self.header.find_offset(value)
    
    def __str__(self):
        return str(self.header)+str(self.trx_img)


def main(input_files,output_file,find_str=None):
    logger=Logging(max_level=Logging.DEBUG)

    logger.LOG_DEBUG("Building firmware from input files: %s" % str(input_files))
    
    fwimage=FirmwareImage(input_files)

    if find_str:
        find=find_str
        if find_str.startswith("0x"):
            find=int(find_str,0)
            logger.LOG_DEBUG("Finding offset of 0x%08x" % find)
        else:
            logger.LOG_DEBUG("Finding offset of %s" % find)

        offset=fwimage.find_offset(find)
        logger.LOG_INFO("Offset: %s" % offset)
    else:
        logger.LOG_INFO("Writing firmware to %s\n" % output_file)
        out=open(output_file,"wb")
        out.write(str(fwimage))
        out.close()

if __name__ == "__main__":
    find=None
    filename=None
    if sys.argv[1].startswith("find="):
        find=sys.argv[1].split("=",1)[1]
    else:
        filename=sys.argv[1]

    parts=sys.argv[2:]
    main(parts,filename,find_str=find)
