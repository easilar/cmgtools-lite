class NanoObject(object):
    '''Wrapper around a nano aod object'''

    not_implemented = set()

    def __init__(self, nano_obj):
        self.nano_obj = nano_obj

    def __getattr__(self, attr): 
        if not attr in self.__dict__:
            if hasattr(self.nano_obj, attr):
                def get_value():
                    return getattr(self.nano_obj, attr)
                return get_value
            else:
                print('not implemented',attr)
                self.__class__.not_implemented.add(attr)
                return self.dummy_value

    def dummy_value(self, *args, **kwargs):
        return -123



