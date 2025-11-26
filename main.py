import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import json

# Set Page Configuration
st.set_page_config(page_title="Advanced Student Report Card System", layout="wide", initial_sidebar_state="expanded")

# Custom Styling for UI
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .main {
            background: #ffffff;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.3);
        }
        
        .stButton>button {
            background: linear-gradient(90deg, #ff7eb3, #ff758c);
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 12px 24px;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0px 4px 15px rgba(255, 126, 179, 0.4);
        }
        
        .stButton>button:hover {
            background: linear-gradient(90deg, #ff758c, #ff7eb3);
            transform: translateY(-2px);
            box-shadow: 0px 6px 20px rgba(255, 126, 179, 0.6);
        }
        
        .report-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0px 8px 20px rgba(0,0,0,0.15);
            margin-bottom: 20px;
            border-left: 5px solid #667eea;
        }
        
        .insight-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
            box-shadow: 0px 8px 25px rgba(102, 126, 234, 0.4);
        }
        
        .recommendation {
            background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
            border-left: 5px solid #3b82f6;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .recommendation:hover {
            transform: translateX(5px);
            box-shadow: 0px 4px 12px rgba(59, 130, 246, 0.3);
        }
        
        .strength {
            background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
            border-left: 5px solid #22c55e;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .strength:hover {
            transform: translateX(5px);
            box-shadow: 0px 4px 12px rgba(34, 197, 94, 0.3);
        }
        
        .weakness {
            background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
            border-left: 5px solid #ef4444;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .weakness:hover {
            transform: translateX(5px);
            box-shadow: 0px 4px 12px rgba(239, 68, 68, 0.3);
        }
        
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0px 8px 25px rgba(0,0,0,0.15);
        }
        
        .achievement-badge {
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            display: inline-block;
            margin: 5px;
            font-weight: bold;
            box-shadow: 0px 4px 10px rgba(251, 191, 36, 0.4);
        }
        
        .progress-bar-container {
            background: #e5e7eb;
            border-radius: 10px;
            height: 25px;
            margin: 10px 0;
            overflow: hidden;
        }
        
        .progress-bar {
            height: 100%;
            border-radius: 10px;
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        
        .tab-content {
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "students" not in st.session_state:
    st.session_state.students = []
if "class_settings" not in st.session_state:
    st.session_state.class_settings = {
        "passing_percentage": 40,
        "excellence_threshold": 85,
        "class_name": "Class 10-A"
    }

# Advanced AI Analysis Function with Predictive Features
def generate_performance_analysis(student_data):
    """Generate intelligent insights and recommendations based on student performance"""
    marks = student_data['marks']
    percentage = student_data['percentage']
    
    # Calculate statistics
    marks_list = list(marks.values())
    avg_marks = np.mean(marks_list)
    std_dev = np.std(marks_list)
    max_mark = max(marks_list)
    min_mark = min(marks_list)
    
    # Identify strengths and weaknesses
    strengths = {subject: mark for subject, mark in marks.items() if mark >= avg_marks + std_dev/2}
    weaknesses = {subject: mark for subject, mark in marks.items() if mark < avg_marks - std_dev/2}
    consistent = {subject: mark for subject, mark in marks.items() 
                  if subject not in strengths and subject not in weaknesses}
    
    # Generate performance category
    if percentage >= 85:
        performance_category = "🏆 Exceptional"
        overall_comment = "Outstanding performance! You're among the top performers."
        emoji = "🌟"
    elif percentage >= 75:
        performance_category = "⭐ Excellent"
        overall_comment = "Excellent work! Keep maintaining this momentum."
        emoji = "🎯"
    elif percentage >= 60:
        performance_category = "👍 Good"
        overall_comment = "Good performance. Focus on consistency for even better results."
        emoji = "📈"
    elif percentage >= 50:
        performance_category = "📚 Satisfactory"
        overall_comment = "Satisfactory results. More dedication needed for improvement."
        emoji = "💪"
    elif percentage >= 40:
        performance_category = "⚠️ Needs Improvement"
        overall_comment = "Requires focused effort. Don't lose hope, improvement is possible!"
        emoji = "📖"
    else:
        performance_category = "🚨 Critical"
        overall_comment = "Immediate intervention required. Let's work together on a recovery plan."
        emoji = "🆘"
    
    # Achievement badges
    badges = []
    if percentage >= 90:
        badges.append("🥇 Gold Medalist")
    elif percentage >= 80:
        badges.append("🥈 Silver Achiever")
    elif percentage >= 70:
        badges.append("🥉 Bronze Performer")
    
    if std_dev < 8:
        badges.append("⚖️ Consistency Champion")
    
    if max_mark == 100:
        badges.append("💯 Perfect Score")
    
    if all(mark >= 75 for mark in marks_list):
        badges.append("🌟 All-Rounder")
    
    # Subject-specific recommendations
    recommendations = {}
    for subject, mark in marks.items():
        if mark >= 90:
            recommendations[subject] = "🎓 Outstanding! Consider advanced topics or mentoring peers."
        elif mark >= 80:
            recommendations[subject] = "📚 Excellent! Aim for perfection with targeted practice."
        elif mark >= 70:
            recommendations[subject] = "✍️ Good work! Focus on mastering complex concepts."
        elif mark >= 60:
            recommendations[subject] = "📖 Decent foundation. Practice 45 mins daily for improvement."
        elif mark >= 50:
            recommendations[subject] = "⚠️ Needs attention. Consider group study or tutoring."
        elif mark >= 40:
            recommendations[subject] = "🚨 Critical! Immediate focus required with teacher support."
        else:
            recommendations[subject] = "🆘 Urgent intervention needed. One-on-one coaching recommended."
    
    # Consistency analysis
    if std_dev < 8:
        consistency_note = "Highly consistent across all subjects"
        consistency_color = "#22c55e"
    elif std_dev < 15:
        consistency_note = "Moderate variation in performance"
        consistency_color = "#f59e0b"
    else:
        consistency_note = "High variation - balance needed"
        consistency_color = "#ef4444"
    
    # Predicted improvement
    improvement_potential = calculate_improvement_potential(marks, avg_marks)
    
    return {
        "performance_category": performance_category,
        "overall_comment": overall_comment,
        "emoji": emoji,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "consistent": consistent,
        "recommendations": recommendations,
        "consistency_note": consistency_note,
        "consistency_color": consistency_color,
        "avg_marks": avg_marks,
        "std_dev": std_dev,
        "max_mark": max_mark,
        "min_mark": min_mark,
        "badges": badges,
        "improvement_potential": improvement_potential
    }

def calculate_improvement_potential(marks, avg_marks):
    """Calculate potential for improvement in next assessment"""
    potential = {}
    for subject, mark in marks.items():
        if mark < 50:
            potential[subject] = min(mark + 20, 75)
        elif mark < 70:
            potential[subject] = min(mark + 15, 85)
        elif mark < 85:
            potential[subject] = min(mark + 10, 95)
        else:
            potential[subject] = min(mark + 5, 100)
    return potential

def calculate_grade(percentage):
    """Calculate letter grade based on percentage"""
    if percentage >= 90:
        return "A+", "#22c55e"
    elif percentage >= 80:
        return "A", "#84cc16"
    elif percentage >= 70:
        return "B+", "#eab308"
    elif percentage >= 60:
        return "B", "#f59e0b"
    elif percentage >= 50:
        return "C", "#f97316"
    elif percentage >= 40:
        return "D", "#ef4444"
    else:
        return "F", "#991b1b"

def export_report_data(student):
    """Export student report as JSON"""
    return json.dumps(student, indent=2)

# Header with animated title
st.markdown("""
    <div style='text-align:center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    border-radius: 15px; margin-bottom: 30px; box-shadow: 0px 8px 25px rgba(102, 126, 234, 0.4);'>
        <h1 style='color: white; margin: 0; font-size: 2.5em;'>🎓 Advanced Student Report Card System</h1>
        <p style='color: #e0e7ff; margin: 10px 0 0 0; font-size: 1.1em;'>
            Powered by AI Analytics & Predictive Insights
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.header("⚙️ System Configuration")

# Class Settings Expander
with st.sidebar.expander("🏫 Class Settings", expanded=False):
    st.session_state.class_settings["class_name"] = st.text_input(
        "Class Name", 
        value=st.session_state.class_settings["class_name"]
    )
    st.session_state.class_settings["passing_percentage"] = st.slider(
        "Passing Percentage", 
        0, 100, 
        st.session_state.class_settings["passing_percentage"]
    )
    st.session_state.class_settings["excellence_threshold"] = st.slider(
        "Excellence Threshold", 
        0, 100, 
        st.session_state.class_settings["excellence_threshold"]
    )

st.sidebar.markdown("---")
st.sidebar.header("📝 Enter Student Details")

# Input Fields
name = st.sidebar.text_input("👤 Student Name:", key="name_input", placeholder="Enter full name")
roll_no = st.sidebar.text_input("🎟️ Roll Number:", key="roll_input", placeholder="e.g., 2024001")

# Date of Assessment
assessment_date = st.sidebar.date_input("📅 Assessment Date:", datetime.now())

# Subject configuration with custom subjects option
st.sidebar.markdown("### 📚 Subject Marks (out of 100)")

use_custom_subjects = st.sidebar.checkbox("Use Custom Subjects")

if use_custom_subjects:
    num_subjects = st.sidebar.number_input("Number of Subjects", min_value=1, max_value=10, value=5)
    subjects = []
    marks = {}
    for i in range(num_subjects):
        subject_name = st.sidebar.text_input(f"Subject {i+1} Name", key=f"subject_name_{i}", value=f"Subject {i+1}")
        subjects.append(subject_name)
        marks[subject_name] = st.sidebar.slider(f"{subject_name} Marks:", 0, 100, key=f"{subject_name}_marks")
else:
    subjects = ["Math", "Physics", "Urdu", "English", "Computer"]
    marks = {}
    for subject in subjects:
        marks[subject] = st.sidebar.slider(f"{subject} Marks:", 0, 100, key=f"{subject}_marks")

# Attendance tracking
attendance_percentage = st.sidebar.slider("📊 Attendance %:", 0, 100, 85)

# Conduct rating
conduct = st.sidebar.select_slider(
    "🎭 Conduct Rating:",
    options=["Poor", "Fair", "Good", "Very Good", "Excellent"],
    value="Good"
)

# Teacher's remarks
teacher_remarks = st.sidebar.text_area(
    "📝 Teacher's Remarks (Optional):",
    placeholder="Enter additional comments..."
)

# Action Buttons
col_btn1, col_btn2 = st.sidebar.columns(2)

with col_btn1:
    generate_btn = st.button("✅ Generate Report", use_container_width=True)

with col_btn2:
    clear_btn = st.button("🗑️ Clear All", use_container_width=True)

# Generate Report Card Logic
if generate_btn:
    if name and roll_no:
        total_marks = sum(marks.values())
        max_possible = len(subjects) * 100
        percentage = (total_marks / max_possible) * 100
        grade, grade_color = calculate_grade(percentage)

        # Store student data
        student_data = {
            "name": name,
            "roll_no": roll_no,
            "marks": marks,
            "total_marks": total_marks,
            "max_possible": max_possible,
            "percentage": percentage,
            "grade": grade,
            "grade_color": grade_color,
            "assessment_date": str(assessment_date),
            "attendance": attendance_percentage,
            "conduct": conduct,
            "teacher_remarks": teacher_remarks,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        st.session_state.students.append(student_data)
        st.sidebar.success(f"✅ Report for {name} generated successfully!")
    else:
        st.sidebar.error("⚠️ Please enter both name and roll number!")

# Clear All Logic
if clear_btn:
    st.session_state.students = []
    st.sidebar.success("🗑️ All reports cleared!")
    st.rerun()

# Main Content Area
if len(st.session_state.students) > 0:
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Individual Reports", 
        "📊 Class Analytics", 
        "📈 Performance Trends",
        "🏆 Rankings & Achievements"
    ])
    
    # TAB 1: Individual Reports
    with tab1:
        st.markdown("<h2 style='text-align:center; color:#444;'>📄 Detailed Student Reports</h2>", unsafe_allow_html=True)
        
        # Student selector
        student_names = [s['name'] for s in st.session_state.students]
        selected_student = st.selectbox("Select Student to View:", student_names)
        
        # Find selected student
        student = next(s for s in st.session_state.students if s['name'] == selected_student)
        
        # Display Report Card Header
        st.markdown(f"""
            <div class="report-card">
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <h2 style='margin: 0; color: #667eea;'>👤 {student['name']}</h2>
                        <p style='margin: 5px 0; color: #666;'>🎟️ Roll No: {student['roll_no']} | 📅 {student['assessment_date']}</p>
                    </div>
                    <div style='text-align: right;'>
                        <h1 style='margin: 0; color: {student['grade_color']}; font-size: 3em;'>{student['grade']}</h1>
                        <p style='margin: 0; color: #666;'>Grade</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Key Metrics Row
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <h3 style='color: #667eea; margin: 0;'>{student['total_marks']}</h3>
                    <p style='color: #666; margin: 5px 0;'>Total Marks</p>
                    <small style='color: #999;'>out of {student['max_possible']}</small>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <h3 style='color: #22c55e; margin: 0;'>{student['percentage']:.2f}%</h3>
                    <p style='color: #666; margin: 5px 0;'>Percentage</p>
                    <small style='color: #999;'>Overall Score</small>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <h3 style='color: #f59e0b; margin: 0;'>{student['attendance']}%</h3>
                    <p style='color: #666; margin: 5px 0;'>Attendance</p>
                    <small style='color: #999;'>Class Presence</small>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <h3 style='color: #8b5cf6; margin: 0;'>{student['conduct']}</h3>
                    <p style='color: #666; margin: 5px 0;'>Conduct</p>
                    <small style='color: #999;'>Behavior Rating</small>
                </div>
            """, unsafe_allow_html=True)
        
        with col5:
            avg_mark = sum(student['marks'].values()) / len(student['marks'])
            st.markdown(f"""
                <div class="metric-card">
                    <h3 style='color: #ec4899; margin: 0;'>{avg_mark:.1f}</h3>
                    <p style='color: #666; margin: 5px 0;'>Average</p>
                    <small style='color: #999;'>Per Subject</small>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Generate AI Analysis
        analysis = generate_performance_analysis(student)
        
        # AI Insights Box
        st.markdown(f"""
            <div class="insight-box">
                <h2 style='margin-top: 0;'>🤖 AI Performance Analysis</h2>
                <h3>{analysis['emoji']} Performance Level: {analysis['performance_category']}</h3>
                <p style='font-size: 1.1em;'>{analysis['overall_comment']}</p>
                <div style='margin-top: 15px;'>
                    <strong>📊 Statistics:</strong> 
                    Average: {analysis['avg_marks']:.1f} | 
                    Highest: {analysis['max_mark']} | 
                    Lowest: {analysis['min_mark']} | 
                    Std Dev: {analysis['std_dev']:.2f}
                </div>
                <div style='margin-top: 10px;'>
                    <strong>⚖️ Consistency:</strong> 
                    <span style='color: {analysis['consistency_color']}; font-weight: bold;'>
                        {analysis['consistency_note']}
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Achievement Badges
        if analysis['badges']:
            st.markdown("### 🏅 Achievement Badges")
            badges_html = "".join([f'<span class="achievement-badge">{badge}</span>' for badge in analysis['badges']])
            st.markdown(f'<div style="text-align: center; margin: 20px 0;">{badges_html}</div>', unsafe_allow_html=True)
        
        # Visualizations Row
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            st.markdown("### 📊 Subject-wise Performance")
            df = pd.DataFrame(list(student["marks"].items()), columns=["Subject", "Marks"])
            
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ['#22c55e' if mark >= analysis['avg_marks'] else '#ef4444' for mark in df["Marks"]]
            bars = ax.bar(df["Subject"], df["Marks"], color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontweight='bold', fontsize=10)
            
            ax.axhline(y=analysis['avg_marks'], color='#3b82f6', linestyle='--', linewidth=2,
                      label=f'Average: {analysis["avg_marks"]:.1f}')
            ax.axhline(y=st.session_state.class_settings["passing_percentage"], 
                      color='#f59e0b', linestyle=':', linewidth=2,
                      label=f'Passing: {st.session_state.class_settings["passing_percentage"]}')
            
            plt.xlabel("Subjects", fontsize=12, fontweight='bold')
            plt.ylabel("Marks", fontsize=12, fontweight='bold')
            plt.title(f"{student['name']}'s Marks Distribution", fontsize=14, fontweight='bold')
            plt.legend(loc='upper right')
            plt.grid(axis="y", linestyle="--", alpha=0.3)
            plt.ylim(0, 110)
            plt.tight_layout()
            st.pyplot(fig)
        
        with col_viz2:
            st.markdown("### 🎯 Performance Radar")
            fig, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(projection='polar'))
            
            subjects_list = list(student['marks'].keys())
            angles = np.linspace(0, 2 * np.pi, len(subjects_list), endpoint=False).tolist()
            marks_values = [student['marks'][subject] for subject in subjects_list]
            marks_values += marks_values[:1]
            angles += angles[:1]
            
            ax.plot(angles, marks_values, 'o-', linewidth=3, color='#667eea', markersize=8)
            ax.fill(angles, marks_values, alpha=0.3, color='#764ba2')
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(subjects_list, fontsize=10, fontweight='bold')
            ax.set_ylim(0, 100)
            ax.set_title(f"{student['name']}'s Performance Radar", 
                       fontsize=14, fontweight='bold', pad=20)
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Add average circle
            avg_circle = [analysis['avg_marks']] * (len(angles))
            ax.plot(angles, avg_circle, linestyle='--', color='#3b82f6', linewidth=2, label='Average')
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
            
            plt.tight_layout()
            st.pyplot(fig)
        
        # Subject-wise Progress Bars
        st.markdown("### 📈 Subject-wise Performance Breakdown")
        for subject, mark in student['marks'].items():
            percentage_val = mark
            if percentage_val >= 85:
                color = "#22c55e"
            elif percentage_val >= 70:
                color = "#84cc16"
            elif percentage_val >= 60:
                color = "#f59e0b"
            elif percentage_val >= 50:
                color = "#f97316"
            else:
                color = "#ef4444"
            
            st.markdown(f"""
                <div style="margin: 15px 0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <strong>{subject}</strong>
                        <strong>{mark}/100</strong>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar" style="width: {percentage_val}%; background: {color};">
                            {percentage_val}%
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # Strengths, Weaknesses & Recommendations
        col_analysis1, col_analysis2 = st.columns(2)
        
        with col_analysis1:
            st.markdown("### 💪 Strengths")
            if analysis['strengths']:
                for subject, mark in analysis['strengths'].items():
                    st.markdown(f"""
                        <div class="strength">
                            <strong>✨ {subject}:</strong> {mark}/100
                            <p style='margin: 5px 0 0 0; color: #666;'>Excellent performance! Keep it up.</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("💡 Focus on building strengths by excelling in your best subjects.")
            
            st.markdown("### ⚠️ Areas for Improvement")
            if analysis['weaknesses']:
                for subject, mark in analysis['weaknesses'].items():
                    st.markdown(f"""
                        <div class="weakness">
                            <strong>📌 {subject}:</strong> {mark}/100
                            <p style='margin: 5px 0 0 0; color: #666;'>Needs focused attention and practice.</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("🎉 No significant weaknesses identified! Great job!")
        
        with col_analysis2:
            st.markdown("### 📚 Personalized Recommendations")
            for subject, recommendation in analysis['recommendations'].items():
                st.markdown(f"""
                    <div class="recommendation">
                        <strong>{subject}</strong>
                        <p style='margin: 5px 0 0 0; color: #444;'>{recommendation}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        # Improvement Potential
        st.markdown("### 🚀 Predicted Improvement Potential")
        st.markdown("*Based on current performance and AI analysis*")
        
        potential_df = pd.DataFrame([
            {
                'Subject': subject,
                'Current': student['marks'][subject],
                'Potential': analysis['improvement_potential'][subject],
                'Gain': analysis['improvement_potential'][subject] - student['marks'][subject]
            }
            for subject in student['marks'].keys()
        ])
        
        fig, ax = plt.subplots(figsize=(12, 6))
        x = np.arange(len(potential_df))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, potential_df['Current'], width, label='Current Marks', 
                      color='#3b82f6', alpha=0.8, edgecolor='black', linewidth=1.5)
        bars2 = ax.bar(x + width/2, potential_df['Potential'], width, label='Predicted Potential',
                       
                      color='#10b981', alpha=0.8, edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for bar in bars1 + bars2:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold', fontsize=10)
            
        ax.set_xticks(x)
        ax.set_xticklabels(potential_df['Subject'], fontsize=10, fontweight='bold')
        ax.set_ylabel("Marks", fontsize=12, fontweight='bold')
        ax.set_title(f"{student['name']}'s Improvement Potential", fontsize=14, fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        ax.set_ylim(0, 110)
        plt.tight_layout()
        st.pyplot(fig)
    # TAB 2: Class Analytics
    with tab2:  
        st.markdown("<h2 style='text-align:center; color:#444;'>📊 Class-wide Analytics</h2>", unsafe_allow_html=True)
        st.info("This section is under development. Stay tuned for upcoming features!")
        



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