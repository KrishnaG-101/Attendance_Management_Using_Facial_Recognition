import os
import time
import numpy as np
import pandas as pd
import csv
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
from datetime import datetime

class AttendanceSystem:
    def __init__(self, window):
        self.window = window
        self.window.title("Face Attendance")
        self.window.geometry("1200x500")
        # self.window.state("zoomed")
        self.detector = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")
        self.cap = None
        self.is_camera_on = False
        self.face_id = None
        self.create_widgets()

    def create_widgets(self):
        header = tk.Label(
            self.window,
            text="Attendance Management System Using Facial Recognition",
            bg="#4470cf",
            fg="white",
            font=('times', 30, 'bold'),
            width=55,
            height=2,
        )
        header.place(x=-50, y=0)

        tk.Label(self.window, text="Enrollment Number", fg="#000000", font=('times', 18, 'bold')).place(x=200, y=150)
        self.enrollment_txt = tk.Entry(self.window, width=25, font=('times', 18))
        self.enrollment_txt.place(x=420, y=150)

        tk.Label(self.window, text="Student Name", fg="#000000", font=('times', 18, 'bold')).place(x=200, y=220)
        self.name_txt = tk.Entry(self.window, width=25, font=('times', 18))
        self.name_txt.place(x=420, y=220)

        self.close_camera_button = tk.Button(
            self.window,
            text = "Close Camera",
            command = self.stop_camera,
            bg = "#e8b81c",
            fg = "black",
            font = ('arial', 15, 'bold'),
            state = tk.DISABLED,
        )
        self.close_camera_button.place(x=950, y=200)

        self.take_img_button = tk.Button(
            self.window,
            text="Take Images",
            command=self.toggle_camera,
            bg="#35a2e6",
            fg="black",
            font=('arial', 15, 'bold'),
        )
        self.take_img_button.place(x=225, y=320)

        self.train_img_button = tk.Button(
            self.window,
            text="Train Images",
            command=self.train_img,
            bg="#35a2e6",
            fg="black",
            font=('arial', 15, 'bold'),
        )
        self.train_img_button.place(x=455, y=320)

        self.smart_att_button = tk.Button(
            self.window,
            text="Smart Attendance",
            command=self.smart_attendance_window,
            bg="#35a2e6",
            fg="black",
            font=('arial', 15, 'bold'),
        )
        self.smart_att_button.place(x=685, y=320)

        self.manual_att_button = tk.Button(
            self.window,
            text="Manual Attendance",
            command=self.manual_attendance_window,
            bg="#35a2e6",
            fg="black",
            font=('arial', 15, 'bold'),
        )
        self.manual_att_button.place(x=930, y=320)

        self.admin_panel_button = tk.Button(
            self.window,
            text="Admin Panel",
            command=self.admin_panel,
            bg="#db1859",
            fg="black",
            font=('arial', 15, 'bold'),
        )
        self.admin_panel_button.place(x=225, y=420)

    def toggle_camera(self):
        if not self.validate_inputs():
            return
        if self.is_camera_on:
            self.stop_camera()
        else:
            self.is_camera_on = True
            self.capture_images()
            self.close_camera_button.config(state=tk.NORMAL)  # Enable the Close Camera button

    def capture_images(self):
        self.cap = cv2.VideoCapture(0)
        count = 0
        if not os.path.exists("./Training_Images"):
            os.makedirs("./Training_Images")

        csv_file_path = "./student_details/student_details.csv"
        if not os.path.exists("./student_details"):
            os.makedirs("./student_details")

        while self.is_camera_on:
            ret, frame = self.cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
            for (x, y, w, h) in faces:
                count += 1
                image_path = f"./Training_Images/{self.name_txt.get().strip()}.{self.face_id}.{count}.jpg"
                cv2.imwrite(image_path, gray[y:y+h, x:x+w])
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                if count >= 10:
                    self.update_student_details_csv(csv_file_path)
                    messagebox.showinfo("Success", "Images Captured and Details Saved Successfully!")
                    return

            cv2.imshow("Capture Images", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cv2.destroyAllWindows()

    def update_student_details_csv(self, csv_file_path):
        enrollment = self.enrollment_txt.get().strip()
        name = self.name_txt.get().strip()
        with open(csv_file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([enrollment, name, time.strftime("%Y-%m-%d %H:%M:%S")])

    def validate_inputs(self):
        enrollment = self.enrollment_txt.get().strip()
        name = self.name_txt.get().strip()
        if not enrollment.isdigit() or not name.isalpha():
            messagebox.showerror("Error", "Please enter valid enrollment and name.")
            return False
        self.face_id = int(enrollment)
        return True

    def stop_camera(self):
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()
        self.is_camera_on = False
        self.close_camera_button.config(state=tk.DISABLED)

    def train_img(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        faces, ids = self.get_images_and_labels("./Training_Images")
        recognizer.train(faces, np.array(ids))
        recognizer.save("./Training_Image_Label/trainner.yml")
        messagebox.showinfo("Success", "Model Trained Successfully!")

    def get_images_and_labels(self, path):
        image_paths = [os.path.join(path, f) for f in os.listdir(path)]
        faces = []
        ids = []
        for image_path in image_paths:
            img = Image.open(image_path).convert("L")
            img_np = np.array(img, "uint8")
            id = int(os.path.split(image_path)[-1].split(".")[1])
            faces.append(img_np)
            ids.append(id)
        return faces, ids

    def smart_attendance_window(self):
        self.smart_window = tk.Toplevel(self.window)
        self.smart_window.title("Smart Attendance")
        self.smart_window.geometry("600x400")
        tk.Label(self.smart_window, text="Enter Subject", font=('times', 14)).pack(pady=20)
        self.subject_entry = tk.Entry(self.smart_window, font=('times', 14))
        self.subject_entry.pack(pady=10)
        tk.Button(self.smart_window, text="Start Attendance", command=self.start_smart_attendance, font=('times', 14), bg="SkyBlue1").pack(pady=10)

    def start_smart_attendance(self):
        subject = self.subject_entry.get().strip()
        if not subject:
            messagebox.showerror("Error", "Please enter a subject.")
            return
        
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("./Training_Image_Label/trainner.yml")
        cap = cv2.VideoCapture(0)
        self.is_camera_on = True
        self.close_camera_button.config(state=tk.NORMAL)  # Enable the Close Camera button
        
        attendance_marked = False

        while self.is_camera_on:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
            for (x, y, w, h) in faces:
                id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
                if confidence < 100:  # Recognition is confident
                    self.mark_attendance(id, subject)
                    messagebox.showinfo("Attendance", f"Attendance marked for ID: {id}.")
                    attendance_marked = True
                    break
            
            if attendance_marked:
                break  # Exit the loop after marking one attendance
            
            cv2.imshow("Smart Attendance", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Option to quit manually
                break

        cap.release()
        cv2.destroyAllWindows()
        self.is_camera_on = False
        self.close_camera_button.config(state=tk.DISABLED)  # Disable the Close Camera button

    def mark_attendance(self, student_id, subject):
        folder = "./smart_attendance"
        if not os.path.exists(folder):
            os.makedirs(folder)
        date_str = datetime.now().strftime("%Y-%m")
        filename = os.path.join(folder, f"{subject}_{date_str}.csv")
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([student_id, time.strftime("%Y-%m-%d %H:%M:%S")])

    def manual_attendance_window(self):
        manually_window = tk.Toplevel(self.window)
        manually_window.title("Manual Attendance")
        manually_window.geometry("600x400")
        tk.Label(manually_window, text="Enrollment number", font=('times', 14)).grid(row=0, column=0)
        enrollment_entry = tk.Entry(manually_window, font=('times', 14))
        enrollment_entry.grid(row=0, column=2)
        tk.Label(manually_window, text="Enter Name", font=('times', 14)).grid(row=1, column=0)
        name_entry = tk.Entry(manually_window, font=('times', 14))
        name_entry.grid(row=1, column=2)
        tk.Label(manually_window, text="Enter Subject", font=('times', 14)).grid(row=2, column=0)
        subject_entry = tk.Entry(manually_window, font=('times', 14))
        subject_entry.grid(row=2, column=2)
        tk.Button(manually_window, text="Submit", font=('times', 14), bg="SkyBlue1", command=lambda: self.submit_manual_attendance(enrollment_entry, name_entry, subject_entry)).grid(row=4, column=2)

    def submit_manual_attendance(self, enrollment_entry, name_entry, subject_entry):
        enrollment = enrollment_entry.get().strip()
        name = name_entry.get().strip()
        subject = subject_entry.get().strip()
        if not enrollment or not name or not subject:
            messagebox.showerror("Error", "All fields are required.")
            return
        folder = "./manual_attendance"
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(os.path.join(folder, "attendance.csv"), mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([enrollment, name, subject, time.strftime("%Y-%m-%d %H:%M:%S")])
        messagebox.showinfo("Success", "Attendance marked successfully!")

    def admin_panel(self):
        self.admin_window = tk.Toplevel(self.window)
        self.admin_window.title("Admin Panel")
        self.admin_window.geometry("800x500")
        self.load_registered_students()

    def load_registered_students(self):
        try:
            student_data = pd.read_csv("./student_details/student_details.csv", on_bad_lines="skip")
            for idx, student in student_data.iterrows():
                tk.Label(self.admin_window, text=f"ID: {student['Enrollment']} - Name: {student['Name']}", font=('times', 12)).pack(pady=5)
        except FileNotFoundError:
            messagebox.showerror("Error", "No registered students found.")

    def on_closing(self):
        self.stop_camera()
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceSystem(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
