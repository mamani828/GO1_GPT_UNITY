import cv2
from flask import Flask, Response
import threading

app = Flask(__name__)
outputFrame = None
lock = threading.Lock()

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def generate():
    """Video streaming generator function."""
    global outputFrame, lock
    while True:
        with lock:
            if outputFrame is None:
                continue
            (flag, encodedImage) = cv2.imencode('.jpg', outputFrame)
            if not flag:
                continue

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

def capture_video():
    global outputFrame, lock
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Check if the resolution has been set correctly
    actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Requested resolution: 640x480, Actual resolution: {int(actual_width)}x{int(actual_height)}")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to retrieve frame")
            break

        with lock:
            outputFrame = frame.copy()
    cap.release()

if __name__ == '__main__':
    t = threading.Thread(target=capture_video)
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=True, threaded=True, use_reloader=False)

