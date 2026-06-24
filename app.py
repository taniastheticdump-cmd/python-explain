import streamlit as st
import io
import contextlib
import os
import sqlite3
import pandas as pd

from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# DATABASE FUNCTIONS START HERE

def create_database():
    conn = sqlite3.connect("pyexplain.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_history(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   code TEXT,
                   concepts TEXT,
                   difficulty TEXT,
                   created_at TEXT
)
""")
    conn.commit()
    conn.close()

def save_analysis(code, concepts, difficulty):
    conn=sqlite3.connect("pyexplain.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO analysis_history
        (code, concepts, difficulty, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            code,
            ",".join(concepts),
            difficulty,
datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )
    conn.commit()
    conn.close()
# DATABASE FUNCTIONS END HERE
create_database()

def get_total_analyses():
    conn = sqlite3.connect("pyexplain.db")
    total = pd.read_sql_query(
        "SELECT  COUNT(*) as total FROM analysis_history",
        conn
    )
    conn.close()
    return total["total"][0]
    total_analyses = get_total_analyses()
    st.metric(
        "📊 Total Analyses",
        total_analyses
        )

st.set_page_config(
    page_title = "PyExplain",
    page_icon = "🐍",
    layout = "wide"
)

st.markdown(
    "<h1 style='text-align:center;'>🐍 PyExplain</h1>",
    unsafe_allow_html = True
)

st.markdown(
    "<p style='text-align:center;'> Your Learning Assistant</p>",
    unsafe_allow_html= True
)
st.caption("Your Python Learning Assistant")
col1, col2, col3 = st.columns(3)
col1.metric("📊Total Analysis",get_total_analyses())
col2.metric("🤖 AI Features",4)

with st.sidebar:
    st.metric("Database", "SQLite")
    if st.button("Show Database"):
        conn = sqlite3.connect("pyexplain.db")

        df = pd.read_sql_query(
            "SELECT id,difficulty, created_at FROM analysis_history ORDER BY id DESC",
            conn
        )
        st.dataframe(df)
        conn.close()


    st.header("📚 PyExplain")
    st.write("version 4.1- SQLite edition")

    st.divider()

    st.write("✅ Concept Detection")
    st.write("✅ Syntax Checker")
    st.write("✅ Difficulty Analysis")
    st.write("✅ Quiz Generator")
    st.write("✅ Interveiw Questions")
    st.write("✅ Export Report")

    st.divider()
    if st.button("📃 Analysis history"):
        conn = sqlite3.connect("pyexplain.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id, difficulty, created_at
        FROM analysis_history
        ORDER BY id DESC
        LIMIT 10
        """)
        rows = cursor.fetchall()

        st.subheader("📃 Recent Analyses")

        for row in rows:
            st.write(
                f"ID: {row[0]} | {row[1]} | {row[2]}"
            )
        conn.close()


st.markdown("""
### Learn Python Smarter🚀
Paste your python code below and get:
✅ Concept Detection
✅Difficulty Analysis
✅Learning Roadamp
✅Quiz Questions
✅Interveiw preparation

Built for students and beginners.
""" )
concept_count = 0
difficulty_display = "N/A"
quiz_count = 0

col1, col2, col3 = st.columns(3)
card1 = col1.empty()
card2 = col2.empty()
card3 = col3.empty()

card1.metric("📚 Concepts",0)
card2.metric("🎯 Difficulty","N/A")
card3.metric("🧠 Quiz Questions",0)

code = st.text_area(
    "Paste Python Code Here:",
    height = 400
)
def check_syntax(code):
    if not code.strip():
        return "No code entered"
    try:
        compile(code,"<string>" , "exec")
        return "✅ No syntax errors found"
    except SyntaxError as e:
        return f"❌ Syntax error: {e}"

