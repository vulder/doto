#!/usr/bin/env python3
"""
Script to auto setup programming environment.
"""
import imp
import sys
try:
    imp.find_module("plumbum")
except ImportError:
    print("Please install plumbum")
    print("https://plumbum.readthedocs.org/en/latest/")
    sys.exit()

BLOCK = True

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
        print("Backing up " + self.name)
        if self.hidden:
            src_path = HOME_PATH + "/." + self.target
            if path.islink(src_path) or path.isfile(src_path):
                mv[src_path, HOME_PATH + "/." + self.target + "_back"]()
        else:
            src_path = HOME_PATH + "/" + self.target
            if path.islink(src_path) or path.isfile(src_path):
                mv[src_path, HOME_PATH + "/" + self.target + "_back"]()

    def link(self):
        """
        Linkes the dot file to the corret location in the home folder.
        """
        print("Linking " + self.name)
        if self.hidden:
            ln["-s", ROOT_PATH + "/" + self.source, HOME_PATH + "/." +
               self.target]()
        else:
            ln["-s", ROOT_PATH + "/" + self.source, HOME_PATH + "/" +
               self.target]()

    def remove(self):
        """
        Removes the symlink.
        """
        from plumbum.cmd import rm  # pylint: disable=E0401
        print("Removing Symlink " + self.name)
        if self.hidden:
            rm[HOME_PATH + "/." + self.target]()
        else:
            rm[HOME_PATH + "/" + self.target]()

    def remove_backup(self):
        """
        Removes the symlink.
        """
        from plumbum.cmd import rm  # pylint: disable=E0401
        print("Removing backup links " + self.name)
        if self.hidden:
            exec_path = HOME_PATH + "/." + self.target + "_back"
            if not exec_path == "/" and not exec_path == HOME_PATH:
                rm["-rf", exec_path]()
            else:
                print("WOOOPS don't delete / or home folder")
        else:
            exec_path = HOME_PATH + "/" + self.target + "_back"
            if not exec_path == "/" and not exec_path == HOME_PATH:
                rm["-rf", exec_path]()
            else:
                print("WOOOPS don't delete / or home folder")

    def __repr__(self):
        string_repr = ""
        string_repr += "{name: \"" + self.name + "\" src_path: \"" + \
                self.source + "\" tar_path: \"" + self.target + "\"}"
        return string_repr


