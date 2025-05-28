import cv2
import os
from deepface import DeepFace

def create_user_folder(name):
    folder_path = os.path.join("registered_faces", name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def register_face(name):
    cam = cv2.VideoCapture(0)
    folder = create_user_folder(name)
    count = 0
    print("[INFO] Press 's' to save image, 'q' to quit.")
    while True:
        ret, frame = cam.read()
        if not ret:
            print("[ERROR] Failed to capture image")
            break
        cv2.imshow("Register Face", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            filepath = os.path.join(folder, f"{count}.jpg")
            cv2.imwrite(filepath, frame)
            print(f"[INFO] Saved: {filepath}")
            count += 1
        elif key == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
    print("[INFO] Registration completed.")

def recognize_faces():
    cam = cv2.VideoCapture(0)
    print("[INFO] Starting recognition. Press 'q' to quit.")
    while True:
        ret, frame = cam.read()
        if not ret:
            print("[ERROR] Failed to capture image")
            break
        try:
            result = DeepFace.find(img_path=frame, db_path="registered_faces", enforce_detection=False)
            if len(result[0]) > 0:
                identity = result[0].iloc[0]['identity']
                name = os.path.basename(os.path.dirname(identity))
                cv2.putText(frame, f"{name}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        except Exception as e:
            print(f"[WARN] Recognition failed: {e}")
        cv2.imshow("Live Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("1. Register Face\n2. Recognize Face")
    choice = input("Choose (1 or 2): ")
    if choice == '1':
        name = input("Enter name: ")
        register_face(name)
    elif choice == '2':
        recognize_faces()