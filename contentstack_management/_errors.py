class ArgumentException(Exception):

    pass
    def __init__(self, f, *args):
        super().__init__(args)
        self.f = f

    def __str__(self):
        return self.f

