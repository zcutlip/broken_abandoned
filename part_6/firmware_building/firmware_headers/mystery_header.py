#!/usr/bin/env python
# Copyright (c) 2015
# - Zachary Cutlip <uid000()gmail.com>
# 
# See LICENSE for more details.
# 

from bowcaster.common.support import LittleEndian
from bowcaster.common.support import BigEndian
from bowcaster.development import OverflowBuffer
from bowcaster.development import SectionCreator
from bowcaster.common.support import Logging
import struct

class MysteryHeader(object):
    """
    Class to generate a stand-in for the 58 byte unidentified header
    at the beginning of Netgear R6200 firmware images.
    """
    
    #Magic gets checked with strcmp()
    #so must be null terminated,
    #but following field is big endian, with a high byte of 0.
    MAGIC="*#$^"
    MAGIC_OFF=0
    
    #observed size in real-world examples.
    #this may be variable
    HEADER_SIZE=58
    HEADER_SIZE_OFF=4
    
    
    def __init__(self,image_data,logger=None):
        """
        Params
        ------
        image_data: The actual data of the firmware image this header should
                    describe and be prepended to.
        logger:     Optional. A Bowcaster Logging object. If a logger is not 
                    provided, one will be instantiated.
        """
        if not logger:
            logger=Logging(max_level=Logging.DEBUG)
        self.logger=logger
        
        logger.LOG_DEBUG("Creating ambit header.")

        self.size=self.HEADER_SIZE
        
        header=self.__build_header()
        self.header=header

    
    def __build_header(self):
        
        logger=self.logger
        
        SC=SectionCreator(BigEndian,logger=logger)
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
        """
        Find the offset of the given value in the Bowcaster OverflowBuffer string.
        
        Params
        ------
        value:  The value whose offset should be found. May be a string or
                integer. If an integer is provided, it will be converted to
                a packed binary string with the same endianness as the
                underlying OverflowBuffer object.
        """
        return self.header.find_offset(value)

