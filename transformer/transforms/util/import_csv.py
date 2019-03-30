from transformer.registry import register
from transformer.transforms.base import BaseTransform
import csv
import urllib
import tempfile
import os

MAX_CSV_FILE_SIZE = 25e6

class UtilImportCSVTransform(BaseTransform):

    category = "util"
    name = "import_csv"
    label = "Import CSV File"
    # Flesh this out to describe more functions
    help_text = (
        "Import a csv file from a public URL, File field from another Zap step, or entered text. "
        "Limited to 500k/1000 rows "
        "More on using csv files [here] (https://zapier.com/help/formatter/#how-process-csvs-formatter)"
    )

    noun = "CSV"
    verb = "import"

    def build_input_field(self):
        return {
            "type": "file",
            "required": True,
            "key": "inputs",
            "label": "CSV file",
        }

    def transform(self, csv_url, options=None, **kwargs):
        # Take a file input and output a set of line-item fields, or a big string field

        if not csv_url:
            return u''

        if options is None:
            options = {}
        else:
            string_output = options.get('line_items')

        input_key = "Line-item(s)"
        url = csv_url
        response = tempfile.NamedTemporaryFile()

        response.seek(0)
        urllib.urlretrieve(url, response.name)

        #check size
        response.seek(0, 2)
        size = response.tell()
        size_in_K = size / 1000

        response.seek(0)
        header = csv.Sniffer().has_header(response.read())
        response.seek(0)
        dialect = csv.Sniffer().sniff(response.read())
        response.seek(0)

        output = {input_key: [], "header": header, "size": size_in_K}
        this_line_item = []

        if header:
            # we have headers
            csvreader = csv.DictReader(response, dialect=dialect)
            for row in csvreader:
                this_line_item.append(row)
            output[input_key] = this_line_item
        else:
            # we don't have headers, so need some fake LI keys, but need number of fields....
            headerreader = csv.reader(response, dialect=dialect)
            row1 = headerreader.next()
            fieldnames = { 'Item {}'.format(i + 1): s for i, s in enumerate(row1)}
            # now we have field names as Item 1..n - lets hope row #1 has everything it needs
            response.seek(0)
            csvreader = csv.DictReader(response, fieldnames=fieldnames, dialect=dialect)
            for row in csvreader:
                this_line_item.append(row)
            output[input_key] = this_line_item
        response.close()
        return output

    def fields(self, *args, **kwargs):
        return [
            {
                "type": "boolean",
                "required": False,
                "key": "line_items",
                "label": "Line-items",
                "help_text": "By default, the csv will be imported into line-item fields. Select No to import into a text field instead."
            }
        ]
register(UtilImportCSVTransform())
