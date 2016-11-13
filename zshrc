# Lines configured by zsh-newuser-install
HISTFILE=~/.zsh_history
HISTSIZE=1000
SAVEHIST=10000
setopt appendhistory
unsetopt beep
bindkey -e
# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename '/home/miw/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall


############ MIW utilities
createDirectoryAndStepIntoIt() {
	mkdir $1
	cd $1
}
alias mkcd=createDirectoryAndStepIntoIt

# Go to a project git-repo
switchToProject() {
	TARGET_PROJECT_VENV_NAME=$1
	SWITCH_TO_TARGET_PROJECT_PATH=$(find $PROJ -name "*$TARGET_PROJECT_VENV_NAME*.git" -type d | sed 1q)
	cd $SWITCH_TO_TARGET_PROJECT_PATH
	# Activate virtualenv if there is one, otherwise just deactivate any currently active virtual environment
	if [ -d ~/.virtualenvs/${TARGET_PROJECT_VENV_NAME} ]; then
		workon $TARGET_PROJECT_VENV_NAME
	else
		# Silence the errormessage if there is no active environment.
		deactivate >& /dev/null
	fi
}
alias pr=switchToProject

# Python's virtualenv wrapper stuff
#source /usr/local/bin/virtualenvwrapper.sh

# Less options
# Tab stop 4 instead of default 8
# Preserve grep colors in
alias less='less -x4 -R'

# Search in python files, annoying to have to write so much
pythonFind() {
	grep -r --include=*.py --exclude-dir=migrations --exclude-dir=tests --exclude=tests.py --line-number "$@" .
}
pythonFindIncludeTests() {
	grep -r --include=*.py --exclude-dir=migrations --line-number "$@" .
}
pythonAndHtmlFind() {
	grep -r --include=*.py --include=*.html --exclude-dir=migrations --exclude-dir=tests --exclude=tests.py --line-number "$@" .
}
alias pf=pythonFind
alias pft=pythonFindIncludeTests
alias pfh=pythonAndHtmlFind

# Shortcuts are nice.
PROJ='/home/miw/projects'
alias proj='cd $PROJ'
# Django testing shortcut
# Standard test case - Run unit tests, fail fast and skip stylechecks
alias dt='tests.py --stop --nostyle --unittests'
# Run everything (except selenium, unless those are requested ofc)
alias dta='tests.py'

# Misc git shortcuts
alias gmb='git mkbranch'
alias gch='git checkout'
gitCommit() {
	git commit -m "$1" ${@:2}
}
alias gco=gitCommit
alias gb='git branch'
alias gs='git status'
alias gl='git tre'
alias ga='git add'
alias gch='git checkout'
alias gs='git status'

