# Transformer (by Zapier)

Transformer is a little web app that performs data transformations. You specify one of the pre-defined transforms to run, along with some input data, and the app will run the data through the transform and return the output.

## Usage

`GET /` - Lists all the available transforms

`GET /?category=<category_name>` - Lists transforms in a category. Category can be one of: date, number, string, util

`GET /fields?transform=<transform_name>` - Tells you required data for the given transform. `transform_name` should be a key from the `/` endpoint

`POST /transform` - Run a transform. The request body will look something like this:

```json
{
  "transform": "string.upper_case",
  "inputs": ["abc"],
}
```

## Setup

```
docker-compose build
```

## Run Locally

```
docker-compose up -d
```

## Test Locally

```
./run_tests.sh
```

## Contributing

If you have a transform that you think would be useful, fork the repo, add the transform, and then make a pull request. To get started, check out the [base class](https://github.com/zapier/transformer/blob/master/transformer/transforms/base.py) for the interface and the [trim space](https://github.com/zapier/transformer/blob/master/transformer/transforms/string/trim_space.py) transform an example.

When making changes, here are some style considerations to keep in mind:

 * We follow a modified version of PEP8. Essentially, keep your code looking like the rest of the codebase and you'll be fine
 * When naming a transform, separate the file name by words. i.e. "Trim space" lives in "trim_space.py"
