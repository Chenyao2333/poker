#! /usr/bin/env pythons

import ruler


class Task(object):
    def __init__(self, args):
        self.dir = args["directory"]
        self.match = ruler.OrRule(args["match"])
        self.ignore = ruler.OrRule(args["ignore"])

    def _search_matched_files(self):
        pass

    def _copy(self, file):
        pass

    def collect(self, to):
        files = self._search_matched_files()
        failed = []
        for f in files:
            try:
                self._copy(f)
            except Exception as e:
                failed.append(f)
        return failed
