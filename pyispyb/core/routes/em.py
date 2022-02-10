
__license__ = "LGPLv3+"


import os
from pyispyb.core.modules.proposal import find_proposal_id
from flask_restx import Resource

from pyispyb.app.extensions.api import api_v1, Namespace, http_exceptions, legacy_api
from pyispyb.app.extensions.auth.decorators import proposal_authorization_required, authentication_required, permission_required, session_authorization_required
from pyispyb.core.modules import em
from flask import send_file


api = Namespace(
    "EM", description="EM related namespace", path="/em"
)

api_v1.add_namespace(api)

############################
#          MOVIES          #
############################


@api.route("/proposal/<int:proposal_id>/datacollection/<int:datacollection_id>/movies")
@legacy_api.route("/<token>/proposal/<proposal_id>/em/datacollection/<datacollection_id>/movie/all")
@api.doc(security="apikey")
class Movies(Resource):

    @authentication_required
    @permission_required("any", ["own_proposal", "all_proposals"])
    @proposal_authorization_required
    def get(self, proposal_id, datacollection_id, **kwargs):
        """Get movies date for datacollection.

        Args:
            proposal_id (str): proposal id or name
            datacollection_id (str): data collection id
        """
        proposal_id = find_proposal_id(proposal_id)
        return em.get_movies_data_by_datacollection_id(
            proposal_id, datacollection_id)


@api.route("/proposal/<int:proposal_id>/movie/<int:movie_id>/thumbnail")
@legacy_api.route("/<token>/proposal/<proposal_id>/em/datacollection/<datacollection_id>/movie/<movie_id>/thumbnail")
@api.doc(security="apikey")
class MovieThumbnail(Resource):

    @authentication_required
    @permission_required("any", ["own_proposal", "all_proposals"])
    @proposal_authorization_required
    def get(self, proposal_id, movie_id, **kwargs):
        """Get thumbnails for movie.

        Args:
            proposal_id (str): proposal id or name
            movie_id (str): movie id
        """
        proposal_id = find_proposal_id(proposal_id)
        path = em.get_movie_thumbnails(proposal_id, movie_id)
        if path and "movie_thumbnail" in path:
            path = path["movie_thumbnail"]
        if path and os.path.isfile(path):
            return send_file(path, mimetype='image/png')
        else:
            http_exceptions.abort(404, "no image found.")


@api.route("/proposal/<int:proposal_id>/movie/<int:movie_id>/thumbnail/motioncorrection")
@legacy_api.route("/<token>/proposal/<proposal_id>/em/datacollection/<datacollection_id>/movie/<movie_id>/motioncorrection/thumbnail")
@api.doc(security="apikey")
class MovieMotionCorrectionThumbnail(Resource):

    @authentication_required
    @permission_required("any", ["own_proposal", "all_proposals"])
    @proposal_authorization_required
    def get(self, proposal_id, movie_id, **kwargs):
        """Get motion correction thumbnail for movie.

        Args:
            proposal_id (str): proposal id or name
            movie_id (str): movie id
        """
        proposal_id = find_proposal_id(proposal_id)
        path = em.get_movie_thumbnails(proposal_id, movie_id)
        if path and "motion_correction_thumbnail" in path:
            path = path["motion_correction_thumbnail"]
        if path and os.path.isfile(path):
            return send_file(path, mimetype='image/png')
        else:
            http_exceptions.abort(404, "no image found.")


@api.route("/proposal/<int:proposal_id>/movie/<int:movie_id>/thumbnail/ctf")
@legacy_api.route("/<token>/proposal/<proposal_id>/em/datacollection/<datacollection_id>/movie/<movie_id>/ctf/thumbnail")
@api.doc(security="apikey")
class MovieCTFThumbnail(Resource):

    @authentication_required
    @permission_required("any", ["own_proposal", "all_proposals"])
    @proposal_authorization_required
    def get(self, proposal_id, movie_id, **kwargs):
        """Get CTF thumbnail for movie.

        Args:
            proposal_id (str): proposal id or name
            movie_id (str): movie id
        """
        proposal_id = find_proposal_id(proposal_id)
        path = em.get_movie_thumbnails(proposal_id, movie_id)
        if path and "ctf_thumbnail" in path:
            path = path["ctf_thumbnail"]
        if path and os.path.isfile(path):
            return send_file(path, mimetype='image/png')
        else:
            http_exceptions.abort(404, "no image found.")


