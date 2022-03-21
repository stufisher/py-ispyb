from flask import request
from pyispyb.app.extensions.api import api_v1, Namespace
from pyispyb.app.extensions.auth.decorators import (
    authentication_required,
)
from pyispyb.core.schemas import sample as sample_schema

from ..modules import samples as crud

from .base import Resource

from flask_restx import reqparse
from flask_restx._http import HTTPStatus

from ..schema import paginated, error_model


parser = reqparse.RequestParser()
parser.add_argument("skip", type=int, help="Number of results to skip", default=0)
parser.add_argument("limit", type=int, help="Number of results to show", default=10)
parser.add_argument("proteinId", type=int, help="Protein id to filter by")


api = Namespace(
    "Samples",
    description="Samples namespace",
    path="/samples",
)


class Samples(Resource):
    @api.expect(parser)
    @api.marshal_with(paginated(sample_schema.f_schema), code=HTTPStatus.OK)
    def get(self):
        """Get available samples."""
        print("user", request.user)
        args = parser.parse_args()
        samples = crud.get_samples(
            args.skip,
            args.limit,
            proteinId=args.proteinId,
        )
        return samples, 200


class Sample(Resource):
    @api.marshal_with(paginated(sample_schema.f_schema), code=HTTPStatus.OK)
    @api.response(404, "No such sample", error_model)
    def get(self, blSampleId: int):
        """Get a single sample."""
        samples = crud.get_samples(
            0, 10, personId=request.user.personId, blSampleId=blSampleId
        )
        try:
            return samples.first, 200
        except IndexError:
            return {"message": "No such sample"}, 404


def register_class(route_class: Resource, api: Namespace, path: str):
    """Automatically decorate class

    Automatically applies:
        * security
        * doc string from __doc__
        ...
    """
    print("register", route_class)
    for k in ["post", "get", "put", "patch", "delete"]:
        fn = getattr(route_class, k, None)
        if fn:
            fn = authentication_required(fn)
            fn = api.doc(description=fn.__doc__)(fn)
            fn = api.doc(security="apikey")(fn)

            setattr(route_class, k, fn)

    api.route(path)(route_class)


def register(app):
    """Importing files should not cause side effects
    Explitly register the name space instead
    """
    api_v1.add_namespace(api)
    register_class(Samples, api, "")
    register_class(Sample, api, "/<int:blSampleId>")
