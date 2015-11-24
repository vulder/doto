#!/usr/bin/env python

from plumbum import local
from plumbum.cmd import cat, ln, mv

from os import path
from glob import glob

rootP = local.env["PWD"]
homeP = local.env["HOME"]

class SymlinkEntry:

    def __init__(self,name,source,target,hidden=True):
        self.name = name
        self.source = source
        self.target = target
        self.hidden = hidden

    def backup(self):
        print "Backing up " + self.name
        if self.hidden:
            srcPath = homeP + "/." + self.target
            if path.islink(srcPath) or path.isfile(srcPath):
                mv[srcPath , homeP + "/." + self.target + "_back"]()
        else:
            srcPath = homeP + "/" + self.target
            if path.islink(srcPath) or path.isfile(srcPath):
                mv[srcPath, homeP + "/vim_new_back"]()

    def link(self):
        print "Linking " + self.name
        if self.hidden:
            ln["-s", rootP + "/" + self.source, homeP + "/." + self.target]()
        else:
            ln["-s", rootP + "/" + self.source, homeP + "/" + self.target]()


class Prog:

    def __init__(self,name,giturl,installLoc,installR=""):
        self.name = name
        self.giturl = giturl
        self.installLoc = installLoc
        self.installR = installR

    def clone(self):
        from plumbum.cmd import git

        if path.exists(self.installLoc):
            with local.cwd(self.installLoc):
                print git["pull"]
                git["pull"]()
        else:
            print git["clone", self.giturl, self.installLoc]
            git["clone", self.giturl, self.installLoc]()

    def install(self):
        pass

if __name__ == "__main__":
    linkEntrys = []
    linkEntrys.append(SymlinkEntry("vim_dir","vim/vim_dir","vim_new"))
    linkEntrys.append(SymlinkEntry("tmux_dir","tmux/tmux_dir","tmux_new"))

    programms = []
    programms.append(Prog("enhanced","git@github.com:b4b4r07/enhancd.git", homeP + "/.enhancd_new"))

    # checkout and install programs
    for prog in programms:
        prog.clone()

    # backing up old files
    for linkEntr in linkEntrys:
        linkEntr.backup()

    # setup symlinks
    for linkEntr in linkEntrys:
        linkEntr.link()

