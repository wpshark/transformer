from transformer.registry import register
from transformer.transforms.base import BaseTransform
import csv
import urllib
import tempfile

class UtilImportCSVTransform(BaseTransform):

    category = "util"
    name = "import_csv"
    label = "Import CSV File"
    # Flesh this out to describe more functions
    help_text = (
        "Import a csv file from a public URL or file field from another Zap step"
        "More on csv files [here] (https://zapier.com/help/formatter/#how-use-line-items-formatterv2)"
    )

    noun = "CSV"
    verb = "import"


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
        urllib.urlretrieve(url, response.name)
        header = csv.Sniffer().has_header(response.read(1024))
        response.seek(0)
        dialect = csv.Sniffer().sniff(response.read(1024))
        response.seek(0)

        output = {input_key: [], "header": header, "dialect": str(dialect)}
        this_line_item = []
        
        if header:
            # we have headers
            csvreader = csv.DictReader(response, dialect=dialect)
            for row in csvreader:
                this_line_item.append(row)
            output[input_key] = this_line_item
        else:
            # we don't have headers, so need some fake LI keys, but need number of fields....
            csvreader = csv.DictReader(response, dialect=dialect)
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
