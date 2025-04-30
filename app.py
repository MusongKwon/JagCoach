from flask import Flask
from JagCoachUI.routes import main_bp  # Import routes from JagCoach/JagCoachUI/routes.py
from JagCoachUI.live_routes import live_bp
from JagCoachUI.config import config  # Import configuration

app = Flask(__name__, template_folder="JagCoachUI/templates", static_folder="JagCoachUI/static")

# Load configurations
app.config.from_object(config)
app.config["UPLOAD_FOLDER"] = "uploads"

# Register routes
app.register_blueprint(main_bp)
app.register_blueprint(live_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=config.DEBUG)
