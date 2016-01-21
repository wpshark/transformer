Comes out of trigger:

order: {

    products: [
        {'quantity': 1, 'name': 'ball'},
        {'quantity': 3, 'name': 'computer'}
    ]
}


what dev app gets:

  "data": {
      'inputs': [{'inputs_sub': 'ball'}, {'inputs_sub': 'computer'}],
  }


what transformer should get:

{
  "transform": "string.uppercase",
  "data": {
      'inputs': ['ball', 'computer'],
  }
}


what trasnformer returns:

{
  "data": {
      'inputs': ['BALL', 'COMPUTER'],
  }
}


what dev app feeds back into Zapier:

  "data": {
      'inputs': [{'inputs_sub': 'BALL'}, {'inputs_sub': 'COMPUTER'}],
  }


User Zap (Quickbooks Invoice)

node.params:
{
    'Line_items': {
        'name': {{transformer__inputs__inputs_sub}},
        'quantity': {{1__products__quantity}}
        }
}


######################## Case 2

Comes out of trigger:

contact: {
    first_name:  'brian',
    last_name: 'cooksey'
}


what dev app gets:

  "first_name": 'brian',
  'last_name': 'cooksey'

what transformer should get:

{
  "transform": "string.uppercase",
  "data": {
      'inputs': {
            "first_name": 'brian',
            'last_name': 'cooksey'
      }
  }
}


what trasnformer returns:

{
  "data": {
      'inputs': {
          "first_name": 'BRIAN',
          'last_name': 'COOKSEY'
        }
  }
}


what dev app feeds back into Zapier:

  "data": {
      'inputs': [{'inputs_sub': 'BALL'}, {'inputs_sub': 'COMPUTER'}],
  }


User Zap (Quickbooks Invoice)

node.params:
{
    'Line_items': {
        'name': {{transformer__inputs__inputs_sub}},
        'quantity': {{1__products__quantity}}
        }
}
