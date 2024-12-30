# Attendance Management Using Facial Recognition

Attendance Management System using facial recognition is a simple python based GUI desktop application for organizations and institutions to set up an automated attendance system that would require facial identification of the student to mark attendance. The application provies various features to mark and monitor attendance of students.

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)                 
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3128/) 
---

## Table of Contents
[Installation Guide](#installation-guide)\
[Features](#features)\
[Technologies Used](#technologies-used)\
[Usage Guide](#usage-guide)\
[Overview and Screenshots](#overview-and-screenshots)

---

## Installation Guide

### Prerequisites
```bash
python 3.7 or above
webcam
```

### Installation
1. **Clone the Repository and go to project folder**
```bash
git clone https://github.com/KrishnaG-101/Attendance_Management_Using_Facial_Recognition.git
cd Attendance_Management_Using_Facial_Recognition
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Open VS Code or Terminal in the project folder**\
   note: it is recommended to scrictly open terminal inside project folder or you must change file paths inside `main.py`

5. **Run the Application**
```bash
python main.py
```
---

## Features
- **Face Recognition**: Automatically recognize students' faces and mark their attendance.
- **Image Capture**: Capture and save images for training the recognition model.
- **Manual Attendance**: Option to manually fill attendance records.
- **CSV Export**: Generate attendance reports in CSV format.
---

## Technologies Used
- **Python**
- **Tkinter**
- **OpenCV**
- **CSV**
- **PIL**
- **Pandas**
- **Numpy**
---

## Usage Guide
### 1. Capture Images
- Run `main.py` to open the GUI.
- Enter the student's enrollment number and name.
- Click on **"Take Images"** to capture their face images.

### 2. Train the Model
- After capturing images, click on **"Train Images"** to train the face recognition model.

### 3. Automatic Attendance
- Select **"Smart Attendance"** and enter subject to mark automatic attendance.

### 4. Manual Attendance
- Use the **"Manually Attendance"** option to manually fill attendance records.

### 5. View Registered Students
- Access the **"Admin Panel"** to view the list of registered students and their details.
---

## Overview and Screenshots
### 1. Main Console
The Application Interface of the project is made using Tkinter library in python.

![screenshot of main console](https://github.com/user-attachments/assets/a3a7b6a4-c166-4d29-a0bf-75ad45f44929)

### 2. Take images
The **Take Images** option is used to take images of the new student which has to be registers, upon using this option a camera window opens taking images of the student which are then automatically saved into desired folder.

![screenshot of using take images option](https://github.com/user-attachments/assets/e77ccef0-cde0-4d60-874b-f662cf1c2e7d)

### 3. Train images
The train images option feeds the taken images to image recognition model along with student details, so that the student’s facial features are mapped with its details.

![screenshot of using train images option](https://github.com/user-attachments/assets/6f3ba24c-5a7b-4c94-a17a-0af596db9cb4)

### 4. Smart Attendance
Smart Attendance option is used to mark automatic attendance for any entered subject, the camera is used to mark attendance.

![screenshot of using smart attendance option](https://github.com/user-attachments/assets/19aa47e6-a18f-4228-9358-6e757fd59c82)

### 5. Manual Attendance
Manual Attendance option is used to mark attendance manually, this option can be used in case of camera or lighting issues, when video feed cannot work properly.

![screenshot of using manual attendance option](https://github.com/user-attachments/assets/f2811260-a6a7-48c6-9e1d-cc34ea6c2396)
