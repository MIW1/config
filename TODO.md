

Backlog:

    - Create the /etc/zsh-config-scripts-defaultuser file (if it doesn't exist).
        - Create the file from user input.
        - Check to use the existing files value as default value, if file exists.

    - GIT email and name prompt.
        - Store in: ~/.localsettings/git_user
        - Prompt to insert name.
        - Prompt to insert email.

    - Create "${USER_HOME}/.vim" and child directories if they don't exist.
        - Create "${USER_HOME}/.vim" if it doesn't exist.
        - Create list of folders in DOT_VIM_FOLDERS if they don't exist.

    - Jedi vim installation is incorrect.
        - Investigate what in the setup is wrong.
        - Fix it (or make more partial steps if needed...)

    - Perhaps extend the gitrepo-tuples with symlink data,
      to keep all config for a gitrepo together.
        * Evaluate and see if worth it.

    - Clean up dead or commented out code.

    - See if configuration is better suited to be moved to a separate file.
      Just to keep things more readable and feeling less entangled.

    - Make a script that goes through all git-repos and updates them,
      and syncs new sha:s to the repo config.
      That way it's easy to keep things up-to-date,
      and there's a log of what things has been updated.
      Probably good to make as an option, "install" / "uninstall" / "gitupdates".

    - Move the dependency-fiddling-script to this machine, also symlink it.
        - See if I want to move it...

    - Have an all-but-symlink-task and an symlink-only-task seems like good
      ideas for debugging etc
        - New symlink-only-option in arguments and documentation.
        - New symlink-only-option implementation.
        - New all-but-symlink-option in arguments and documentation.
        - New all-but-symlink-option implementation.

    - Build a JavaScript search script also (like the python one I already have).
        * zshrc task.
    - Build a Java search script also (like the python one I already have).
        * zshrc task.

    - Idea: Install apt-stuff if it's a ubuntu machine?
      Perhaps just output a .apt-line from a file?
      Answer: Ignore for now, would be nice, but nowhere to easily test it.
              Fix in the future when it's needed.

    - Uninstall NOT to remove .vim-subfolders, and .vim folder.
        - IF and only IF there are other files not created by me here.
          If only files by this script, delete them too.
        - Log output at end to clearly indicate there are files to remove manually.
          (Or save ofc if reusable in any way).

    - Ask user if the localsettingsfolder & downloadsfolder content should be deleted
      on uninstall. Or if to be kept. Such a usecase to keep it is to avoid
      downloading it all again, e.g. if just redoing the linking is required.
        - Create new point when this is done for installation to NOT reclone,
          but just update, appropriate files in localsettingsfolder and downloadsfolder.
