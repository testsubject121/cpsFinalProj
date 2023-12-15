import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import keyboard
import tkinter as tk
import PIL
from PIL import ImageTk, Image

global cam_enable
cam_enable = 1

contrast = 0
brightness = 0
gauss = 0
remove_gauss = 0
tracking = 1


main_window = tk.Tk()
main_window.title("CPS843 Final Project")
main_window.geometry("1000x550")

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

#slider variables
contrast_text = tk.Label(main_window, text="Adjust Contrast")
contrast_text.place(x=650, y=200)
contrast_s = tk.Scale(main_window, from_=0, to=100, length=200, orient=tk.HORIZONTAL)
contrast_s.place(x=750, y=180)
contrast_s.set(10)

brightness_text = tk.Label(main_window, text="Adjust brightness")
brightness_text.place(x=650, y=250)
brightness_s = tk.Scale(main_window, from_=-127, to=127, length=200, orient=tk.HORIZONTAL)
brightness_s.place(x=750, y=230)

gaussian_noise_text = tk.Label(main_window, text="Adjust gauss noise")
gaussian_noise_text.place(x=650, y=300)
gaussian_noise_s = tk.Scale(main_window, from_=0, to=200, length=200, orient=tk.HORIZONTAL)
gaussian_noise_s.place(x=750, y=280)

noise_removal_text = tk.Label(main_window, text="Noise Removal")
noise_removal_text.place(x=650, y=350)
noise_removal_s = tk.Scale(main_window, from_=0, to=20, length=200, orient=tk.HORIZONTAL)
noise_removal_s.place(x=750, y=320)

en_l = tk.Label(main_window, text="Tracking enabled. Use Ctrl-s to disable")
en_l.place(x=680,y=50)

def toggleTracking(selection):
    global tracking
    if tracking == 1:
        tracking = 0
        en_l.config(text="Tracking disabled. Use Ctrl-s to enable")
    else:
        tracking = 1
        en_l.config(text="Tracking enabled. Use Ctrl-s to disable")

main_window.bind("<Control-s>", toggleTracking)

def updateVals():
    global contrast
    contrast = contrast_s.get()
    global brightness
    brightness = brightness_s.get()
    global gauss
    gauss = gaussian_noise_s.get()
    global remove_gauss
    remove_gauss = noise_removal_s.get()

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

def add_gaussian_noise(image, mean=0, sigma=25):
    # Generate random Gaussian noise
    row, col, ch = image.shape
    gauss = np.random.normal(mean, sigma, (row, col, ch))

    # Add the noise to the image
    noisy = image + gauss

    # Clip values to be in the valid range [0, 255]
    noisy = np.clip(noisy, 0, 255)

    return noisy.astype(np.uint8)

def remove_gaussian_noise(image, kernel_size=(5, 5), sigma=1.5):
    # Apply Gaussian blur to the image
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)

    return blurred

webcam_text = tk.Label(main_window, text="Select webcam ID:")
webcam_text.place(x=650, y=105)
webcamoption = tk.OptionMenu(main_window, "name", 0, 1, 2, 3, 4, command=updateCam)  # fix later
webcamoption.place(x=750, y=100)

toggle_b = tk.Button(main_window, text="Enable/Disable Camera", command=toggleCam)
toggle_b.place(x=650, y=140)


def update():
    global brightness
    global contrast
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
                if tracking == 1:
                    pyautogui.moveTo(screen_x, screen_y)
        left_eye = [landmarks[145], landmarks[159]]
        for landmark in left_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        if (left_eye[0].y - left_eye[1].y) < 0.003:
            print("click")
            if tracking == 1:
                pyautogui.click()
                pyautogui.sleep(1)
    # cv2.imshow('video output', frame)
    # cv2.waitKey(1)
    # if keyboard.is_pressed("q"):
    #   print("quitting now...")
    #  break
    rgb_framee = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #image processing...
    updateVals()
    #rgb_framee = cv2.convertScaleAbs(rgb_framee, rgb_framee, contrast/10, brightness)
    rgb_framee = cv2.addWeighted(rgb_framee, contrast/10, rgb_framee, 0, brightness)#contrast and brightness
    if gauss > 0:
        rgb_framee = add_gaussian_noise(rgb_framee, gauss, gauss)#gauss noise
    if remove_gauss > 0:
        rgb_framee = remove_gaussian_noise(rgb_framee, (5,5), remove_gauss)#gauss blur
    imagee = Image.fromarray(rgb_framee)
    nimg = ImageTk.PhotoImage(image=imagee)

    test1.n_img = nimg
    test1.configure(image=nimg)
    if cam_enable == 1:
        main_window.after(2, update)


update()
main_window.mainloop()
