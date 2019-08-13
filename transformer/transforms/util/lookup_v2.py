from transformer.registry import register
from transformer.transforms.base import BaseTransform
import csv
import urllib
import tempfile

#Approximate size of a 1000 line CSV with 14 columns, some text in each
#This takes ~3-5 seconds to turn into line-items in Zapier
#So not arbitrary, but I'm sure it could be tweaked
MAX_CSV_FILE_SIZE = 150000

class UtilLookupV2Transform(BaseTransform):

    category = 'util'
    name = 'lookup_v2'
    label = 'Lookup Table V2'
    help_text = 'Given a key, and a CSV file with key and value table - find the matching value.'

    noun = 'Value'
    verb = 'lookup'

    def build_input_field(self):
        return {
            'type': 'unicode',
            'required': False,
            'key': 'inputs',
            'label': 'Lookup Key',
            'help_text': '{} you would like to {}.'.format(self.noun or 'Value', self.verb or 'transform')
        }

    def transform(self, input_key, csv_url, column_key=0,column_value=1,fallback=u'', **kwargs):

        if not csv_url:
            return u''

        # create a temp file, then load the csv into it
        response = tempfile.NamedTemporaryFile()
        response.seek(0)
        urllib.urlretrieve(csv_url, response.name)

        #check file size
        response.seek(0, 2)
        size = response.tell()
        if (size > MAX_CSV_FILE_SIZE):
            self.raise_exception('CSV File must be < 150K.')

        # use csv utils to see if there is a dialect, if the file is malformed in anyway, this will fail and report that error to the user
        response.seek(0)
        dialect = csv.Sniffer().sniff(response.read())
        response.seek(0)
        header = csv.Sniffer().has_header(response.read())
        response.seek(0)

        output = {"key": input_key, "value": "","table": ""}
        # output line-items
        table = {}
        csv_reader = csv.reader(response, dialect=dialect)
        if header:
            # we have headers
            header_row = csv_reader.next()
        for row in csv_reader:
            table[row[int(column_key)]] = row[int(column_value)]
        response.seek(0)
        # additonal hack here for one column
        output["table"] = response.read()
        response.close()
        if input_key and input_key in table:
            output["value"] = table[input_key]
            return output
        return fallback


    def fields(self, *args, **kwargs):
        return [
            #{
                #'type': 'password',
                #'required': False,
                #'key': 'storage_key',
                #'label': 'Storage Key',
                #'help_text': 'Key (password) used to store and retrieve table entries in Zapier Storage.',
            #},
            {
                'type': 'file',
                'required': False,
                'key': 'csv_url',
                'label': 'CSV File',
                'help_text': (
                    "Import a CSV file from a public URL, File field from another Zap step, or entered text.  "
                    "Limited to 150k.  "
                )
            },
            {
                'type': 'integer',
                'required': False,
                'key': 'column_key',
                'label': 'Column for Key',
                'help_text': 'Column in csv used for key (Defaults to 1st column).'
            },
            {
                'type': 'integer',
                'required': False,
                'key': 'column_value',
                'label': 'Column for Value',
                'help_text': 'Column in csv used for value (defaults to 2nd column).'
            },
            {
                'type': 'unicode',
                'required': False,
                'key': 'fallback',
                'label': 'Fallback Value',
                'help_text': 'The value to be used if we do not find a matching value in Lookup Table.'
            }
        ]

register(UtilLookupV2Transform())