def explain_lines(code):

    explanations = []

    lines = code.split("\n")

    for line_no, line in enumerate(lines, start=1):
        line = line.strip()

        if not line:
            continue

        if "=" in line and"==" not in line:
            explanations.append(
                f"Line {line_no}: variable assignment detected."
            )

        elif line.startswith("print"):
            explanations.append(
                f"Line {line_no}: prints output on the screen."
            )
        elif line.startswith("input"):
            explanations.append(
                f"Line {line_no}: Takes input from the user."
            )
        elif line.startswith("for"):
            explanations.append(
                f"Line {line_no}: Starts a for loop."
            )
        elif line.startswith("while"):
            explanations.append(
                f"Line {line_no}:Starts a while loop."
            )
        elif line.startswith("if"):
            explanations.append(
                f"Line {line_no}: Checks a condition."
            )
        elif line.startswith("def"):
            explanations.append(
                f"Line {line_no}: Defines a function."
            )
        elif line.startswith("return"):
            explanations.append(
                f"Line {line_no}:Returns a value from the function."
            )
        elif line.startswith("class"):
            explanations.append(
                f"Line {line_no}: Defines a class."
            )
        elif line.startswith("import"):
            explanations.append(
                f"Line {line_no}: Imports a module."
            )
    return explanations

def get_difficulty(code):
    if not code.strip():
        return "No code entered"
    score = 0
    beginner = ["print(", "input(", "if", "for", "while"]
    intermidiate = ["def", "list", "dict", "set", "tuple"]
    advanced = ["class", "try:", "except", "lambda", "import"]
    for item in beginner:
        if item in code:
            score += 1
    for item in intermidiate:
        if item in code:
            score += 2
    for item in advanced:
        if item in code:
            score += 3
    
    if score <= 3:
        return f"Beginner ({score}/10)"
    elif score <= 8:
        return f"Intermediate ({score}/10)"
    else:
        return f"Advanced ({score}/10)"
    
def generate_summary(code):
    if not code.strip():
        return "No code enterd."
    
    summary = []

    if "=" in code and "==" not in code:
        summary.append("creates variable")
    if "for" in code:
        summary.append("uses a for loop")
    if "while" in code:
        summary.append("uses a while loop")
    if "if" in code:
        summary.append("checks condition")
    if "def" in code:
        summary.append("defines a function")
    if "class" in code:
        summary.append("uese object-oriented programming")
    if "print(" in code:
        summary.append("displays output")
    if not summary:
        return "This program contains python code."
    return "This program " + ",".join(summary) + "."

def get_learning_tips(code):
    tips = []
    if "for" in code:
        tips.append("For loops are used when the number of iterations is known.")
    if "while" in code:
        tips.append("While loops run until a condition becomes false.")
    if "if" in code:
        tips.append("If statements help make decisions in a program.")
    if "def" in code:
        tips.append("Functions help in organizing code and reusing it.")
    if "list" in code:
        tips.append("Lists are mutable and can store multiple values.")
    if "dict" in code:
        tips.append("Dictionaries store data as key-value pairs.")
    if "class" in code:
        tips.append("Classes are used in object-oriented programming (OOP).")
    if "try:" in code:
        tips.append("use try-except blocks to handle runtime errors safely.")
    if "print(" in code:
        tips.append("print() is used to display output on the screen.")
    return tips

def generate_roadmap(code):
    roadmap = []

    if "for" in code or "while" in code:
        roadmap.append("Learn function")
    if "def" in code:
        roadmap.append("Learn dictionaries")
    if "dict" in code or "{" in code:
        roadmap.append("Learn file handling")
    if "try:" in code:
        roadmap.append("Learn Object Oriented Programming(OOP)")
    if "class" in code:
        roadmap.append("Learn Database Integration")
    if not roadmap:
        roadmap.append("Start with variables, input/output and loops")

    return roadmap

def generate_quiz(code):
    quiz = []
    if "for" in code:
        quiz.append(
            "Q1. What is the purpose of a for loop?"
        )
        quiz.append(
            "Q2 What does range() do?"
        )
        quiz.append(
            "Q3 What is the difference between for and while loops?"
        )
    if "if" in code:
        quiz.append(
            "Q4 What does an if statement do?"
        )
        quiz.append(
            "Q5 what is the difference between if,elif and else?"
        )

    if "def" in code:
        quiz.append(
            "Q6 Why do we use functions in python?"
        )
        quiz.append(
            "Q7 What are the parameters and arguments?"
        )
    if "list" in code :
        quiz.append(
            "Q8 What is difference between a list and a tuple?"
            )
        quiz.append(
            "Q9 How is a list different from a tuple?"
        )
    if "class" in code:
        quiz.append(
            "Q10 what is a class in python?"
        )
        quiz.append(
            "What is Object-Oriented Programming?"
        )
    if not code.strip():
        return []
    
    return quiz

