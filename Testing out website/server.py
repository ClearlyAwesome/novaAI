from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/click', methods=['GET'])
def handle_click():
    simulated_data = {
        "ip": "192.168.1.1",
        "city": "Los Angeles",
        "region": "California",
        "country": "USA",
        "loc": "34.0522,-118.2437"
    }
    return jsonify({
        "message": "Thanks for clicking the button!",
        "location_data": simulated_data
    })


if __name__ == '__main__':
    app.run(debug=True)
