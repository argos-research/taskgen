# Only Ubuntu 16.04 and python 3.5 are supported by taskgen.

install: taskgen mongodb

taskgen:
	sudo apt-get update
	sudo apt-get install python3 python3-pip
	pip3 install --user -r ./taskgen/requirements.txt

# mongodb community edition
# https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
mongodb:
	# Import the public key used by the package management system.
	sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
	# Create a list file for MongoDB.
	echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
	sudo apt-get update
	# Install the latest stable version of MongoDB
	sudo apt-get install -y mongodb-org
	@echo "MongoDB is not started automatically. If you want to use MongoDB, please run:"
	@echo "sudo service mongod start|stop"
