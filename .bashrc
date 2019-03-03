#!/bin/bash

# .bashrc file
# Author: Zheng Hao Tan <tanzhao@umich.edu>
# MIT License

# These are my bashrc settings. Feel free to take whatever you want.

BLUE_BOLD='\[\e[01;34m\]'
RED_BOLD='\[\e[01;31m\]'
WHITE_BOLD='\[\e[01;0m\]'
PS1="${RED_BOLD}\t ${BLUE_BOLD}[${RED_BOLD}\W${BLUE_BOLD}]-> ${WHITE_BOLD}"

# Ignore case during tab completion.
bind 'set completion-ignore-case on'

# Get the aliases and functions
# shellcheck source=/dev/null
if [ -f ~/.oxalate_shell_rc ]; then
  . ~/.oxalate_shell_rc
fi

# shellcheck source=/dev/null
[[ -f "$HOME/git-completion.bash" ]] && source "$HOME/git-completion.bash"

# shellcheck source=/dev/null
[ -f ~/.fzf.bash ] && source ~/.fzf.bash
