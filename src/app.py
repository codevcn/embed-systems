from flask import Flask, request, render_template
import wave
import time
import os
from flask import jsonify, send_from_directory

app = Flask(__name__)


@app.route("/ui")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_audio():
    audio_data = request.data  # Nhận dữ liệu từ ESP32
    if not audio_data:
        return "No data received", 400

    # Kiểm tra xem dữ liệu có rỗng không
    data_length = len(audio_data)
    print(f">>> Received audio data: {data_length} bytes")

    filename = f"src/audios/audio_{int(time.time())}.wav"

    with wave.open(filename, "wb") as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(4)  # 32-bit
        wav_file.setframerate(16000)  # 16 kHz
        wav_file.writeframes(audio_data)

    print(f">>> Saved {filename}")
    return "Received", 200


UPLOAD_FOLDER = "src/audios"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/files", methods=["GET"])
def list_files():
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".wav")]
    return jsonify(files)


@app.route("/src/audios/<filename>", methods=["GET"])
def get_file(filename):
    print(">>> filename:", filename)
    return send_from_directory(f"../{UPLOAD_FOLDER}", filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
