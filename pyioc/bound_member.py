from inspect import signature


class BoundMember:
    def __init__(self, annotation, implementation, scope):
        params = signature(implementation).parameters
        self.annotation = annotation
        self.annotation = annotation
        self.implementation = implementation
        self.scope = scope
        self.parameters = [params[p].annotation for p in params]
        self.depends_on = []


