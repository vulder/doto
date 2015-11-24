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



if __name__ == "__main__":
    linkEntrys = []
    linkEntrys.append(SymlinkEntry("vim_dir","vim/vim_dir","vim_new"))
    linkEntrys.append(SymlinkEntry("tmux_dir","tmux/tmux_dir","tmux_new"))

    # backing up old files
    for linkEntr in linkEntrys:
        linkEntr.backup()

    # setup symlinks
    for linkEntr in linkEntrys:
        linkEntr.link()

