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

    def __repr__(self):
        string_repr = ""
        string_repr += "{name: \"" + self.name + "\" src_path: \"" + \
                self.source + "\" tar_path: \"" + self.target + "\"}"
        return string_repr


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

    def __repr__(self):
        string_repr = ""
        string_repr += "{name: \"" + self.name + "\" giturl: \"" + self.giturl \
                + "\" install_location: \"" + self.install_loc + "\"}"
        return string_repr


class Config(object):
    """
    A configuration file for the configs and programs to install.
    """

    link_entrys = []
    programms = []

    def __init__(self, config_file):
        with open(config_file, "r") as conf:
            import json
            jsn = json.load(conf)
            # read dot files to link
            for dot_file in jsn["dot_files"]:
                self.link_entrys.append(SymlinkEntry(dot_file["name"], \
                        dot_file["src_path"], dot_file["tar_path"]))
            # read programs to install
            for prog_file in jsn["programs"]:
                self.programms.append(Prog(prog_file["name"], \
                    prog_file["git_url"], \
                    HOME_PATH + prog_file["install_path"]))

    def link_all(self):
        """
        Links all dot files specified in the config.
        """
        for link_entry in self.link_entrys:
            link_entry.link()


    def backup_all(self):
        """
        Backs up all dot files that could be touched by new files.
        """
        for link_entry in self.link_entrys:
            link_entry.backup()

    def install_all(self):
        """
        Installs all programs specified in the config.
        """
        pass

    def clone_all(self):
        """
        Checks out all programs specified in the config.
        """
        for prog in self.programms:
            prog.clone()


def main():
    """
    Executs the setup of the specified config file.
    """
    conf = Config("/home/sattlerf/git/doto/doto.conf")

    conf.backup_all()
    conf.link_all()
    conf.clone_all()


if __name__ == "__main__":
    main()
