import os
import importlib

# Dynamically import all .py files in this folder
module_dir = os.path.dirname(__file__)
modules = [
    f[:-3] for f in os.listdir(module_dir)
    if f.endswith(".py") and f != "__init__.py"
]

# Import each module and expose its single function
for module_name in modules:
    module = importlib.import_module(f".{module_name}", package=__name__)
    globals()[module_name] = getattr(module, module_name)

# Define what is available for import when importing *
__all__ = modules
