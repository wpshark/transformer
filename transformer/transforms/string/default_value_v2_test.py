import unittest
import default_value_v2

class TestStringDefaultValueV2Transform(unittest.TestCase):
    def test_default_value(self):
        transformer = default_value_v2.StringDefaultValueV2Transform()

        self.assertEqual(transformer.transform_many("", options={"default_value":"test"}), "test")
        self.assertEqual(transformer.transform_many(u"", options={"default_value":"test"}), "test")
        self.assertEqual(transformer.transform_many(None, options={"default_value":"test"}), "test")

        self.assertEqual(transformer.transform_many("a", options={"default_value":"test"}), "a")
        self.assertEqual(transformer.transform_many(0, options={"default_value":"test"}), 0)
        self.assertEqual(transformer.transform_many(1, options={"default_value":"test"}), 1)
        self.assertEqual(transformer.transform_many(True, options={"default_value":"test"}), True)
        self.assertEqual(transformer.transform_many(False, options={"default_value":"test"}), False)

        #arrays
        self.assertEqual(transformer.transform_many(["a"], options={"default_value":"test"}), ["a"])
        self.assertEqual(transformer.transform_many(["a",""], options={"default_value":"test"}), ["a","test"])
        self.assertEqual(transformer.transform_many(["",None], options={"default_value":"test"}), ["test","test"])
        self.assertEqual(transformer.transform_many([], options={"default_value":"test"}), ["test"])
