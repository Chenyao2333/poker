#! /urs/bin/env pythons

import unittest
import os

import ruler


class TestNameRule(unittest.TestCase):
    def test_singal(self):
        r = ruler.NameRule("tttt")

        self.assertTrue(r.match("tttt"))
        self.assertTrue(r.match("/home/tttt"))
        self.assertFalse(r.match("ttttttttt"))
        self.assertFalse(r.match("/home/ttttttttt"))

    def test_multi(self):
        r = ruler.NameRule(["tttt", "aaa"])

        self.assertTrue(r.match("tttt"))
        self.assertTrue(r.match("/home/aaa"))
        self.assertFalse(r.match("ttttttttt"))
        self.assertFalse(r.match("/home/aaaa"))


class TestSuffixRule(unittest.TestCase):
    def test_singal(self):
        r = ruler.SuffixRule("tar.gz")

        self.assertTrue(r.match("a.tar.gz"))
        self.assertTrue(r.match("/etc/back.tar.gz"))
        self.assertFalse(r.match("/abc/a.tar.gzz"))
        self.assertFalse(r.match("/abc/abc.tar.xx.gz"))

    def test_multi(self):
        r = ruler.SuffixRule(["tar.gz", "pdf"])

        self.assertTrue(r.match("a.tar.gz"))
        self.assertTrue(r.match("/etc/back.tar.gz"))
        self.assertTrue(r.match("/etc/homwwork.pdf"))
        self.assertTrue(r.match("/abc/abc.tar.xx.gz.pdf"))
        self.assertFalse(r.match("/abc/a.tar.gzz"))
        self.assertFalse(r.match("/abc/abc.tar.xx.gz"))
        self.assertFalse(r.match("xxxxx.pdf.tar"))


class TestFileSizeRule(unittest.TestCase):
    def setUp(self):
        self.dir_for_test = "/tmp/ttttest"
        self.f1 = self.dir_for_test + "/" + "file1"
        self.f1_size = 4096
        self.f2 = self.dir_for_test + "/" + "file2"
        self.f2_size = 1024 * 1024 + 512 * 1024  # 1.5m

        os.mkdir(self.dir_for_test)

    def tearDown(self):
        os.system("rm -rf %s" % self.dir_for_test)

    def test_less(self):
        pass


class TestDirSizeRule(unittest.TestCase):
    pass


class TestAndRule(unittest.TestCase):
    pass


class TestOrRule(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
