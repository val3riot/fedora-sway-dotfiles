# History
HISTFILE="$HOME/.zsh_history"
HISTSIZE=50000
SAVEHIST=50000

setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE
setopt SHARE_HISTORY
setopt AUTO_CD

# Completion
autoload -Uz compinit
compinit

zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'

# Autosuggestions
source /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh

# Syntax highlighting - must stay last
source /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# >>> Codex installer >>>
export PATH="/home/valeriot/.local/bin:$PATH"
# <<< Codex installer <<<
