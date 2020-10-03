from flask import (
    abort,
    Blueprint,
    jsonify,
)
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from dtool_lookup_server import AuthenticationError

from .utils import (
    config_to_dict,
    query_datasets_by_user,
    aggregate_datasets_by_user,
)

__version__ = "0.1.0"


mongo_bp = Blueprint("mongo", __name__, url_prefix="/mongo")

@mongo_bp.route("/config", methods=["GET"])
@jwt_required
def plugin_config():
    """Return the JSON-serialized plugin configuration."""
    username = get_jwt_identity()
    try:
        config = config_to_dict(username)
    except AuthenticationError:
        abort(401)
    return jsonify(config)


mongo_bp.route("/query", methods=["POST"])
@jwt_required
def query_datasets():
    """Query datasets a user has access to."""
    username = get_jwt_identity()
    query = request.get_json()
    current_app.logger.debug("Received aggregate request '{}' from user '{}'.".format(query, username))
    try:
        datasets = query_datasets_by_user(username, query)
    except AuthenticationError:
        abort(401)
    return jsonify(datasets)


mongo_bp.route("/aggregate", methods=["POST"])
@jwt_required
def aggregate_datasets():
    """Aggregate the datasets a user has access to."""
    username = get_jwt_identity()
    query = request.get_json()
    current_app.logger.debug("Received aggregate request '{}' from user '{}'.".format(query, username))
    try:
        datasets = aggregate_datasets_by_user(username, query)
    except AuthenticationError:
        abort(401)
    return jsonify(datasets)