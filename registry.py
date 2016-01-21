__GLOBAL_REGISTRY = {}

def register(name, transform):
    global __GLOBAL_REGISTRY
    if name in __GLOBAL_REGISTRY:
        raise Exception("Transform with the name {} already exists".format(name))
    __GLOBAL_REGISTRY[name] = transform
    print __GLOBAL_REGISTRY

def lookup(name):
    if name in __GLOBAL_REGISTRY:
        return __GLOBAL_REGISTRY[name]
    return None

def getall(category=""):
    return [k for k in __GLOBAL_REGISTRY if not category or k.startswith(category)]

def make_registry():
    from transforms import string # NOQA
