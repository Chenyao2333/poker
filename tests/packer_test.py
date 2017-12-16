#! /urs/bin/env pythons

import unittest
import os

import poker.utils as utils
import poker.packer as packer

class TestPacker(unittest.TestCase):
    def setUp(self):
        self.test_path_1 = "/tmp/testpacker1"
        self.test_path_2 = "/tmp/testpacker2"

        self.struct_1 = [
            "1.txt",
            "b.txt",
            {
                "a": ["a.txt"]
            }
        ]

        self.struct_2 = [
            "2.txt",
            {
                "b": ["b.txt"]
            }
        ]

        os.makedirs(self.test_path_1, exist_ok = True)
        os.makedirs(self.test_path_2, exist_ok = True)
        utils.create_dirs_from_struct_tree(self.struct_1, self.test_path_1)
        utils.create_dirs_from_struct_tree(self.struct_2, self.test_path_2)

    def tearDown(self):
        os.system("rm -rf %s %s" % (self.test_path_1, self.test_path_2))

    def test(self):
        self.task_file = "/tmp/tasks.yaml"
        with open(self.task_file, "w") as f:
            f.write("""
            tasks:
              packa:
                directory: /tmp/testpacker1
                ignore:
                  - name: b.txt
              
              packb:
                directory: /tmp/testpacker2
            """)

        t = packer.Packer(self.task_file)
        collection_path = t.collect()
        print(collection_path)
        struct = [
            "tasks.yml",
            {
                "packa": [
                    "1.txt",
                    {
                        "a": ["a.txt"]
                    }
                ]
            },
            {
                "packb": [
                    "2.txt",
                    {
                        "b": ["b.txt"]
                    }
                ]
            }
        ]
        self.assertTrue(utils.compare_struct_tree_and_dirs(struct, collection_path))
        
        os.system("rm -rf %s" % collection_path)


if __name__ == '__main__':
    unittest.main()