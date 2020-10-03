def test_direct_query():
    from dtool_lookup_server.config import Config
    from dtool_lookup_server.utils import _dict_to_mongo_query
    # Test with direct queries disabled
    query = dict(query={'key': 'value'})
    assert _dict_to_mongo_query(query) == {}
    # Test with direct queries enabled
    query = dict(query={'key': 'value'})
    expected_mongo_query = {"key": "value"}
    Config.ALLOW_DIRECT_QUERY = True
    Config.QUERY_DICT_VALID_KEYS.append("query")
    assert _dict_to_mongo_query(query) == expected_mongo_query
    # Test empty query.
    query = dict(query={})
    assert _dict_to_mongo_query(query) == {}