def generate_interveiw_questions(code):
     questions = []
    
     if "for" in code:
         questions.append(
             "explain how a for loop works in python?"
         )
         questions.append(
             "what is the difference between for and while loops?"
         )
         questions.append(
             "What does range() do in a for loop?"
         )
     if "def" in code:
         questions.append(
             "What are the advantages of using function?"
         )
         questions.append(
            " What is the difference between  parameters and arguments?"
         )
         questions.append(
             "Why is code reusability important?"
         )
     
     if "if" in code:
        questions.append(
            "What is the difference between if, elif and else?"
        )
        questions.append(
            "How are conditions evaluated in python?"
        )

     if not code.strip():
         return []
     
     
     if  not questions:
         questions.append(
             "What are the main features of python?"
         )

     return  questions
def ai_explain_code(code):

    if not code.strip():
        return "Please enter some Python code first."

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": f"""
Explain this Python code in simple beginner-friendly English.

Provide:
1. Purpose of the code
2. Concepts used
3. Difficulty level
4. Improvements
5. What should the student learn next?

Code:
{code}
"""
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {e}"

def ai_generate_quiz(code):

    if not code.strip():
        return "Please enter some Python code first."

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": f"""
Generate 5 quiz questions based on this Python code.

For each question provide:

1. Question
2. Correct Answer
3. Explanation

Code:
{code}
"""
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {e}"
    

def ai_interview_coach(code):

    if not code.strip():
        return "Please enter some Python code first."

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": f"""
You are a Python technical interviewer.

Based on this code generate:

1. 5 Interview Questions
2. Ideal Answer for each question
3. Interview Tip for each question

Keep answers beginner friendly.

Code:
{code}
"""
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {e}"
    
def ai_learn_mode(code):

    if not code.strip():
        return "Please enter some Python code first."

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": f"""
Act as an expert Python teacher.
Analyze this code and provide:

1. Concepts Explained
2. Beginner Notes
3. Real World Example
4. Common Mistakes
5. Learning Roadmap
6. Mini Project Idea

