from flask import request, jsonify
from models import db, Advertisement
import json

def register_routes(app):

    @app.route('/advertisements', methods=['POST'])
    def create_ad():
        try:
            if not request.is_json:
                return jsonify({'error': 'Content-Type must be application/json'}), 400

            data = request.get_json()

            required_fields = ['title', 'description', 'owner']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing field: {field}'}), 400
                if not isinstance(data[field], str) or not data[field].strip():
                    return jsonify({'error': f'Field {field} must be a non-empty string'}), 400

            ad = Advertisement(
                title=data['title'].strip(),
                description=data['description'].strip(),
                owner=data['owner'].strip()
            )

            db.session.add(ad)
            db.session.commit()

            return jsonify(ad.to_dict()), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Database error: {str(e)}'}), 500

    @app.route('/advertisements/<ad_id>', methods=['GET'])
    def get_ad(ad_id):
        try:
            ad = Advertisement.query.get(ad_id)

            if not ad:
                return jsonify({'error': 'Advertisement not found'}), 404

            return jsonify(ad.to_dict()), 200

        except Exception as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500

    @app.route('/advertisements/<ad_id>', methods=['PUT'])
    def update_ad_full(ad_id):
        try:
            ad = Advertisement.query.get(ad_id)

            if not ad:
                return jsonify({'error': 'Advertisement not found'}), 404

            if not request.is_json:
                return jsonify({'error': 'Content-Type must be application/json'}), 400

            data = request.get_json()

            required_fields = ['title', 'description', 'owner']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing field: {field} for full update'}), 400
                if not isinstance(data[field], str) or not data[field].strip():
                    return jsonify({'error': f'Field {field} must be a non-empty string'}), 400

            ad.title = data['title'].strip()
            ad.description = data['description'].strip()
            ad.owner = data['owner'].strip()

            db.session.commit()

            return jsonify(ad.to_dict()), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Database error: {str(e)}'}), 500

    @app.route('/advertisements/<ad_id>', methods=['PATCH'])
    def update_ad_partial(ad_id):
        try:
            ad = Advertisement.query.get(ad_id)

            if not ad:
                return jsonify({'error': 'Advertisement not found'}), 404

            if not request.is_json:
                return jsonify({'error': 'Content-Type must be application/json'}), 400

            data = request.get_json()

            if 'title' in data:
                if not isinstance(data['title'], str) or not data['title'].strip():
                    return jsonify({'error': 'Title must be a non-empty string'}), 400
                ad.title = data['title'].strip()

            if 'description' in data:
                if not isinstance(data['description'], str) or not data['description'].strip():
                    return jsonify({'error': 'Description must be a non-empty string'}), 400
                ad.description = data['description'].strip()

            if 'owner' in data:
                if not isinstance(data['owner'], str) or not data['owner'].strip():
                    return jsonify({'error': 'Owner must be a non-empty string'}), 400
                ad.owner = data['owner'].strip()

            db.session.commit()

            return jsonify(ad.to_dict()), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Database error: {str(e)}'}), 500

    @app.route('/advertisements/<ad_id>', methods=['DELETE'])
    def delete_ad(ad_id):
        try:
            ad = Advertisement.query.get(ad_id)

            if not ad:
                return jsonify({'error': 'Advertisement not found'}), 404

            db.session.delete(ad)
            db.session.commit()

            return '', 204

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Database error: {str(e)}'}), 500
