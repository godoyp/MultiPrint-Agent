from flask import Flask
from flask_cors import CORS
from core.agent_config import AGENT_CONFIG
from core.ssl_config import get_ssl_context
from routes.api.print import bp as print_bp
from routes.api.auth import bp as auth_bp
from routes.ui.printers import bp as printers_bp
from routes.ui.state import bp as state_bp
from routes.ui.logs import bp as logs_bp
from routes.ui.print_test import bp as print_test_bp
from routes.ui.ui import bp as ui_bp


ssl_context = get_ssl_context()

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
    app.run(
        host= "127.0.0.1",
        port= AGENT_CONFIG.get("agent_port", 9108),
        ssl_context=ssl_context,
    )
