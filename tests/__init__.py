def compare_nested(A, B):
    """Compare nested dicts and lists."""
    if isinstance(A, list) and isinstance(B, list):
        for a, b in zip(A, B):
            if not compare_nested(a, b):
                return False
        return True
    if isinstance(A, dict) and isinstance(B, dict):
        if set(A.keys()) == set(B.keys()):
            for k in A.keys():
                if not compare_nested(A[k], B[k]):
                    return False
            return True
        else:
            return False
    return A == B

@pytest.fixture
def tmp_app_with_data_and_relaxed_security(request, tmp_app_with_data):
    from dtool_lookup_server.config import Config
    Config.ALLOW_DIRECT_QUERY = True
    Config.QUERY_DICT_VALID_KEYS.append("query")
    Config.ALLOW_DIRECT_AGGREGATION = True
    return tmp_app_with_data
