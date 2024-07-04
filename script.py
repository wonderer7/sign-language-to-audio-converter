import cv2
import mediapipe as mp
import pyttsx3
from tkinter import *
from PIL import Image, ImageTk

#for  Initializing global variables
finger_tips = [4, 8, 12, 16, 20]
thumb_tip = 2
w, h = 640, 480
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
process_frame_count = 0  #  to throttle gesture recognition

# Tkinter window
win = Tk()
win.title('Sign Language to Audio Converter')

# canvas to display the webcam feed
canvas = Canvas(win, width=w, height=h, bg="#FFFFF7")
canvas.pack()

# Function to perform live sign language recognition
def live():
    global process_frame_count
    _, img = cap.read()

    if process_frame_count % 10 == 0:  # every 10th frame
        img = cv2.flip(img, 1)  # Flip image horizontally for natural mirror view
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (w, h))
        results = hands.process(img)

        if results.multi_hand_landmarks:
            lm_list = [lm for hand_landmarks in results.multi_hand_landmarks for lm in hand_landmarks.landmark]
            detect_gesture(lm_list)

        img = ImageTk.PhotoImage(image=Image.fromarray(img))
        canvas.create_image(0, 0, anchor=NW, image=img)
        canvas.image = img

    process_frame_count += 1
    win.after(1, live)

# Function to detect gestures
def detect_gesture(lm_list):
    finger_fold_status = [lm_list[tip].y < lm_list[tip - 1].y for tip in finger_tips]

    # Gesture recognition logic
    if all(finger_fold_status):
        gesture_recognized = False
        
        if lm_list[4].y < lm_list[2].y and all(lm_list[tip].y < lm_list[tip - 1].y for tip in range(2, 20, 4)):
            recognize_gesture('stop ! dont move')
            gesture_recognized = True
        elif lm_list[4].y > lm_list[3].y and all(lm_list[tip].y < lm_list[tip - 1].y for tip in range(2, 20, 4)):
            recognize_gesture('Perfect , You did a great job.')
            gesture_recognized = True
        elif lm_list[4].y > lm_list[3].y and all(lm_list[tip].y > lm_list[tip - 1].y for tip in range(2, 20, 4)):
            recognize_gesture('Good to see you.')
            gesture_recognized = True
        elif all(lm_list[tip].y > lm_list[tip - 1].y for tip in range(2, 20, 4)):
            recognize_gesture('You Come here.')
            gesture_recognized = True
        elif lm_list[4].y < lm_list[3].y and all(lm_list[tip].y > lm_list[tip - 1].y for tip in range(2, 20, 4)):
            recognize_gesture('Yes , we won.')
            gesture_recognized = True
        elif all(lm_list[tip].x < lm_list[tip - 1].x for tip in range(2, 20, 4)):
            recognize_gesture('Move Left')
            gesture_recognized = True
        elif all(lm_list[tip].x > lm_list[tip - 1].x for tip in range(2, 20, 4)):
            recognize_gesture('Move Right')
            gesture_recognized = True

        if not gesture_recognized:
            if lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y:
                recognize_gesture('I Like it')
            elif lm_list[thumb_tip].y > lm_list[thumb_tip - 1].y > lm_list[thumb_tip - 2].y:
                recognize_gesture('I dont like it.')
            elif lm_list[4].y < lm_list[2].y and all(lm_list[tip].y < lm_list[tip - 1].y for tip in range(2, 20, 4)):
                recognize_gesture('Hello! Nice to see you.')
            elif lm_list[4].y < lm_list[2].y and all(lm_list[tip].y > lm_list[tip - 1].y for tip in range(2, 20, 4)):
                recognize_gesture("What's your name?")

# Function to convert the recognized sign to voice
def recognize_gesture(gesture):
    print(gesture)
    speak_gesture(gesture)

def speak_gesture(gesture):
    engine = pyttsx3.init('sapi5')
    engine.say(gesture)
    engine.runAndWait()

# Start the live sign language recognition
live()

# Start the Tkinter event loop
win.mainloop()
