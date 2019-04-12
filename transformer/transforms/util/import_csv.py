from transformer.registry import register
from transformer.transforms.base import BaseTransform
import csv
import urllib
import tempfile

#Approximate size of a 1000 line CSV with 14 columns, some tezt in each
#This takes ~3-5 seconds to turn into line-items in Zapier, and is still workable in the editor
#So not arbitrary, but I'm sure it could be tweaked
MAX_CSV_FILE_SIZE = 150000

class UtilImportCSVTransform(BaseTransform):

    category = "util"
    name = "import_csv"
    label = "Import CSV File"
    help_text = (
        "Import a csv file from a public URL, File field from another Zap step, or entered text. "
        "Limited to 150k/1000 rows. "
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

    def transform(self, csv_url, line_items=None, **kwargs):
        # Take a file input and output a set of line-item fields, or a big string field

        if not csv_url:
            return u''

        if line_items is None:
            li_output = True
        else:
            li_output = line_items

        # create a temp file, then load the csv into it
        url = csv_url
        response = tempfile.NamedTemporaryFile()
        response.seek(0)
        urllib.urlretrieve(url, response.name)

        #check file size
        response.seek(0, 2)
        size = response.tell()
        if (size > MAX_CSV_FILE_SIZE):
            self.raise_exception('CSV Import only supports file sizes < 150K.')

        # use csv utils to see if there is a header, and get the dialect (format) of the csv
        response.seek(0)
        header = csv.Sniffer().has_header(response.read())
        response.seek(0)
        dialect = csv.Sniffer().sniff(response.read())
        response.seek(0)

        if li_output:
            # output line-items
            input_key = "Line-item(s)"
            if header:
            # we have headers
                output = {input_key: [], "header": header, "line item output": li_output}
                this_line_item = []
                csvreader = csv.DictReader(response, dialect=dialect)
                for row in csvreader:
                    this_line_item.append(row)
                output[input_key] = this_line_item
            else:
                # we don't have headers, so need some fake LI keys, but first need number of fields, so grab the first row....
                headerreader = csv.reader(response, dialect=dialect)
                row1 = headerreader.next()
                fieldnames = { 'Item {}'.format(i + 1): s for i, s in enumerate(row1)}
                # now we have field names as Item 1..n - lets hope row #1 has everything it needs
                response.seek(0)
                csvreader = csv.DictReader(response, fieldnames=fieldnames, dialect=dialect)
                for row in csvreader:
                    this_line_item.append(row)
                output[input_key] = this_line_item

        else:
            #output is a big string
            input_key = "CSV Text"
            output = {input_key: "", "header": header,"line item output": li_output}
            output[input_key] = response.read()

        response.close()
        return output

    def fields(self, *args, **kwargs):
        return [
            {
                "type": "boolean",
                "required": False,
                "key": "line_items",
                "label": "Line-items",
                "help_text": "By default, the csv file will be imported into line-item fields. Select No to import into a text field instead."
            }

        ]
register(UtilImportCSVTransform())
