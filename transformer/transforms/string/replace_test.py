# -*- coding: utf-8 -*-
import unittest
import replace

class TestStringReplaceTransform(unittest.TestCase):
    def test_replace(self):
        transformer = replace.StringReplaceTransform()
        self.assertEqual(transformer.transform("", "", ""), "")
        self.assertEqual(transformer.transform("", ""), "")
        self.assertEqual(transformer.transform("a", "", ""), "")
        self.assertEqual(transformer.transform("", "a", ""), "")
        self.assertEqual(transformer.transform(None, None, None), "")
        self.assertEqual(transformer.transform("a", None, None), "")
        self.assertEqual(transformer.transform(None, "a", None), "")
        self.assertEqual(transformer.transform("hello", "h", "j"), "jello")
        self.assertEqual(transformer.transform("aaa", "a", ""), "")
        self.assertEqual(transformer.transform("abba", "a", "b"), "bbbb")
        self.assertEqual(transformer.transform("banana", "na", "s"), "bass")
        self.assertEqual(transformer.transform("xy1212xy", "12", "0"), "xy00xy")
        self.assertEqual(transformer.transform("Abc", "A", "a"), "abc")
        self.assertEqual(transformer.transform("a, b", ",", ""), "a b")
        self.assertEqual(transformer.transform("å", "å", "b"), "b")
        self.assertEqual(transformer.transform("hello world", "[:space:]", "-"), "hello-world")
        self.assertEqual(transformer.transform("he llo  world", "[:space:][:space:]", "-"), "he llo-world")
        self.assertEqual(transformer.transform("he llo  world", "[:space:]", "-"), "he-llo--world")
        self.assertEqual(transformer.transform("he llo  world", "[:s:][:space:]", "-"), "he llo-world")
        self.assertEqual(transformer.transform("a\ta", "[:tab:]", "[:space:]"), "a a")
        self.assertEqual(transformer.transform("a a", "[:space:]", "[:newline:]"), "a\na")
