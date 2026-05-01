import pyaudio
from flask import Flask, Response, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Audio Settings (High Quality)
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 2048 # Bada chunk = Better Quality, Chhota chunk = Kam Lag

audio = pyaudio.PyAudio()

def generate_pc_audio():
    # 'input=True' PC ke Stereo Mix se awaaz uthayega
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    
    # WAV Header (Taki browser ko pata chale ye high quality audio hai)
    yield (b'RIFF\xff\xff\xff\xffWAVEfmt \x10\x00\x00\x00\x01\x00' +
           CHANNELS.to_bytes(2, 'little') +
           RATE.to_bytes(4, 'little') +
           (RATE * CHANNELS * 2).to_bytes(4, 'little') +
           (CHANNELS * 2).to_bytes(2, 'little') +
           b'\x10\x00data\xff\xff\xff\xff')

    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        yield data

@app.route('/stream')
def stream():
    return Response(generate_pc_audio(), mimetype='audio/x-wav')

if __name__ == '__main__':
    # '0.0.0.0' ka matlab hai aap network mein kahin se bhi access kar sakte hain
    app.run(host='0.0.0.0', port=8000, threaded=True, debug=False)