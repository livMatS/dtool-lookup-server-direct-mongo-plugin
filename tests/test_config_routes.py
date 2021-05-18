"""Test the /mongo/config blueprint route."""

import json
import dtool_lookup_server_direct_mongo_plugin

from . import tmp_app_with_users  # NOQA

from . import snowwhite_token

def test_config_info_route(tmp_app_with_users):  # NOQA

    headers = dict(Authorization="Bearer " + snowwhite_token)
    r = tmp_app_with_users.get(
        "/mongo/config",
        headers=headers,
    )
    assert r.status_code == 200

    expected_content = {
        'allow_direct_query': True,
        'allow_direct_aggregation': False,
        'version': dtool_lookup_server_direct_mongo_plugin.__version__}

    response = json.loads(r.data.decode("utf-8"))
    assert response == expected_content
