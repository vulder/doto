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
    git_options = []
    install_cmds = []

    def __init__(self, json_repr):
        self.name = json_repr["name"]
        self.giturl = json_repr["git_url"]
        self.install_loc = HOME_PATH + json_repr["install_path"]
        print self.install_loc
        self.install_cmds = [e for e in json_repr["install_cmds"] \
                if isinstance(e, dict) and e.has_key("cmd")]

        for git_opt in json_repr["git_opts"]:
            for key in git_opt:
                self.git_options.append(str(key))
                self.git_options.append(str(git_opt[key]))

    def clone(self):
        """
        Clones the git repo of the program.
        """
        from plumbum.cmd import git

        if not path.exists(self.install_loc):
            print "Cloning " + self.name
            git["clone", self.git_options, self.giturl, self.install_loc]()

    def update(self):
        """
        Updates the git repo of the program.
        """
        print "Updating " + self.name
        from plumbum.cmd import git

        if path.exists(self.install_loc):
            with local.cwd(self.install_loc):
                git["pull"]()

    def install(self):
        """
        Installs the program in the default setup.
        """
        print "Installing " + self.name
        with local.cwd(self.install_loc):
            for cmd in self.install_cmds:
                exec_cmd = local[cmd["cmd"]]
                args = cmd["args"] if cmd.has_key("args") else []
                print "before"
                print args
                args = [arg.replace("$HOME", local.env["HOME"]) \
                        for arg in args]
                print "after"
                print args
                exec_cmd = exec_cmd[args]
                with local.env(**cmd["env"] if cmd.has_key("env") else {}):
                    print exec_cmd()

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
                hidden = (dot_file["hidden"] == "True")
                self.link_entrys.append(SymlinkEntry(dot_file["name"], \
                        dot_file["src_path"], dot_file["tar_path"], hidden))
            # read programs to install
            for prog_file in jsn["programs"]:
                self.programms.append(Prog(prog_file))

    def link_all(self):
        """
        Links all dot files specified in the config.
        """
        for link_entry in self.link_entrys:
            link_entry.link()
        print "Finished linking dot files"

    def backup_all(self):
        """
        Backs up all dot files that could be touched by new files.
        """
        for link_entry in self.link_entrys:
            link_entry.backup()
        print "Finished backup old dot files"

    def install_all(self):
        """
        Installs all programs specified in the config.
        """
        for prog in self.programms:
            prog.install()
        print "Finished installing programs"

    def clone_all(self):
        """
        Checks out all programs specified in the config.
        """
        for prog in self.programms:
            prog.clone()
        print "Finished cloning program repositories"

    def update_all(self):
        """
        Updates all programs specified in the config.
        """
        for prog in self.programms:
            prog.update()
        print "Finished updating programs"


def main():
    """
    Executs the setup of the specified config file.
    """
    import sys

    conf = Config("/home/sattlerf/git/doto/doto.conf")

    # handling user flags
    for arg in sys.argv:
        if arg == "install":
            conf.backup_all()
            conf.link_all()
            conf.clone_all()
            conf.install_all()
        if arg == "update":
            conf.update_all()


if __name__ == "__main__":
    main()
