#!/usr/bin/env python

import subprocess
import sys

HOST = ''
ROOT_DIRECTORY = ''
LOU_FILE = '.lou'


def run_remote_command(command):
    return subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)


def create_new_directory(dir_name):
    """Create .lou file for current directory and create remote directory
    """

    cmd = "ssh %(host)s 'cd %(root_dir)s && mkdir %(dir_name)s'" % {'host': HOST, 'root_dir': ROOT_DIRECTORY, 'dir_name': dir_name}

    try:
        out = run_remote_command(cmd)
    except subprocess.CalledProcessError as e:
        print e.output
    else:
        create_lou_file(dir_name)


def list_remote_directories():
    cmd = "ssh %(host)s 'cd %(root_dir)s && ls'" % {'host': HOST, 'root_dir': ROOT_DIRECTORY}
    
    try:
        out = run_remote_command(cmd)
    except subprocess.CalledProcessError as e:
        if 'No such file or directory' in e.output:
            print 'Root directory %s not found.' % ROOT_DIRECTORY
        else:
            print e.output
    else:
        for d in out.split('\n'):
            print d


def sync(source, destination):
    cmd = "rsync -az %(source)s %(dest)s" % {'source': source, 'dest': destination}

    try:
        out = run_remote_command(cmd)
    except subprocess.CalledProcessError as e:
        print e.output


def sync_pull(directory=None):
    """
    Pull remote files to local directory.
    """
    # otherwise pull from the passed directory
    if directory:
        dir = "%(host)s:%(root)s/%(directory)s" % {'host': HOST, 'root': ROOT_DIRECTORY, 'directory': directory}
        sync(dir + '/.', '.')
        return

    # first try to pull from .lou file
    dir = read_lou_file()
    if dir:
        sync(dir + '/.', '.')
    else:
		print 'Not a Lou directory. Run `lou new remote_dir_name` to create or `lou pull remote_dir_name` to sync.'

def sync_push():
    """
    Pushes local files to remote directory.
    """
    dir = read_lou_file()
    if dir:
        sync('.', dir) 


def create_lou_file(dir_name):
    file = open(LOU_FILE, 'w')
    file.write('%(host)s:%(root)s/%(dir_name)s' % {'host': HOST, 'root': ROOT_DIRECTORY, 'dir_name': dir_name}) 


def read_lou_file():
    try:
        file = open(LOU_FILE)
        return file.readline()
    except IOError:
        return None 

def print_help():
    print """Options
 list    list remote directories
 new     create new directory on remote for current directory
 pull    pull changes from remote directory to local directory
 push    push changes from local directory to remote directory
 help    print this help text"""


if __name__ == '__main__':
    args = sys.argv[1:]

    if not args:
        print_help()
    else:
        if args[0] == 'list':
            list_remote_directories()
        elif args[0] == 'new':
            create_new_directory(args[1])
        elif args[0] == 'push':
            sync_push()
        elif args[0] == 'pull':
            sync_pull(args[1] if len(args) > 1 else None)
        else:
            print args

