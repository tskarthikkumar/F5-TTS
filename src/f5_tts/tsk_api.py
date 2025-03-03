from flask import Flask, request, send_file, jsonify
import os
from f5_tts.api import F5TTS  
import base64

app = Flask(__name__)

f5tts = F5TTS()

# API endpoint to accept ref_audio, ref_text, and gen_text
@app.route('/process', methods=['POST'])
def process_data():
    ref_audio = request.form.get('ref_audio')
    ref_text = request.form.get('ref_text')
    gen_text = request.form.get('gen_text')
    speed = request.form.get('speed')
    seed = request.form.get('seed')
    response_type = request.form.get('response_type')
    output_file_name = request.form.get('output_file_name')

    if not gen_text or not ref_audio or not speed or not seed or not response_type or not output_file_name:
        return jsonify({"error": "Missing ref_audio or gen_text or speed or seed or response_type or output_file_name"}), 400

    output_wave_path = f"output/{output_file_name}"

    try:
        wav, sr, spect = f5tts.infer(
            ref_file=ref_audio,
            ref_text=ref_text,
            gen_text=gen_text,
            file_wave=output_wave_path,
            speed=float(speed),
            seed=seed  # Using random seed (-1)
        )
       
    except Exception as e:
        return jsonify({"error": f"F5TTS inference failed: {str(e)}"}), 500
    
    if response_type == "json":
        with open(output_wave_path, "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
        return {"audio_base64": audio_base64, "message": "TTS generated successfully"}

    elif response_type == "file":
        return send_file(output_wave_path, mimetype="audio/wav")
           
def run_api():
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    run_api()