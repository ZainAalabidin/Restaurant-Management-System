#wsgi.py

# Import the Flask application instance from the run.py file
from run import flask_app

# Check if the script is executed directly (not imported as a module)
if __name__ == '__main__':
    # Run the Flask application
    flask_app.run()
