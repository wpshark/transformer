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
        "When you do your Test Step, you'll only see the first 50 rows of your CSV file, but when your Zap runs all rows will be processed. "
        "More on importing CSV files [here.](https://zapier.com/help/create/format/import-csv-files-into-zaps)"
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


    def transform(self, csv_url, forced_header, forced_dialect='default', **kwargs):
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
            self.raise_exception('Import CSV File only supports file sizes < 150K.')

        # use csv utils to see if there is a dialect, if the file is malformed in anyway, this will fail and report that error to the user
        response.seek(0)
        if forced_dialect == 'one':
            #Python CSV Parser can't deal with a one column csv, so create a new file
            #with a comma delimeter
            csv.register_dialect('one',delimiter=',')
            one_column_file = response
            new_file = tempfile.TemporaryFile()
            for line in response:
                new_file.write(line.splitlines()[0] + "," + "\n")
            response = new_file
            response.seek(0)
        dialect = csv.Sniffer().sniff(response.read())
        response.seek(0)
        # these two are not standard dialects, so create them
        csv.register_dialect('comma',delimiter=',')
        csv.register_dialect('semicolon',delimiter=';')
        if forced_dialect != 'default':
            #user has selected a forced dialect, so assign that
            dialect = csv.get_dialect(forced_dialect)
        header = csv.Sniffer().has_header(response.read())
        response.seek(0)

        output = {"line_items": [],"csv_text": "", "header": header, "dialect": forced_dialect}
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
            # need to set up an exception for 1 column CSVs
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
        # additonal hack here for one column
        if forced_dialect == "one":
            one_column_file.seek(0)
            output["csv_text"] = one_column_file.read()
            one_column_file.close()
        else:
            output["csv_text"] = response.read()
        response.close()
        return output


    def fields(self, *args, **kwargs):
        return [
            {
                "type": "bool",
                "required": False,
                "key": "forced_header",
                "label": "Force First Row as Header Row",
                "default": "no",
                "help_text": (
                    "By default, Import CSV File will try to determine if your file has a header row. "
                    "If you find in your Test Step that this did not work (the header field will be False), you can force it here by selecting yes."
                ),  # NOQA
            },
            {
                "type": "unicode",
                "required": False,
                "key":  "forced_dialect",
                "choices": "default|Detect Automatically,comma|Comma Delimited,semicolon|Semicolon Delimited,excel|Excel Comma Delimited,excel-tab|Excel Tab Delimited,one|One Column",
                "label": "Type of CSV File",
                "default": "default",
                "help_text": (
                    "By default, Import CSV File will try to detect the type of your file. "
                    "If you find in your Test Step that your file was not recognized correctly, you can force it here by selecting your file type."
                ),  # NOQA
            },
        ]

register(UtilImportCSVTransform())
