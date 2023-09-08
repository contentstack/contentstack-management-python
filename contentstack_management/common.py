class Parameter(object):
    def __init__(self, client):
        self.client = client
        self.params = {}

    def add_param(self, key, value):
        self.params[key] = value

    def add_header_dict(self, headers):
        self.client.headers.update(headers)

    def add_header(self, key, value):
        self.client.headers[key] = value

    def add_param_dict(self, parameters):
        self.params.update(parameters)
