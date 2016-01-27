import unittest
import choose

class TestUtilChooseTransform(unittest.TestCase):
    def test_choose_empty(self):
        transformer = choose.UtilChooseTransform()
        self.assertEqual(0, transformer.transform_many([], options={'operation': 'first', 'default':0}))
        self.assertEqual(0, transformer.transform_many([], options={'operation': 'last', 'default':0}))
        self.assertEqual(0, transformer.transform_many([], options={'operation': 'random', 'default':0}))

        self.assertEqual(0, transformer.transform_many([0], options={'operation': 'first', 'default':1}))
        self.assertEqual(0, transformer.transform_many([0], options={'operation': 'last', 'default':1}))
        self.assertEqual(0, transformer.transform_many([0], options={'operation': 'random', 'default':1}))

        self.assertEqual(0, transformer.transform_many([0, 0], options={'operation': 'first', 'default':1}))
        self.assertEqual(0, transformer.transform_many([0, 0], options={'operation': 'last', 'default':1}))
        self.assertEqual(0, transformer.transform_many([0, 0], options={'operation': 'random', 'default':1}))

        self.assertEqual(0, transformer.transform_many([''], options={'operation': 'first', 'default':0}))
        self.assertEqual(0, transformer.transform_many([''], options={'operation': 'last', 'default':0}))
        self.assertEqual(0, transformer.transform_many([''], options={'operation': 'random', 'default':0}))

        self.assertEqual(0, transformer.transform_many(['', ''], options={'operation': 'first', 'default':0}))
        self.assertEqual(0, transformer.transform_many(['', ''], options={'operation': 'last', 'default':0}))
        self.assertEqual(0, transformer.transform_many(['', ''], options={'operation': 'random', 'default':0}))

    def test_choose_full(self):
        transformer = choose.UtilChooseTransform()

        self.assertEqual(1, transformer.transform_many([1, 2, 3], options={'operation': 'first', 'default':0}))
        self.assertEqual(3, transformer.transform_many([1, 2, 3], options={'operation': 'last', 'default':0}))

        self.assertNotEqual(0, transformer.transform_many([1, 2, 3], options={'operation': 'random', 'default':0}))
        self.assertNotEqual('', transformer.transform_many(['', 1, 2, 3, 'a'], options={'operation': 'random', 'default':''}))

        self.assertEqual(1, transformer.transform_many([1, '', ''], options={'operation': 'first', 'default':0}))
        self.assertEqual(1, transformer.transform_many([1, '', ''], options={'operation': 'last', 'default':0}))
        self.assertEqual(1, transformer.transform_many([1, '', ''], options={'operation': 'random', 'default':0}))
        self.assertEqual(1, transformer.transform_many([1, '', ''], options={'operation': 'random', 'default':0}))
        self.assertEqual(1, transformer.transform_many([1, '', ''], options={'operation': 'random', 'default':0}))

        self.assertEqual(1, transformer.transform_many(['', 1, ''], options={'operation': 'first', 'default':0}))
        self.assertEqual(1, transformer.transform_many(['', 1, ''], options={'operation': 'last', 'default':0}))
        self.assertEqual(1, transformer.transform_many(['', 1, ''], options={'operation': 'random', 'default':0}))
        self.assertEqual(1, transformer.transform_many(['', 1, ''], options={'operation': 'random', 'default':0}))
        self.assertEqual(1, transformer.transform_many(['', 1, ''], options={'operation': 'random', 'default':0}))

        self.assertEqual(1, transformer.transform_many(['', '', 1], options={'operation': 'first', 'default':0}))
        self.assertEqual(1, transformer.transform_many(['', '', 1], options={'operation': 'last', 'default':0}))
        self.assertEqual(1, transformer.transform_many(['', '', 1], options={'operation': 'random', 'default':0}))
        self.assertEqual(1, transformer.transform_many(['', '', 1], options={'operation': 'random', 'default':0}))
        self.assertEqual(1, transformer.transform_many(['', '', 1], options={'operation': 'random', 'default':0}))

        self.assertEqual(2, transformer.transform_many(['', 2, 3, ''], options={'operation': 'first', 'default':0}))
        self.assertEqual(3, transformer.transform_many(['', 2, 3, ''], options={'operation': 'last', 'default':0}))

        self.assertEqual('a', transformer.transform_many(['a', 2, 3, 'b'], options={'operation': 'first', 'default':0}))
        self.assertEqual('b', transformer.transform_many(['a', 2, 3, 'b'], options={'operation': 'last', 'default':0}))
