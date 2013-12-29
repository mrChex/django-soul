def render_to(template=None):
    def renderer(function):
        def wrapper(self, request, *args, **kwargs):
            print "test"

        return wrapper
    return renderer