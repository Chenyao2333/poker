#! /usr/bin/env python3

import os


def create_file_with_zeros(p, size=0):
    os.system("touch %s" % p)
    os.system("dd bs=%d count=1 if=/dev/zero of=%s 2> /dev/null" % (size, p))

def create_folders_struct_from_tree(t):
    pass