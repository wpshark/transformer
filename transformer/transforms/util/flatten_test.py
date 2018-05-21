import unittest
import flatten


class TestUtilFlattenTransform(unittest.TestCase):


    def test_flatten_empty(self):
        transformer = flatten.UtilFlattenTransform()
    
        self.assertEqual('', transformer.transform_many([],options={'separator':','}))
        self.assertEqual('', transformer.transform_many([None],options={'separator':','}))
        self.assertEqual('', transformer.transform_many([''],options={'separator':','}))
        self.assertEqual('', transformer.transform_many([""],options={'separator':','}))
  
    def test_flatten_many_empty(self):
        transformer = flatten.UtilFlattenTransform()
      
        self.assertEqual(',c,d', transformer.transform_many(['', 'c','d'], options={'separator':','}))
        self.assertEqual(',,c,d', transformer.transform_many(['', '', 'c,d'], options={'separator':','}))
        self.assertEqual(',', transformer.transform_many(['', ''], options={'separator':','}))
        self.assertEqual('c,d,', transformer.transform_many(['c,d',None], options={'separator':','}))
        self.assertEqual(',,c,d', transformer.transform_many([None, None, 'c,d'], options={'separator':','}))
        self.assertEqual(',', transformer.transform_many([None, None], options={'separator':','}))
          
    def test_flatten_one(self):
        transformer = flatten.UtilFlattenTransform()
        self.assertEqual('a', transformer.transform_many(['a'], options={'separator':','}))


    def test_flatten_many(self):
        transformer = flatten.UtilFlattenTransform()
        self.assertEqual('a,b,c,d', transformer.transform_many(['a,b', 'c,d'], options={'separator':','}))
        self.assertEqual('a,b,c,d', transformer.transform_many(['a','b','c','d'], options={'separator':','}))
        self.assertEqual('a,b,c,d', transformer.transform_many(['a,b,c,d'], options={'separator':','}))
        self.assertEqual('a b c d', transformer.transform_many(['a','b','c','d'], options={'separator':'[:space:]'}))
        self.assertEqual('a b c d', transformer.transform_many(['a','b','c','d'], options={'separator':'[:s:]'}))
        self.assertEqual('a;b;c;d', transformer.transform_many(['a','b','c','d'], options={'separator':';'}))






