#!/usr/bin/env python

from bowcaster.common.support import LittleEndian
from bowcaster.common.support import BigEndian
from bowcaster.development import OverflowBuffer
from bowcaster.development import SectionCreator
from bowcaster.common.support import Logging
import struct

class MysteryHeader(object):
    #ambit magic gets checked with strcmp()
    #so must be null terminated,
    #but following field is big endian, with a high byte of 0.
    MAGIC="*#$^\x00"

    #observed size in real-world examples.
    #this may be variable
    HEADER_SIZE=58
    HEADER_SIZE_OFF=4
    
    
    def __init__(self,image_data,logger=None):
        if not logger:
            logger=Logging(max_level=Logging.DEBUG)
        self.logger=logger
        
        logger.LOG_DEBUG("Creating ambit header.")

        self.size=self.HEADER_SIZE
        
        header=self.__build_header(logger=logger)
        self.header=header

    
    def __build_header(self,checksum=0):
        
        logger=self.logger
        
        SC=SectionCreator(self.endianness,logger=logger)
        SC.string_section(self.MAGIC_OFF,self.MAGIC,
                            description="Magic bytes for ambit header.")
        SC.gadget_section(self.HEADER_SIZE_OFF,self.size,"Size field representing length of ambit header.")
        
        buf=OverflowBuffer(BigEndian,self.size,
                            overflow_sections=SC.section_list,
                            logger=logger)
        return buf
            
    def __str__(self):
        return str(self.header)
    
    def find_offset(self,value):
        return self.header.find_offset(value)

