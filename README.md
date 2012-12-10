# Meet Lou.
## He manages your rsyncs.

### Lou was built for one purpose:
To manage ad-hoc directory backups & syncs to a remote server.

### So, it does what Google Drive and Dropbox do but not as well?

Yes and no.

### Here are some benefits
#### It's cheaper
If you already are paying for web hosting, then why pay for Drive or Dropbox? Lou helps you use the resources you already have.
#### It's flexible
Maybe you don't want to sync ALL your files to your work computer. Lou lets you sync only the stuff you want.

### Installation
1. Clone Lou somewhere appropriate.
2. You might have chmod 755 lou.py
3. Create a symlink: `ln -s /wherever_you_put/lou.py /somewhere_in_your_PATH/lou`
4. In lou.py, change HOST and ROOT_DIRECTORY to `you@yourhost.biz` and `path_to_sync_to`, respectively.

### Using Lou
1. Try Lou out by running `lou list` at the command line. This command lists the directories you've synced. There probably won't be any listed at this point.
2. In a directory you'd like to sync, execute `lou new dir_name` to create a remote directory "dir_name" and `lou push` to push your local files to the remote host.
3. To pull files from a remote directory use the commaned `lou pull dir_name` where "dir_name" is the remote directory. Hint: use `lou list` to see which remote directories are available to pull.

### How it works
Lou is just a simple rsync wrapper. It doesn't muck with anything on your remote server other than creating new directories and rsyncing inside your ROOT_DIRECTORY path. Lou remembers where to rsync by creating a .lou file in the directories you have synced.