#! /usr/bin/env python3

import os


class Rule(object):
    def __init__(self):
        pass

    def match(self, name):
        pass


class NameRule(Rule):
    def __init__(self, args):
        super().__init__()

        self.names = []
        self.help = "NameRule's parameter should be string, or list of strings."

        if type(args) == str:
            self.names.append(args)
        elif type(args) == list or type(args) == tuple:
            for name in args:
                if type(name) != str:
                    raise Exception(self.help + " But %s is %s!" %
                                    (name, type(name)))
                self.names.append(name)
        else:
            raise Exception(self.help + " But it's %s!" % type(args))

    def match(self, name):
        return name in self.names


class SuffixRule(Rule):
    def __init__(self, args):
        super().__init__()

        self.suffixes = []
        self.help = "SuffixRule's parameter should be string, or list of strings."

        if type(args) == str:
            self.suffixes.append(args)
        elif type(args) == list or type(args) == tuple:
            for name in args:
                if type(name) != str:
                    raise Exception(self.help + " But %s is %s!" %
                                    (name, type(name)))
                self.suffixes.append(name)
        else:
            raise Exception(self.help + " But it's %s!" % type(args))

    def match(self, name):
        for suff in self.suffixes:
            if name.endswith("." + suff):
                return True
            else:
                return False


def parse_size_limit(s):
    op = ""
    size = ""

    s = s.strip()
    op = s[0]
    size = float(s[1:-1].strip())
    unit = s[-1]

    assert(op in ["<", ">", ">=", "<="])
    assert(unit in ["k", "m", "g"])

    if unit == "k":
        unit = 1024
    elif unit == "m":
        unit = 1024 * 1024
    elif unit == "g":
        unit = 1024 * 1024 * 1024

    size = size * unit
    size = int(size)

    return (op, size)


def get_directory_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


class FileSizeRule(Rule):
    def __init__(self, args):
        super().__init__()

        self.help = "FileSizeRule's parameter shoule be string with format \"[>|<|>=|<=] [FLOAT][k|m|g]\""
        self.op = ""
        self.size = ""

        if type(args) != str:
            raise Exception(self.help + " But it's %s" % type(args))
        args = args.strip()

        try:
            self.op, self.size = parse_size_limit(args)
        except Exception as e:
            raise Exception(self.help)

    def match(self, path):
        if not os.path.isfile(path):
            return False

        size = os.path.getsize(path)
        if self.op == "<":
            return size < self.size
        elif self.op == ">":
            return size > self.size
        elif self.op == "<=":
            return size <= self.size
        elif self.op == ">=":
            return size >= self.size


class DirSizeRule(Rule):
    def __init__(self, args):
        super().__init__()

        self.help = "DirSizeRule's parameter shoule be string with format \"[>|<|>=|<=] [FLOAT][k|m|g]\""
        self.op = ""
        self.size = ""

        if type(args) != str:
            raise Exception(self.help + " But it's %s" % type(args))
        args = args.strip()

        try:
            self.op, self.size = parse_size_limit(args)
        except Exception as e:
            raise Exception(self.help)

    def match(self, path):
        if not os.path.isdir(path):
            return False

        size = get_directory_size(path)
        if self.op == "<":
            return size < self.size
        elif self.op == ">":
            return size > self.size
        elif self.op == "<=":
            return size <= self.size
        elif self.op == ">=":
            return size >= self.size


class AndRule(Rule):
    def __init__(self, args):
        super().__init__()
        self.rules = []
        self.help = "AndRules' parameter shoud be list or tuple of rules."

        if type(args) != tuple and type(args) != list:
            raise Exception(self.help + " But it's %s" % type(args))

        for rule in args:
            if rule in _RULE_PROCESSER:
                proc = _RULE_PROCESSER[rule]
                self.rules.append(proc(rule))
            else:
                raise Exception("Can't recognize rule %s" % rule)

    def match(self, name):
        for rule in self.rules:
            if not rule.match(name):
                return False
        return True


_RULE_PROCESSER = {
    "name": NameRule,
    "and": AndRule,
    "suffix": SuffixRule,
    "file_size": FileSizeRule,
    "dir_size": DirSizeRule
}


class Rules(Rule):
    def __init__(self, args):
        super().__init__()

        self.rules = []
        self.help = "Rules' parameter shoud be list or tuple of rules."

        if type(args) != tuple and type(args) != list:
            raise Exception(self.help + " But it's %s" % type(args))

        for rule in args:
            if rule in _RULE_PROCESSER:
                proc = _RULE_PROCESSER[rule]
                self.rules.append(proc(rule))
            else:
                raise Exception("Can't recognize rule %s" % rule)

    def match(self, name):
        for rule in self.rules:
            if rule.match(name):
                return True
        return False
