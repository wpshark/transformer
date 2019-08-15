from transformer.registry import register
from transformer.transforms.base import BaseTransform
import csv
import urllib
import tempfile

#Approximate size of a 1000 line CSV with 14 columns, some text in each
#This takes ~3-5 seconds to turn into line-items in Zapier
#So not arbitrary, but I'm sure it could be tweaked
MAX_CSV_FILE_SIZE = 150000

class UtilLookupCSVTransform(BaseTransform):

    category = 'util'
    name = 'lookup_csv'
    label = 'Lookup Table CSV'
    help_text = 'Given a key, and a CSV file with key and value columns - find the matching value.'

    noun = 'Value'
    verb = 'lookup'

    def build_input_field(self):
        return {
            'type': 'unicode',
            'required': True,
            'key': 'inputs',
            'label': 'Lookup Key',
            'help_text': '{} you would like to {}.'.format(self.noun or 'Value', self.verb or 'transform')
        }

    def transform(self, input_key, csv_url, column_key=0,column_value=1,fallback=u'', **kwargs):

        output = {"key": input_key, "value": "", "key_found": False}
        if not csv_url:
            output["value"] = fallback
            return output

        # create a temp file, then load the csv into it
        # new delete attribute, let's verify if it works
        response = tempfile.NamedTemporaryFile(delete=True)
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

        # output the found key, or the fallback
        table = {}
        csv_reader = csv.reader(response, dialect=dialect)
        if header:
            # we have headers, ignore them!
            header_row = csv_reader.next()
        for row in csv_reader:
            if row[int(column_key)] == input_key:
                output["key_found"] = True
                output["value"] = row[int(column_value)]
                response.close()
                return output
        # if we go through whole file sans finding a row, output fallback
        response.close()
        return fallback


    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'file',
                'required': False,
                'key': 'csv_url',
                'label': 'CSV File',
                'help_text': (
                    "Import a CSV file from entred text, a public URL or a File field from another Zap step. "
                    "Limited to 150k.  "
                )
            },
            {
                'type': 'integer',
                'required': False,
                'key': 'column_key',
                'label': 'Column for Key',
                'help_text': 'Column in CSV file used for key (defaults to 1st column).'
            },
            {
                'type': 'integer',
                'required': False,
                'key': 'column_value',
                'label': 'Column for Value',
                'help_text': 'Column in CSV file used for value (defaults to 2nd column).'
            },
            {
                'type': 'unicode',
                'required': False,
                'key': 'fallback',
                'label': 'Fallback Value',
                'help_text': 'The value to be used if we do not find a matching value in Lookup Table.'
            }
        ]

register(UtilLookupCSVTransform())
