
class Stub:

    def __init__(self):
        self.calls = []

    def _add_call(self, name, *args, **kwargs):
        self.calls.append((name, args, kwargs))
