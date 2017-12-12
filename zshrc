#### LOCAL MACHINE ALIASES AND SETTINGS
# Place custom things related to machine / environment here.
# E.g. Aliases for a specific project, environment variables.

# Set to user from user@hostname to hide that part from the prompt when being that user.
source /etc/zsh-config-scripts-defaultuser  # Should _only_ contain DEFAULT_USER, e.g. export DEFAULT_USER=foobar
DEFAULT_USER_HOME=/home/$DEFAULT_USER

# Load 
for machineCustomConfigFile in ${DEFAULT_USER_HOME}/.localsettings/*.sh; do
	source $machineCustomConfigFile
done

#### LOCAL MACHINE ALIASES AND SETTINGS END


# Disable the default virtualenvwrapper prompt
export VIRTUAL_ENV_DISABLE_PROMPT=1

# Enable virtualenvwrapper
source /usr/local/bin/virtualenvwrapper.sh

# Node version manager.
# https://github.com/creationix/nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This load nvm

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

# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH=/home/martin/.oh-my-zsh

# Set name of the theme to load. Optionally, if you set this to "random"
# it'll load a random theme each time that oh-my-zsh is loaded.
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
#ZSH_THEME="agnoster"
#ZSH_THEME="cloud"
#ZSH_THEME="jnrowe"
ZSH_THEME="miw"

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion. Case
# sensitive completion must be off. _ and - will be interchangeable.
HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

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
# HIST_STAMPS="yyyy-mm-dd"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git zsh-autosuggestions pip django pass)

source $ZSH/oh-my-zsh.sh

# Prevent Python from writing bytecode (.pyc) files.
export PYTHONDONTWRITEBYTECODE=pretty_please

# User configuration

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"
#

############ Aliases
# Less options
# Tab stop 4 instead of default 8
# Preserve grep colors in
alias less='less -x4 -R'

# Always list PID for jobs command
alias jobs='jobs -l'

# Shortcuts are nice.
PROJ='/home/miw/projects'
alias proj='cd $PROJ'

# JSON formatting
alias jsonformat='python -m json.tool'

# Pytest with last-failed option (run last failed tests, or all of them if none failed last run).
alias ptlf='pytest --last-failed'

# Misc git shortcuts
alias gmb='git mkbranch'
alias gch='git checkout'
gitCommit() {
	if [ -n "$1" ]; then
		git commit -m "$1" ${@:2}
	else
		git commit
	fi
}
alias gco=gitCommit
alias gb='git branch'
alias gs='git status'
alias gl='git tre'
alias glf='git tref'
alias ga='git add'
alias gch='git checkout'


############ Functions
# Create directory and immediately step into it
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

# Search in python files, annoying to have to write so much
pythonFind() {
	grep -r --include='*.py' --exclude-dir='migrations' --exclude-dir='tests' --exclude-dir='node_modules' --exclude-dir='.tox' --exclude='tests.py' --line-number "$@" .
}
pythonFindIncludeTests() {
	grep -r --include='*.py' --exclude-dir='migrations' --exclude-dir='node_modules' --exclude-dir='.tox' --line-number "$@" .
}
pythonAndHtmlFind() {
	grep -r --include='*.py' --include='*.html' --exclude-dir='migrations' --exclude-dir='tests' --exclude-dir='node_modules' --exclude-dir='.tox' --exclude='tests.py' --line-number "$@" .
}
alias pf=pythonFind
alias pft=pythonFindIncludeTests
alias pfh=pythonAndHtmlFind

# Fix dependencies-script, supports multiple project folder structures and also can relink external egg dependencies.
alias smurf=~/.dependency_fiddling.py
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion


# NOTE: This must be at the end of the file for sdkman to work
export SDKMAN_DIR="/home/martin/.sdkman"
[[ -s "/home/martin/.sdkman/bin/sdkman-init.sh" ]] && source "/home/martin/.sdkman/bin/sdkman-init.sh"
