# taskgen

A taskset generation framework for the
[genode-Taskloader](https://github.com/argos-research/genode-Taskloader)
component.



# Installation

## Python3.5

Only Ubuntu 16.04 with the default python version 3.5 is supported.

```
sudo apt-get install python3 python3-pip
```

## (Optional) MongoDB

Please follow external [Installation Guide](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)


## Toolchain

```
git clone --branch taskgen https://github.com/pecheur/toolchain-host.git
cd toolchain-host
git checkout tags/v1.0 
pip3 install --user -r ./taskgen/requirements.txt
```

# Getting started

The core of taskgen is the distribution of task-sets to running
genode-Taskloader instances. taskgen is shipped with a command line tool.


```bash
./taskgen-cli --help
```

Use the tool to list all available tasksets:

```bash
./taskgen-cli list --taskset
```

Task-sets in `example.*` are good starting points for testing and exploring
taskgen.

We want to distribute the `example.Hey0TaskSet` task-set to one destination
instance. The `stdio.StdIOSession` session prints the task-set to stdout,
instead of sending it over the network. 

```bash
./taskgen-cli run -d -t example.Hey0TaskSet -s stdio.StdIOSession 172.25.0.1
```


# Documentation
* [Overview](docs/overview.md) **up-to-date**
* [Command line](docs/commandline.md) **up-to-date**
* [Distributors](docs/distributor.md) **up-to-date**
* [Task-Sets](docs/taskset.md) **up-to-date**
* [Tasks](docs/tasks.md) **up-to-date**
* [Task Blocks](docs/blocks.md) **up-to-date**
* [Admission Control](docs/admctrl.md) **up-to-date**
* [Monitors](docs/monitor.md) **up-to-date**
* [Sessions](docs/session.md) **up-to-date**
* [Dictionary to XML format](docs/dict2xml.md) **up-to-date**
* [Qemu Startup Script](docs/qemu.md) **up-to-date**
