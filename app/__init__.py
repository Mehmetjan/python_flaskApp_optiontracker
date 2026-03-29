from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    from app.models import db        # ← get db from models
    db.init_app(app)

    with app.app_context():
        from app.models import Stock
        db.create_all()
        print("✅ Tables created successfully!")

    from app.routes import main
    app.register_blueprint(main)

    return app