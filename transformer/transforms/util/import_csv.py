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
        "Import a CSV file from a public URL, File field from another Zap step, or entered text. "
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

    def transform(self, csv_url, **kwargs):
        # Take a file input and output a set of line-item fields, or a big string field

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

        # use csv utils to see if there is a dialect, if the file is malformed in anyway, this will fail
        response.seek(0)
        #try:
        dialect = csv.Sniffer().sniff(response.read())
        #except:
            #self.raise_exception('This CSV file has a format that Formatter does not understand')
        # worked, so let's look for a header
        response.seek(0)
        header = csv.Sniffer().has_header(response.read())

        response.seek(0)

        output = {"Line-item(s)": [],"CSV text": "", "Header": header}
        # output line-items
        this_line_item = []
        if header:
            # we have headers
            csv_reader = csv.DictReader(response, dialect=dialect)
            for row in csv_reader:
                this_line_item.append(row)
            output["Line-item(s)"] = this_line_item
        else:
                # we don't have headers, so need some fake LI keys, but first need number of fields, so grab the first row....
            header_reader = csv.reader(response, dialect=dialect)
            row_1 = header_reader.next()
            field_names = { 'Item {}'.format(i + 1): s for i, s in enumerate(row_1)}
            # now we have field names as Item 1..n - lets hope row #1 has everything it needs
            response.seek(0)
            csvreader = csv.DictReader(response, fieldnames=field_names, dialect=dialect)
            for row in csvreader:
                this_line_item.append(row)
            output["Line-item(s)"] = this_line_item

        #also output a big string of the csv contents
        response.seek(0)
        output["CSV text"] = response.read()

        response.close()
        return output

register(UtilImportCSVTransform())
