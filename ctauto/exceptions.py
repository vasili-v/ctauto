class CTAutoError(Exception):
    def __init__(self, **kwargs):
        super(CTAutoError, self).__init__(self.template % kwargs)

class CTAutoSourceError(CTAutoError):
    def __init__(*args, **kwargs):
        self, source = args
        self.template = "%s: %s" % (source, self.template)
        super(CTAutoSourceError, self).__init__(**kwargs)

class CTAutoMissingEndOfMetablockError(CTAutoSourceError):
    template = "missing end of metablock"
