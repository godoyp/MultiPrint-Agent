from flask import Flask
from flask_cors import CORS
from core.agent_config import CONFIG
from routes.print import bp as print_bp
from routes.printers import bp as printers_bp
from routes.state import bp as state_bp
from routes.logs import bp as logs_bp
from routes.print_test import bp as print_test_bp
from routes.ui import bp as ui_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(print_bp)
app.register_blueprint(printers_bp)
app.register_blueprint(state_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(print_test_bp)
app.register_blueprint(ui_bp)

if __name__ == "__main__":
    print("🖨️ MultiPrint Web Agent Initialized")
    app.run(
        host= "127.0.0.1",
        port= CONFIG.get("agent_port", 9108),
        ssl_context=("certs/localhost.crt", "certs/localhost.key")
    )
