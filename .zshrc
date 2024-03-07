# User configuration

# Always start in emacs mode
bindkey -e

PS1='%F{red}%* %F{cyan}(%~) %(?.%F{green}.%F{red})%#%f '

# Get the aliases and functions
if [ -f ~/.oxalate_shell_rc ]; then
  . ~/.oxalate_shell_rc
fi

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

