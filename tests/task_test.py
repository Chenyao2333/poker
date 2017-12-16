#! /urs/bin/env pythons

import unittest
import os

import poker.task as task
import poker.ruler as ruler
import poker.utils as utils


class TestNameRule(unittest.TestCase):
    def setUp(self):
        self.source = "/tmp/testtask/src"
        self.target = "/tmp/testtask/dst"
        self.task_name = "dst"

        self.src_struct = [
            "b.txt",
            "ortest",
            "a.test.or",
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
                            "2m|pointer",
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
            "a.test.or",
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
        utils.create_dirs_from_struct_tree(self.src_struct, self.source)

    def tearDown(self):
        os.system("rm -rf %s" % self.source)
        os.system("rm -rf %s" % self.target)

    def test(self):
        t = task.Task(self.task_name, self.task)
        self.assertTrue(type(t.match) == ruler.OrRule)
        self.assertTrue(t.match.match("/tmp/b.txt"))
        self.assertTrue(t.match.match("b.txt"))
        self.assertEqual(t.collect(os.path.dirname(self.target)), [])

        self.assertTrue(utils.compare_struct_tree_and_dirs(
            self.dst_struct, self.target))


if __name__ == '__main__':
    unittest.main()
