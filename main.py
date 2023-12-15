import cv2
import mediapipe as mp
import pyautogui
import keyboard
import tkinter as tk
import PIL
from PIL import ImageTk, Image

global cam_enable
cam_enable = 1

main_window = tk.Tk()
main_window.title("CPS843 Final Project")
main_window.geometry("1200x800")

var = tk.StringVar()
text = tk.Label(main_window, textvariable=var, relief=tk.RAISED)
text.config(font=('Helvetica bold', 26))
text.place(x=150, y=2)
var.set("VIDEO CAMERA FEED")

global camera
camera = cv2.VideoCapture(1)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

test1 = tk.Label(main_window, text="")
test1.place(x=5, y=50)


def updateCam(selection):
    global camera
    camera = cv2.VideoCapture(int(selection))


def toggleCam():
    global cam_enable
    if cam_enable == 1:
        cam_enable = 0
    else:
        cam_enable = 1
        update()


webcam_text = tk.Label(main_window, text="Select webcam ID:")
webcam_text.place(x=650, y=105)
webcamoption = tk.OptionMenu(main_window, "name", 0, 1, 2, 3, 4, command=updateCam)  # fix later
webcamoption.place(x=750, y=100)

toggle_b = tk.Button(main_window, text="Enable/Disable Camera", command=toggleCam)
toggle_b.place(x=650, y=140)


def update():
    _, frame = camera.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    out = face_mesh.process(rgb_frame)
    landmarks_points = out.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    if landmarks_points:
        landmarks = landmarks_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):  # 468:478
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            # print(x,y)
            if id == 1:
                screen_x = screen_w / frame_w * x
                screen_y = screen_h / frame_h * y
                pyautogui.moveTo(screen_x, screen_y)
        left_eye = [landmarks[145], landmarks[159]]
        for landmark in left_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        if (left_eye[0].y - left_eye[1].y) < 0.003:
            print("click")
            pyautogui.click()
            pyautogui.sleep(1)
    # cv2.imshow('video output', frame)
    # cv2.waitKey(1)
    # if keyboard.is_pressed("q"):
    #   print("quitting now...")
    #  break
    rgb_framee = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imagee = Image.fromarray(rgb_framee)
    nimg = ImageTk.PhotoImage(image=imagee)

    test1.n_img = nimg
    test1.configure(image=nimg)
    if cam_enable == 1:
        main_window.after(2, update)


update()
main_window.mainloop()
