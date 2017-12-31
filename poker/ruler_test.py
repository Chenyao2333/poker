#! /urs/bin/env pythons

import unittest
import os

import poker.ruler as ruler
import poker.utils as utils


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
        self.f3_size = 1024 * 1024 * 2  # 2m

        os.makedirs(self.dir_for_test, exist_ok=True)
        os.system("dd bs=%d count=1 if=/dev/zero of=%s 2> /dev/null" %
                  (self.f1_size, self.f1))
        os.system("dd bs=%d count=1 if=/dev/zero of=%s 2> /dev/null" %
                  (self.f2_size, self.f2))
        os.system("dd bs=%d count=1 if=/dev/zero of=%s 2> /dev/null" %
                  (self.f3_size, self.f3))

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
    def setUp(self):
        self.dir = "/tmp/tttest"
        self.f1 = self.dir + "/f1"
        self.f2 = self.dir + "/f2"
        self.total_size = 0
        self.f1_size = 0
        self.f2_size = 0

        os.makedirs(self.dir, exist_ok=False)
        os.makedirs(self.f1, exist_ok=False)
        os.makedirs(self.f2, exist_ok=False)

        self.total_size += 2048
        os.system("dd bs=%s count=1 if=/dev/zero of=%s 2> /dev/null" %
                  (2048, self.dir + "/file1"))
        self.total_size += 4096
        self.f1_size += 4096
        os.system("dd bs=%s count=1 if=/dev/zero of=%s 2> /dev/null" %
                  (4096, self.f1 + "/file1"))
        self.total_size += 8192
        self.f1_size += 8192
        os.system("dd bs=%s count=1 if=/dev/zero of=%s 2> /dev/null" %
                  (8192, self.f1 + "/file2"))
        self.total_size += 8888
        self.f2_size += 8888
        os.system("dd bs=%s count=1 if=/dev/zero of=%s 2> /dev/null" %
                  (8888, self.f2 + "/file1"))

    def tearDown(self):
        os.system("rm -rf %s" % self.dir)

    def test_size_calculator(self):
        # total = 23334 = 22.6796875k
        r1 = ruler.DirSizeRule("<= 22.6796875k")
        r2 = ruler.DirSizeRule("<= 22.6796874k")

        self.assertTrue(r1.match(self.dir))
        self.assertFalse(r2.match(self.dir))

    def test_less(self):
        r1 = ruler.DirSizeRule("< 8888b")
        r2 = ruler.DirSizeRule("< 8889b")

        self.assertFalse(r1.match(self.f2))
        self.assertTrue(r2.match(self.f2))

    def test_great(self):
        # f1 = 12288
        r1 = ruler.DirSizeRule("> 12288b")
        r2 = ruler.DirSizeRule("> 12287b")
        r3 = ruler.DirSizeRule(">= 12288b")
        r4 = ruler.DirSizeRule(">= 12289b")

        self.assertFalse(r1.match(self.f1))
        self.assertTrue(r2.match(self.f1))
        self.assertTrue(r3.match(self.f1))
        self.assertFalse(r4.match(self.f1))


class TestAndRule(unittest.TestCase):
    def setUp(self):
        utils.create_file_with_zeros("/tmp/nihao", 2048)

    def tearDown(self):
        os.system("rm -rf /tmp/nihao")

    def test_normal(self):
        r1 = ruler.AndRule([
            {
                "name": "nihao"
            },
            {
                "file_size": "> 1024b"
            }
        ])

        r2 = ruler.AndRule([
            {
                "name": "nihao"
            },
            {
                "file_size": "<= 2047b"
            }
        ])

        self.assertTrue(r1.match("/tmp/nihao"))
        self.assertFalse(r2.match("/tmp/nihao"))

    def test_exception(self):
        with self.assertRaises(Exception):
            ruler.AndRule({
                "name": "nihao",
                "file_size": "> 1024b"
            })


class TestOrRule(unittest.TestCase):
    def setUp(self):
        utils.create_file_with_zeros("/tmp/nihao", 2048)

    def tearDown(self):
        os.system("rm -rf /tmp/nihao")

    def test(self):
        r1 = ruler.OrRule([
            {
                "name": "bye"
            },
            {
                "file_size": "> 1024b"
            }
        ])

        r2 = ruler.OrRule({
            "name": "bye",
            "file_size": "> 1024b"
        })

        r3 = ruler.OrRule({
            "name": "bye",
            "file_size": "< 1024b"
        })

        self.assertTrue(r1.match("/tmp/nihao"))
        self.assertTrue(r2.match("/tmp/nihao"))
        self.assertFalse(r3.match("/tmp/nihao"))


class TestAlwaysTrueAndFalse(unittest.TestCase):
    def test(self):
        t = ruler.AlwaysTrueRule()
        self.assertTrue(t.match("23"))

        f = ruler.AlwaysFalseRule()
        self.assertFalse(f.match("23"))


if __name__ == '__main__':
    unittest.main()
