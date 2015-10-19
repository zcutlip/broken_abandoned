SRC=$(PWD)/src

MKSQUASHFS=netgear-r6200-mksquashfs
stage2-rootfs.bin:
	make -C $(SRC) install
	$(MKSQUASHFS) $(SRC)/rootfs $@ -noappend -all-root

clean:
	-rm -f stage2-rootfs.bin
	make -C $(SRC) $@

