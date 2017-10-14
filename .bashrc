#!/bin/bash

# .bashrc file
# Author: Zheng Hao Tan <tanzhao@umich.edu>
# MIT License

# These are my bashrc settings. Feel free to take whatever you want.

PS1='\[\033[01;36m\]\t \[\033[01;34m\][\[\033[01;31m\]\W\[\033[01;34m\]]-> \[\033[0;0m\]'

# Ignore case during tab completion.
bind 'set completion-ignore-case on'

# Get the aliases and functions
# shellcheck source=/dev/null
if [ -f ~/.oxalate_shell_rc ]; then
  . ~/.oxalate_shell_rc
fi

# shellcheck source=/dev/null
[[ -f "$HOME/git_completion.bash" ]] && source "$HOME/git_completion.bash"
