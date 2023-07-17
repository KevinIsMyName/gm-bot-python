# Deployment

## Tux

1. Get a copy of the code using one of the following options
    - Clone a install of the repository from [GitHub](https://github.com/KevinIsMyName/gm-bot) with the `git clone` command
    - Retrieve a working copy the latest data (all streak data is stored in `datastore/`) from tux.cs.drexel.edu with `scp -r <userid>@tux.cs.drexel.edu:<remote-path> <local-path>`.
        - e.g. `scp -r kw875@tux.cs.drexel.edu:~/code/gm-bot ~/Desktop/gm-bot`
    - Retrieve a working copy from someone (I can send you a zip file of the code and data).
2. Upload your files to Tux with `scp -r ~/Desktop/gm-bot <user-id>@tux.cs.drexel.edu:~/code/gm-bot`.
3. SSH into Tux with `ssh <user-id>@tux.cs.drexel.edu`.
4. Navigate to the directory with the code with `cd ~/code/gm-bot`.
5. Install the dependencies with `make build`. *Alternatively, use `python3 -m pip install -r requirements.txt`*
6. Test that the application works with `make run`
    - If everything is working, you can kill the program with `Ctrl+C`.
7. Use your favorite application to run programs in the background (such as `tmux`, `screen`).
    1. I like `tmux` which is a window manager that can manage multiple shell sessions and run them in the background. It is also installed on Tux.
    1. Start a new session with `tmux new -s <session-name>`.
    1. Attach to the session with `tmux attach`
    1. Run the application as specified in the [README.md](./README.md#Usage).
    1. Once everything appears to be working, detach from the session with `Ctrl+B` then `D`.
    1. That's it! In the future if you need to reattach to the shell session, use `tmux attach` and you will be back where you left off.