class SetupCmd(object):
    """
    Run sequence of commands to finalize setup.
    """

    def __init__(self, json_repr):
        self.name = json_repr["name"]
        self.desc = json_repr["desc"]
        self.cmds = [e for e in json_repr["cmds"]\
                     if isinstance(e, dict) and "cmd" in e]

    def run(self):
        """
        Run the setup command chain.
        """
        print("Running " + self.name)
        for cmd in self.cmds:
            exec_cmd = local[cmd["cmd"]]
            args = cmd["args"] if "args" in cmd else []
            args = [arg.replace("$HOME", local.env["HOME"]) \
                    for arg in args]
            exec_cmd = exec_cmd[args]
            with local.env(**cmd["env"] if "env" in cmd else {}):
                print("Dbg: ", exec_cmd)
                print(exec_cmd())

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
        self.install_cmds = [e for e in json_repr["install_cmds"] \
                if isinstance(e, dict) and "cmd" in e]
        self.uninstall_cmds = [e for e in json_repr["uninstall_cmds"] \
                if isinstance(e, dict) and "cmd" in e]

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
            print("Cloning " + self.name)
            git["clone", self.git_options, self.giturl, self.install_loc]()

    def update(self):
        """
        Updates the git repo of the program.
        """
        print("Updating " + self.name)
        from plumbum.cmd import git

        if path.exists(self.install_loc):
            with local.cwd(self.install_loc):
                git["pull"]()

    def install(self):
        """
        Installs the program in the default setup.
        """
        print("Installing " + self.name)
        with local.cwd(self.install_loc):
            for cmd in self.install_cmds:
                exec_cmd = local[cmd["cmd"]]
                args = cmd["args"] if "args" in cmd else []
                args = [arg.replace("$HOME", local.env["HOME"]) \
                        for arg in args]
                exec_cmd = exec_cmd[args]
                with local.env(**cmd["env"] if "env" in cmd else {}):
                    print(exec_cmd())

    def uninstall(self):
        """
        Uninstalls the program.
        """
        from plumbum.cmd import rm  # pylint: disable=E0401
        print("Uninstalling " + self.name)
        with local.cwd(self.install_loc):
            for cmd in self.uninstall_cmds:
                exec_cmd = local[cmd["cmd"]]
                args = cmd["args"] if "args" in cmd else []
                args = [arg.replace("$HOME", local.env["HOME"]) \
                        for arg in args]
                exec_cmd = exec_cmd[args]
                with local.env(**cmd["env"] if "env" in cmd else {}):
                    print(exec_cmd())
        rm("-rf", self.install_loc)

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
    setup_cmds = []

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

            # read setup cmds
            for setup_file in jsn["setup_cmds"]:
                self.setup_cmds.append(SetupCmd(setup_file))

    def link_all(self):
        """
        Links all dot files specified in the config.
        """
        for link_entry in self.link_entrys:
            link_entry.link()
        print("Finished linking dot files")

    def backup_all(self):
        """
        Backs up all dot files that could be touched by new files.
        """
        for link_entry in self.link_entrys:
            link_entry.backup()
        print("Finished backup old dot files")

    def install_all(self):
        """
        Installs all programs specified in the config.
        """
        for prog in self.programms:
            prog.install()
        print("Finished installing programs")
        print("Running setup")
        for setup_cmd in self.setup_cmds:
            setup_cmd.run()

    def uninstall_all(self):
        """
        Uninstalls all programs.
        """
        for prog in self.programms:
            prog.uninstall()
        print("Finished uninstalling programs")

    def clone_all(self):
        """
        Checks out all programs specified in the config.
        """
        for prog in self.programms:
            prog.clone()
        print("Finished cloning program repositories")

    def update_all(self):
        """
        Updates all programs specified in the config.
        """
        for prog in self.programms:
            prog.update()
        print("Finished updating programs")

    def remove_all(self):
        """
        Removes all Symlinks.
        """
        for link_entry in self.link_entrys:
            link_entry.remove()
        print("Finished removing Symlinks.")

    def remove_backups_all(self):
        """
        Removes all backup Symlinks.
        """
        for link_entry in self.link_entrys:
            link_entry.remove_backup()
        print("Finished removing Symlinks.")


def print_help():
    """
    Prints help output to the console.
    """
    # TODO impl help txt
    print("Only use setup if you now what you're doing.\nJust set block = false")


def which(program):
    """
    Checks if the given program exists in the current enviroment.
    """
    import os

    def is_exe(fpath):
        """
        Checks if file behind fpath is a executable.
        """
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for current_path in os.environ["PATH"].split(os.pathsep):
            current_path = current_path.strip('"')
            exe_file = os.path.join(current_path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def main():
    """
    Executs the setup of the specified config file.
    """

    config_path = "doto.conf"

    config = Config(config_path)

    with open(config_path, "r") as conf:
        import json
        jsn = json.load(conf)
        # checking requirements
        for requirement in jsn["requirements"]:
            if which(requirement["name"]) == None:
                print("Please install " + requirement["name"] \
                + " on your system.")
                # TODO: add check for ZSH
                # TODO: add check if all deps are present

    if BLOCK:
        print_help()
        return

    if len(sys.argv) != 1:
        print_help()

    # handling user flags
    for arg in sys.argv:
        if arg == "install":
            config.backup_all()
            config.link_all()
            config.clone_all()
            config.install_all()
        if arg == "update":
            config.update_all()
        if arg == "help":
            print_help()
        if arg == "uninstall":
            config.uninstall_all()
        if arg == "remove":
            config.remove_all()
        if arg == "remove_backups":
            config.remove_backups_all()

        # TODO: give last instructions

if __name__ == "__main__":
    main()
