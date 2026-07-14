import streamlit as st
import sqlite3
import datetime
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. EMAIL SENDER FUNCTION (SMTP Configuration) ---
def send_email_to_student(to_email, student_name, course_name, score, total_questions, percentage, status):
    # ⚠️ Apni Gmail ID aur App Password yahan set karein taaki email automatically jaa sake
    # Gmail se auto-email bhejne ke liye "App Password" generate karna zaroori hai.
    sender_email = "your_email@gmail.com"  
    sender_password = "your_app_password"   
    
    if sender_email == "your_email@gmail.com" or sender_password == "your_app_password":
        # Agar default email change nahi kiya hai to skip karein taaki app crash na ho
        return False

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = f"🎓 Quiz Assessment Result for {course_name} - {student_name}"

    body = f"""
    Hi {student_name},

    Thank you for taking the assessment. Here is your official report card:

    ------------------------------------------
    Course Name: {course_name}
    Exam Date: {datetime.date.today().strftime('%d-%b-%Y')}
    Total Score: {score} / {total_questions}
    Percentage: {percentage}%
    Status: {status}
    ------------------------------------------

    Regards,
    🤖 AI Training & Assessment Agent
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

# --- 2. DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("assessment_db.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT student_name FROM results LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("DROP TABLE IF EXISTS results")
        
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            student_email TEXT,
            user_language TEXT,
            searched_course TEXT,
            score INTEGER,
            total_questions INTEGER,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- 3. DYNAMIC QUIZ GENERATOR ---
def get_course_questions(course_title):
    return [
        {"q": f"What is the primary core objective of studying {course_title}?", "opts": ["Skill Development", "Entertainment", "Hardware Designing", "None"], "ans": "Skill Development", "sec": "Core Introduction"},
        {"q": f"Which of the following is considered a foundational pillar of {course_title}?", "opts": ["Structured Logic", "Random Guessing", "Manual Processes", "Static Memory"], "ans": "Structured Logic", "sec": "Core Introduction"},
        {"q": f"What is the standard entry-level requirement to practice {course_title} projects?", "opts": ["Fundamental Concepts", "Advanced Calculus", "Hardware Prototyping", "Operating Systems Construction"], "ans": "Fundamental Concepts", "sec": "Basics & Logic"},
        {"q": f"In a modern workspace, {course_title} workflows are primarily integrated for:", "opts": ["Automation & Efficiency", "Manual Typo Checking", "Social Media Buffering", "Graphic Textures"], "ans": "Automation & Efficiency", "sec": "Basics & Logic"},
        {"q": f"Which of the following errors is most common during initial execution in {course_title}?", "opts": ["Syntax/Logic Error", "Hardware Thermal Defect", "Network Router Crash", "Disk Storage Failure"], "ans": "Syntax/Logic Error", "sec": "Error Management"},
        {"q": f"What is the best way to scale performance in a standard {course_title} model?", "opts": ["Optimizing algorithms and resources", "Ignoring variables", "Adding static loops", "Deleting files"], "ans": "Optimizing algorithms and resources", "sec": "Advanced Concepts"},
        {"q": f"In {course_title} architecture, a modular design approach helps to achieve:", "opts": ["High Code Reusability", "Slow compile times", "Increased error rates", "System Dependency"], "ans": "High Code Reusability", "sec": "Advanced Concepts"},
        {"q": f"Which repository or system is commonly used to track versions of {course_title} setups?", "opts": ["Version Control System (Git)", "Media Player", "Word Processor", "Spreadsheet Editor"], "ans": "Version Control System (Git)", "sec": "Best Practices"},
        {"q": f"What does a diamond box represent in a structural logic flowchart for {course_title}?", "opts": ["Decision/Condition block", "Process/Action block", "Start/End block", "Terminal connection"], "ans": "Decision/Condition block", "sec": "Diagrams & Design"},
        {"q": f"What is considered the final step before deploying a {course_title} project solution?", "opts": ["Thorough testing and validation", "Writing raw pseudocode", "Changing the theme", "Restarting the compiler"], "ans": "Thorough testing and validation", "sec": "Best Practices"}
    ]

# --- 4. STREAMLIT UI ---
st.title("🤖 AI Training & Assessment Agent")

# 📂 SIDEBAR (Student Details)
st.sidebar.header("👤 Student Profile Information")
student_name = st.sidebar.text_input("Student Name", placeholder="Enter student full name")
student_email = st.sidebar.text_input("Student Email ID", placeholder="student@example.com")
user_lang = st.sidebar.selectbox("Select Language", ["Odia", "English", "Hindi", "Kannada", "French"])

tab1, tab2 = st.tabs(["📝 Take AI Assessment", "📊 Admin View & Server Logs"])

with tab1:
    st.subheader("🔍 Search Your Course & Start Quiz")
    course_search = st.text_input("Search Course Name (e.g., Python, Java, Web Development):", placeholder="Type course name here...")
    
    if st.button("🔍 Search Course & Generate 10-Question Quiz"):
        if not course_search:
            st.warning("⚠️ Please type a course name to search first!")
        else:
            with st.spinner(f"Generating 10 questions for '{course_search}'..."):
                st.session_state["searched_quiz"] = get_course_questions(course_search)
                st.session_state["current_course"] = course_search
                st.session_state["quiz_submitted"] = False  # Reset status
                st.success(f"🎉 10 Questions prepared for: **{course_search}**!")

    # Display Quiz
    if "searched_quiz" in st.session_state and st.session_state["searched_quiz"]:
        current_quiz = st.session_state["searched_quiz"]
        
        # User answers store karne ke liye session state variable
        if "user_answers" not in st.session_state:
            st.session_state["user_answers"] = {i: None for i in range(len(current_quiz))}
        
        st.write("---")
        st.info(f"💡 **Exam Mode:** {st.session_state['current_course']} | Language: **{user_lang}**")
        
        # Questions render karein (Agar submit ho gaya hai to disabled rakhein)
        for i, q_item in enumerate(current_quiz):
            st.markdown(f"**Q{i+1}. {q_item['q']}**")
            
            # Agar submitted hai aur galat hai, to sahi answer highlight karke dikhao
            if st.session_state.get("quiz_submitted", False):
                selected = st.session_state["user_answers"][i]
                st.write(f"Your Answer: **{selected}**")
                if selected == q_item['ans']:
                    st.success("✅ Correct Answer!")
                else:
                    st.error(f"❌ Wrong Answer! **Correct Answer kauta: {q_item['ans']}**")
            else:
                st.session_state["user_answers"][i] = st.radio(
                    f"Select option for Q{i+1}:", 
                    q_item['opts'], 
                    index=None, 
                    key=f"sq_{i}"
                )
            st.write("---")
            
        # Submit Button (Sirf tab dikhega jab quiz submit na hua ho)
        if not st.session_state.get("quiz_submitted", False):
            if st.button("🚀 Publish & Submit Assessment", type="primary"):
                if not student_name or not student_email:
                    st.warning("⚠️ Please complete the Student Profile in the sidebar first!")
                else:
                    score = 0
                    all_answered = True
                    sections_data = {}
                    
                    for q in current_quiz:
                        sections_data[q['sec']] = {"asked": 0, "correct": 0}
                        
                    for i, q_item in enumerate(current_quiz):
                        sections_data[q_item['sec']]["asked"] += 1
                        if st.session_state["user_answers"][i] is None:
                            all_answered = False
                        elif st.session_state["user_answers"][i] == q_item['ans']:
                            score += 1
                            sections_data[q_item['sec']]["correct"] += 1
                            
                    if not all_answered:
                        st.error("❌ Please answer all 10 questions before submitting.")
                    else:
                        st.session_state["quiz_submitted"] = True
                        
                        # 💾 Save to Database
                        conn = sqlite3.connect("assessment_db.db")
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO results (student_name, student_email, user_language, searched_course, score, total_questions, date)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (student_name, student_email, user_lang, st.session_state["current_course"], score, len(current_quiz), str(datetime.date.today())))
                        conn.commit()
                        conn.close()
                        
                        percentage = int((score / len(current_quiz)) * 100)
                        status = "PASS" if percentage >= 70 else "NEEDS IMPROVEMENT"
                        
                        # 📧 Automatically Send Email to Student
                        email_sent = send_email_to_student(student_email, student_name, st.session_state["current_course"], score, len(current_quiz), percentage, status)
                        
                        st.success("🎉 Data Saved to Server Database Successfully!")
                        if email_sent:
                            st.success(f"📧 Official Score Card email successfully sent to {student_email}!")
                        else:
                            st.info("ℹ️ Data Saved! Configure your SMTP credentials in code to enable real email deliveries.")
                            
                        st.balloons()
                        st.rerun() # Refresh to instantly show correct/incorrect markers on top

        # Agar submitted hai, tab Score Sheet dikhao niche
        if st.session_state.get("quiz_submitted", False):
            # Recalculate variables for report view
            score = sum(1 for i, q in enumerate(current_quiz) if st.session_state["user_answers"][i] == q['ans'])
            percentage = int((score / len(current_quiz)) * 100)
            status = "PASS" if percentage >= 70 else "NEEDS IMPROVEMENT"
            
            st.header("📊 Official Score Sheet Summary")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Student Name:** {student_name}")
                st.write(f"**Student Email:** {student_email}")
                st.write(f"**Language:** {user_lang}")
            with col2:
                st.write(f"**Course Name:** {st.session_state['current_course']}")
                st.write(f"**Exam Date:** {datetime.date.today().strftime('%d-%b-%Y')}")
            
            st.write("---")
            m1, m2, m3 = st.columns(3)
            m1.metric(label="Percentage Score", value=f"{percentage}%")
            m2.metric(label="Exam Status", value=status)
            m3.metric(label="Total Marks", value=f"{score} / 10")
            st.write("---")
            
            if st.button("🔄 Clear Result & Take Another Quiz"):
                del st.session_state["searched_quiz"]
                del st.session_state["user_answers"]
                st.session_state["quiz_submitted"] = False
                st.rerun()

with tab2:
    st.subheader("💾 Permanent Server Database Logs (Admin View)")
    conn = sqlite3.connect("assessment_db.db")
    df_logs = pd.read_sql_query("SELECT * FROM results ORDER BY id DESC", conn)
    conn.close()
    
    if not df_logs.empty:
        st.dataframe(df_logs, use_container_width=True)
    else:
        st.info("No logs found in the server database yet.")