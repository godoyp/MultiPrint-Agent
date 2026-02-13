from flask import Flask
from flask_cors import CORS
from multiprint_web_agent.core.agent_config import get_port
from multiprint_web_agent.core.ssl_config import get_ssl_context
from multiprint_web_agent.routes.api.print import bp as print_bp
from multiprint_web_agent.routes.api.auth import bp as auth_bp
from multiprint_web_agent.routes.ui.printers import bp as printers_bp
from multiprint_web_agent.routes.ui.state import bp as state_bp
from multiprint_web_agent.routes.ui.logs import bp as logs_bp
from multiprint_web_agent.routes.ui.print_test import bp as print_test_bp
from multiprint_web_agent.routes.ui.ui import bp as ui_bp


app = Flask(__name__)
CORS(app)

app.register_blueprint(print_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(printers_bp)
app.register_blueprint(state_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(print_test_bp)
app.register_blueprint(ui_bp)


if __name__ == "__main__":
    print("🖨️ MultiPrint Web Agent Initialized")

    ssl_context = get_ssl_context()

    if not ssl_context:
        raise RuntimeError("HTTPS is mandatory but SSL context could not be loaded")

    app.run(
        host="127.0.0.1",
        port=get_port(),
        ssl_context=ssl_context,
        debug=False,
    )