# AWS EC2 dev box guide

Default instance type: `g4dn.2xlarge`

AMI Name: *Deep Learning AMI GPU PyTorch 2.0.1 (Ubuntu 20.04) 20230620*

[Allocate static / elastic IP for the newly created instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html#using-instance-addressing-eips-allocating)

From [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/managing-users.html#create-user-account)

Default user is `ubuntu`.

## Add new user
`sudo adduser tzhenghao --disabled-password`

`sudo su - tzhenghao`

`mkdir .ssh`

`chmod 700 .ssh`

`touch .ssh/authorized_keys`

`chmod 600 .ssh/authorized_keys`

Set a password:

Exit and go back as `ubuntu` user, then run `sudo passwd tzhenghao`


### Granting tzhenghao sudo privileges
`sudo usermod -a -G wheel tzhenghao`


### Configuring Docker

From [here](https://docs.docker.com/engine/install/linux-postinstall).

`sudo usermod -aG docker $USER`


### AWS Deep Learning AMI with PyTorch 2.0.1
`source activate pytorch`

### (Optional): Removing a User

`sudo userdel -r olduser`

## Set Up mosh

`sudo apt install mosh`

Make sure AWS security group allows inbound connection from the UDP port ranges
60000-61000

## Set Up Git / GitHub

