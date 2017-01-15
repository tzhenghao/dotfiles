# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH=/Users/zhenghaotan/.oh-my-zsh

# Set name of the theme to load. Optionally, if you set this to "random"
# it'll load a random theme each time that oh-my-zsh is loaded.
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="cloud"

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion. Case
# sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# The optional three formats: "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git)

source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# ssh
# export SSH_KEY_PATH="~/.ssh/rsa_id"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"


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
alias loadsecrets='source ~/.secrets.sh'

# Typos.
alias sl='ls'
alias givm='gvim'

# Moar environment variables.
export EDITOR=vim

# Ctags.
alias gentags='ctags -R .'

# ARM toolchain
export PATH=$PATH:~/toolchains/gcc-arm-none-eabi-4_9-2015q3/bin

# MSP toolchain
export PATH=$PATH:~/toolchains/ti/gcc/bin

# CUDA toolchain
export PATH=$PATH:/Developer/NVIDIA/CUDA-7.5/bin
export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:/Developer/NVIDIA/CUDA-7.5/lib

# Go path.
export GOPATH=$HOME/Dropbox/GoProjects
export PATH=$PATH:$GOPATH/bin

# That's all folks!

# Shortcuts to remote machine logins.

export CLICOLOR=1
export LSCOLORS=GxFxCxDxBxegedabagacedkk

export PATH="/usr/local/sbin:$PATH"

export PATH="$PATH:/$HOME/toolchains/arcanist/bin"

alias userupdater='cd /Users/zhenghaotan/Dropbox/Arduino/firmware/Arduino_IDE_Integration/user/konektdash/cores/arduino'
alias systemupdater='cd /Users/zhenghaotan/Dropbox/Arduino/firmware/Releases/system_module/src/konekt_system_module'
