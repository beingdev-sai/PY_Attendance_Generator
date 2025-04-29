#  Face Recognition Attendance System

An easy-to-use GUI-based application for marking student attendance by recognizing faces in class photos, using InsightFace deep learning models.

---

##  Features
- Upload student images to build a face database.
- Upload a class group photo to automatically mark attendance.
- Progress bar for real-time feedback during processing.
- Attendance is saved as a CSV file (`Attendance_<date>.csv`).
- Simple and intuitive GUI using Tkinter.

---

##  Requirements
Install the following Python libraries before running the project:
```bash
pip install opencv-python insightface pillow
```

Ensure you have Python 3.10 or later installed.

---

##  Project Structure
```plaintext
/
├── Attendance/         # Folder where daily attendance CSV files are saved
├── known_faces/        # Folder storing known student faces
├── your_script.py      # Main Python code
└── README.md           # (This file)
```

---

##  How to Add New Student Faces
1. Run the program (`python your_script.py`).
2. Click the **"Add New Face"** button.
3. Enter the student's **name** and **roll number** when prompted.
4. Choose a **clear face photo** of the student.
5. The system saves it into `known_faces/` as `Name_RollNo.jpg`.

---

##  How to Mark Attendance
1. Click the **"Upload Photo"** button.
2. Select a **class group photo** containing students' faces.
3. The system detects and recognizes faces, marking attendance for known students.
4. Attendance is saved automatically in the `Attendance/` folder as a CSV file.
   - Example: `Attendance_2025-04-28.csv`
5. A popup shows how many students were successfully recognized.

---

##  Attendance CSV Format
Each attendance file will contain:
| Name | Roll No | Date | Time |
|:----:|:-------:|:----:|:----:|

---

##  Notes
- Only images (`.jpg`, `.png`) are supported.
- Matching threshold is set at **0.5** cosine similarity.
- Each day generates a **new** attendance CSV file.
- Unknown faces (not added beforehand) will be **ignored** during attendance marking.

---

##  Tips
- Use **clear, front-facing** photos for best recognition accuracy.
- You can re-train by simply replacing images in `known_faces/`.
- Make sure names and roll numbers are unique to avoid overwriting files.

---

