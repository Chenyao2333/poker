#! /urs/bin/env pythons

import unittest
import os

import task
import utils


class TestNameRule(unittest.TestCase):
    def setUp(self):
        self.source = "/tmp/testtask/src"
        self.target = "/tmp/testtask/dst"

        self.src_struct = [
            "b.txt",
            "ortest",
            "test.or",
            "test_or",
            {
                "document": [
                    "c.txt",
                    "500k|hw1.pdf",
                    "20m|ktbook.pdf"
                ]
            },
            {
                "poker": [
                    {
                        ".git": [
                            {
                                "obj": [
                                    "5m|a",
                                    "3m|b"
                                ]
                            },
                            "2m|pointer"
                            "2m|nameneeded"
                        ]
                    },
                    "ppp",
                    "ddd",
                    "poker.py"
                ]
            },
            {
                "dtable": [
                    {
                        ".git": {
                            "obj": [
                                "1m|a",
                                "2m|b"
                            ]
                        }
                    },
                    "main.py"
                ]
            }
        ]

        self.task = {
            "directory": self.source,
            "match": [
                {
                    "name": ["b.txt", "c.txt"]
                },
                {
                    "and": [
                        {"suffix": "pdf"},
                        {"file_size": "< 1m"}
                    ]
                },
                {
                    "or": [
                        {"name": "ortest"},
                        {"suffix": "test.or"},
                    ]
                },
                {
                    "and": [
                        {"name": ".git"},
                        {"dir_size": "< 10m"}
                    ]
                }
            ]
        }

        self.dst_struct = [
            "b.txt",
            "ortest",
            "test.or",
            {
                "document": [
                    "c.txt",
                    "500k|hw1.pdf"
                ]
            },
            {
                "dtable": [
                    {
                        ".git": {
                            "obj": [
                                "1m|a",
                                "2m|b"
                            ]
                        }
                    }
                ]
            }
        ]

        os.system("rm -rf %s" % self.source)
        os.system("rm -rf %s" % self.target)
        os.makedirs(self.source, exist_ok=True)
        os.makedirs(self.target, exist_ok=True)
        utils.create_folders_struct_from_tree(self.src_struct)

    def tearDown(self):
        os.system("rm -rf %s" % self.source)
        os.system("rm -rf %s" % self.target)

    def test(self):
        t = task.Task(self.task)
        t.collect(self.target)
        # TODO self.assertTrue(uitls.compare_folders_and_tree(self.dst_struct, self.target))


if __name__ == '__main__':
    unittest.main()
