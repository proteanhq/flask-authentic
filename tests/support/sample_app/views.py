""" Views of the sample app"""
from protean_flask.core.viewsets import GenericAPIResourceSet

from flask_authentic.decorators import authenticated_viewset

from .schemas import HumanSchema
from .serializers import HumanSerializer


class HumanResourceSet(GenericAPIResourceSet):
    """ Resource Set for the Human Entity"""
    schema_cls = HumanSchema
    serializer_cls = HumanSerializer
    decorators = [authenticated_viewset()]