Code:
{code}
"""
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {e}"
    


concepts = []
quiz = []
difficulty = "N/A"

btn1, btn2, btn3, btn4, btn5, btn6 = st.columns(6)
with btn1:
    run_code = st.button("▶️ Run Code",use_container_width=True)
with btn2:
    analyze = st.button("🚀 Analyze code",use_container_width= True)
with btn3:
    ai_button = st.button("🤖 AI Mentor")
with btn4:
    ai_quiz_button = st.button("📚 AI Quiz")
with btn5:
    interview_ai_button = st.button("🎤 Ai Interviewer")
with btn6:
    learn_mode = st.button("📖 AI Learn")

if analyze:
    
    concepts = []

# Variables
    if "=" in code and "==" not in code:
        concepts.append("Variable Assignment")

# Data Types
    if '"' in code or "'" in code:
        concepts.append("String")
    
    if "True" in code or "False" in code:
        concepts.append("Boolean")

    if "None" in code:
        concepts.append("None Type")

    if "int(" in code :
        concepts.append("Integer")
        
    if "float(" in code:
        concepts.append("float")

#collections
    if"[" in code and "]" in code:
        concepts.append("List")


    if "{" in code and ":" in code and "}" in code:
        concepts.append("Dictionary")

    if "set(" in code:
        concepts.append("Set")

# Input  output
    if "input(" in code:
        concepts.append("Input Statement")

    if "print(" in code:
        concepts.append("Print Statement")

 #Conditions
    if "if" in code:
        concepts.append("If Statement")

    if "elif" in code:
        concepts.append("Elif statement")

    if "else:" in code:
        concepts.append("Else Statement")

    #Lops
    if "for" in code:
        concepts.append("For Loop")

    if "while" in code:
        concepts.append("While Loop")

# Functions
    if "def" in code:
        concepts.append("Function Definition")

    if " return" in code:
        concepts.append("Return Statement")

    if "lambda" in code:
        concepts.append("Lambda Function")

# operators
    if"+" in code or "-" in code or"*" in code or "/" in code:
        concepts.append("Arithmetic operators")

    if "==" in code or"!=" in code or ">" in code or "<" in code:
        concepts.append("Comparison operators")
    
# Exception handling 
    if "try:" in code:
        concepts.append("Try Block")

    if "except" in code:
        concepts.append("Except Block")

    if "finally:" in code:
        concepts.append("Finally Block")

#  OOP
    if "class" in code:
        concepts.append("Class Definition")
    
    if "__init__" in code:
        concepts.append("Constructor")

    if "self" in code:
       concepts.append("Instance Variables")

# Modules 
    if "import" in code:
        concepts.append("Import Statement")

    if"from" in code and "import" in code:
        concepts.append("From import statement")

# file handling
    if "open(" in code:
        concepts.append("File handling")

    st.subheader("Concepts Found")
    if concepts:
        concepts = list(set(concepts))
        for concept in concepts:
         st.write("✅", concept)

    else:
        st.write("No concepts detected.")
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Analysis", "📚 Learning", "🧠 Quiz", "🎤 Interview"]
        )
    
    
    with tab1:
     st.subheader("📃 Line-by-Line Explanation")
     explanations = explain_lines(code)
     for explanation in explanations:
      st.write(explanation)

     st.subheader("🔍 Syntax Check")
     result = check_syntax(code)
     st.write(result)

     st.subheader("🎯 Difficulty level")
     difficulty = get_difficulty(code)
     st.write(difficulty)

     st.subheader("📝  code Summary")
     summary = generate_summary(code)
     st.write(summary)

    with tab2:

     with st.expander("💡 learning Tips"):
        tips = get_learning_tips(code)
        if tips:
            for tip in tips:
                st.write("👉", tip)
        else:
            st.write("No learning tips available.")

    with st.expander("Learning roadmap🛣️"):
        roadmap = generate_roadmap(code)
        for step in roadmap:
            st.write("🚀", step)

    with tab3:

     with st.expander ("🧠 Quiz Generator"):
        quiz = generate_quiz(code)
        if quiz:
            for question in quiz:
                st.write(question)
    card1.metric("📚 Concepts", len(concepts))
    card2.metric("🎯 Difficulty",difficulty)
    card3.metric("🧠 Quiz Questions",len(quiz))

    with tab4:
    
     with st.expander("🎤 Interveiw Questions"):
        questions = generate_interveiw_questions(code)
        for question in questions:
            st.write("❓" , question)

    if 'concepts' not in locals():
     concepts = []

    report = f"""
PYEXPLAIN REPORT

     Concepts found:
     {','.join(concepts)}

     Difficulty:
     {difficulty}

     Learning tips:
     {','.join(tips)}

     Learning roadmap:
    { ',' .join(roadmap)}

     Quiz questions:
    {chr(10).join(quiz)}

     Interveiw questions:
    {chr(10).join(questions)}
"""
    
    if code.strip():
        save_analysis(
            code,
            concepts,
            difficulty
        )
    st.download_button(
        label = "📩 Download Report",
        data = report,
        file_name = "PyExplain_report.txt",
        mime = "text/plain"
        )
    
if run_code:
    st.subheader("▶️ Program output")
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            exec(code)
        st.success("Code executed successfully!")
        st.code(output.getvalue())
    except Exception as e:
        st.error(f"Runtime Error:{e}")

if ai_button:

    st.subheader("🤖 AI Mentor")

    with st.spinner("Thinking..."):

        ai_result = ai_explain_code(code)

        st.write(ai_result)

if ai_quiz_button:

    st.subheader("📚 AI Quiz with Answers")
    
    with st.spinner("Generating Quiz..."):
        
        quiz_result = ai_generate_quiz(code)
        st.write(quiz_result)

if interview_ai_button:

    st.subheader("🎤 AI Interview Coach")

    with st.spinner("Preparing interview questions..."):

        interview_result = ai_interview_coach(code)
        st.write(interview_result)

if learn_mode:

    st.subheader("📖 AI Learn mode")

    with st.spinner("Preparing learning guide..."):

        learn_result = ai_learn_mode(code)
        st.write(learn_result)



