""" Entities used by the sample application """
from protean.core.entity import Entity
from protean.core import field


class Human(Entity):
    """ This is a dummy Human class """
    id = field.Integer(identifier=True)
    name = field.String(required=True, max_length=50)
    contact = field.StringMedium()
