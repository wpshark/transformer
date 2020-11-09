import unittest
from . import import_csv


class TestUtilImportCSVTransform(unittest.TestCase):

    def test_import_csv_utf8(self):
        transformer = import_csv.UtilImportCSVTransform()
        self.assertEqual(
            {
                "csv_text": b"\xc3\xb8o,\xc3\xa9e,\xc3\xbcu\n1,2,3\n4,5,6\n8,\xc3\xbcu,10\n".decode(),
                "line_items": [{b"\xc3\xb8o".decode(): "1", b"\xc3\xa9e".decode(): "2", b"\xc3\xbcu".decode(): "3"},
                               {b"\xc3\xb8o".decode(): "4", b"\xc3\xa9e".decode(): "5", b"\xc3\xbcu".decode(): "6"},
                               {b"\xc3\xb8o".decode(): "8", b'\xc3\xa9e'.decode(): b"\xc3\xbcu".decode(), b"\xc3\xbcu".decode(): "10"}],
                "header": True,
                "dialect": "default"
            },
            transformer.transform('https://cdn.zapier.com/storage/files/eb326ab5507c719578c9e6086fef13b2.txt', True, 'default'))

    def test_import_csv_nocsv(self):
        transformer = import_csv.UtilImportCSVTransform()
        self.assertEqual(
            {
                "csv_text": "garbage stuff here.....",
                "line_items": [],
                "header": True,
                "dialect": "default"
            },
            transformer.transform('https://cdn.zapier.com/storage/files/4604a501b648795718a8ebe7143f2531.txt', True, 'default'))

    def test_import_csv_noheaders(self):
        transformer = import_csv.UtilImportCSVTransform()
        # no headers - values missing, but all delimited
        self.assertEqual(
            {
                "csv_text": "1,2,3,4,5\n5,6,7,,8\n9,,11,,12\n,,14,15,16",
                "line_items": [
                    {   
                        "item_1": "1",
                        "item_2": "2",
                        "item_3": "3",
                        "item_4": "4",
                        "item_5": "5"
                     },
                    {
                        "item_1": "5",
                        "item_2": "6",
                        "item_3": "7",
                        "item_4": "",
                        "item_5": "8"
                    },
                    {
                        "item_1": "9",
                        "item_2": "",
                        "item_3": "11",
                        "item_4": "",
                        "item_5": "12"
                    },
                    {
                        "item_1": "",
                        "item_2": "",
                        "item_3": "14",
                        "item_4": "15",
                        "item_5": "16"
                    }
                ],
                "header": False,
                "dialect": "default"
            },
            transformer.transform('https://cdn.zapier.com/storage/files/3a6f0142ef7840096103c615ebaf4c7b.csv', False, 'default'))

        
    def test_import_csv_noheaders_forced_dialect(self):
      # forced_header headers - values missing, but all delimited
        transformer = import_csv.UtilImportCSVTransform()
        self.assertEqual(
            {
                "csv_text": "1,2,3,4,5\n5,6,7,,8\n9,,11,,12\n,,14,15,16",
                "line_items": [
                    {   
                        "item_1": "1",
                        "item_2": "2",
                        "item_3": "3",
                        "item_4": "4",
                        "item_5": "5"
                     },
                    {
                        "item_1": "5",
                        "item_2": "6",
                        "item_3": "7",
                        "item_4": "",
                        "item_5": "8"
                    },
                    {
                        "item_1": "9",
                        "item_2": "",
                        "item_3": "11",
                        "item_4": "",
                        "item_5": "12"
                    },
                    {
                        "item_1": "",
                        "item_2": "",
                        "item_3": "14",
                        "item_4": "15",
                        "item_5": "16"
                    }
                ],
                "header": False,
                "dialect": "comma"
            },
            transformer.transform('https://cdn.zapier.com/storage/files/3a6f0142ef7840096103c615ebaf4c7b.csv', False, 'comma'))

    def test_import_csv_noheaders_forced(self):
      # forced_header headers - values missing, but all delimited
        transformer = import_csv.UtilImportCSVTransform()
        self.assertEqual(
            {
                "csv_text": "1,2,3,4,5\n5,6,7,,8\n9,,11,,12\n,,14,15,16",
                "line_items": [
                    {
                        "1": "5",
                        "2": "6",
                        "3": "7",
                        "4": "",
                        "5": "8"
                    },
                    {
                        "1": "9",
                        "2": "",
                        "3": "11",
                        "4": "",
                        "5": "12"
                    },
                    {
                        "1": "",
                        "2": "",
                        "3": "14",
                        "4": "15",
                        "5": "16"
                    }
                ],
                "header": "forced",
                "dialect": "default"
            },
            transformer.transform('https://cdn.zapier.com/storage/files/3a6f0142ef7840096103c615ebaf4c7b.csv', True, 'default'))  

    def test_import_csv_headers_semicolon(self):
      # forced_header, quoted text, commas, semicolon
        transformer = import_csv.UtilImportCSVTransform()
        self.maxDiff = None
        self.assertEqual(
            {
                "csv_text": "name;address;city\nKirk,G;10515;BI\nFred;\"10515 NE Morning, Lane\"; BI\nStella;home;\"Lot\'s of stuff here,,,,\"\n",
                "line_items": [
                    {
                        "name": "Kirk,G",
                        "address": "10515",
                        "city": "BI",
                    },
                    {
                        "name": "Fred",
                        "address": "10515 NE Morning, Lane",
                        "city": " BI",
                    },
                    {
                        "name": "Stella",
                        "address": "home",
                        "city": "Lot's of stuff here,,,,"
                    }
                ],
                "header": "forced",
                "dialect": "default"
            },
            transformer.transform('https://cdn.zapier.com/storage/files/ec27f0d1a5686c615eb0ad494e9f0885_2.csv', True, 'default'))     


    def test_import_csv_crlf_header(self):
      # forced_header, commas, crlf
        transformer = import_csv.UtilImportCSVTransform()
        self.maxDiff = None
        self.assertEqual(
            {
                "csv_text": "Publisher Name,App Name,Bundle Name,App Store URL,Device\nBigStar,roku.bigstartv.bigstar,roku.bigstartv.bigstar,roku.bigstartv.bigstar,roku.bigstartv.bigstar\n,com.bigstartv.bigstar,com.bigstartv.bigstar,com.bigstartv.bigstar,com.bigstartv.bigstar\n,com.bigstar.movie,com.bigstar.movie,com.bigstar.movie,com.bigstar.movie\n",
                "line_items": [
                    {
                        "Publisher Name": "BigStar",
                        "App Name": "roku.bigstartv.bigstar",
                        "Bundle Name": "roku.bigstartv.bigstar",
                        "App Store URL": "roku.bigstartv.bigstar",
                        "Device": "roku.bigstartv.bigstar"
                    },
                    {
                        "Publisher Name": "",
                        "App Name": "com.bigstartv.bigstar",
                        "Bundle Name": "com.bigstartv.bigstar",
                        "App Store URL": "com.bigstartv.bigstar",
                        "Device": "com.bigstartv.bigstar"
                    },
                    {
                        "Publisher Name": "",
                        "App Name": "com.bigstar.movie",
                        "Bundle Name": "com.bigstar.movie",
                        "App Store URL": "com.bigstar.movie",
                        "Device": "com.bigstar.movie"
                    }
                ],
                "header": "forced",
                "dialect": "default"
            },
            transformer.transform('https://cdn.zapier.com/storage/files/055e7c81a171202ac73a068e884bbf6c.csv', True, 'default'))     
     
    def test_import_csv_tsv_header(self):
      # forced_header, commas, crlf
        transformer = import_csv.UtilImportCSVTransform()
        self.maxDiff = None
        self.assertEqual(
            {
                "csv_text": "WO#\tProperty\tProperty Name\tUnit\tPriority\tCategory\tName\tPhone Number\tEmail\tCompleted Date\tEmployee\n646179\t4026\tVellagio Apts\t118\tLow\tPlumbing\tGraciela Ochoa\t\t\t6/18/2019\tomara\n653957\t4018\tPine Village South Apts\t4220P-2\tMed\tOther\tJonathan Leybag\t\t\t6/18/2019\tluisd,raulav\n658318\t4026\tVellagio Apts\t192\tHigh\tSection8\tKaryn Dejohnette\t\t\t6/18/2019\tisaac,omara,orlando",
                "line_items": [
                    {
                        "WO#": "646179",
                        "Property": "4026",
                        "Property Name": "Vellagio Apts",
                        "Unit": "118",
                        "Priority": "Low",
                        "Category": "Plumbing",
                        "Name": "Graciela Ochoa",
                        "Phone Number": "",
                        "Email": "",
                        "Completed Date": "6/18/2019",
                        "Employee": "omara"
                    },
                    {
                       "WO#": "653957",
                        "Property": "4018",
                        "Property Name": "Pine Village South Apts",
                        "Unit": "4220P-2",
                        "Priority": "Med",
                        "Category": "Other",
                        "Name": "Jonathan Leybag",
                        "Phone Number": "",
                        "Email": "",
                        "Completed Date": "6/18/2019",
                        "Employee": "luisd,raulav"
                    },
                    {
                        "WO#": "658318",
                        "Property": "4026",
                        "Property Name": "Vellagio Apts",
                        "Unit": "192",
                        "Priority": "High",
                        "Category": "Section8",
                        "Name": "Karyn Dejohnette",
                        "Phone Number": "",
                        "Email": "",
                        "Completed Date": "6/18/2019",
                        "Employee": "isaac,omara,orlando"
                    }
                ],
                "header": True,
                "dialect": "default"
            },
            transformer.transform('https://cdn.zapier.com/storage/files/c7005379664c3e46dd7ee44ee2af0ac7.tsv', False, 'default'))     
     
    def test_import_csv_onecolum(self):
        transformer = import_csv.UtilImportCSVTransform()
      # one colum testing
        self.assertEqual(
            {
                "csv_text": "test\n1\n2\n3\n4\n5",
                "line_items": [
                    {
                        "test": "1",
                        "": ""
                    },
                    {
                        "test": "2",
                        "": ""
                    },
                    {
                        "test": "3",
                        "": ""
                    },
                    {
                        "test": "4",
                        "": ""
                    },
                    {
                        "test": "5",
                        "": ""
                    }
                ],
                "header": "forced",
                "dialect": "one"
            },
            transformer.transform('https://cdn.zapier.com/storage/files/15df84b0ed71dcdee2588ceb5c371367_2.csv', True, 'one'))

    def test_import_csv_onecolum_noheader(self):
        transformer = import_csv.UtilImportCSVTransform()
      # one colum testing # one column, no header
        self.assertEqual(
            {
                "csv_text": "test\n1\n2\n3\n4\n5",
                "line_items": [
                    {
                        "item_1": "test",
                        "item_2": ""
                    },
                    {
                        "item_1": "1",
                        "item_2": ""
                    },
                    {
                        "item_1": "2",
                        "item_2": ""
                    },
                    {
                        "item_1": "3",
                        "item_2": ""
                    },
                    {
                        "item_1": "4",
                        "item_2": ""
                    },
                    {
                        "item_1": "5",
                        "item_2": ""
                    }
                ],
                "header": False,
                "dialect": "one"
            },
            transformer.transform('https://cdn.zapier.com/storage/files/15df84b0ed71dcdee2588ceb5c371367_2.csv', False, 'one'))


    def test_import_csv_notcsv(self):
        transformer = import_csv.UtilImportCSVTransform()
      # has csv data, but header gets in the way, so using "text" as dialect
        self.assertEqual(
            {
                "csv_text": "# ----------------------------------------\n# All Web Site Data\n# Google Ads Keywords\n# 20190930-20190930\n# ----------------------------------------\n\nKeyword,Clicks,Cost,CPC,Users,Sessions,Bounce Rate,Pages / Session,Ecommerce Conversion Rate,Transactions,Revenue\nlive chat,19,$22.50,$1.18,17,20,75.00%,0.95,0.00%,0,$0.00\nonsip,16,$114.43,$7.15,29,55,29.09%,1.16,0.00%,0,$0.00\n\nDay Index,Users\n9/30/19,58\n,58\n\n",
                "line_items": [],
                "header": "",
                "dialect": "text"
            },
            transformer.transform('https://zappy.zapier.com/csv%20not%20working%202019-10-1011%20at%2011.09.12.csv', False, 'text'))
            