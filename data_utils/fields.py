
class Field:
    """ This is supposed to be used as a field (attribute) in a dataclass. It
    provides type validation out of the box and accepts a default value and
    extra validators.
    """
    def __init__(self, type, validators=(), default=None):
        self.type = type
        self.validators = validators
        self.default = default

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if not instance:
            return self
        return instance.__dict__[self.name]

    def __delete__(self, instance):
        del instance.__dict__[self.name]

    def __set__(self, instance, value):
        if self.default is not None:
            if self.name not in instance.__dict__ and value is self:
                value = self.default
        if not isinstance(value, self.type):
            raise TypeError(f"{self.name!r} must be of type {self.type!r}")
        for validator in self.validators:
            validator(self.name, value)
        instance.__dict__[self.name] = value
