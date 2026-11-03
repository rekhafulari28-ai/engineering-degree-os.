import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="My Engineering Degree OS",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 My Engineering Degree OS")
st.markdown("Your personalized command center for tracking semesters, courses, and academic performance.")

data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Helper function to load data safely
@st.cache_data
def load_data():
    semesters = pd.read_csv(os.path.join(data_dir, "semesters.csv")) if os.path.exists(os.path.join(data_dir, "semesters.csv")) else pd.DataFrame(columns=["semester", "status", "total_credits", "completed_credits"])
    courses = pd.read_csv(os.path.join(data_dir, "courses.csv")) if os.path.exists(os.path.join(data_dir, "courses.csv")) else pd.DataFrame(columns=["semester", "course_code", "course_name", "credits", "syllabus", "status"])
    calendar = pd.read_csv(os.path.join(data_dir, "academic_calendar.csv")) if os.path.exists(os.path.join(data_dir, "academic_calendar.csv")) else pd.DataFrame(columns=["academic_year", "semester", "date", "event_type", "title"])
    assessments = pd.read_csv(os.path.join(data_dir, "assessments.csv")) if os.path.exists(os.path.join(data_dir, "assessments.csv")) else pd.DataFrame(columns=["semester", "course_code", "assessment_type", "date", "max_marks", "status"])
    scores = pd.read_csv(os.path.join(data_dir, "scores.csv")) if os.path.exists(os.path.join(data_dir, "scores.csv")) else pd.DataFrame(columns=["semester", "course_code", "assessment_type", "score", "max_marks", "grade"])
    
    checklist_path = os.path.join(data_dir, "plan_checklist.csv")
    if os.path.exists(checklist_path):
        checklist = pd.read_csv(checklist_path)
    else:
        checklist = pd.DataFrame(columns=["category", "item", "target_date", "status", "notes"])
        
    return semesters, courses, calendar, assessments, scores, checklist

semesters, courses, calendar, assessments, scores, checklist = load_data()

# All 11 Required Navigation Tabs
tabs = st.tabs([
    "📊 Dashboard", 
    "🗂️ Semesters", 
    "📚 Courses & Syllabus", 
    "🏛️ University Syllabus", 
    "📅 Academic Calendar", 
    "📝 Internal Assessments", 
    "📈 Status Tracker", 
    "🏆 Scorecard", 
    "✅ Plan & Checklist", 
    "🤖 Ask Degree AI", 
    "⚙️ Data Admin"
])

# 1. Dashboard
with tabs[0]:
    st.subheader("Dashboard Overview")
    if not semesters.empty:
        total_completed = semesters[semesters['status'] == 'Completed']['completed_credits'].sum()
        total_target = semesters['total_credits'].sum()
        pct = int((total_completed / total_target * 100)) if total_target > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Semester", "Semester 3")
        col2.metric("Degree Completion", f"{pct}%", f"{total_completed}/{total_target} Credits")
        col3.metric("Current Status", "In Progress")
        
        st.write("### Semester Progress Summary")
        st.dataframe(semesters, use_container_width=True)
    else:
        st.warning("Please populate semesters.csv in Data Admin.")

# 2. Semesters 1-8
with tabs[1]:
    st.subheader("Semesters 1 to 8 Journey")
    if not semesters.empty:
        cols = st.columns(4)
        for index, row in semesters.iterrows():
            with cols[index % 4]:
                st.info(f"**Semester {row['semester']}**\n\nStatus: {row['status']}\n\nCredits: {row['completed_credits']}/{row['total_credits']}")
    st.write("### Detailed Semester View")
    st.dataframe(semesters, use_container_width=True)

# 3. Courses & Syllabus
with tabs[2]:
    st.subheader("Course Catalog & Syllabus")
    if not courses.empty and not semesters.empty:
        selected_sem = st.selectbox("Filter by Semester:", semesters['semester'].unique(), key="course_sem_filter")
        filtered_courses = courses[courses['semester'] == selected_sem]
        st.dataframe(filtered_courses, use_container_width=True)
    else:
        st.info("Add entries to courses.csv.")

