from flask import Flask
from JagCoachUI.routes import main_bp  # Import routes from JagCoach/JagCoachUI/routes.py
from config import config  # Import configuration

app = Flask(__name__, template_folder="JagCoachUI/templates", static_folder="JagCoachUI/static")

# Load configurations
app.config.from_object(config)

# Register routes
app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=config.DEBUG)
