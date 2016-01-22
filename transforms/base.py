class BaseTransform:
    category = ''
    name = ''

    @property
    def key(self):
        return '{}.{}'.format(self.category, self.name)

    def transform(self, *args, **kwargs):
        raise Exception('Must implement transform method')

    def fields(self, *args, **kwargs):
        return []

    def _fields_internal(self, *args, **kwargs):
        return [
            # up to dev app to do the parent_key hack
            {
                'type': 'unicode',
                'list': True,
                'required': True,
                'key': 'inputs',
            }
        ] + self.fields(*args, **kwargs)
