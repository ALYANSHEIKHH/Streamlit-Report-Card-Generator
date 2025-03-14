import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set Page Configuration
st.set_page_config(page_title="Student Report Card", layout="wide")

# Custom Styling for UI
st.markdown("""
    <style>
        body {
            background-color: #f4f4f4;
        }
        .main {
            background: #ffffff;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
        }
        .stButton>button {
            background: linear-gradient(90deg, #ff7eb3, #ff758c);
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px 20px;
            transition: 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #ff758c, #ff7eb3);
            transform: scale(1.05);
        }
        .report-card {
            background: #ffffff;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
            margin-bottom: 15px;
        }
        .chart-container {
            padding: 15px;
            border-radius: 10px;
            background: white;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State for Storing Student Data
if "students" not in st.session_state:
    st.session_state.students = []

# Header
st.markdown("<h1 style='text-align:center; color:#333;'>📜 Report Card Generator</h1>", unsafe_allow_html=True)

# Sidebar for user input
st.sidebar.header("📝 Enter Student Details")

# Input Fields
name = st.sidebar.text_input("Enter Student Name:", key="name_input")
roll_no = st.sidebar.text_input("Enter Roll Number:", key="roll_input")

# Subject List
subjects = ["Math", "Physics", "Urdu", "English", "Computer"]
marks = {}

# Input for each subject
for subject in subjects:
    marks[subject] = st.sidebar.slider(f"{subject} Marks (0-100):", 0, 100, key=f"{subject}_marks")

# Grade Calculation Function
def calculate_grade(percentage):
    if percentage >= 80:
        return "A+"
    elif percentage >= 70:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    else:
        return "F"

# Button to Generate Report Card
if st.sidebar.button("✅ Generate Report Card"):
    if name and roll_no:
        total_marks = sum(marks.values())
        percentage = (total_marks / 500) * 100
        grade = calculate_grade(percentage)

        # Store student data in session state
        st.session_state.students.append({
            "name": name,
            "roll_no": roll_no,
            "marks": marks,
            "total_marks": total_marks,
            "percentage": percentage,
            "grade": grade
        })

        st.sidebar.success(f"✅ Report Card for {name} generated successfully!")

# Display All Report Cards
st.markdown("<h2 style='text-align:center; color:#444;'>📄 Student Report Cards</h2>", unsafe_allow_html=True)

if len(st.session_state.students) > 0:
    for student in st.session_state.students:
        with st.container():
            st.markdown(f"""
                <div class="report-card">
                    <h4>👤 <b>Student Name:</b> {student['name']}</h4>
                    <p>🎟 <b>Roll Number:</b> {student['roll_no']}</p>
                    <p>📊 <b>Total Marks:</b> {student['total_marks']} / 500</p>
                    <p>📈 <b>Percentage:</b> {student['percentage']:.2f}%</p>
                    <p>🏅 <b>Grade:</b> {student['grade']}</p>
                </div>
            """, unsafe_allow_html=True)

            # Data for Visualization
            df = pd.DataFrame(list(student["marks"].items()), columns=["Subject", "Marks"])

            # Marks Visualization - Bar Chart
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(df["Subject"], df["Marks"], color=["#ff5733", "#33ff57", "#3357ff", "#ff33a8", "#33fff5"])
            plt.xlabel("Subjects")
            plt.ylabel("Marks")
            plt.title(f"{student['name']}'s Marks Distribution")
            plt.grid(axis="y", linestyle="--", alpha=0.7)

            st.pyplot(fig)

# # Reset Button to Clear All Data
# if st.button("🗑 Reset All Data"):
#     st.session_state.students = []
#     st.rerun()










# Step-by-Step Working of the Program
# Ask for Student Information

# Enter Name and Roll Number.
# Enter marks for Math, Physics, Urdu, English, and Computer (0-100 only).
# Store Data & Ask to Continue

# Saves the student’s details.
# Asks: "Do you want to insert more?"
# Press 'Y' to add another student, 'N' to stop.
# Calculate Results

# Adds up total marks (out of 500).
# Calculates percentage.
# Assigns grades based on percentage:
# 80%+ → A+
# 70-79% → A
# 60-69% → B
# 50-59% → C
# Below 50% → F
# Generate Report Cards

# Displays student details, marks, total, percentage, and grade.
# Error Handling

# Ensures valid marks (0-100).
# Only allows 'Y' or 'N' for choices.
# 👉 Final Output: A formatted report card for each student! 🎓










# This code is an interactive student report card generator built using Streamlit with a beautiful and user-friendly UI. Here's a breakdown of how it works:

# 🔹 1. Setup & UI Customization
# Imports Streamlit, Pandas, and Matplotlib to handle the UI, data, and graphs.
# st.set_page_config() sets the page title, icon, and layout.
# Adds a Sidebar where users input student details.
# 🔹 2. User Inputs (Student Details)
# User enters name and roll number.
# Marks are entered via sliders for subjects like Math, Physics, Urdu, etc.
# A button ("✅ Generate Report Card") triggers the report generation.
# 🔹 3. Report Card Generation
# calculate_grade() function assigns grades based on percentage.
# Displays the student’s marks in a table for clarity.
# Shows total marks, percentage, and grade in a structured format.
# 🔹 4. Data Visualization (Extraordinary Feature 🎨)
# A bar chart is generated using Matplotlib to visualize marks.
# The graph displays subject-wise scores, making it easier to analyze performance.
# 🔹 5. Dynamic Student Entries
# After generating one report card, the app asks if the user wants to add another student.
# If the user selects "No", a thank-you message appears, and the program stops.