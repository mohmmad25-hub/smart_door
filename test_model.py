import cv2
from controller import doorAutomate, readButtonState, controlLED
import time

# Face recognition setup
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("Trainer.yml")

# Authorized users
authorized_names = ["mohmmad", "Mohmmad"]

is_authorized = False  # Store face recognition status

while True:
    ret, frame = video.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        serial, conf = recognizer.predict(gray[y:y+h, x:x+w])

        if conf < 50 and serial < len(authorized_names):  # Authorized face
            name = authorized_names[serial]
            is_authorized = True
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Green box
            cv2.putText(frame, f"Authorized: {name}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            controlLED(True, False)  # Green LED ON, Red LED OFF
        else:  # Unauthorized face
            is_authorized = False
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)  # Red box
            cv2.putText(frame, "Unauthorized", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            controlLED(False, True)  # Green LED OFF, Red LED ON

    # Display the live video feed directly
    frame = cv2.resize(frame, (640, 480))
    cv2.imshow("Frame", frame)

    k = cv2.waitKey(1)
    # pushButtonPressed = readButtonState()  # Read button state

    # Open the door if the button is pressed and face is authorized
    if is_authorized:
        doorAutomate(0)  # Open the door
        time.sleep(5)
        doorAutomate(1)  # Close the door

    if k == ord("q"):  # Quit the program
        controlLED(False, False)
        break

# Release resources
video.release()
cv2.destroyAllWindows()
