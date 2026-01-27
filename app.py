from flask import Flask
from flask_cors import CORS
from core.agent_config import AGENT_PORT
from routes.print import bp as print_bp
from routes.printers import bp as printers_bp
from routes.config import bp as config_bp
from routes.health import bp as health_bp
from routes.logs import bp as logs_bp
from routes.version import bp as version_bp
from routes.print_test import bp as print_test_bp
from routes.ui import bp as ui_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(print_bp)
app.register_blueprint(printers_bp)
app.register_blueprint(config_bp)
app.register_blueprint(health_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(version_bp)
app.register_blueprint(print_test_bp)
app.register_blueprint(ui_bp)

if __name__ == "__main__":
    print("🖨️ LocalPrint Agent Initialized")
    app.run(
        host="127.0.0.1",
        port=AGENT_PORT,
        ssl_context=("certs/localhost.crt", "certs/localhost.key")
    )
