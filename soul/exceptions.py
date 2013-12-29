class NotFound(Exception):
    pass


class Forbidden(Exception):
    pass


class NotModified(Exception):
    pass


class Redirect(Exception):
    def __init__(self, path):
        self.path = path