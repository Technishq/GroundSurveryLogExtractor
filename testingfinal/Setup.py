import importlib

# List of required libraries
required_libraries = [
    'struct',
    'pandas',
    'numpy',
    'plotly',
    'csv',
    'datetime',
    'plotly.express',
    'plotly.graph_objects',
    'plotly.io',
    'os'
]

# Iterate through required libraries
for lib in required_libraries:
    try:
        # Try importing the library
        importlib.import_module(lib)
        print(f"{lib} already installed.")
    except ImportError:
        # If not installed, try to install it
        print(f"{lib} not found. Installing...")
        try:
            import pip
            pip.main(['install', lib])
        except AttributeError:
            import subprocess
            subprocess.call(['pip', 'install', lib])

print("All required libraries have been installed.")
