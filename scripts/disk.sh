#!/usr/bin/env bash

disk_write_speed() {
    time sh -c "dd if=/dev/zero of=ddfile bs=8k count=250000 && sync"
    rm ddfile
}

disk_read_speed() {
    ## Direct Read
    sudo hdparm -t /dev/nvme0n1
    ## Cache Read
    sudo hdparm -T /dev/nvme0n1
}
