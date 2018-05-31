import unittest
import convert_s_li

class TestUtilConvert_s_liTransform(unittest.TestCase):

    def test_convert_s_li(self):
        transformer = convert_s_li.UtilConvert_s_liTransform()
        
        self.assertEqual(['a','b','c','d'], transformer.transform('a,b,c,d'))
        self.assertEqual(['a','b','c','d',''], transformer.transform('a,b,c,d,'))
            


def test_convert_s_li_empty(self):
    transformer = convert_s_li.UtilConvert_s_liTransform()
    
    self.assertEqual('', transformer.transform(''))
    self.assertEqual('', transformer.transform(None))

def test_convert_s_li_many(self):
    transformer = convert_s_li.UtilConvert_s_liTransform()
        
    self.assertEqual([['a', 'b'], ['c', 'd']], transformer.transform_many(['a,b', 'c,d']))

def test_convert_s_li_many_empty(self):
    transformer = convert_s_li.UtilConvert_s_liTransform()
    
    self.assertEqual(['', ['c', 'd']], transformer.transform_many(['', 'c,d']))
    self.assertEqual(['', '', ['c', 'd']], transformer.transform_many(['', '', 'c,d']))
    self.assertEqual(['', ''], transformer.transform_many(['', '']))
        
    self.assertEqual(['', ['c', 'd']], transformer.transform_many([None, 'c,d']))
    self.assertEqual(['', '', ['c', 'd']], transformer.transform_many([None, None, 'c,d']))
    self.assertEqual(['', ''], transformer.transform_many([None, None]))
