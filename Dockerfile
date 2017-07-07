FROM ubuntu:latest

MAINTAINER Zheng Hao Tan <tanzhao@umich.edu>

# Installations
RUN apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y vim git zsh wget tmux
  && apt-get autoclean \
  && apt-get autoremove

# Install zsh
RUN sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
CMD zsh

# Download software configs
RUN git clone https://github.com/tzhenghao/SoftwareDevConfigs.git

# Set up bash configs.
RUN cp SoftwareDevConfigs/.bashrc ~
CMD ["source", "~/.bashrc"]

# Set up zsh configs.
RUN cp SoftwareDevConfigs/.zshrc ~
CMD ["source", "~/.zshrc"]

# Set up vim configs.
RUN cp SoftwareDevConfigs/.vimrc ~

# Set up tmux configs.
RUN cp SoftwareDevConfigs/.tmux.conf ~
