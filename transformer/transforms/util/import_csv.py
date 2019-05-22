from transformer.registry import register
from transformer.transforms.base import BaseTransform
import csv
import urllib
import tempfile

#Approximate size of a 1000 line CSV with 14 columns, some text in each
#This takes ~3-5 seconds to turn into line-items in Zapier
#So not arbitrary, but I'm sure it could be tweaked
MAX_CSV_FILE_SIZE = 150000

class UtilImportCSVTransform(BaseTransform):

    category = "util"
    name = "import_csv"
    label = "Import CSV File"
    help_text = (
        "Import a CSV file from a public URL, File field from another Zap step, or entered text.  "
        "Limited to 150k (around 1000 rows).  "
        "Output is a line-item field for each column, and a text field with CSV file contents.  "
        "More on importing csv files [here.](https://zapier.com/help/formatter/#how-import-csv-files-formatter)"
    )

    noun = "CSV"
    verb = "import"

    def build_input_field(self):
        return {
            "type": "file",
            "required": True,
            "key": "inputs",
            "label": "CSV File",
        }

    def transform(self, csv_url, forced_header, **kwargs):
        # Take a file input and output a set of line-item fields and a big string field
        # note use of temp file and lots of seek(0). This was required as Python file-type objects
        # don't support resetting the iterator back to 0.

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
            self.raise_exception('CSV Import only supports file sizes < 150K.')

        # use csv utils to see if there is a dialect, if the file is malformed in anyway, this will fail and report that error to the user
        response.seek(0)
        dialect = csv.Sniffer().sniff(response.read())
        response.seek(0)
        header = csv.Sniffer().has_header(response.read())

        response.seek(0)

        output = {"line_items": [],"csv_text": "", "header": header}
        # output line-items
        this_line_item = []
        if header:
            # we have headers
            csv_reader = csv.DictReader(response, dialect=dialect)
            for row in csv_reader:
                this_line_item.append(row)
            output["line_items"] = this_line_item
        else:
            # we don't have headers, so need some line-item labels, but first need number of fields, so grab the first row....
            header_reader = csv.reader(response, dialect=dialect)
            row_1 = header_reader.next()
            if forced_header:
                # user says that the first row is a header row, lets hope it has everything we need
                field_names = list(s.format(i + 1) for i, s in enumerate(row_1))
                output["header"] = 'forced'
            else:
                # user says that the first row is not a header row, create field names item_1...item_n which become the line-item labels
                field_names = list('item_{}'.format(i + 1) for i, s in enumerate(row_1))
                response.seek(0)
            csvreader = csv.DictReader(response, fieldnames=field_names, dialect=dialect)
            for row in csvreader:
                this_line_item.append(row)
            output["line_items"] = this_line_item

        #also output a big string of the csv contents
        response.seek(0)
        output["csv_text"] = response.read()

        response.close()
        return output


    def fields(self, *args, **kwargs):
        return [
            {
                'type': 'bool',
                'required': False,
                'key': 'forced_header',
                'label': 'Force First Row as Header Row',
                "default": "no",
                'help_text': (
                    'By default, Import CSV file will try to determine if your file has a header row. '
                    'If you find in your test step that this magic did not work (header will be false), you can force it here by selecting yes.'
                ),  # NOQA
            },
        ]

register(UtilImportCSVTransform())
