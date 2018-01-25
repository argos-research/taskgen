`taskgen` is the command line tool for distributing and running task-sets at
multiple destination instances.

```bash
$ ./taskgen --help
usage: taskgen [-h] {run,list} ...

positional arguments:
  {run,list}
    run       runs a list of tasksets
    list      lists available tasksets

optional arguments:
  -h, --help  show this help message and exit
```

# Command parameters

| Command | Parameter          | Description                                |
| ------- | ------------------ | ------------------------------------------ |
| list    | -h, --help         | show this help message                     |
| list    | -t, --taskset      | print all available taskset  classes       |
| list    | -m, --monitor      | print all available monitors               |
| list    | -s, --session      | print all available session classes        |

| Command | Parameter                      | Description                                         |
| ------- | ------------------------------ | --------------------------------------------------- |
| run     | -h, --help                     | show this help message                              |
| run     | -d, --debug                    | print debug information to stdout                   |
| run     | -p PORT, --port PORT           | destination port. default: 3001                     |
| run     | -t CLASS, --taskset CLASS      | select a taskset class                              |
| run     | -m CLASS, --monitor CLASS      | select a monitor class                              |
| run     | -s CLASS, --session CLASS      | select a session class. default: PingSession        |
| run     | IP [IP ...]                    | IP address or a range of IP addresses (CIDR format) |


# Examples

Send the example taskset to all hosts in `172.25.0.0/24`. Before a connection is
established, all host are pinged. IP ranges are defined as
[CIDR](https://de.wikipedia.org/wiki/Classless_Inter-Domain_Routing)
format. 

```bash
./taskgen run -t example.Hey0TaskSet 172.25.0.0/24
```

Connect to multiple IP addresses or IP ranges:

```bash
./taskgen run -t example.Hey0TaskSet 172.25.0.0/24 172.26.0.0/24
```

Enable debug information:

```bash
./taskgen run -d -t example.Hey0TaskSet 172.25.0.1
```

Pretend the connection with `StdIOSession`:

When using the `stdio.StdIOSession` session, no real connection is established
and the actual task-sets are printed to stdout.

```bash
./taskgen run  -t example.Hey0TaskSet -s stdio.StdIOSession 172.25.0.1
```

Monitors handle incoming event logs:
```bash
./taskgen run -m sqlite.SQLiteMonitor 172.25.0.1
```

List all available task-sets:

```bash
./taskgen list --taskset
```

List all available monitors:

```bash
./taskgen list --monitor
```

List all available sessions:

```bash
./taskgen list --session
```

