from flask import Flask, request, jsonify
from utils.pdf_processor import PDFProcessor
from model.analyzer import MedicalReportAnalyzer  # Add this import
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
analyzer = MedicalReportAnalyzer()
pdf_processor = PDFProcessor()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/analyze', methods=['POST'])
def analyze_report():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '' or not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Invalid file format'}), 400

    try:
        text_content = pdf_processor.extract_text(file)
        analysis_result = analyzer.analyze_report(text_content)
        return jsonify(analysis_result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)