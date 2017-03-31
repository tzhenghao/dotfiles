# .bashrc file
# Author: Zheng Hao Tan <tanzhao@umich.edu>

# These are my bashrc settings. Feel free to take whatever you want.
alias gcc='gcc-6'
alias g++='g++-6'
alias tar='gtar'

PS1='\[\033[01;36m\]\t \[\033[01;34m\][\[\033[01;31m\]\W\[\033[01;34m\]]-> \[\033[0;0m\]'

# Ignore case during tab completion.
bind 'set completion-ignore-case on'

# My own aliases.
alias q='exit'
alias c='clear'
alias h='history'
alias cs='clear;ls'
alias p='cat'
alias pd='pwd'
alias lsa='ls -a'
alias lsl='ls -l'
alias pd='pwd'
alias t='time'
alias null='/dev/null'

# Directories
alias home='cd ~'
alias root='cd /'
alias dtop='cd ~/Desktop'
alias dbox='cd ~/Dropbox'
alias box='cd ~/Box\ Sync'
alias gdrive='cd ~/Google\ Drive'
alias code='cd ~/code'
alias o=open
alias ..='cd ..'
alias ...='cd ..; cd ..'
alias ....='cd ..; cd ..; cd ..'

# Git Shortcuts
alias g='git'
alias st='git status'
alias com='git commit -m'
alias clone='git clone'
alias sth='git stash'
alias lg='git log'
alias u='git add -u'
alias all='git add .'

# Shortcuts to my software projects
alias projects='cd ~/Dropbox/Projects'
alias iosprojects='cd ~/Dropbox/Projects/iOSProjects'
alias pebbleprojects='cd ~/Dropbox/Projects/PebbleProjects'
alias cppprojects='cd ~/Dropbox/Projects/C++Projects'
alias cprojects='cd ~/Dropbox/Projects/CProjects'
alias pythonprojects='cd ~/Dropbox/Projects/PythonProjects'
alias goprojects='cd ~/Dropbox/Projects/GoProjects'
alias rustprojects='cd ~/Dropbox/Projects/RustProjects'
alias arduinoprojects='cd ~/Dropbox/Arduino'
alias notebook='cd ~/Dropbox/Notebook'
alias docs='cd ~/Documents'

# Shortcuts to vimrc and bashrc
alias vimrc='vim ~/.vimrc'
alias bashrc='vim ~/.bash_profile'
alias zshrc='vim ~/.zshrc'
alias loadbash='source ~/.bash_profile'
alias loadzsh='source ~/.zshrc'
alias loadsecrets='source ~/.secrets.sh'

# Typos.
alias sl='ls'
alias givm='gvim'

# Moar environment variables.
export EDITOR=vim

# Grep options
export GREP_OPTIONS='--color=auto'

# Ctags.
alias gentags='ctags -R .'

# ARM toolchain
export PATH=$PATH:~/toolchains/gcc-arm-none-eabi-4_9-2015q3/bin

# MSP toolchain
export PATH=$PATH:~/toolchains/ti/gcc/bin

# CUDA toolchain
export PATH=$PATH:/Developer/NVIDIA/CUDA-8.0/bin
export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:/Developer/NVIDIA/CUDA-8.0/lib

export CLICOLOR=1
export LSCOLORS=GxFxCxDxBxegedabagacedkk

export PATH="/usr/local/sbin:$PATH"

export PATH="$PATH:/$HOME/toolchains/arcanist/bin"

# MagicSnippets scripts
export PATH="$PATH:/Users/zhenghaotan/Dropbox/Projects/MagicSnippets"

alias meow='cat'

# Help with extractions
extract () {
  if [ -f $1 ] ; then
    case $1 in
      *.tar.bz2)   tar xvjf $1    ;;
      *.tar.gz)    tar xvzf $1    ;;
      *.bz2)       bunzip2 $1     ;;
      *.rar)       unrar x $1       ;;
      *.gz)        gunzip $1      ;;
      *.tar)       tar xvf $1     ;;
      *.tbz2)      tar xvjf $1    ;;
      *.tgz)       tar xvzf $1    ;;
      *.zip)       unzip $1       ;;
      *.Z)         uncompress $1  ;;
      *.7z)        7z x $1        ;;
      *)           echo "don't know how to extract '$1'..." ;;
    esac
  else
    echo "'$1' is not a valid file!"
  fi
}

# That's all folks!
