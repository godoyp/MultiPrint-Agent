from flask import Blueprint, Response
from multiprint_agent.modules.observability.eventlog import event_stream
from multiprint_agent.modules.security.auth import require_session_token


bp = Blueprint("logs", __name__)

@bp.route("/logs/stream")
@require_session_token
def logs_stream_route():    
    return Response(event_stream(), mimetype="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )