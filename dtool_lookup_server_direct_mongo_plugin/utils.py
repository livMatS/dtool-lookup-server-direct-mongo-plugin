from flask import current_app


def _dict_to_mongo_aggregation(query_dict):
    """Construct mongo query as usual and prepend to aggregation pipeline."""
    if "aggregation" in query_dict and isinstance(query_dict["aggregation"], list):
        aggregation_tail = query_dict["aggregation"]
        del query_dict["aggregation"]
        aggregation_tail = []
    # unset any _id field, as type ObjectId usually not serializable
    aggregation_tail.append({'$unset': '_id'})
    match_stage = _dict_to_mongo_query(query_dict)
    if len(match_stage) > 0:
        aggregation_head = [{'$match': match_stage}]
    else:
        aggregation_head = []
    aggregation = [*aggregation_head, *aggregation_tail]
    current_app.logger.debug("Constructed mongo aggregation: {}".format(aggregation))
    return aggregation


def aggregate_datasets_by_user(username, query):
    """Aggregate the datasets the user has access to.
    Valid keys for the query are: creator_usernames, base_uris, free_text,
    aggregation. If the query dictionary is empty, all datasets that a user has
    access to are returned.
    :param username: username
    :param query: dictionary specifying query
    :returns: List of dicts if user is valid and has access to datasets.
              Empty list if user is valid but has not got access to any
              datasets.
    :raises: AuthenticationError if user is invalid.
    """
    if not Config.ALLOW_DIRECT_AGGREGATION:
        current_app.logger.warning(
            "Received aggregate request '{}' from user '{}', but direct "
            "aggregations are disabled.".format(query, username))
        return []  # silently reject request
    query = _preprocess_privileges(username, query)
    # If there are no base URIs at this point it means that the user has not
    # got privileges to search for anything.
    if len(query["base_uris"]) == 0:
        return []
    datasets = []
    mongo_aggregation = _dict_to_mongo_aggregation(query)
    cx = mongo.db[MONGO_COLLECTION].aggregate(mongo_aggregation)
    # Opposed to search_datasets_by_user, here it is the aggregator's
    # responsibility to project out desired fields and remove non-serializable
    # content. The only modification always applied is removing any '_id' field.
    for ds in cx:
        datasets.append(ds)
    return datasets
