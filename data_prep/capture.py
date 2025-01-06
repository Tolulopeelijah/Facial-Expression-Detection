import cv2
from pathlib import Path

classes = ['happy', 'angry', 'frown'] 


def capture(n: int, emotion: str, dir: Path):
    emotion_dir = dir / emotion
    emotion_dir.mkdir(exist_ok=True, parents=True)

    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        print("Cannot access webcam")
        return

    count = 0
    while count < n:
        ret, frame = capture.read()
        if not ret:
            print("Error: Cannot read from the webcam")
            break  


        cv2.imshow("Capture Images - Press 's' to Save, 'q' to Quit", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'): 
            img_path = emotion_dir / f"frame_{count}.jpg"
            cv2.imwrite(str(img_path), frame)
            print(f"Saved: {img_path}")
            count += 1
        elif key == ord('q'): 
            print("Quitting...")
            break

    capture.release()
    cv2.destroyAllWindows()


capture(10, 'crying', Path('..', 'data'))