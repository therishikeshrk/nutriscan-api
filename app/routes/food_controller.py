from flask import Blueprint, request, jsonify
from ..services.food_service import detect_food_and_calories

api_bp = Blueprint('api', __name__)

@api_bp.route('/v1/food/detect', methods=['POST'])
def detect_food_and_calories_route():
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'Image file is required.'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected.'}), 400

    try:
        base64_image = convert_image_to_base64(file)

        result = detect_food_and_calories(base64_image)
        return jsonify({'success': True, 'result': result}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

def convert_image_to_base64(file):
    import base64
    file_data = file.read()
    mime_type = file.content_type
    base64_encoded = base64.b64encode(file_data).decode('utf-8')
    return f"data:{mime_type};base64,{base64_encoded}"
