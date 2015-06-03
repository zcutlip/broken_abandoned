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
from checksums.libacos import LibAcosChecksum
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
    #Hard code for now. This can be made configurable later.
    HEADER_SIZE=58
    HEADER_SIZE_OFF=4
    
    HEADER_CHECKSUM_OFF=36
    
    #This is the board ID extracted from NVRAM.
    #Hard code for now. We can make this configurable later.
    BOARD_ID="U12H192T00_NETGEAR"
    BOARD_ID_OFF=40
    
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
        
        logger.LOG_INFO("Building header without checksum.")
        header=self.__build_header()
        logger.LOG_INFO("Calculating header checksum.")
        chksum=self.__checksum(header)
        logger.LOG_DEBUG("Calculated header checksum: 0x%08x" % chksum)
        logger.LOG_INFO("Building header with checksum.")
        header=self.__build_header(checksum=chksum)
        self.header=header

    
    def __build_header(self,checksum=0):
        
        logger=self.logger
        
        SC=SectionCreator(BigEndian,logger=logger)
        SC.string_section(self.MAGIC_OFF,self.MAGIC,
                            description="Magic bytes for ambit header.")
        SC.gadget_section(self.HEADER_SIZE_OFF,self.size,"Size field representing length of ambit header.")
        #Set header checksum
        SC.gadget_section(self.HEADER_CHECKSUM_OFF,checksum)
        
        #Set board ID
        SC.string_section(self.BOARD_ID_OFF,self.BOARD_ID,
                            description="Board ID string.")
        
        buf=OverflowBuffer(BigEndian,self.size,
                            overflow_sections=SC.section_list,
                            logger=logger)
        return buf
    
    def __checksum(self,header):
        data=str(header)
        size=len(data)
        chksum=LibAcosChecksum(data,size)
        return chksum.checksum
            
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

