from flask import Blueprint, Response
from modules.observability.eventlog import event_stream
from modules.security.auth import require_session_token


bp = Blueprint("logs", __name__, url_prefix="/ui")

@bp.route("/logs/stream")
def logs_stream_route():

    auth = require_session_token()
    if auth:
        return auth
    
    return Response(event_stream(), mimetype="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )