class NotFound(Exception):
    def __init__(self, template='404.html'):
        self.template = template


class Forbidden(Exception):
    def __init__(self, template='403.html'):
        self.template = template


class NotModified(Exception):
    pass


class Redirect(Exception):
    def __init__(self, path):
        self.path = path


class BadRequest(Exception):
    pass