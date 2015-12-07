#!/usr/bin/env python
"""
Script to auto setup programming environment.
"""

from plumbum import local
from plumbum.cmd import cat, ln, mv

from os import path

ROOT_PATH = local.env["PWD"]
HOME_PATH = local.env["HOME"]


class SymlinkEntry(object):
    """
    Handling a symlink to a given dot file.
    """

    def __init__(self, name, source, target, hidden=True):
        self.name = name
        self.source = source
        self.target = target
        self.hidden = hidden

    def backup(self):
        """
        Backups the current installed config to a dot file with {name}_back.
        """
        print "Backing up " + self.name
        if self.hidden:
            src_path = HOME_PATH + "/." + self.target
            if path.islink(src_path) or path.isfile(src_path):
                mv[src_path, HOME_PATH + "/." + self.target + "_back"]()
        else:
            src_path = HOME_PATH + "/" + self.target
            if path.islink(src_path) or path.isfile(src_path):
                mv[src_path, HOME_PATH + "/vim_new_back"]()

    def link(self):
        """
        Linkes the dot file to the corret location in the home folder.
        """
        print "Linking " + self.name
        if self.hidden:
            ln["-s", ROOT_PATH + "/" + self.source, HOME_PATH + "/." +
               self.target]()
        else:
            ln["-s", ROOT_PATH + "/" + self.source, HOME_PATH + "/" +
               self.target]()


class Prog(object):
    """
    A program that needs to be installed for the config to work.
    """

    def __init__(self, name, giturl, install_loc, install_r=""):
        self.name = name
        self.giturl = giturl
        self.install_loc = install_loc
        self.install_r = install_r

    def clone(self):
        """
        Clones the git repo for the program.
        """
        from plumbum.cmd import git

        if path.exists(self.install_loc):
            with local.cwd(self.install_loc):
                print git["pull"]
                git["pull"]()
        else:
            print git["clone", self.giturl, self.install_loc]
            git["clone", self.giturl, self.install_loc]()

    def install(self):
        """
        Installs the program in the default setup.
        """
        pass


class Config(object):
    """
    A configuration file for the configs and programs to install.
    """

    def __init__(self, config_file):
        with open(config_file, "r") as conf:
            for line in conf.readlines:
                print line


def main():
    """
    Executs the setup of the specified config file.
    """
    Config("~/git/doto.conf")

    link_entrys = []
    link_entrys.append(SymlinkEntry("vim_dir", "vim/vim_dir", "vim_new"))
    link_entrys.append(SymlinkEntry("tmux_dir", "tmux/tmux_dir", "tmux_new"))

    programms = []
    programms.append(Prog("enhanced", "git@github.com:b4b4r07/enhancd.git", \
            HOME_PATH + "/.enhancd_new"))

    # checkout and install programs
    for prog in programms:
        prog.clone()

    # backing up old files
    for link_entry in link_entrys:
        link_entry.backup()

    # setup symlinks
    for link_entry in link_entrys:
        link_entry.link()


if __name__ == "__main__":
    main()
