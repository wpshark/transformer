from transformer.registry import register
from transformer.transforms.base import BaseTransform
import csv
import urllib2

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

    def transform(self, csv_url, line_items=true, **kwargs):
        # Take a file input and output a set of line-item fields, or a big string field

        if not csv_url:
            return u''

        input_key = "Line-item(s)"
        url = csv_url
        response1 = urllib2.urlopen(url)
        response2 = urllib2.urlopen(url)
        response3 = urllib2.urlopen(url)
        header = csv.Sniffer().has_header(response2.read(1024))
        dialect = csv.Sniffer().sniff(response3.read(1024))
        this_line_item = []
        csvreader = csv.DictReader(response1, dialect=dialect)
        for row in csvreader:
            this_line_item.append(row)
        return {input_key: this_line_item}

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
