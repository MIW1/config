#!/usr/bin/env python3

import argparse
import logging
import os
import shutil
import subprocess
import urllib.request
from collections import namedtuple

def strip_dotgit(reponame):
    """Remove/strip the .git part from a repo name"""
    return os.path.basename(reponame)

### Configuration
Symlink = namedtuple('Symlink', ['source', 'dest'])
Copy = namedtuple('Copy', ['source', 'dest'])
Download = namedtuple('Download', ['url', 'filename', 'dest'])
Gitrepo = namedtuple('Gitrepo', ['url', 'reponame', 'sha', 'dest'])

USER_HOME = 'dummy-install-folder-for-testing-purposes'  # Exists so it's easy to test everything and install it in another folder than "~/" when developing.
#USER_HOME = '~'  # MUST NOT have trailing slash "/"
LOCALSETTINGS = 'machine-specific-files/localsettings'
DOWNLOADS_AND_GITREPOS = 'machine-specific-files/downloads_and_gitrepos'
#ZSH_CONFIG_DEFAULT_USER_FILE = '/etc/zsh-config-scripts-defaultuser'
ZSH_CONFIG_DEFAULT_USER_FILE = 'dummy-install-folder-for-testing-purposes/zsh-config-scripts-defaultuser'  # xxx testfile
#GIT_USER_FILE = '{localsettings}/git_user'.format(localsettings=LOCALSETTINGS)
GIT_USER_FILE = 'dummy-install-folder-for-testing-purposes/git_user'  # xxx testfile


#DOT_VIM_PATH = '%s/dotvim' % USER_HOME  # ~/.vim for real use
DOT_VIM_PATH = '{user_home}/.vim'.format(user_home=USER_HOME)
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
JEDI_VIM = 'jedi-vim.git'  # FIXME something goes wrong with this installation, something is not setup properly by default. Have not done any digging but see issue in new envs.
NERDTREE_VIM = 'nerdtree.git'
SYNTASTIC_VIM = 'syntastic.git'
AIRLINE_VIM = 'vim-airline.git'
AIRLINE_THEMES_VIM = 'vim-airline-themes.git'
COLORS_SOLARIZED_VIM = 'vim-colors-solarized.git'
COLORSCHEMES_VIM = 'vim-colorschemes.git'
PYTHON_SYNTAX_VIM = 'python-syntax.git'
PYTHON_INDENT_VIM = 'python-indent.vim'
LESS_SYNTAX_VIM = 'less-syntax.vim'

