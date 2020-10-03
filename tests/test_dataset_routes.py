from . import tmp_app, tmp_app_with_data, tmp_app_with_users, tmp_app_with_data_and_relaxed_security  # NOQA
from . import compare_nested

def test_dataset_aggregate_route(tmp_app_with_data_and_relaxed_security):  # NOQA
    headers = dict(Authorization="Bearer " + grumpy_token)
    # first, repeat all tests from test_dataset_search_route
    # without any aggregation specified, aggregate should behave equivalenty to search
    query = {}  # Everything.
    r = tmp_app_with_data_and_relaxed_security.post(
        "/dataset/aggregate",
        headers=headers,
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 200
    assert len(json.loads(r.data.decode("utf-8"))) == 3
    r = tmp_app_with_data_and_relaxed_security.post(
        "/dataset/aggregate",
        headers=dict(Authorization="Bearer " + sleepy_token),
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 200
    assert len(json.loads(r.data.decode("utf-8"))) == 0
    r = tmp_app_with_data_and_relaxed_security.post(
        "/dataset/aggregate",
        headers=dict(Authorization="Bearer " + dopey_token),
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 401
    r = tmp_app_with_data_and_relaxed_security.post(
        "/dataset/aggregate",
        headers=dict(Authorization="Bearer " + noone_token),
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 401
    # Search for apples (in README).
    headers = dict(Authorization="Bearer " + grumpy_token)
    query = {"free_text": "apple"}
    r = tmp_app_with_data_and_relaxed_security.post(
        "/dataset/aggregate",
        headers=headers,
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 200
    assert len(json.loads(r.data.decode("utf-8"))) == 2
    # Search for U00096 (in manifest).
    headers = dict(Authorization="Bearer " + grumpy_token)
    query = {"free_text": "U00096"}
    r = tmp_app_with_data_and_relaxed_security.post(
        "/dataset/aggregate",
        headers=headers,
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 200
    assert len(json.loads(r.data.decode("utf-8"))) == 2
    # Search for crazystuff (in annotaitons).
    headers = dict(Authorization="Bearer " + grumpy_token)
    query = {"free_text": "crazystuff"}
    r = tmp_app_with_data_and_relaxed_security.post(
        "/dataset/aggregate",
        headers=headers,
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 200
    assert len(json.loads(r.data.decode("utf-8"))) == 1
    # second, try some direct aggregation
    query = {
        'aggregation': [
            {
                '$sort': {'base_uri': 1}
            }, {
                '$group':  {
                    '_id': '$name',
                    'count': {'$sum': 1},
                    'available_at': {'$push': '$base_uri'}
                }
            }, {
                '$project': {
                    'name': '$_id',
                    'count': True,
                    'available_at': True,
                    '_id': False,
                }
            }, {
                '$sort': {'name': 1}
            }
        ]
    }
    r = tmp_app_with_data_and_relaxed_security.post(
        "/dataset/aggregate",
        headers=headers,
        data=json.dumps(query),
        content_type="application/json"
    )
    assert r.status_code == 200
    expected_response = [
        {
            'available_at': ['s3://mr-men', 's3://snow-white'],
            'count': 2,
            'name': 'bad-apples'
        }, {
            'available_at': ['s3://snow-white'],
            'count': 1,
            'name': 'oranges'
        }
    ]
    response = json.loads(r.data.decode("utf-8"))
    assert compare_nested(response, expected_response)
    #assert len(response) == 2
