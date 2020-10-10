from flask import Flask
from flask_cors import CORS
from apis import blueprint
from apis import api

app = Flask(__name__)
CORS(app)

app.register_blueprint(blueprint)
app.config.from_pyfile('configuration.py')

# Register app error handlers
@app.errorhandler(404)
def handle_not_found(error):
    # Analytics
    status_code = 404
    # Recorder('not_found_error', status_code).recordUsage()

    response = {"message": "Resource not found."}
    return response, status_code

@app.errorhandler(Exception)
def handle_internal_server_error(error):
    # Analytics
    status_code = 500
    # Recorder('internal_server_error', status_code).recordUsage()

    print(error.__class__)
    print(error)

    response = {"message": "Internal server error."}
    return response, status_code

# Run
app.run(debug=True)