@api.route("/proposal/<int:proposal_id>/movie/<int:movie_id>/plot/motioncorrectiondrift")
@legacy_api.route("/<token>/proposal/<proposal_id>/em/datacollection/<datacollection_id>/movie/<movie_id>/motioncorrection/drift")
@api.doc(security="apikey")
class MovieMotionCorrectionDrift(Resource):

    @authentication_required
    @permission_required("any", ["own_proposal", "all_proposals"])
    @proposal_authorization_required
    def get(self, proposal_id, movie_id, **kwargs):
        """Get motion correction drift thumbnail for movie.

        Args:
            proposal_id (str): proposal id or name
            movie_id (str): movie id
        """
        proposal_id = find_proposal_id(proposal_id)
        path = em.get_movie_thumbnails(proposal_id, movie_id)
        if path and "motion_correction_drift" in path:
            path = path["motion_correction_drift"]
        if path and os.path.isfile(path):
            return send_file(path, mimetype='image/png')
        else:
            http_exceptions.abort(404, "no image found.")

############################
#          STATS           #
############################


@api.route("/session/<int:session_id>/stats")
@legacy_api.route("/<token>/proposal/<proposal>/em/session/<session_id>/stats")
@api.doc(security="apikey")
class StatsSession(Resource):

    @authentication_required
    @permission_required("any", ["own_sessions", "all_sessions"])
    @session_authorization_required
    def get(self, session_id, **kwargs):
        """Get stats for session.

        Args:
            session_id (str): session id
        """
        return em.get_stats_by_session_id(session_id)


@api.route("/proposal/<int:proposal_id>/data_collections/<string:data_collections_ids>/stats")
@api.doc(security="apikey")
class StatsDataCollectionIds(Resource):

    @authentication_required
    @permission_required("any", ["own_proposal", "all_proposals"])
    @proposal_authorization_required
    def get(self, proposal_id, data_collections_ids):
        """Get stats for data collection ids.

        Args:
            proposal_id (str): proposal id or name
            data_collections_ids (str): comma-separated datacollection ids
        """
        proposal_id = find_proposal_id(proposal_id)
        return em.get_stats_by_data_collections_ids(
            proposal_id, data_collections_ids)


@api.route("/proposal/<int:proposal_id>/data_collections_group/<string:data_collections_group_id>/stats")
@api.doc(security="apikey")
class StatsDataCollectionGroupId(Resource):

    @authentication_required
    @permission_required("any", ["own_proposal", "all_proposals"])
    @proposal_authorization_required
    def get(self, proposal_id, data_collections_group_id, **kwargs):
        """Get stats for datacollection group.

        Args:
            proposal_id (str): proposal id or name
            data_collections_group_id (str): data collection group id
        """
        proposal_id = find_proposal_id(proposal_id)
        return em.get_stats_by_data_collections_group_id(
            proposal_id, data_collections_group_id)

############################
#     DATA COLLECTION      #
############################


@api.route("/proposal/<int:proposal_id>/session/<int:session_id>/data_collections/groups")
@legacy_api.route("/<token>/proposal/<proposal_id>/em/datacollection/session/<session_id>/list")
@api.doc(security="apikey")
class DataCollectionGroup(Resource):

    @authentication_required
    @permission_required("any", ["own_proposal", "all_proposals"])
    @permission_required("any", ["own_sessions", "all_sessions"])
    @proposal_authorization_required
    @session_authorization_required
    def get(self, proposal_id, session_id, **kwargs):
        """Get datacollection groups for session.

        Args:
            proposal_id (str): proposal id or name
            session_id (str): session id
        """
        proposal_id = find_proposal_id(proposal_id)
        return em.get_data_collections_groups(proposal_id, session_id)

############################
#     CLASSIFICATION       #
############################


@api.route("/session/<int:session_id>/classification")
@legacy_api.route("/<token>/proposal/<proposal_id>/em/session/<int:session_id>/classification")
@api.doc(security="apikey")
class ClassificationSession(Resource):

    @authentication_required
    @permission_required("any", ["own_sessions", "all_sessions"])
    @session_authorization_required
    def get(self, session_id, **kwargs):
        """Get classification for session.

        Args:
            session_id (str): session id
        """
        return em.get_classification_by_session_id(session_id)
