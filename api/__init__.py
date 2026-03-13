from flask import Blueprint
from .organizations import organizations_bp
from .schools import schools_bp
from .categories import categories_bp
from .courses import courses_bp

def register_blueprints(app):
    """Register all API blueprints"""
    app.register_blueprint(organizations_bp, url_prefix='/api/v1')
    app.register_blueprint(schools_bp, url_prefix='/api/v1')
    app.register_blueprint(categories_bp, url_prefix='/api/v1')
    app.register_blueprint(courses_bp, url_prefix='/api/v1')
