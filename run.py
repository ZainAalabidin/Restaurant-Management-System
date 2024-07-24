from app import create_app

# Create an instance of the Flask application
flask_app = create_app()

if __name__ == '__main__':
    # Run the Flask application
    flask_app.run(host='0.0.0.0', debug=True, port=8000)
    # The application will be accessible on all IP addresses (0.0.0.0),
    # will run in debug mode, and will listen on port 8000.
