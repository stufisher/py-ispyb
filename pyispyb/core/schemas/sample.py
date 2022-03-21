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


__license__ = "LGPLv3+"


from marshmallow import Schema, fields as ma_fields
from flask_restx import fields as f_fields
from marshmallow_jsonschema import JSONSchema

from pyispyb.app.extensions.api import api_v1 as api
from .crystal import f_schema as crystal_schema

sample_meta_schema = api.model(
    "SampleMetadata",
    {
        "subsamples": f_fields.Integer(description="Number of sub samples"),
        "datacollections": f_fields.Integer(description="Number of data collections"),
    },
)

dict_schema = {
    'blSampleId': f_fields.Integer(required=True, description=''),
    'diffractionPlanId': f_fields.Integer(required=False, description=''),
    'crystalId': f_fields.Integer(required=False, description=''),
    'containerId': f_fields.Integer(required=False, description=''),
    'name': f_fields.String(required=False, description=''),
    'code': f_fields.String(required=False, description=''),
    'location': f_fields.String(required=False, description=''),
    'holderLength': f_fields.String(required=False, description=''),
    'loopLength': f_fields.String(required=False, description=''),
    'loopType': f_fields.String(required=False, description=''),
    'wireWidth': f_fields.String(required=False, description=''),
    'comments': f_fields.String(required=False, description=''),
    'completionStage': f_fields.String(required=False, description=''),
    'structureStage': f_fields.String(required=False, description=''),
    'publicationStage': f_fields.String(required=False, description=''),
    'publicationComments': f_fields.String(required=False, description=''),
    'blSampleStatus': f_fields.String(required=False, description=''),
    'isInSampleChanger': f_fields.Integer(required=False, description=''),
    'lastKnownCenteringPosition': f_fields.String(required=False, description=''),
    'recordTimeStamp': f_fields.DateTime(required=True, description='Creation or last update date/time'),
    'SMILES': f_fields.String(required=False, description='the symbolic description of the structure of a chemical compound'),
    'lastImageURL': f_fields.String(required=False, description=''),
    'positionId': f_fields.Integer(required=False, description=''),
    'blSubSampleId': f_fields.Integer(required=False, description=''),
    'screenComponentGroupId': f_fields.Integer(required=False, description=''),
    'volume': f_fields.Float(required=False, description=''),
    'dimension1': f_fields.String(required=False, description=''),
    'dimension2': f_fields.String(required=False, description=''),
    'dimension3': f_fields.String(required=False, description=''),
    'shape': f_fields.String(required=False, description=''),
    'subLocation': f_fields.Integer(required=False, description='Indicates the samples location on a multi-sample pin, where 1 is closest to the pin base'),
    'Crystal': f_fields.Nested(crystal_schema),
    '_metadata': f_fields.Nested(sample_meta_schema)
}


class SampleSchema(Schema):
    """Marshmallows schema class representing Sample table"""

    blSampleId = ma_fields.Integer()
    diffractionPlanId = ma_fields.Integer()
    crystalId = ma_fields.Integer()
    containerId = ma_fields.Integer()
    name = ma_fields.String()
    code = ma_fields.String()
    location = ma_fields.String()
    holderLength = ma_fields.String()
    loopLength = ma_fields.String()
    loopType = ma_fields.String()
    wireWidth = ma_fields.String()
    comments = ma_fields.String()
    completionStage = ma_fields.String()
    structureStage = ma_fields.String()
    publicationStage = ma_fields.String()
    publicationComments = ma_fields.String()
    blSampleStatus = ma_fields.String()
    isInSampleChanger = ma_fields.Integer()
    lastKnownCenteringPosition = ma_fields.String()
    recordTimeStamp = ma_fields.DateTime()
    SMILES = ma_fields.String()
    lastImageURL = ma_fields.String()
    positionId = ma_fields.Integer()
    blSubSampleId = ma_fields.Integer()
    screenComponentGroupId = ma_fields.Integer()
    volume = ma_fields.Float()
    dimension1 = ma_fields.String()
    dimension2 = ma_fields.String()
    dimension3 = ma_fields.String()
    shape = ma_fields.String()
    subLocation = ma_fields.Integer()


f_schema = api.model('Sample', dict_schema)
ma_schema = SampleSchema()
json_schema = JSONSchema().dump(ma_schema)
