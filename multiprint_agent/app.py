from flask import Flask, Blueprint
from flask_cors import CORS
from multiprint_agent.core.agent_config import get_port
from multiprint_agent.core.ssl_config import get_ssl_context
from multiprint_agent.core.handlers import register_api_error_handlers, register_ui_error_handlers
from multiprint_agent.routes.api.print import bp as print_bp
from multiprint_agent.routes.api.auth import bp as auth_bp
from multiprint_agent.routes.ui.printers import bp as printers_bp
from multiprint_agent.routes.ui.state import bp as state_bp
from multiprint_agent.routes.ui.logs import bp as logs_bp
from multiprint_agent.routes.ui.print_test import bp as print_test_bp
from multiprint_agent.routes.ui.ui import bp as ui_bp
from multiprint_agent.core.paths import STATIC_DIR


app = Flask(__name__, static_folder=str(STATIC_DIR))
CORS(app)

# Root API v1
api_v1_root = Blueprint("api_v1", __name__, url_prefix="/api/v1")
register_api_error_handlers(api_v1_root)

# Root UI
ui_root = Blueprint("ui_root", __name__, url_prefix="/ui")
register_ui_error_handlers(ui_root)

# API Children
api_v1_root.register_blueprint(print_bp)
api_v1_root.register_blueprint(auth_bp)

# UI Children
ui_root.register_blueprint(printers_bp)
ui_root.register_blueprint(state_bp)
ui_root.register_blueprint(logs_bp)
ui_root.register_blueprint(print_test_bp)
ui_root.register_blueprint(ui_bp)

# Roots in APP
app.register_blueprint(api_v1_root)
app.register_blueprint(ui_root)


def run():
    ssl_context = get_ssl_context()

    if not ssl_context:
        raise RuntimeError("HTTPS is mandatory but SSL context could not be loaded")

    app.run(
        host="127.0.0.1",
        port=get_port(),
        ssl_context=ssl_context,
        debug=False,
    )

if __name__ == "__main__":
    run()