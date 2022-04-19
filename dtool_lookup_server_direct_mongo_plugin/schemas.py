from marshmallow import Schema
from marshmallow.fields import Dict


class QueryDatasetSchema(Schema):
    query = Dict()