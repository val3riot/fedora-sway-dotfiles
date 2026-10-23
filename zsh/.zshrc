# History
HISTFILE="$HOME/.zsh_history"
HISTSIZE=50000
SAVEHIST=50000

setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE
setopt SHARE_HISTORY
setopt AUTO_CD

# Completion
autoload -Uz compinit vcs_info
compinit

zstyle ':vcs_info:*' enable git
zstyle ':vcs_info:git:*' formats ' [%F{yellow}%b%f]'
zstyle ':vcs_info:git:*' actionformats ' [%F{yellow}%b%f|%F{red}%a%f]'
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'

# Git branch
precmd() { vcs_info }
setopt prompt_subst
PROMPT='%F{cyan}%~%f${vcs_info_msg_0_} %# '
# Autosuggestions
source /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh

# Syntax highlighting - must stay last
source /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# >>> Codex installer >>>
export PATH="/home/valeriot/.local/bin:$PATH"
# <<< Codex installer <<<

#THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
