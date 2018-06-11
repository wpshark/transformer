import unittest
import append


class TestUtilAppendTransform(unittest.TestCase):


    def test_append_one(self):
        transformer = append.UtilAppendTransform()
        self.assertEqual(['a','e'], transformer.transform_many(['a'], options={'append_text':'e'}))

    def test_append_empty(self):
        transformer = append.UtilAppendTransform()
    
        self.assertEqual(['e'], transformer.transform_many([],options={'append_text': 'e'}))
        self.assertEqual([None,'e'], transformer.transform_many([None],options={'append_text': 'e'}))
        self.assertEqual(['e'], transformer.transform_many([''],options={'append_text': 'e'}))
        self.assertEqual(['e'], transformer.transform_many([""],options={'append_text': 'e'}))
  
    def test_append_many_empty(self):
        transformer = append.UtilAppendTransform()
      
        self.assertEqual(['', 'c','d','e'], transformer.transform_many(['', 'c','d'], options={'append_text':'e'}))
        self.assertEqual(['', '', 'c,d','e'], transformer.transform_many(['', '', 'c,d'], options={'append_text':'e'}))
        self.assertEqual(['', '','e'], transformer.transform_many(['', ''], options={'append_text':'e'}))
        self.assertEqual(['c,d',None,'e'], transformer.transform_many(['c,d',None], options={'append_text':'e'}))
        self.assertEqual([None,None,'c,d','e'], transformer.transform_many([None, None, 'c,d'], options={'append_text':'e'}))
        self.assertEqual([None,None,'e'], transformer.transform_many([None, None], options={'append_text':'e'}))



    def test_append_many(self):
        transformer = append.UtilAppendTransform()
        self.assertEqual(['a,b', 'c,d','e'], transformer.transform_many(['a,b', 'c,d'], options={'append_text':'e'}))
        self.assertEqual(['a','b','c','d','e'], transformer.transform_many(['a','b','c','d'], options={'append_text':'e'}))
        self.assertEqual(['a,b,c,d','e'], transformer.transform_many(['a,b,c,d'], options={'append_text':'e'}))
        self.assertEqual(['a','b','c','d','lots of funky text here'], transformer.transform_many(['a','b','c','d'], options={'append_text':'lots of funky text here'}))

    def test_append_list(self):
        transformer = append.UtilAppendTransform()
        self.assertEqual(['a,b', 'c,d','e'], transformer.transform_many(['a,b','c,d'], options={'append_text':['e']}))






