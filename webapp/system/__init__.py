def create_module(app, **kwargs):
    from .controllers import system_blueprint
    app.register_blueprint(system_blueprint)