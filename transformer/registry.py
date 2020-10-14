__GLOBAL_REGISTRY = {}

def register(transform):
    global __GLOBAL_REGISTRY
    name = '{}.{}'.format(transform.category, transform.name)
    if name in __GLOBAL_REGISTRY:
        raise Exception("Transform with the name {} already exists".format(name))
    __GLOBAL_REGISTRY[name] = transform

def lookup(name, category=""):
    if category:
        name = '{}.{}'.format(category, name)
    if name in __GLOBAL_REGISTRY:
        return __GLOBAL_REGISTRY[name]
    return None

def get_all(category=""):
    legacy_transforms = ["util.append","util.lineitem_to_string","string.default_value"]
    return [v for k, v in __GLOBAL_REGISTRY.iteritems() if not category or category == v.category and not k in legacy_transforms]

def make_registry():
    import transformer.transforms # NOQA
