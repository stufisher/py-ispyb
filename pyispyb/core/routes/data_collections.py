"""
Project: py-ispyb.

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


from flask_restx import Resource

from pyispyb.app.extensions.api import api_v1, Namespace, legacy_api
from pyispyb.app.extensions.auth.decorators import session_authorization_required, authentication_required, permission_required

from pyispyb.core.modules import data_collections


__license__ = "LGPLv3+"


api = Namespace(
    "Data collections",
    description="Data collection related namespace",
    path="/data_collections",
)
api_v1.add_namespace(api)


@api.route("/groups/session/<int:session_id>")
@legacy_api.route("/<token>/proposal/session/<session_id>/list")
@api.doc(security="apikey")
class DataColletionGroups(Resource):

    @authentication_required
    @permission_required("any", ["own_sessions", "all_sessions"])
    @session_authorization_required
    def get(self, session_id, **kwargs):
        """Get data collection groups for session.

        Args:
            session_id (str): session id
        """
        return data_collections.get_data_collections_groups(session_id)