symlinks = [
    Symlink(source='bashrc',
            dest='{home}/.bashrc'.format(home=USER_HOME)),
    Symlink(source='gitconfig',
            dest='{home}/.gitconfig'.format(home=USER_HOME)),
    Symlink(source='git-meld.py',
            dest='{home}/.git-meld.py'.format(home=USER_HOME)),
    Symlink(source='gvimrc',
            dest='{home}/.gvimrc'.format(home=USER_HOME)),
    Symlink(source='vimrc',
            dest='{home}/.vimrc'.format(home=USER_HOME)),
    Symlink(source='zshrc',
            dest='{home}/.zshrc'.format(home=USER_HOME)),
    Symlink(source='zshrc.zni',
            dest='{home}/.zshrc.zni'.format(home=USER_HOME)),

    Symlink(source=LOCALSETTINGS,
            dest='{home}/.localsettings'.format(home=USER_HOME)),

    Symlink(source='{download}/{pythonindent}'.format(download=DOWNLOADS_AND_GITREPOS, pythonindent=PYTHON_INDENT_VIM),
            dest='{vimpath}/indent/python.vim'.format(vimpath=DOT_VIM_PATH)),
    Symlink(source='{download}/{lesssyntax}'.format(download=DOWNLOADS_AND_GITREPOS, lesssyntax=LESS_SYNTAX_VIM),
            dest='{vimpath}/syntax/less.vim'.format(vimpath=DOT_VIM_PATH)),

    # XXX Perhaps extend the gitrepo-tuples with symlink data, to keep all config for a gitrepo together.

    Symlink(source='{downloads}/{powerlinerepo}'.format(downloads=DOWNLOADS_AND_GITREPOS, powerlinerepo=POWERLINE_FONTS),
            dest='{home}/.powerlinefonts'.format(home=USER_HOME)),

    Symlink(source='{downloads}/{colorschemesrepo}/colors/molokai.vim'.format(downloads=DOWNLOADS_AND_GITREPOS,
                                                                              colorschemesrepo=COLORSCHEMES_VIM),
            dest='{vimpath}/colors/molokai.vim'.format(vimpath=DOT_VIM_PATH)),
    Symlink(source='{downloads}/{colorschemesrepo}/colors/solarized.vim'.format(downloads=DOWNLOADS_AND_GITREPOS,
                                                                                colorschemesrepo=COLORSCHEMES_VIM),
            dest='{vimpath}/colors/solarized.vim'.format(vimpath=DOT_VIM_PATH)),

    Symlink(source='{downloads}/{pathogenrepo}/autoload/pathogen.vim'.format(downloads=DOWNLOADS_AND_GITREPOS, pathogenrepo=PATHOGEN_VIM),
            dest='{vimpath}/autoload/pathogen.vim'.format(vimpath=DOT_VIM_PATH)),

    Symlink(source='{downloads}/{solarizedrepo}'.format(downloads=DOWNLOADS_AND_GITREPOS, solarizedrepo=COLORS_SOLARIZED_VIM),
            dest='{vimpath}/bundle/{solarizedvim}'.format(vimpath=DOT_VIM_PATH, solarizedvim=strip_dotgit(COLORS_SOLARIZED_VIM))),
    Symlink(source='{downloads}/{ctrlprepo}'.format(downloads=DOWNLOADS_AND_GITREPOS, ctrlprepo=CTRLP_VIM),
            dest='{vimpath}/bundle/{ctrlp}'.format(vimpath=DOT_VIM_PATH, ctrlp=strip_dotgit(CTRLP_VIM))),
    Symlink(source='{downloads}/{emmetrepo}'.format(downloads=DOWNLOADS_AND_GITREPOS, emmetrepo=EMMET_VIM),
            dest='{vimpath}/bundle/{emmetvim}'.format(vimpath=DOT_VIM_PATH, emmetvim=strip_dotgit(EMMET_VIM))),
    Symlink(source='{downloads}/{jedirepo}'.format(downloads=DOWNLOADS_AND_GITREPOS, jedirepo=JEDI_VIM),
            dest='{vimpath}/bundle/{jedivim}'.format(vimpath=DOT_VIM_PATH, jedivim=strip_dotgit(JEDI_VIM))),
    Symlink(source='{downloads}/{nerdtreerepo}'.format(downloads=DOWNLOADS_AND_GITREPOS, nerdtreerepo=NERDTREE_VIM),
            dest='{vimpath}/bundle/{nerdtreevim}'.format(vimpath=DOT_VIM_PATH, nerdtreevim=strip_dotgit(NERDTREE_VIM))),
    Symlink(source='{downloads}/{syntasticrepo}'.format(downloads=DOWNLOADS_AND_GITREPOS, syntasticrepo=SYNTASTIC_VIM),
            dest='{vimpath}/bundle/{syntasticvim}'.format(vimpath=DOT_VIM_PATH, syntasticvim=strip_dotgit(SYNTASTIC_VIM))),
    Symlink(source='{downloads}/{airlinerepo}'.format(downloads=DOWNLOADS_AND_GITREPOS, airlinerepo=AIRLINE_VIM),
            dest='{vimpath}/bundle/{airlinevim}'.format(vimpath=DOT_VIM_PATH, airlinevim=strip_dotgit(AIRLINE_VIM))),
    Symlink(source='{downloads}/{airline_themesrepo}'.format(downloads=DOWNLOADS_AND_GITREPOS, airline_themesrepo=AIRLINE_THEMES_VIM),
            dest='{vimpath}/bundle/{airline_themesvim}'.format(vimpath=DOT_VIM_PATH, airline_themesvim=strip_dotgit(AIRLINE_THEMES_VIM))),

    Symlink(source='{downloads}/{pythonsyntax}/syntax/python.vim'.format(downloads=DOWNLOADS_AND_GITREPOS,
                                                                                           pythonsyntax=PYTHON_SYNTAX_VIM),
            dest='{vimpath}/syntax/python.vim'.format(vimpath=DOT_VIM_PATH)),
]

