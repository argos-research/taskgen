#!/bin/bash

# For more information read `taskgen/docs/qemu.md`.

# CHOOSE A TAP DEVICE NAME
tap="$2"  # tap + first parameter
# CHOOSE A BRIDGE
bridge="$1"
image="../build/genode-focnados_pbxa9/var/run/dom0-HW/image.elf"

# taskgen.sessions.QemuSession write IP addresses for killing into this file
log="/tmp/taskgen_qemusession_ip_kill.log"

# create tap device
ip tuntap add name $tap mode tap
brctl addif $bridge $tap
ip link set dev $tap up

function cmd_del_tap {
    # delete tap device
    ip link set dev $tap down
    brctl delif $bridge $tap
    ip tuntap del $tap mode tap
}


pid=0

# this trap will clean up
function cmd_stop {
    #kill qemu
    kill -9 $pid
    cmd_del_tap
    exit
}

trap 'cmd_stop' SIGINT ERR
while true;
do
    # generate random MAC address
    mac="$(hexdump -vn3 -e '/3 "52:54:00"' -e '/1 ":%02x"' -e '"\n"' /dev/urandom)"

    # start qemu in background
    qemu-system-arm -net tap,ifname=$tap,script=no,downscript=no \
		            -net nic,macaddr=$mac \
		            -net nic,model=lan9118 \
		            -nographic \
		            -smp 2 \
		            -m 1000 \
		            -M realview-pbx-a9 \
		            -kernel $image &
    pid=$!

    # wait until file exists
    until [ -f $log ]
    do
        sleep 1
    done

    # read file and kill own qemu instance if necessary
    tail -f -n0 $log | while read kill_ip
    do
        kill_mac=$(arp -n | grep -w -i $kill_ip | awk '{print $3}')
        echo "read  $kill_ip $kill_mac"

        # compare the target MAC with our own MAC
        if [ "$kill_mac" == "$mac" ]; then
            kill -9 $pid
            arp -d $mac
            break
        fi
    done
done
