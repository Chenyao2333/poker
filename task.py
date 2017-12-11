#! /usr/bin/env pythons

import ruler

class Task(object):
    def __init__(self, args):
        self.dir = args["directory"]
        self.matchs = ruler.OrRule(args["matchs"])
        self.ignores = ruler.OrRule(args["ignores"])
    
    def collect(self, to):
        pass
