import unittest
import fix_lineitems


class UtilFixLineitemsTransform(unittest.TestCase):
    def test_fix_lineitems(self):
        transformer = fix_lineitems.UtilFixLineitemsTransform()
        self.assertEqual(
            {
                "Shopify Tax Lines Rate": [ "17.97","17.97","5.34","0.00","13.73","20.59","40.72","39.89"],
                "test2": ["B","E","I"],
                "test5": ["CAD"],
                "test4": ["Line 1","Line 2","Preview","_pplr_preview"]
            },
            transformer.transform("",{"Shopify Tax Lines Rate":"17.97,17.97,5.34,0.00,13.73,20.59,40.72,39.89","test2":"B,E,I","test5":"CAD","test4":"Line 1,Line 2,Preview,_pplr_preview"})
        )