from flask import Flask, jsonify, request
from flask_cors import CORS


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/', methods=['GET'])
def ping_pong():
    return jsonify('The app is up and running!')

Strokes = []

@app.route('/teddy', methods=['GET', 'POST'])
def the_strokes():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        global Strokes
        post_data = request.get_json()
        Strokes = post_data
        response_object['message'] = 'Strokes added!'
    else:
        response_object['strokes'] = Strokes
    return jsonify(response_object)

if __name__ == '__main__':
    app.run()