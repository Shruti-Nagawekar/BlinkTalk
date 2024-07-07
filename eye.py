import cv2
import dlib
import numpy as np
from scipy.spatial import distance as dist

# Constants for Morse Code
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
    '----.': '9'
}

# Initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Update this line with the correct path

def eye_aspect_ratio(eye):
    # Compute the euclidean distances between the two sets of vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # Compute the euclidean distance between the horizontal eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    return ear

# Grab the indexes of the facial landmarks for the left and right eye, respectively
(lStart, lEnd) = (42, 48)
(rStart, rEnd) = (36, 42)

EYE_AR_THRESH = 0.2
EYE_AR_CONSEC_FRAMES = 3

# Initialize counters and variables
COUNTER = 0
TOTAL = 0
morse_sequence = ""
text = ""
blink_start_time = 0
blink_detected = False
last_blink_time = 0
MORSE_CHAR_PAUSE = 1.5  # 1.5 seconds to consider end of character
MORSE_WORD_PAUSE = 3.5  # 3.5 seconds to consider end of word

# Start the video stream from the webcam (using CAP_DSHOW backend)
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Error: Could not open video device.")
else:
    print("Successfully opened video device.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break

    if frame is None or frame.size == 0:
        print("Warning: Received an empty frame.")
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    for rect in rects:
        shape = predictor(gray, rect)
        shape = np.array([[p.x, p.y] for p in shape.parts()])

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        ear = (leftEAR + rightEAR) / 2.0

        if ear < EYE_AR_THRESH:
            COUNTER += 1

            if not blink_detected:
                blink_start_time = cv2.getTickCount()
                blink_detected = True

        else:
            if blink_detected:
                blink_duration = (cv2.getTickCount() - blink_start_time) / cv2.getTickFrequency()
                blink_detected = False
                last_blink_time = cv2.getTickCount() / cv2.getTickFrequency()

                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    if blink_duration < 0.3:  # Short blink
                        morse_sequence += "."
                    else:  # Long blink
                        morse_sequence += "-"

                    TOTAL += 1
                    print(f"Blinks: {TOTAL} Morse: {morse_sequence}")

                COUNTER = 0

    current_time = cv2.getTickCount() / cv2.getTickFrequency()
    time_since_last_blink = current_time - last_blink_time

    if time_since_last_blink > MORSE_WORD_PAUSE and morse_sequence:
        # Consider as end of word
        morse_sequence += "   "
        last_blink_time = current_time

    if time_since_last_blink > MORSE_CHAR_PAUSE and morse_sequence.endswith("   "):
        # Decode the current Morse sequence
        morse_sequence = morse_sequence.strip()
        words = morse_sequence.split("   ")

        for word in words:
            letters = word.split(" ")
            for letter in letters:
                text += MORSE_CODE_DICT.get(letter, '')

            text += ' '

        morse_sequence = ""
        print(f"Decoded text: {text.strip()}")

    cv2.putText(frame, f"Blinks: {TOTAL} Morse: {morse_sequence} Text: {text.strip()}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
