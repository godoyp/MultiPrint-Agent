from flask import Blueprint, Response
from modules.eventlog import event_stream

bp = Blueprint("logs", __name__)

@bp.route("/logs/stream")
def logs_stream():
    return Response(event_stream(), mimetype="text/event-stream")
