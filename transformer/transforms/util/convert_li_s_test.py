import unittest
import convert_li_s


class TestUtilConvert_li_sTransform(unittest.TestCase):


    def test_convert_li_s_empty(self):
        transformer = convert_li_s.UtilConvert_li_sTransform()
    
        self.assertEqual('', transformer.transform_many([],options={'separator':','}))
        self.assertEqual('', transformer.transform_many([None],options={'separator':','}))
        self.assertEqual('', transformer.transform_many([''],options={'separator':','}))
        self.assertEqual('', transformer.transform_many([""],options={'separator':','}))
  
    def test_convert_li_s_many_empty(self):
        transformer = convert_li_s.UtilConvert_li_sTransform()
      
        self.assertEqual(',c,d', transformer.transform_many(['', 'c','d'], options={'separator':','}))
        self.assertEqual(',,c,d', transformer.transform_many(['', '', 'c,d'], options={'separator':','}))
        self.assertEqual(',', transformer.transform_many(['', ''], options={'separator':','}))
        self.assertEqual('c,d,', transformer.transform_many(['c,d',None], options={'separator':','}))
        self.assertEqual(',,c,d', transformer.transform_many([None, None, 'c,d'], options={'separator':','}))
        self.assertEqual(',', transformer.transform_many([None, None], options={'separator':','}))
          
    def test_convert_li_s_one(self):
        transformer = convert_li_s.UtilConvert_li_sTransform()
        self.assertEqual('a', transformer.transform_many(['a'], options={'separator':','}))


    def test_convert_li_s_many(self):
        transformer = convert_li_s.UtilConvert_li_sTransform()
        self.assertEqual('a,b,c,d', transformer.transform_many(['a,b', 'c,d'], options={'separator':','}))
        self.assertEqual('a,b,c,d', transformer.transform_many(['a','b','c','d'], options={'separator':','}))
        self.assertEqual('a,b,c,d', transformer.transform_many(['a,b,c,d'], options={'separator':','}))
        self.assertEqual('a b c d', transformer.transform_many(['a','b','c','d'], options={'separator':'[:space:]'}))
        self.assertEqual('a b c d', transformer.transform_many(['a','b','c','d'], options={'separator':'[:s:]'}))
        self.assertEqual('a;b;c;d', transformer.transform_many(['a','b','c','d'], options={'separator':';'}))






