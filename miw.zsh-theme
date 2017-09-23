# # Goals
#
# The aim of this theme is to only show you *relevant* information. Like most
# prompts, it will only show git information when in a git working directory.
# However, it goes a step further: everything from the current user and
# hostname to whether the last call exited with an error to whether background
# jobs are running in this shell will all be displayed automatically when
# appropriate.

### Segment drawing
# End the prompt, closing any open segments
prompt_end() {
  echo -n "%F{white}→"
}

### Prompt components
# Each component will draw itself, and hide itself if no information needs to be shown

# Context: user@hostname (who am I and where am I)
prompt_context() {
  if [[ "$USER" != "$DEFAULT_USER" || -n "$SSH_CLIENT" ]]; then
    echo -n "%(!.%{%F{130}%}.)$USER@%m"
  fi
}

# Git: branch/detached head, dirty status
prompt_git() {
  (( $+commands[git] )) || return
  local ref dirty repo_path
  repo_path=$(git rev-parse --git-dir 2>/dev/null)

  if $(git rev-parse --is-inside-work-tree >/dev/null 2>&1); then
    #dirty=$(parse_git_dirty)
    ref=$(git symbolic-ref HEAD 2> /dev/null) || ref="➦ $(git rev-parse --short HEAD 2> /dev/null)"
    #if [[ -n $dirty ]]; then
    #  prompt_segment yellow black
    #else
    #  prompt_segment green black
    #fi
    #prompt_segment green black
    #prompt_segment magenta black

    setopt promptsubst
    autoload -Uz vcs_info

    zstyle ':vcs_info:*' enable git
    zstyle ':vcs_info:*' check-for-changes true
    #zstyle ':vcs_info:*' get-revision true
    #zstyle ':vcs_info:*' stagedstr '✚'
    #zstyle ':vcs_info:*' unstagedstr '●'
    #zstyle ':vcs_info:*' formats ' %u%c'
    #zstyle ':vcs_info:*' actionformats ' %u%c'

    # from kolo start
    zstyle ':vcs_info:*' stagedstr '%F{green}●'
    zstyle ':vcs_info:*' unstagedstr '%F{yellow}●'
    #zstyle ':vcs_info:*' check-for-changes true
    #zstyle ':vcs_info:(sv[nk]|bzr):*' branchformat '%b%F{1}:%F{11}%r'
    #zstyle ':vcs_info:*' enable git svn
    theme_precmd () {
        if [[ -z $(git ls-files --other --exclude-standard 2> /dev/null) ]] {
            zstyle ':vcs_info:*' formats ' [%b%c%u%B%F{green}]'
        } else {
            #zstyle ':vcs_info:*' formats ' [%b%c%u%B%F{red}●%F{green}]'
            zstyle ':vcs_info:*' formats ' [%b%c%u%B%F{red}●%F{magenta}]'
        }

        vcs_info
    }
    autoload -U add-zsh-hook
    add-zsh-hook precmd  theme_precmd
    # from kolo end

    vcs_info
    echo -n "%F{040}[%F{027}${ref/refs\/heads\//}%F{040}] "
  fi
}

# Dir: current working directory
prompt_dir() {
  echo -n '%F{040}%~ '
}

# Virtualenv: current working virtualenv
prompt_virtualenv() {
  local virtualenv_path="$VIRTUAL_ENV"
  if [[ -n $virtualenv_path ]]; then
    echo -n "%F{226}(`basename $virtualenv_path`) "
  fi
}

# Status:
# - was there an error
# - am I root
# - are there background jobs?
prompt_status() {
  local symbols
  symbols=()
  [[ $RETVAL -ne 0 ]] && symbols+="%{%F{red}%}✘"
  [[ $UID -eq 0 ]] && symbols+="%{%F{yellow}%}⚡"
  [[ $(jobs -l | wc -l) -gt 0 ]] && symbols+="%{%F{cyan}%}⚙"

  [[ -n "$symbols" ]] && echo -n "$symbols "
}

## Main prompt
build_prompt() {
  RETVAL=$?
  prompt_status
  prompt_virtualenv
  prompt_context
  prompt_dir
  prompt_git
  prompt_end
}

PROMPT='%{%f%b%k%}$(build_prompt) '
