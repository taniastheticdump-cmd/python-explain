import streamlit as st

st.title("PyExplain")

st.write("Understand code,Don't just Copy it")

code = st.text_area(
    "Paste Python Code Here:",
    height = 300
)
def check_syntax(code):
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

if st.button("Explain Code"):
    
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
st.subheader("📃 Line-by-Line Explanation")
explanations = explain_lines(code)
for explanation in explanations:
    st.write(explanation)

st.subheader("🔍 Syntax Check")
result = check_syntax(code)
st.write(result)

