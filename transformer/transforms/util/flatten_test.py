import unittest
import flatten


class TestUtilFlattenTransform(unittest.TestCase):
    
 def test_flatten(self):
        transformer = flatten.UtilFlattenTransform()
        
        tests = [
                 # input, separator, output
                 (['a','b','c','d'], ',', 0, 'a'),
                 ('a:b', ':', 1, 'b'),
                 ('a:b', ':', -1, 'b'),


  def test_flatten_empty(self):
    transformer = flatten.UtilFlattenTransform()
    
    self.assertEqual('', transformer.transform_many(separator=','))
    self.assertEqual(None, transformer.transform_many(separator=','))

  def test_flatten_many(self):
        transformer = flatten.UtilFlattenTransform()
        
        self.assertEqual([['a', 'b'], ['c', 'd']], transformer.transform_many(['a,b', 'c,d'], dict(separator=',')))

  def test_flatten_many_empty(self):
    transformer = flatten.UtilFlattenTransform()
    
        self.assertEqual(['','c','d']], transformer.transform_many(['', 'c,d'], dict(separator=',')))
        self.assertEqual(['','','c','d'], transformer.transform_many(['', '', 'c,d'], dict(separator=',')))
        self.assertEqual(['', ''], transformer.transform_many(['', ''], dict(separator=',')))
        self.assertEqual(['', ['c', 'd']], transformer.transform_many([None, 'c,d'], dict(separator=',')))
        self.assertEqual(['', '', ['c', 'd']], transformer.transform_many([None, None, 'c,d'], dict(separator=',',)))
        self.assertEqual(['', ''], transformer.transform_many([None, None], dict(separator=',',)))
