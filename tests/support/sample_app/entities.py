""" Entities used by the sample application """
from protean.core import field
from protean.core.entity import Entity


class Human(Entity):
    """ This is a dummy Human class """
    id = field.Integer(identifier=True)
    name = field.String(required=True, max_length=50)
    contact = field.StringMedium()
