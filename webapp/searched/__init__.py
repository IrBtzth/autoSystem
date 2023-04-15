def create_module(app, **kwargs):
    from .controllers import searched_blueprint
    app.register_blueprint(searched_blueprint)