from pyispyb.app.extensions.api import api_v1
from flask_restx import fields as f_fields


error_model = api_v1.model(
    "Error",
    {
        "message": f_fields.String,
    },
)


def paginated(model):
    return api_v1.model(
        f"Paginated<{model.name}>",
        {
            "results": f_fields.Nested(model, as_list=True),
            "total": f_fields.Integer(),
            "skip": f_fields.Integer(),
            "limit": f_fields.Integer(),
        },
    )
