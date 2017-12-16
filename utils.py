#! /usr/bin/env python3

import os
import ruler


def create_file_with_zeros(p, size=0):
    os.system("touch %s" % p)
    os.system("dd bs=%d count=1 if=/dev/zero of=%s 2> /dev/null" % (size, p))


def _parse_size_name(s):
    # s = "1m|a.txt"
    if "|" in s:
        #print(s)
        size, name = s.split("|")
        size = ruler.parse_size(size)
    else:
        size, name = 0, s
    return size, name

def test_parse_size_name():
    assert(_parse_size_name("5m|2.txt") == (1024*1024*5, "2.txt"))
    assert(_parse_size_name("nihao.txt") == (0, "nihao.txt"))


def create_dirs_from_struct_tree(struct, root_dir):
    if type(struct) == list:
        for x in struct:
            if type(x) == str:
                size, name = _parse_size_name(x)
                path = os.path.join(root_dir, name)
                create_file_with_zeros(path, size)
            elif type(x) == dict:
                create_dirs_from_struct_tree(x, root_dir)
                
    elif type(struct) == dict:
        for dir_name in struct:
            path = os.path.join(root_dir, dir_name)
            os.makedirs(path, exist_ok = True)
            create_dirs_from_struct_tree(struct[dir_name], path)
                

def compare_struct_tree_and_dirs(struct, root_dir):
    if type(struct) == list:
        for x in struct:
            if type(x) == str:
                size, name = _parse_size_name(x)
                path = os.path.join(root_dir, name)
                if not os.path.isfile(path):
                    print("not find", path)
                    return False
                if os.path.getsize(path) != size:
                    return False
            elif type(x) == dict:
                if not compare_struct_tree_and_dirs(x, root_dir):
                    return False
    
    elif type(struct) == dict:
        for dir_name in struct:
            path = os.path.join(root_dir, dir_name)
            if not os.path.isdir(path):
                return False
            if not compare_struct_tree_and_dirs(struct[dir_name], path):
                return False
    
    return True


def test_create_dirs_from_struct_tree():
    struct = [
        "a.txt",
        "b.txt",
        {
            "c": [
                "a.txt"
            ]
        },
        {
            "d": [
                {
                    "e": {
                        "e.txt"
                    }
                }
            ]
        }
    ]
    
    create_dirs_from_struct_tree(struct, "/tmp/testutils")
    assert(compare_struct_tree_and_dirs(struct, "/tmp/testutils") == True)