#!/usr/bin/env python3

import argparse
import logging
import os
import shutil
import subprocess
import urllib.request
from collections import namedtuple

### Configuration
Symlink = namedtuple('Symlink', ['source', 'dest'])
Copy = namedtuple('Copy', ['source', 'dest'])
Download = namedtuple('Download', ['url', 'filename', 'dest'])
Gitrepo = namedtuple('Gitrepo', ['url', 'reponame', 'sha', 'dest'])

LOCALSETTINGS = 'localsettings'
DOWNLOADS_AND_GITREPOS = 'downloads_and_gitrepos'

DOT_VIM_FOLDERS = (
    'autoload',
    'bundle',
    'colors',
    'ftplugin',
    'indent',
    'plugin',
    'syntax',
)

POWERLINE_FONTS = 'powerline_fonts.git'
PATHOGEN_VIM = 'pathogen-vim.git'
CTRLP_VIM = 'ctrlp-vim.git'
EMMET_VIM = 'emmet-vim.git'
JEDI_VIM = 'jedi-vim.git'
NERDTREE_VIM = 'nerdtree.git'
SYNTASTIC_VIM = 'syntastic.git'
AIRLINE_VIM = 'vim-airline.git'
AIRLINE_THEMES_VIM = 'vim-airline-themes.git'
COLORS_SOLARIZED_VIM = 'vim-colors-solarized.git'
COLORSCHEMES_VIM = 'vim-colorschemes.git'
PYTHON_SYNTAX_VIM = 'python-syntax.git'

symlinks = [
    Symlink(source='bashrc',
            dest='~/.bashrc'),
    Symlink(source='gitconfig',
            dest='~/.gitconfig'),
    Symlink(source='git-meld.py',
            dest='~/.git-meld.py'),
    Symlink(source='gvimrc',
            dest='~/.gvimrc'),
    Symlink(source='vimrc',
            dest='~/.vimrc'),
    Symlink(source='zshrc',
            dest='~/.zshrc'),
    Symlink(source='zshrc.zni',
            dest='~/.zshrc.zni'),

    Symlink(source=LOCALSETTINGS,
            dest='~/.localsettings'),

    Symlink(source=DOWNLOADS_AND_GITREPOS + "/" + POWERLINE_FONTS,
            dest='~/.powerlinefonts'),
]

#git_symlinks = [  # All these sources are prepended with: DOWNLOADS_AND_GITREPOS + "/"
#    Symlink(source=PATHOGEN_VIM + '/', dest=),
#    Symlink(source=, dest=),
#    Symlink(source=, dest=),
#    Symlink(source=, dest=),
#    Symlink(source=, dest=),
#    Symlink(source=, dest=),
#    # Symlink(source='gnome-term-profile.txt', dest='~/    <- this files content should be added to README.md
#    # Symlink(source='install.py', dest='~/
#    # Symlink(source='miw_base.zsh-theme', dest='~/
#    # Symlink(source='miw.zsh-theme', dest='~/
#    # Symlink(source='README.md', dest='~/
#    # Symlink(source='show_256_colors.sh', dest='~/
#    # Symlink(source='vim_plugins.txt', dest='~/
#]

#copyactions = [
#    Copy(source=PATHOGEN_VIM, dest=),
#    Copy(source=, dest=),
#    Copy(source=, dest=),
#    Copy(source=, dest=),
#]
downloads = [
    Download(url='http://www.vim.org/scripts/download_script.php?src_id=4316',
             filename='python.vim',  # wget "URL" -O filename
             dest=DOWNLOADS_AND_GITREPOS),
]

git_repos = [
    Gitrepo(url='https://github.com/powerline/fonts.git',
            reponame=POWERLINE_FONTS,
            sha='b0abc65f621eba332002cba88b49d50e99a126f9',
            dest=DOWNLOADS_AND_GITREPOS),
    Gitrepo(url='https://github.com/tpope/vim-pathogen.git',
            reponame=PATHOGEN_VIM,
            sha='379b8f70822c4a89370575c3967f33cb116087ea',
            dest=DOWNLOADS_AND_GITREPOS),  # COPY TO autoload
    Gitrepo(url='https://github.com/ctrlpvim/ctrlp.vim.git',
            reponame=CTRLP_VIM,
            sha='cbd52e3bdd388afd7accaba6e0aea754f32da271',
            dest=DOWNLOADS_AND_GITREPOS),
    Gitrepo(url='https://github.com/mattn/emmet-vim.git',
            reponame=EMMET_VIM,
            sha='6c38fe86c1fd7f68d40bf4f220c5e1f360d0b57a',
            dest=DOWNLOADS_AND_GITREPOS),
    Gitrepo(url='https://github.com/davidhalter/jedi-vim.git',
            reponame=JEDI_VIM,
            sha='40a02a7fd187bf82ce3cda517feffbda8015ef5c',
            dest=DOWNLOADS_AND_GITREPOS),
    Gitrepo(url='https://github.com/scrooloose/nerdtree.git',
            reponame=NERDTREE_VIM,
            sha='0b84d458d607f0326b7718c92ba20f2627f63342',
            dest=DOWNLOADS_AND_GITREPOS),
    Gitrepo(url='https://github.com/vim-syntastic/syntastic.git',
            reponame=SYNTASTIC_VIM,
            sha='5efeecece3f512076513e8ee1e7444157a16a77b',
            dest=DOWNLOADS_AND_GITREPOS),
    Gitrepo(url='https://github.com/vim-airline/vim-airline.git',
            reponame=AIRLINE_VIM,
            sha='466198adc015a9d81e975374d8e206dcf3efd173',
            dest=DOWNLOADS_AND_GITREPOS),
    Gitrepo(url='https://github.com/vim-airline/vim-airline-themes.git',
            reponame=AIRLINE_THEMES_VIM,
            sha='3a39c85598aae19052aa0e2fe0512c8b228c0136',
            dest=DOWNLOADS_AND_GITREPOS),
    Gitrepo(url='https://github.com/altercation/vim-colors-solarized.git',
            reponame=COLORS_SOLARIZED_VIM,
            sha='528a59f26d12278698bb946f8fb82a63711eec21',
            dest=DOWNLOADS_AND_GITREPOS),  # COPY TO bundle
    # vim-colorschemes.git/colors/molokai.vim, solarized.vim
    Gitrepo(url='https://github.com/flazz/vim-colorschemes.git',
            reponame=COLORSCHEMES_VIM,
            sha='b8dff40f69f1873effbed97c759a8452ecb240ed',
            dest=DOWNLOADS_AND_GITREPOS),  # COPY TO colors (the files above)
    Gitrepo(url='https://github.com/hdima/python-syntax.git',
            reponame=PYTHON_SYNTAX_VIM,
            sha='69760cb3accce488cc072772ca918ac2cbf384ba',
            dest=DOWNLOADS_AND_GITREPOS),  # COPY TO syntax
]

