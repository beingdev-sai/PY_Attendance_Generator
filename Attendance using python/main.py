import os
import cv2
import numpy as np
import insightface
import csv
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from tkinter import simpledialog

# Paths
KNOWN_FACES_DIR = 'known_faces'
ATTENDANCE_DIR = 'Attendance'
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)
os.makedirs(ATTENDANCE_DIR, exist_ok=True)

# Load model
model = insightface.app.FaceAnalysis(name='buffalo_l')
model.prepare(ctx_id=0)  # set to 0 for GPU, -1 for CPU

# Load known face embeddings
def load_known_faces():
    known_embeddings = []
    student_details = []
    for filename in sorted(os.listdir(KNOWN_FACES_DIR), key=lambda x: int(os.path.splitext(x)[0].split('_')[1])):
        if filename.endswith(('.jpg', '.png')):
            path = os.path.join(KNOWN_FACES_DIR, filename)
            img = cv2.imread(path)
            faces = model.get(img)
            if faces:
                known_embeddings.append(faces[0].embedding)
                name, roll = os.path.splitext(filename)[0].split('_')
                student_details.append((name, roll))
    return known_embeddings, student_details

# Cosine similarity
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Mark attendance
def mark_attendance(image_path, progress_bar):
    known_embeddings, student_details = load_known_faces()

    img = cv2.imread(image_path)
    faces = model.get(img)

    recognized_students = set()
    total = len(faces)

    for i, face in enumerate(faces):
        best_match_index = -1
        best_score = -1

        for idx, known_embedding in enumerate(known_embeddings):
            similarity = cosine_similarity(face.embedding, known_embedding)
            if similarity > best_score:
                best_score = similarity
                best_match_index = idx

        if best_score > 0.5:  # threshold for matching
            name, roll = student_details[best_match_index]
            recognized_students.add((name, roll))

        progress_bar['value'] = ((i + 1) / total) * 100
        progress_bar.update()

    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M:%S')
    filename = f"Attendance_{date_str}.csv"
    filepath = os.path.join(ATTENDANCE_DIR, filename)

    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Roll No', 'Date', 'Time'])
        for name, roll in sorted(recognized_students, key=lambda x: int(x[1])):
            writer.writerow([name, roll, date_str, time_str])

    return len(recognized_students)

# Add new face to known faces folder
def add_face(progress_bar):
    name = simpledialog.askstring("Input", "Enter student's name:")
    roll = simpledialog.askstring("Input", "Enter student's roll number:")

    if name and roll:
        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.jpg *.png')])
        if file_path:
            try:
                # Clear previous image and update UI immediately
                image_label.config(image='')
                root.update_idletasks()
                
                img = Image.open(file_path)
                img.thumbnail((400, 300))
                photo = ImageTk.PhotoImage(img)
                
                # Update image label
                image_label.config(image=photo)
                image_label.image = photo
                
                # Reset and show progress bar
                progress_bar['value'] = 0
                root.update_idletasks()

                # Process in steps
                for i in range(1, 11):
                    progress_bar['value'] = i * 10
                    root.update()
                    root.after(50)  # Small delay for smooth progress

                # Save the image
                filename = f"{name}_{roll}.jpg"
                save_path = os.path.join(KNOWN_FACES_DIR, filename)
                img_cv = cv2.imread(file_path)
                cv2.imwrite(save_path, img_cv)

                messagebox.showinfo("Success", f"Face of {name} (Roll No: {roll}) added successfully.")
                reset_gui()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process image: {str(e)}")
                reset_gui()
    else:
        messagebox.showerror("Error", "Please provide both name and roll number.")

# Reset GUI to initial state
def reset_gui():
    image_label.config(image='')
    progress_bar['value'] = 0
    label.config(text="Upload class photo for attendance")
    add_face_btn.config(state=tk.NORMAL)
    upload_btn.config(state=tk.NORMAL)
    root.update_idletasks()  # Force UI update

# GUI
root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("600x500")
root.configure(bg="#f0f8ff")
root.resizable(False, False)

# Main frame for better organization
main_frame = tk.Frame(root, bg="#f0f8ff")
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Class photo preview
image_label = tk.Label(main_frame, bg="#f0f8ff")
image_label.pack(pady=10)

# Label with clear background
label = tk.Label(main_frame, 
                text="Upload class photo for attendance", 
                font=("Arial", 16), 
                bg="#f0f8ff", 
                fg="#333")
label.pack(pady=20)

progress_bar = ttk.Progressbar(main_frame, 
                             orient="horizontal", 
                             length=400, 
                             mode='determinate')
progress_bar.pack(pady=10)

# Button frame
button_frame = tk.Frame(main_frame, bg="#f0f8ff")
button_frame.pack(pady=20)

# Browse for attendance image
def browse_image():
    upload_btn.config(state=tk.DISABLED)
    add_face_btn.config(state=tk.DISABLED)
    root.update_idletasks()  # Immediate UI update
    
    file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.jpg *.png')])
    if file_path:
        try:
            # Clear previous image immediately
            image_label.config(image='')
            root.update_idletasks()
            
            img = Image.open(file_path)
            img.thumbnail((400, 300))
            photo = ImageTk.PhotoImage(img)
            
            # Update image label
            image_label.config(image=photo)
            image_label.image = photo
            
            # Reset progress bar
            progress_bar['value'] = 0
            root.update_idletasks()

            count = mark_attendance(file_path, progress_bar)
            messagebox.showinfo("Success", f"Attendance marked for {count} student(s).")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {str(e)}")
        finally:
            reset_gui()

upload_btn = tk.Button(button_frame, 
                      text="Upload Photo", 
                      command=browse_image, 
                      font=("Arial", 12), 
                      bg="#4682b4", 
                      fg="white", 
                      width=20, 
                      height=2)
upload_btn.pack(side=tk.LEFT, padx=10)

add_face_btn = tk.Button(button_frame, 
                        text="Add New Face", 
                        command=lambda: add_face(progress_bar), 
                        font=("Arial", 12), 
                        bg="#32CD32", 
                        fg="white", 
                        width=20, 
                        height=2)
add_face_btn.pack(side=tk.LEFT, padx=10)

root.mainloop()