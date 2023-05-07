from marshmallow import Schema
from marshmallow.fields import List, Dict, String, UUID


class QueryDatasetSchema(Schema):
    free_text = String()
    creator_usernames = List(String)
    base_uris = List(String)
    uuids = List(UUID)
    tags = List(String)
    query = Dict()