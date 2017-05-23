# # Goals
#
# The aim of this theme is to only show you *relevant* information. Like most
# prompts, it will only show git information when in a git working directory.
# However, it goes a step further: everything from the current user and
# hostname to whether the last call exited with an error to whether background
# jobs are running in this shell will all be displayed automatically when
# appropriate.


### Color defines
# These works for all terminals supporint ASCII colors.
# Including Putty, MobaXTerm etc as well as GnomeTerminal.
# Using the 'echo "%F{colorcode}..."' variant doesn't work in most terminals.
prompt_setcolor_reset() {
	printf "\33[m"
}

prompt_setcolor_blue() {
	printf "\33[00;38;5;027m"
}

prompt_setcolor_green() {
	printf "\33[00;38;5;040m"
}

prompt_setcolor_lightblue() {
	printf "\33[00;38;5;105m"
}

prompt_setcolor_brown() {
	printf "\33[00;38;5;130m"
}

prompt_setcolor_red() {
	printf "\33[00;38;5;160m"
}

prompt_setcolor_yellow() {
	printf "\33[00;38;5;226m"
}

### Segment drawing
# End the prompt, closing any open segments
prompt_end() {
	prompt_setcolor_reset
	echo -n "→"
}

### Prompt components
# Each component will draw itself, and hide itself if no information needs to be shown

# Context: user@hostname (who am I and where am I)
prompt_context() {
	if [[ "$USER" != "$DEFAULT_USER" || -n "$SSH_CLIENT" ]]; then
		prompt_setcolor_brown
		echo -n "$USER@%m"
	fi
}

# Git: branch/detached head, dirty status
prompt_git() {
  (( $+commands[git] )) || return
  local ref repo_path
  repo_path=$(git rev-parse --git-dir 2>/dev/null)

  if $(git rev-parse --is-inside-work-tree >/dev/null 2>&1); then
    ref=$(git symbolic-ref HEAD 2> /dev/null) || ref="➦ $(git rev-parse --short HEAD 2> /dev/null)"
    prompt_setcolor_green
    echo -n "["
    prompt_setcolor_blue
    echo -n "${ref/refs\/heads\//}"
    prompt_setcolor_green
    echo -n "] "
  fi
}

# Dir: current working directory
prompt_dir() {
	prompt_setcolor_green
	echo -n '%~ '
}

# Virtualenv: current working virtualenv
prompt_virtualenv() {
	local virtualenv_path="$VIRTUAL_ENV"
	if [[ -n $virtualenv_path ]]; then
		prompt_setcolor_yellow
		echo -n "(`basename $virtualenv_path`) "
	fi
}

# Status:
# - was there an error
# - am I root
# - are there background jobs?
prompt_status() {
	local symbols
	symbols=()
	[[ $RETVAL -ne 0 ]] && prompt_setcolor_red && echo -n "✘" && symbols=1
	[[ $UID -eq 0 ]] && prompt_setcolor_yellow && echo -n "⚡" && symbols=1
	[[ $(jobs -l | wc -l) -gt 0 ]] && prompt_setcolor_lightblue && echo -n "⚙" && symbols=1
	
	# print space if one or more symbols are printed
	[[ -n "$symbols" ]] && echo -n " "
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

PROMPT='$(build_prompt) '