#copyactions = [
#    Copy(source=PATHOGEN_VIM, dest=),
#    Copy(source=, dest=),
#    Copy(source=, dest=),
#    Copy(source=, dest=),
#]
downloads = [  # wget "URL" -O filename
    Download(url='http://www.vim.org/scripts/download_script.php?src_id=4316',
             filename=PYTHON_INDENT_VIM,
             dest=DOWNLOADS_AND_GITREPOS),
    Download(url='https://gist.githubusercontent.com/bryanjswift/161047/raw/ef495b2a734058b1e45f63f2e8dec1f314ae8f14/less.vim',
             filename=LESS_SYNTAX_VIM,
             dest=DOWNLOADS_AND_GITREPOS),
]

git_repos = [
    # These are symlinked to .vim/bundle
    Gitrepo(url='https://github.com/powerline/fonts.git',
            reponame=POWERLINE_FONTS,
            sha='b0abc65f621eba332002cba88b49d50e99a126f9',
            dest=DOWNLOADS_AND_GITREPOS),
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
            dest=DOWNLOADS_AND_GITREPOS),
    # Symlinked to  .vim/autoload
    Gitrepo(url='https://github.com/tpope/vim-pathogen.git',
            reponame=PATHOGEN_VIM,
            sha='379b8f70822c4a89370575c3967f33cb116087ea',
            dest=DOWNLOADS_AND_GITREPOS),
    # Symlink to .vim/colors: vim-colorschemes.git/colors/molokai.vim, solarized.vim
    Gitrepo(url='https://github.com/flazz/vim-colorschemes.git',
            reponame=COLORSCHEMES_VIM,
            sha='b8dff40f69f1873effbed97c759a8452ecb240ed',
            dest=DOWNLOADS_AND_GITREPOS),
    # Symlink to .vim/syntax
    Gitrepo(url='https://github.com/hdima/python-syntax.git',
            reponame=PYTHON_SYNTAX_VIM,
            sha='69760cb3accce488cc072772ca918ac2cbf384ba',
            dest=DOWNLOADS_AND_GITREPOS),
]

# TODO Make a script that goes through all git-repos and updates them, and syncs new sha:s to the repo config.
#      That way it's easy to keep things up-to-date, and there's a log of what things has been updated.
#      Probably good to make as an option, "install" / "uninstall" / "gitupdates".

# TODO move the dependency-fiddling-script to this machine, also symlink it.

# XXX Idea: Install apt-stuff if it's a ubuntu machine?
#     Perhaps just output a .apt-line from a file?
#     Answer: Ignore for now, would be nice, but nowhere to easily test it.
#             Fix in the future when it's needed.

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
    # TODO Have an all-but-symlink-task and an symlink-only-task seems like good ideas for debugging etc
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
    _create_or_update_zsh_config_default_user_file()

    _create_or_update_git_user_file()

    _create_folders()

    _download_files()

    _clone_gitrepos()

    _create_symlinks()


