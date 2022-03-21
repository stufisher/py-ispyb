def init_app(app):
    from .routes.samples import register

    register(app)
