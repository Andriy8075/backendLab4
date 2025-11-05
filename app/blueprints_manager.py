def register_blueprints_in_routes(app, blueprints):
    """Dynamically import and register Flask blueprints.
    
    Args:
        app: Flask application instance
        blueprints: List of blueprint names (e.g., ['general', 'user'])
    
    For each name in blueprints, imports {name}_bp from app.routes.{name}
    and registers it with the app.
    """
    for name in blueprints:
        module_path = f'app.routes.{name}'
        blueprint_name = f'{name}_bp'
        
        # Dynamically import the blueprint
        module = __import__(module_path, fromlist=[blueprint_name])
        blueprint = getattr(module, blueprint_name)
        
        # Register the blueprint with the app
        app.register_blueprint(blueprint)