def _create_folders():
    """Create all folders that must exist, e.g. '.vim'"""
    def _create_folder(folder, created_message, exists_message):
        """Create a folder. If the folder already exists nothing happens."""
        if not os.path.exists(folder):
            log.debug(created_message)
            os.mkdir(folder)
        else:
            log.debug(exists_message)

    _create_folder(folder=DOT_VIM_PATH,
                   created_message="Creating .vim folder {folder}".format(folder=DOT_VIM_PATH),
                   exists_message="Folder {folder} exists, skipping creation".format(folder=DOT_VIM_PATH))

    for vimfolder in DOT_VIM_FOLDERS:
        folder = '{vimpath}/{foldername}'.format(vimpath=DOT_VIM_PATH, foldername=vimfolder)
        _create_folder(folder=folder,
                       created_message="Creating vim folder {folder}".format(folder=folder),
                       exists_message="Vim folder {folder} exists, skipping creation".format(folder=folder))


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
    for url, reponame, sha, dest in git_repos:
        destexpanded = os.path.expanduser(dest)
        path = os.path.join(destexpanded, reponame)
        # git clone part
        if not os.path.exists(path):
            cmd = 'git clone {url} {name}'.format(url=url, name=reponame)
            log.info(cmd)
            subprocess.call(cmd, shell=True, cwd=destexpanded)
        else:
            log.info('Folder {path} exits, no new cloning of {repo}'.format(path=path, repo=url))
        # git checkout part
        current_sha = subprocess.check_output('git log --pretty=format:%H -n1', shell=True, cwd=path)
        current_sha = current_sha.decode('utf-8')
        if current_sha != sha:
            log.debug("{repo} current {current_sha} != requested {requested_sha}, doing git checkout to fix.".format(
                repo=path, current_sha=current_sha, requested_sha=sha))
            subprocess.call('git checkout {commitish}'.format(commitish=sha), shell=True, cwd=path, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
        else:
            log.debug("{repo} current {current_sha} == requested {requested_sha}, do nothing.".format(
                repo=path, current_sha=current_sha, requested_sha=sha))


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


def _create_or_update_zsh_config_default_user_file():
    """
    Create the file with default user used in some scripts.

    cat /etc/zsh-config-scripts-defaultuser
    # Used by the custom zsh-config to know what the default user is for loading the correct settings and configs.
    export DEFAULT_USER=user-name-goes-here
    """
    # Default value reading.
    if os.path.exists(ZSH_CONFIG_DEFAULT_USER_FILE):  # todo test that this works fine when the file does not exist also!
        with open(ZSH_CONFIG_DEFAULT_USER_FILE, "r") as f:
            # Discard comment lines
            done = False
            while not done:
                line = f.readline()
                done = not line.startswith("#")
            defaultvalue = line.rstrip().split("=")[1]  # Remove export part, keep only name.
    else:
        defaultvalue = None

    # Get user input
    please_input_default_user_text = "Insert default user, for $DEFAULT_USER{default}: ".format(
        default="" if defaultvalue is None else ' [' + defaultvalue + ']')
    default_user = ""
    while len(default_user) == 0:
        default_user = input(please_input_default_user_text).rstrip()
        if defaultvalue is not None and len(default_user) == 0:
            default_user = defaultvalue

    # Write file
    filetext = "# Used by the custom zsh-config to know what the default user is for loading the correct settings and configs.\n" \
        "export DEFAULT_USER={user}".format(user=default_user)
    subprocess.call("sudo echo '{filetext}' > {configfile}".format(filetext=filetext, configfile=ZSH_CONFIG_DEFAULT_USER_FILE),
                    shell=True)


def _create_or_update_git_user_file():
    """
    Create the file with name and email, that is import from the gitconfig-file.
    """
    # Default value reading.
    default_name = None
    default_email = None
    if os.path.exists(GIT_USER_FILE):
        with open(GIT_USER_FILE, 'r') as f:
            done = False
            while not done:
                line = f.readline()
                if len(line) == 0:
                    done = True
                if 'name' in line:
                    default_name = line.rstrip().split("= ")[1]
                if 'email' in line:
                    default_email = line.rstrip().split("= ")[1]

    name = ""
    while len(name) == 0:
        name = input("git setting user.name{default}: ".format(default="" if default_name is None else ' [' + default_name + ']')).rstrip()
        if default_name is not None and len(name) == 0:
            name = default_name
    email = ""
    while len(email) == 0:
        email = input("git setting user.email{default}: ".format(default="" if default_email is None else ' [' + default_email + ']')).rstrip()
        if default_email is not None and len(email) == 0:
            email = default_email

    with open(GIT_USER_FILE, "w") as f:
        f.write("[user]\n")
        f.write("    name = {name}\n".format(name=name))
        f.write("    email = {email}".format(email=email))


def uninstall():
    log.debug('Deleting symlinks.')

    # TODO ask user if the localsettingsfolder & downloadsfolder should be deleted also? Or kill it, unless asked to keep it?
    if os.path.exists(LOCALSETTINGS):
        log.info('Deleting {dir} including its content.'.format(dir=LOCALSETTINGS))
        shutil.rmtree(LOCALSETTINGS)
    if os.path.exists(DOWNLOADS_AND_GITREPOS):
        log.info('Deleting {dir} including its content.'.format(dir=DOWNLOADS_AND_GITREPOS))
        shutil.rmtree(DOWNLOADS_AND_GITREPOS)
    if os.path.exists(ZSH_CONFIG_DEFAULT_USER_FILE):
        log.info('Deleting {file}.'.format(dir=ZSH_CONFIG_DEFAULT_USER_FILE))
        subprocess.call('sudo rm {file}'.format(file=ZSH_CONFIG_DEFAULT_USER_FILE))

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
