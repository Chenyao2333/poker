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
        name = os.path.basename(name)
        return name in self.names


class SuffixRule(Rule):
    def __init__(self, args):
        super().__init__()

        self.suffixes = []
        self.help = "SuffixRule's parameter should be string, or list of strings."

        if type(args) == str:
            self.suffixes.append(args)
        elif type(args) == list or type(args) == tuple:
            for suff in args:
                if type(suff) != str:
                    raise Exception(self.help + " But %s is %s!" %
                                    (suff, type(suff)))
                self.suffixes.append(suff)
        else:
            raise Exception(self.help + " But it's %s!" % type(args))

    def match(self, name):
        for suff in self.suffixes:
            if name.endswith("." + suff):
                return True
        
        return False


def parse_size_limit(s):
    op = ""
    size = ""

    s = s.strip()

    OPS = [">", "<", ">=", "<="]
    UNITS = ["k", "m", "g"]
    op = ""
    unit = ""
    for x in OPS:
        if s.startswith(x) and len(x) > len(op):
            op = x
    for x in UNITS:
        if s.endswith(x) and len(x) > len(unit):
            unit = x

    assert(op in OPS)
    assert(unit in UNITS)
    
    size = float(s[len(op):-len(unit)].strip())

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
        self.help = "AndRule's parameter shoud be list or tuple of rules."

        if type(args) != tuple and type(args) != list:
            raise Exception(self.help + " But it's %s" % type(args))

        for rule in args:
            if type(rule) == dict:
                proc = _RULE_PROCESSER["or"]
            elif type(rule) == str and rule in _RULE_PROCESSER:
                proc = _RULE_PROCESSER[rule]
            else:
                raise Exception("Can't recognize rule %s" % rule)
            
            self.rules.append(proc(rule))

    def match(self, name):
        for rule in self.rules:
            if not rule.match(name):
                return False
        return True

class OrRule(Rule):
    def __init__(self, args):
        super().__init__()

        self.rules = []
        self.help = "OrRule's parameter shoud be list or tuple of rules."

        if type(args) != tuple and type(args) != list:
            raise Exception(self.help + " But it's %s" % type(args))


        for rule in args:
            if type(rule) == dict:
                proc = _RULE_PROCESSER["or"]
            elif type(rule) == str and rule in _RULE_PROCESSER:
                proc = _RULE_PROCESSER[rule]
            else:
                raise Exception("Can't recognize rule %s" % rule)
            
            self.rules.append(proc(rule))

    def match(self, name):
        for rule in self.rules:
            if rule.match(name):
                return True
        return False


_RULE_PROCESSER = {
    "name": NameRule,
    "suffix": SuffixRule,
    "file_size": FileSizeRule,
    "dir_size": DirSizeRule,
    "and": AndRule,
    "or": OrRule
}
