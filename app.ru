from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

ads = {}

class Ad:
    def __init__(self, title, description, owner):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.created_at = datetime.now().isoformat()
        self.owner = owner

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at,
            'owner': self.owner
        }

@app.route('/ads', methods=['POST'])
def create_ad():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        required_fields = ['title', 'description', 'owner']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        ad = Ad(
            title=data['title'],
            description=data['description'],
            owner=data['owner']
        )

        ads[ad.id] = ad

        return jsonify(ad.to_dict()), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/ads/<ad_id>', methods=['GET'])
def get_ad(ad_id):
    try:
        ad = ads.get(ad_id)

        if not ad:
            return jsonify({'error': 'Ad not found'}), 404

        return jsonify(ad.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ads/<ad_id>', methods=['PUT'])
def update_ad(ad_id):
    try:
        ad = ads.get(ad_id)

        if not ad:
            return jsonify({'error': 'Ad not found'}), 404

        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        if 'title' in data:
            ad.title = data['title']

        if 'description' in data:
            ad.description = data['description']

        if 'owner' in data:
            ad.owner = data['owner']

        return jsonify(ad.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ads/<ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    try:
        if ad_id not in ads:
            return jsonify({'error': 'Ad not found'}), 404

        del ads[ad_id]

        return jsonify({'message': 'Ad deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ads', methods=['GET'])
def get_all_ads():
    try:
        all_ads = [ad.to_dict() for ad in ads.values()]
        return jsonify(all_ads), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