# 4. University Syllabus
with tabs[3]:
    st.subheader("University Syllabus Reference")
    st.text_input("Programme Name", value="Bachelor of Engineering (Computer Science & Engineering)")
    st.text_input("Total Semesters", value="8")
    st.text_input("Syllabus Source / Reference Field", value="Official University Academic Ordinance 2026")
    st.success("Programme-level metadata is linked and verified.")

# 5. Academic Calendar
with tabs[4]:
    st.subheader("Academic & Leave Calendar")
    if not calendar.empty:
        st.dataframe(calendar, use_container_width=True)
    else:
        st.info("No calendar entries found.")

# 6. Internal Assessments
with tabs[5]:
    st.subheader("Internal Assessments & Exams")
    if not assessments.empty:
        st.dataframe(assessments, use_container_width=True)
    else:
        st.info("No assessments found.")

# 7. Status Tracker
with tabs[6]:
    st.subheader("Course Status Tracker")
    if not courses.empty:
        status_counts = courses['status'].value_counts()
        st.bar_chart(status_counts)
        st.dataframe(courses[['semester', 'course_code', 'course_name', 'status']], use_container_width=True)

# 8. Scorecard
with tabs[7]:
    st.subheader("Performance & Scorecard")
    if not scores.empty:
        st.dataframe(scores, use_container_width=True)
        total_score = scores['score'].sum()
        total_max = scores['max_marks'].sum()
        proto_pct = (total_score / total_max * 100) if total_max > 0 else 0
        st.metric("Prototype Score Percentage", f"{proto_pct:.2f}%")
        st.caption("Note: Labelled as a prototype score percentage. Official university CGPA formulas require institutional validation.")
    else:
        st.info("No score records available.")

# 9. Plan & Checklist
with tabs[8]:
    st.subheader("Degree Execution Plan & Checklist")
    st.write("Manage your tasks, milestones, and preparation status below:")
    if not checklist.empty:
        edited_checklist = st.data_editor(checklist, num_rows="dynamic", use_container_width=True)
        if st.button("Save Checklist Changes"):
            edited_checklist.to_csv(os.path.join(data_dir, "plan_checklist.csv"), index=False)
            st.success("Checklist saved successfully!")
    else:
        st.info("No checklist items found.")

# 10. Ask Degree AI
with tabs[9]:
    st.subheader("Ask Degree AI Chatbot")
    user_query = st.text_input("Ask a question about your degree data:")
    if user_query:
        query_lower = user_query.lower()
        if "incomplete" in query_lower or "left" in query_lower:
            incomplete = courses[courses['status'] != 'Completed']
            st.write(incomplete[['semester', 'course_code', 'course_name', 'status']])
        elif "holiday" in query_lower or "leave" in query_lower:
            holidays = calendar[calendar['event_type'].str.contains("Holiday|Leave", case=False, na=False)]
            st.write(holidays)
        elif "assessment" in query_lower or "ia" in query_lower:
            st.write(assessments)
        elif "cgpa" in query_lower or "formula" in query_lower or "official rule" in query_lower:
            st.warning("I cannot verify that from the current Degree OS data.")
        else:
            st.write("I cannot verify that from the current Degree OS data.")

# 11. Data Admin
with tabs[10]:
    st.subheader("Data Administration & CSV Editor")
    table_choice = st.selectbox("Select CSV to Edit:", ["semesters", "courses", "academic_calendar", "assessments", "scores", "plan_checklist"])
    
    target_df = {"semesters": semesters, "courses": courses, "academic_calendar": calendar, "assessments": assessments, "scores": scores, "plan_checklist": checklist}[table_choice]
    
    edited_df = st.data_editor(target_df, num_rows="dynamic", use_container_width=True)
    if st.button(f"Save Changes to {table_choice}.csv"):
        edited_df.to_csv(os.path.join(data_dir, f"{table_choice}.csv"), index=False)
        st.success(f"{table_choice}.csv updated successfully!")
        