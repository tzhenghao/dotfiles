# Always start in emacs mode
bindkey -e

PS1='%F{red}%* %F{cyan}(%~) %(?.%F{green}.%F{red})%#%f '

HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt SHARE_HISTORY HIST_IGNORE_DUPS

bindkey '^U' backward-kill-line

# Get the aliases and functions
[[ ! -f ~/.oxalate_shell_rc ]] || source ~/.oxalate_shell_rc

source <(fzf --zsh 2>/dev/null)
