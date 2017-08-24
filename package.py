#! /usr/bin/env python3

from multiprocessing import Pool

import os
import re
import argparse
import shutil
import logging
from pathlib import Path

join = os.path.join
BASE = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(level = logging.INFO)

class Ignores:
    def __init__(self, file):
        self.progs  = []
        with open(file) as f:
            for l in f.readlines():
                l = l.strip()
                if not len(l): continue
                if l.startswith("#"): continue

                self.progs.append(re.compile(l))
    
    def ignoring(self, name):
        for prog in self.progs:
            if prog.match(name):
                return True
        return False


# def relpath(p, relative_to):
#     return os.path.relpath(relative_to, p)

def link(source, target):
    to = os.path.relpath(os.path.realpath(source), os.path.dirname(source))
    os.symlink(to, target)
    shutil.copystat(source, target, follow_symlinks=False)
    # TODO: there is a bug, that we can not copysate of link
    #print("copystat", source)

def copy_file(source, target):
    if os.path.islink(source):
        link(source, target)
    else:
        shutil.copyfile(source, target)
        shutil.copystat(source, target)
        #print("copystat", source)

def pack(source, target, ignore = None):
    logging.info(source)
    if os.path.islink(source):
        link(source, target)
        return
    else:
        os.mkdir(target)

    dirs = os.listdir(source)
    for d in dirs:
        # don't ignore .git file
        if d == ".git" and not os.path.isfile(join(source, d)):
            pack(join(source, d), join(target, d))
            continue

        if ignore and ignore.ignoring(d):
            continue

        if os.path.isfile(join(source, d)):
            copy_file(join(source, d), join(target, d))
        else:
            pack(join(source, d), join(target, d), ignore)

    shutil.copystat(source, target)
    #print("copystat", source)

def main(source, target, ignore_file):
    source = os.path.realpath(source)
    target = os.path.realpath(target)
    target = join(target, os.path.basename(source))

    if os.path.exists(target):
        raise(Exception("Target exists!"))
    
    ignore = Ignores(ignore_file)
    pack(source, target, ignore)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("source", metavar = "source_directory")
    parser.add_argument("-t", dest = "target", metavar = "target_directory", default = "/tmp")
    parser.add_argument("-e", dest = "ignore_file", default = join(BASE, "ignore.txt"))
    args = parser.parse_args()
    #print(args.source)
    #print(args)
    main(args.source, args.target, args.ignore_file)