# TODO Make a script that goes through all git-repos and updates them, and syncs new sha:s to the repo config.
#      That way it's easy to keep things up-to-date, and there's a log of what things has been updated.
#      Probably good to make as an option, "install" / "uninstall" / "gitupdates".

# TODO Make script part taking user input and addeding it to localsettingsfolder.
#      also create that folder and then symlink it.

# TODO move the dependency-fiddling-script to this machine, also symlink it.

# XXX Idea: Install apt-stuff if it's a ubuntu machine?
#     Perhaps just output a .apt-line from a file?
#     Answer: Ignore for now, would be nice, but nowhere to easily test it.
#             Fix in the future when it's needed.

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
    _create_folders()

    _create_localsettings()

    _download_files()

    _clone_gitrepos()

    #_create_symlinks()


def _create_folders():
    """Create all folders for storing local settings, downloads, gitrepos etc."""
    def _create_folder(folder, created_message, exists_message):
        """Create a folder. If the folder already exists nothing happens."""
        if not os.path.exists(folder):
            log.debug(created_message)
            os.mkdir(folder)
        else:
            log.debug(exists_message)

    _create_folder(folder=LOCALSETTINGS,
                   created_message='Creating localsettings folder "{dir}".'.format(
                       dir=LOCALSETTINGS),
                   exists_message='Localsettings folder "{dir}" exists, skipping creation.'.format(
                       dir=LOCALSETTINGS))

    _create_folder(folder=DOWNLOADS_AND_GITREPOS,
                   created_message='Creating downloads_and_gitrepos folder "{dir}".'.format(
                       dir=DOWNLOADS_AND_GITREPOS),
                   exists_message='Downloads_and_gitrepos folder "{dir}" exists, skipping creation.'.format(
                       dir=DOWNLOADS_AND_GITREPOS))


def _create_localsettings():
    # TODO input to store GIT user data
    pass


def _download_files():
    """Download files to their destinations as specified in settings. If file exists nothing happens."""
    for url, filename, dest in downloads:
        path = os.path.join(os.path.expanduser(dest), filename)
        if not os.path.exists(path):
            log.info('Downloading {url} to {file}'.format(url=url, file=path))
            with urllib.request.urlopen(url) as response, \
                 open(path, mode='wb') as output:
                     shutil.copyfileobj(response, output)
        else:
            log.info('File {file} exits, no new download from {url}'.format(file=path, url=url))


def _clone_gitrepos():
    """Clone gitrepos and check out specified sha. If repo already exists nothing happens."""
    orig_cwd = os.getcwd()
    log.debug('Saved CWD {cwd}'.format(cwd=orig_cwd))
    for url, reponame, sha, dest in git_repos:
        os.chdir(orig_cwd)  # Reset every passthrough
        destexpanded = os.path.expanduser(dest)
        path = os.path.join(destexpanded, reponame)
        if not os.path.exists(path):
            os.chdir(destexpanded)
            cmd = 'git clone {url} {name}'.format(url=url, name=reponame)
            log.info(cmd)
            subprocess.call(cmd, shell=True)
        else:
            log.info('Folder {path} exits, no new cloning of {repo}'.format(path=path, repo=url))
    os.chdir(orig_cwd)
    log.debug('Restored CWD {cwd}'.format(cwd=orig_cwd))


def _create_symlinks():
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

    # TODO ask user if the localsettingsfolder & downloadsfolder should be deleted also? Or kill it, unless asked to keep it?
    if os.path.exists(LOCALSETTINGS):
        log.info('Deleting {dir} including its content'.format(dir=LOCALSETTINGS))
    if os.path.exists(DOWNLOADS_AND_GITREPOS):
        log.info('Deleting {dir} including its content'.format(dir=DOWNLOADS_AND_GITREPOS))

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
    logformat = '%(levelname)s: %(message)s'
    logging.basicConfig(level=loglevel, format=logformat)
    log = logging.getLogger(__name__)

    main(args)
