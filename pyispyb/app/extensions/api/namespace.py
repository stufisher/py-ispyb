"""Project: py-ispyb.

https://github.com/ispyb/py-ispyb

This file is part of py-ispyb software.

py-ispyb is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

py-ispyb is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with py-ispyb. If not, see <http://www.gnu.org/licenses/>.
"""


__license__ = "LGPLv3+"


from functools import wraps
import logging

# import flask_marshmallow

from flask_restx import Namespace as BaseNamespace

from .webargs_parser import CustomWebargsParser


log = logging.getLogger(__name__)


class Namespace(BaseNamespace):
    """Having app-specific handlers here."""

    WEBARGS_PARSER = CustomWebargsParser()

    def resolve_object(self, object_arg_name, resolver):
        """
        Resolve object instance from arguments e.g. identity.

        Example:
        >>> @namespace.route('/<int:user_id>')
        ... class MyResource(Resource):
        ...    @namespace.resolve_object(
        ...        object_arg_name='user',
        ...        resolver=lambda kwargs: User.query.get_or_404(kwargs.pop('user_id'))
        ...    )
        ...    def get(self, user):
        ...        # user is a User instance here
        """

        def decorator(func_or_class):
            if isinstance(func_or_class, type):
                # Handle Resource classes decoration
                # pylint: disable=protected-access
                func_or_class._apply_decorator_to_methods(decorator)
                return func_or_class

            @wraps(func_or_class)
            def wrapper(*args, **kwargs):
                kwargs[object_arg_name] = resolver(kwargs)
                return func_or_class(*args, **kwargs)

            return wrapper

        return decorator

    def model(self, name=None, model=None, **kwargs):
        """Register a model aka schema / definition."""
        # if isinstance(model, flask_marshmallow.Schema) and not name:
        #     name = model.__class__.__name__
        #     if name.endswith("Schema"):
        #         name = name[: -len("Schema")]
        return super(Namespace, self).model(name=name, model=model, **kwargs)

    def marshal(self, *, input=None, output=None, responses=None):
        pass
