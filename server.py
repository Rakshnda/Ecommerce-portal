import os
import tempfile
import subprocess
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from faster_whisper import WhisperModel
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get the directory where server.py is located
# This assumes all your frontend files (index.html, style.css, assets/)
# are in the SAME directory as server.py
current_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            template_folder=current_dir,  # Look for HTML files in the current directory
            static_folder=current_dir)    # Look for static files (CSS, JS, images) in the current directory

CORS(app)

model_size = "small.en" # Using small.en for better accuracy

try:
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    logging.info(f"Faster Whisper model '{model_size}' loaded successfully on CPU.")
except Exception as e:
    logging.error(f"Failed to load Faster Whisper model: {e}")
    model = None

@app.route('/')
def home():
    # Flask will now look for 'index.html' directly in 'current_dir'
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if model is None:
        return jsonify({'error': 'Speech-to-text model failed to load.'}), 500

    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    temp_webm_path = tempfile.NamedTemporaryFile(delete=False, suffix=".webm").name
    wav_path = None

    try:
        audio_file.save(temp_webm_path)
        logging.info(f"Received audio saved to: {temp_webm_path}")

        wav_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        ffmpeg_command = [
            'ffmpeg',
            '-i', temp_webm_path,
            '-ar', '16000',
            '-ac', '1',
            wav_path,
            '-y'
        ]

        result = subprocess.run(ffmpeg_command, check=True, capture_output=True)
        logging.info(f"FFmpeg conversion successful: {wav_path}")
        if result.stderr:
            logging.warning(f"FFmpeg stderr: {result.stderr.decode().strip()}")

        segments, info = model.transcribe(
            wav_path,
            beam_size=7,
            language="en",
            vad_filter=True,
            vad_parameters={"min_speech_duration_ms": 100, "threshold": 0.6}
        )

        recognized_text = ""
        for segment in segments:
            recognized_text += segment.text.strip() + " "

        recognized_text = recognized_text.strip()
        logging.info(f"Transcribed Text: '{recognized_text}' (Language: {info.language})")

        return jsonify({'text': recognized_text, 'language': info.language})

    except subprocess.CalledProcessError as e:
        logging.error(f"FFmpeg conversion failed: {e.stderr.decode()}", exc_info=True)
        return jsonify({'error': f'Audio conversion failed: {e.stderr.decode()}'}), 500
    except Exception as e:
        logging.error(f"An error occurred during transcription: {e}", exc_info=True)
        return jsonify({'error': f'Transcription failed: {str(e)}'}), 500
    finally:
        if os.path.exists(temp_webm_path):
            os.remove(temp_webm_path)
        if wav_path and os.path.exists(wav_path):
            os.remove(wav_path)

# This route will catch any requests for files not handled by other routes (like /),
# and try to serve them directly from the project root.
# This is crucial for files like style.css, assets/product1.jpg, assets/audio/product_audio_0.mp3
# Make sure this is the LAST route defined if you have others,
# to avoid it catching everything.
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(current_dir, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)