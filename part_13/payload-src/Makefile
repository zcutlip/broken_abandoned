# Copyright (c) 2015
# - Zachary Cutlip <uid000()gmail.com>
# 
# See LICENSE for more details.
# 

STAGE1_DIR=$(PWD)/stage1
STAGE1_ROOTFS=$(STAGE1_DIR)/stage1-rootfs.bin
BUILD_FW_DIR=$(PWD)/../
STAGE1_IMAGE=stage1.chk

stage1:$(STAGE1_IMAGE)

$(STAGE1_IMAGE):$(STAGE1_ROOTFS) kernel-lzma.bin
	../firmware_building/build_janky_fw.py $@ kernel-lzma.bin $<
	
$(STAGE1_ROOTFS):
	make -C $(STAGE1_DIR)

bare clean:
	make -C $(STAGE1_DIR) $@
	-rm $(STAGE1_IMAGE)

