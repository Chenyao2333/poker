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
        self.f3 = self.dir_for_test + "/" + "file3"
        self.f3_size = 1024 * 1024 * 2 # 2m

        os.makedirs(self.dir_for_test, exist_ok=True)
        os.system("dd bs=%d count=1 if=/dev/zero of=%s 2> /dev/null" % (self.f1_size, self.f1))
        os.system("dd bs=%d count=1 if=/dev/zero of=%s 2> /dev/null" % (self.f2_size, self.f2))
        os.system("dd bs=%d count=1 if=/dev/zero of=%s 2> /dev/null" % (self.f3_size, self.f3))

    def tearDown(self):
        os.system("rm -rf %s" % self.dir_for_test)

    def test_less(self):
        r = ruler.FileSizeRule("< 1m")
        self.assertTrue(r.match(self.f1))
        self.assertFalse(r.match(self.f2))

        r = ruler.FileSizeRule("<1024k")
        self.assertTrue(r.match(self.f1))
        self.assertFalse(r.match(self.f2))

        r = ruler.FileSizeRule("< 0.0009765625g")
        self.assertTrue(r.match(self.f1))
        self.assertFalse(r.match(self.f2))

    def test_great(self):
        r = ruler.FileSizeRule("> 1m")
        self.assertFalse(r.match(self.f1))
        self.assertTrue(r.match(self.f2))

        r = ruler.FileSizeRule("> 1024k")
        self.assertFalse(r.match(self.f1))
        self.assertTrue(r.match(self.f2))

        r = ruler.FileSizeRule(">0.0009765625g")
        self.assertFalse(r.match(self.f1))
        self.assertTrue(r.match(self.f2))
        
    def test_le(self):
        r = ruler.FileSizeRule("<= 1.5m")
        self.assertTrue(r.match(self.f1))
        self.assertTrue(r.match(self.f2))
        self.assertFalse(r.match(self.f3))

    def test_ge(self):
        r = ruler.FileSizeRule(">= 1.5m")
        self.assertFalse(r.match(self.f1))
        self.assertTrue(r.match(self.f2))
        self.assertTrue(r.match(self.f3))


class TestDirSizeRule(unittest.TestCase):
    pass


class TestAndRule(unittest.TestCase):
    pass


class TestOrRule(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
