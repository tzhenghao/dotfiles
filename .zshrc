# User configuration

# Always start in emacs mode
bindkey -e

PS1='%F{red}%* %F{cyan}(%~) %(?.%F{green}.%F{red})%#%f '

HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=1000
setopt SHARE_HISTORY

# Get the aliases and functions
if [ -f ~/.oxalate_shell_rc ]; then
  . ~/.oxalate_shell_rc
fi

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

