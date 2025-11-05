import os


def _to_bool(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in ("true", "1", "yes", "y", "on")


def add_env_to_config(app, items):
    """Populate Flask app.config from environment variables or existing config.

    Supported item formats:
    - 'KEY': set app.config['KEY'] from os.getenv('KEY')
    - ['KEY', 'bool']: set app.config['KEY'] as boolean from os.getenv('KEY')
    - ['KEY', 'another_var', 'OTHER']: copy app.config['OTHER'] into app.config['KEY']
    """
    for item in items:
        if isinstance(item, str):
            app.config[item] = os.getenv(item)
            continue

        if not isinstance(item, (list, tuple)) or len(item) < 2:
            continue

        key = item[0]
        mode = item[1]

        if mode == 'bool':
            app.config[key] = _to_bool(os.getenv(key))
        elif mode == 'another_var' and len(item) >= 3:
            other_key = item[2]
            app.config[key] = app.config.get(other_key)
        else:
            raise ValueError(f"Invalid mode: {mode}")
 
