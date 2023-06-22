# AWS EC2 dev box guide

Default instance type: `g4dn.2xlarge`
AMI Name: Deep Learning AMI GPU PyTorch 2.0.1 (Amazon Linux 2) 20230613

From:
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/managing-users.html#create-user-account


sudo adduser tzhenghao
sudo su - tzhenghao
mkdir .ssh
chmod 700 .ssh
touch .ssh/authorized_keys
chmod 600 .ssh/authorized_keys
sudo passwd tzhenghao

# (Optional): Removing a User

`sudo userdel -r olduser`
