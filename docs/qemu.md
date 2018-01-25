# Qemu on Localhost

Sometimes a genonde instanse freezes and does not respond to connection establishments. The only way to solve this problem is killing the qemu instance and restarting the operating system. The `qemu-up.sh` script and `taskgen.sessions.geenode.QemuSession` are a solution to automatically do this job.

## qemu-up.sh

1. Create a TAP device and add it to a bridge
2. Randomly choose a MAC address for the simulated OS
3. Start a qemu instance
4. Listen for a new IP address in `/tmp/taskgen_qemusession_ip_kill.log` until an IP address is appended to the file
5. Look up its MAC address in the ARP table
6. If the MAC address is similar to the MAC address of the simulated OS, the qemu instance is killed
7. The entry with this MAC address is removed from the ARP table
7. Goto 2

This process can be stopped by pressing `CTRL-C`. A bash-trap will execute following last commands:

1. Kill currecntly running qemu instance
2. Remove TAP device from bridge

## QemuSession

The `QemuSession` behaves like a normal Ping/GenodeSession, but whenever a socket timeout occurs, the IP address of the target plattform is pushed to `/tmp/taskgen_qemusession_ip_kill.log`.


## Limitations

* The `qemu-up.sh` script only works with a virtual network bridge. `VDE` is not supported.
* VirtualBox is not supported.
* You have to create the bridge.
* The mechanims for sharing the IP addresses between `QemuSesion` and `qemu-up.sh` is done by a file. Due to this limitation, it is not possible to use this concept via network. The qemu instances have to run on you localhost.
* The user, who starts the `taskgen` process needs `WRITE` rights for `/tmp`.
* It is possible to start multiple `qemu-up.sh` scripts.
* `qemu-up.sh` have to run as `root`.


## Example

A bridge is created with the name `netbr1` and the IP range `172.25.1.0` and submask `255.255.255.0`. Furthermore a DHCP server is listening.

### Terminal 1

Create the first qemu instance.

```
sudo qemu-up.sh netbr1 tap1
```


### Terminal 2

Create a second qemu instance.

```
sudo qemu-up.sh netbr1 tap2
```


### Terminal 3

```
./taskgen-cli run -d -t test.Test1 -s genode.QemuSession 172.25.1.0/24
```
