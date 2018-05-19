import unittest
import flatten


class TestUtilFlattenTransform(unittest.TestCase):


  def test_flatten_empty(self):
    transformer = flatten.UtilFlattenTransform()
    
    self.assertEqual('', transformer.transform_many([],separator=','))
    self.assertEqual('', transformer.transform_many([None],separator=','))
    self.assertEqual('', transformer.transform_many([''],separator=','))

  def test_flatten_many(self):
    transformer = flatten.UtilFlattenTransform()
        
    self.assertEqual('a,b,c,d', transformer.transform_many(['a,b', 'c,d'], separator=','))
    self.assertEqual('a,b,c,d', transformer.transform_many(['a','b','c','d'], separator=','))
    self.assertEqual('a,b,c,d', transformer.transform_many(['a,b,c,d'], separator=','))

  def test_flatten_many_empty(self):
    transformer = flatten.UtilFlattenTransform()
    
    self.assertEqual('','c','d', transformer.transform_many(['', 'c,d'], separator=','))
    self.assertEqual('','','c','d', transformer.transform_many(['', '', 'c,d'], separator=','))
    self.assertEqual('', '', transformer.transform_many(['', ''], separator=','))
    self.assertEqual('', 'c', 'd', transformer.transform_many([None, 'c,d'], separator=','))
    self.assertEqual('', '', 'c', 'd', transformer.transform_many([None, None, 'c,d'], separator=','))
    self.assertEqual('', '', transformer.transform_many([None, None], separator=','))
