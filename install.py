#!/usr/bin/env python3

import argparse
import logging
import os
from collections import namedtuple


### Configuration
Symlink = namedtuple('Symlink', ['source', 'dest'])
Download = namedtuple('Download', ['url', 'dest'])
Gitrepo = namedtuple('Gitrepo', ['url', 'reponame', 'sha'])
symlinks = [
MÅSTE FIXA CONFIGEN SÅ ATT git-meld-SYMLÄNKEN FUNKAR, UPPDATERA gitconfig!
OCH FIXA SYNTAX-HIGHLIGHTING I TERMINAL-VIN!
    Symlink(source='bashrc', dest='~/.bashrc'),
    Symlink(source='gitconfig', dest='~/.gitconfig'),
    Symlink(source='git-meld.py', dest='~/.git-meld.py'),
    Symlink(source='gvimrc', dest='~/.gvimrc'),
    Symlink(source='vimrc', dest='~/.vimrc'),
    Symlink(source='zshrc', dest='~/.zshrc'),
    Symlink(source='zshrc.zni', dest='~/.zshrc.zni'),

    # Symlink(source='gnome-term-profile.txt', dest='~/    <- this files content should be added to README.md
    # Symlink(source='install.py', dest='~/
    # Symlink(source='miw_base.zsh-theme', dest='~/
    # Symlink(source='miw.zsh-theme', dest='~/
    # Symlink(source='README.md', dest='~/
    # Symlink(source='show_256_colors.sh', dest='~/
    # Symlink(source='vim_plugins.txt', dest='~/
]
downloads = [
    Download(url='', dest=''),
]
git_repos = [
NÄSTA GÅNG FORTSÄTT HÄR.
FIXA SÅ JAG KLONAR GIT-REPON TILL BRA-STÄLLE<tm>
    Gitrepo(url='https://github.com/powerline/fonts.git',
            reponame='powerline_fonts.git',
            sha='b0abc65f621eba332002cba88b49d50e99a126f9')
]

# XXX anything more to do?
# TODO config changes, such as insert git email & username, more stuff?
'''
 cat ~/.zprofile
# User for which the username is hidden in the prompt
# DEFAULT_USER=miw

cat ~/.profile
# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022

# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
        if [ -f "$HOME/.bashrc" ]; then
                . "$HOME/.bashrc"
                    fi
                    fi

# set PATH so it includes user's private bin directories
PATH="$HOME/bin:$HOME/.local/bin:$PATH"

# User for which the username is hidden in the prompt
DEFAULT_USER=miw
'''

### Code

def main(args):
    if args.task == 'install':
        install()
    else:
        uninstall()

def parseargs():
    parser = argparse.ArgumentParser(description='Install & uninstall script for these settings files.')

    choices = ['install', 'uninstall']
    parser.add_argument('task', metavar='TASK', default='install', choices=choices,
                       help='TODO helptext')

    loglevels = ['error', 'info', 'debug', 'nologging']
    parser.add_argument('--loglevel', metavar='L', default='info', choices=loglevels, nargs='?',
                       help='TODO helptext')

    return parser.parse_args()

def install():
    log.debug('Creating symlinks.')
    cwd = os.getcwd()
    for symlink in symlinks:
        src = os.path.join(cwd, symlink.source)
        dst = os.path.expanduser(symlink.dest)
        if os.path.exists(dst):
            log.warning('No link created, {dst} exists'.format(dst=dst))
        else:
            log.info('Creating symlink {src} -> {dst}'.format(src=src, dst=dst))
            os.symlink(src, dst)
    log.debug('All symlinks created.')

def uninstall():
    log.debug('Deleting symlinks.')

    for symlink in symlinks:
        link = os.path.expanduser(symlink.dest)
        if os.path.islink(link):
            log.info('Deleting symlink {link}'.format(link=link))
            os.remove(link)
        else:
            log.warning('Could not delete {link}, file not found'.format(link=link))
    log.debug('All symlinks deleted.')

if __name__ == '__main__':
    args = parseargs()

    loglevel = getattr(logging, args.loglevel.upper(), None)
    logformat = '%(levelname)s:%(message)s'
    logging.basicConfig(level=loglevel, format=logformat)
    log = logging.getLogger(__name__)
    
    main(args)
