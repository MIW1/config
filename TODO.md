Active/prioritized tasks (top highest prio, bottom lowest prio):
    - Restructure things in the repo, to make it easier to find stuff.
        * E.g. some scripts are to be installed, some are for maintenance purposes
          and everything just sits in a flat directory.
        - Fix a new structure (copyfiles only!!!!)
        - Move current files to new structure (delete old).
            X - Moved and updated download_repo
            - Update install.py for download_repo.
            - Update all symlinks currently in use...
            - Above step would benefit from symlink-only-task described in other task.

    - See if configuration is better suited to be moved to a separate file.
      Just to keep things more readable and feeling less entangled.

    - Clean up dead or commented out code.

    - Add flag to use real settings or test settings?
        * Could ease testing a bit.
        * Could have a few values in the file, and read rest from settings file.


Backlog:

    - Jedi vim installation is incorrect.
        - Investigate what in the setup is wrong.
        - Fix it (or make more partial steps if needed...)

    - Perhaps extend the gitrepo-tuples with symlink data,
      to keep all config for a gitrepo together.
        * Evaluate and see if worth it.

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
