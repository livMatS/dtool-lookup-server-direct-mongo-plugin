try:
    from importlib.metadata import version, PackageNotFoundError
except ModuleNotFoundError:
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
   pass

from flask import (
    abort,
    jsonify,
    request,
    current_app,
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from flask_smorest import Blueprint
from flask_smorest.pagination import PaginationParameters

from dtool_lookup_server import AuthenticationError
from dtool_lookup_server.schemas import ConfigSchema
from dtool_lookup_server.sql_models import DatasetSchema

from .config import Config
from .schemas import QueryDatasetSchema
from .utils import (
    config_to_dict,
    query_datasets_by_user,
    aggregate_datasets_by_user,
)


mongo_bp = Blueprint("mongo", __name__, url_prefix="/mongo")


@mongo_bp.route("/config", methods=["GET"])
@mongo_bp.response(200, ConfigSchema)
@jwt_required()
def plugin_config():
    """Return the JSON-serialized plugin configuration."""
    username = get_jwt_identity()
    try:
        config = config_to_dict(username)
    except AuthenticationError:
        abort(401)
    return jsonify(config)


@mongo_bp.route("/query", methods=["POST"])
@mongo_bp.arguments(QueryDatasetSchema(partial=True))
@mongo_bp.response(200, DatasetSchema(many=True))
@mongo_bp.paginate()
@jwt_required()
def query_datasets(
            query: QueryDatasetSchema, pagination_parameters: PaginationParameters
        ):
    """Query datasets a user has access to."""
    if not Config.ALLOW_DIRECT_QUERY:
        abort(404)
    username = get_jwt_identity()
    current_app.logger.debug("Received query request '{}' from user '{}'.".format(query, username))
    try:
        datasets = query_datasets_by_user(username, query)
    except AuthenticationError:
        abort(401)
    pagination_parameters.item_count = len(datasets)
    return jsonify(
        datasets[pagination_parameters.first_item : pagination_parameters.last_item + 1]
    )


@mongo_bp.route("/aggregate", methods=["POST"])
@mongo_bp.arguments(QueryDatasetSchema(partial=True))
@mongo_bp.response(200, DatasetSchema(many=True))
@mongo_bp.paginate()
@jwt_required()
def aggregate_datasets(
            query: QueryDatasetSchema, pagination_parameters: PaginationParameters
        ):
    """Aggregate the datasets a user has access to."""
    if not Config.ALLOW_DIRECT_AGGREGATION:
        abort(404)
    username = get_jwt_identity()
    current_app.logger.debug("Received aggregate request '{}' from user '{}'.".format(query, username))
    try:
        datasets = aggregate_datasets_by_user(username, query)
    except AuthenticationError:
        abort(401)
    pagination_parameters.item_count = len(datasets)
    return jsonify(
        datasets[pagination_parameters.first_item: pagination_parameters.last_item + 1]
    )
