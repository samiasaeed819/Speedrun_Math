import time
import random
import os
import sqlite3
from fractions import Fraction

# importing Flask and other modules
from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
 
# Flask constructor
app = Flask(__name__)   
app.secret_key = "a_very_secret_key_for_session"  # Replace with a secure key in production 
DB_PATH = os.path.join(app.root_path, "quhack.db")


def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            total_answered INTEGER DEFAULT 0,
            correct_answered INTEGER DEFAULT 0,
            incorrect_answered INTEGER DEFAULT 0
        )
    """)
    connection.commit()
    connection.close()


def get_empty_stats():
    return {"answered": 0, "correct": 0, "incorrect": 0}


def get_session_stats():
    return session.get("stats", get_empty_stats())


def add_to_stats(answered, correct, incorrect):
    stats = get_session_stats()
    stats["answered"] = stats.get("answered", 0) + answered
    stats["correct"] = stats.get("correct", 0) + correct
    stats["incorrect"] = stats.get("incorrect", 0) + incorrect
    session["stats"] = stats

    user_id = session.get("user_id")
    if user_id:
        connection = get_db_connection()
        connection.execute(
            """
            UPDATE users
            SET total_answered = total_answered + ?,
                correct_answered = correct_answered + ?,
                incorrect_answered = incorrect_answered + ?
            WHERE id = ?
            """,
            (answered, correct, incorrect, user_id)
        )
        connection.commit()
        connection.close()


def get_account_stats():
    user_id = session.get("user_id")
    if not user_id:
        return None

    connection = get_db_connection()
    user = connection.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    connection.close()
    return user


def get_site_stats():
    connection = get_db_connection()
    stats = connection.execute(
        """
        SELECT
            COUNT(*) AS users,
            COALESCE(SUM(total_answered), 0) AS answered,
            COALESCE(SUM(correct_answered), 0) AS correct,
            COALESCE(SUM(incorrect_answered), 0) AS incorrect
        FROM users
        """
    ).fetchone()
    connection.close()
    return stats


init_db()


######FLASK####
@app.route('/')
def home():
    return render_template(
        'quhack.html',
        session_stats=get_session_stats(),
        account_stats=get_account_stats(),
        site_stats=get_site_stats()
    )

@app.route('/quhack2.html')
def page_adition():
    return render_template('quhack2.html')

@app.route('/quhack3.html')
def sub():
    return render_template('quhack3.html')

@app.route('/quhack4.html')
def multi():
    return render_template('quhack4.html')

@app.route('/quhack5.html')
def div():
    return render_template('quhack5.html')

@app.route('/quhack6.html')
def mix():
    return render_template('quhack6.html')

@app.route('/quhack7.html')
def about():
    return render_template('quhack7.html')

@app.route('/quhack9.html')
def assement():
    return render_template('quhack9.html')

@app.route('/quhack10.html')
def advanced_random():
    return render_template('quhack10.html', problem=False)

@app.route('/quhack11.html')
def full_test_page():
    return render_template('quhack11.html', test=False)

@app.route('/quhack12.html')
def account_page():
    return render_template(
        'quhack12.html',
        user=get_account_stats(),
        site_stats=get_site_stats()
    )



max_number = 0
#########################################################################################################
 ## Subtraction ###################

# ----------------------------
# Subtraction Problem Generator
# ----------------------------
def generate_problem_sub(max_number):
    # Types: 4) a - b = ?, 5) a - ? = c, 6) ? - b = c
    problem_type = random.choice([4, 5, 6])
    for _ in range(100):
        a = random.randint(0, max_number)
        b = random.randint(0, max_number)

        if problem_type == 4:
            c = a - b
            if 0 <= c <= max_number:
                return (a, b)
        elif problem_type == 5:
            c = random.randint(0, max_number)
            missing = a - c
            if 0 <= missing <= max_number:
                return (a, c)
        elif problem_type == 6:
            c = random.randint(0, max_number)
            missing = b + c
            if 0 <= missing <= max_number:
                return (missing, b)
    return (4, 2)

# ----------------------------
# Subtraction Route
# ----------------------------
@app.route('/sub', methods=["GET", "POST"])
def subtraction():
    if request.method == "POST":
        action = request.form.get("action", "")

        # Initialize problems if starting session
        if "max_number" in request.form and "num_questions" in request.form:
            max_number = int(request.form["max_number"])
            total_questions = int(request.form["num_questions"])

            problems = [generate_problem_sub(max_number) for _ in range(total_questions)]
            session["problems"] = problems
            session["current"] = 0
            session["results"] = []
            session["max_number"] = max_number
            session["total_questions"] = total_questions

        # Safety check
        if "problems" not in session or session["current"] >= len(session["problems"]):
            return render_template("quhack3.html", problem=False, results=session.get("results", []))

        current_index = session["current"]
        a, b = session["problems"][current_index]

        # -------------------
        # Hint requested
        # -------------------
        if action == "hint":
            low = max((a - b) - 5, 0)
            high = (a - b) + 5
            hint_text = f"The answer is between {low} and {high}."
            return render_template("quhack3.html", problem_str=f"{a} - {b} = ?", hint=hint_text)

        # -------------------
        # User submitted answer
        # -------------------
        if "user_answer" in request.form:
            user_answer_str = request.form.get("user_answer", "").strip()
            if not user_answer_str.isdigit():
                return render_template(
                    "quhack3.html",
                    problem_str=f"{a} - {b} = ?",
                    message="Enter a valid integer."
                )
            user_answer = int(user_answer_str)
            correct_answer = a - b

            # Record result
            results = session.get("results", [])
            results.append({
                "problem": f"{a} - {b} = ?",
                "your_answer": user_answer,
                "correct_answer": correct_answer,
                "status": "Correct" if user_answer == correct_answer else "Incorrect"
            })
            session["results"] = results

            # Move to next question
            session["current"] += 1

            # If all done, show summary
            if session["current"] >= session["total_questions"]:
                return render_template("quhack3.html", problem=False, results=results)

        # -------------------
        # Show current problem
        # -------------------
        if session["current"] < len(session["problems"]):
            a, b = session["problems"][session["current"]]
            return render_template("quhack3.html", problem_str=f"{a} - {b} = ?")

    # GET request → show start form
    return render_template("quhack3.html", problem=False)


#########################################################################################################
 ## Adition ###################

###############################
# ADDITION MODE (LIKE SUBTRACTION)
###############################

@app.route('/quhack2.html', methods=["GET", "POST"])
@app.route('/add', methods=["GET", "POST"])
def index_add():

    # --- FIRST PAGE LOAD ---
    if request.method == "GET":
        return render_template("quhack2.html", problem=False, message=None)

    # --- USER PRESSED START ---
    if "max_number" in request.form and "num_questions" in request.form:
        max_str = request.form['max_number'].strip()
        count_str = request.form['num_questions'].strip()

        if not max_str.isdigit() or not count_str.isdigit():
            return render_template("quhack2.html", problem=False,
                                   message="Please enter valid numbers.")

        max_number = int(max_str)
        total_questions = int(count_str)

        # Create list of problems
        problem_list = []
        for _ in range(total_questions):
            a = random.randint(0, max_number)
            b = random.randint(0, max_number)
            problem_list.append((a, b))

        # Save to session
        session["problems"] = problem_list
        session["answers"] = []
        session["current"] = 0
        session["total"] = total_questions

        a, b = problem_list[0]
        return render_template("quhack2.html", problem=True,
                               problem_str=f"{a} + {b}",
                               message=None)

    # --- USER CLICKED "HINT" ---
    if request.form.get("action") == "hint":
        problems = session.get("problems")
        cur = session.get("current")

        if problems is None:
            return redirect("/quhack2.html")

        a, b = problems[cur]
        correct = a + b

        # Range of width 10
        low = correct - 5
        high = correct + 5

        if low < 0:
            low = 0
            high = 10

        hint_text = f"The answer is between {low} and {high}."

        return render_template("quhack2.html",
                               problem=True,
                               problem_str=f"{a} + {b}",
                               hint=hint_text)

    # --- USER SUBMITTED AN ANSWER ---
    if "user_answer" in request.form:
        ans_str = request.form["user_answer"].strip()

        if not ans_str.isdigit():
            problems = session["problems"]
            cur = session["current"]
            a, b = problems[cur]
            return render_template("quhack2.html", problem=True,
                                   problem_str=f"{a} + {b}",
                                   message="Enter a valid integer.")

        user_ans = int(ans_str)

        problems = session["problems"]
        cur = session["current"]
        a, b = problems[cur]
        correct = a + b

        session["answers"].append({
            "problem": f"{a} + {b}",
            "your_answer": user_ans,
            "correct_answer": correct,
            "status": "Correct" if user_ans == correct else "Incorrect"
        })

        session["current"] += 1

        # If finished → show summary table
        if session["current"] >= session["total"]:
            return render_template("quhack2.html",
                                   problem=False,
                                   results=session["answers"])

        # Otherwise show next problem
        a, b = problems[session["current"]]
        return render_template("quhack2.html",
                               problem=True,
                               problem_str=f"{a} + {b}",
                               message=None)

    # fallback
    return redirect("/quhack2.html")


 #########################################################################################################
 ## Multiplication###################
# ----------------------------
# Multiplication Problem Generator
# ----------------------------
def generate_problem_mul(max_number):
    a = random.randint(0, max_number)
    b = random.randint(0, max_number)
    return (a, b)

# ----------------------------
# Multiplication Route
# ----------------------------
@app.route('/mul', methods=["GET", "POST"])
def multiplication():
    if request.method == "POST":
        action = request.form.get("action", "")

        # Initialize problems
        if "max_number" in request.form and "num_questions" in request.form:
            max_number = int(request.form["max_number"])
            total_questions = int(request.form["num_questions"])

            problems = [generate_problem_mul(max_number) for _ in range(total_questions)]
            session["problems"] = problems
            session["current"] = 0
            session["results"] = []
            session["max_number"] = max_number
            session["total_questions"] = total_questions

        # Safety check
        if "problems" not in session or session["current"] >= len(session["problems"]):
            return render_template("quhack4.html", problem=False, results=session.get("results", []))

        current_index = session["current"]
        a, b = session["problems"][current_index]

        # -------------------
        # Hint requested
        # -------------------
        if action == "hint":
            low = max((a * b) - 5, 0)
            high = (a * b) + 5
            hint_text = f"The answer is between {low} and {high}."
            return render_template("quhack4.html", problem_str=f"{a} × {b} = ?", hint=hint_text)

        # -------------------
        # User submitted answer
        # -------------------
        if "user_answer" in request.form:
            user_answer_str = request.form.get("user_answer", "").strip()
            if not user_answer_str.isdigit():
                return render_template(
                    "quhack4.html",
                    problem_str=f"{a} × {b} = ?",
                    message="Enter a valid integer."
                )
            user_answer = int(user_answer_str)
            correct_answer = a * b

            # Record result
            results = session.get("results", [])
            results.append({
                "problem": f"{a} × {b} = ?",
                "your_answer": user_answer,
                "correct_answer": correct_answer,
                "status": "Correct" if user_answer == correct_answer else "Incorrect"
            })
            session["results"] = results

            # Move to next question
            session["current"] += 1

            # If all done, show summary
            if session["current"] >= session["total_questions"]:
                return render_template("quhack4.html", problem=False, results=results)

        # -------------------
        # Show current problem
        # -------------------
        if session["current"] < len(session["problems"]):
            a, b = session["problems"][session["current"]]
            return render_template("quhack4.html", problem_str=f"{a} × {b} = ?")

    # GET request → show start form
    return render_template("quhack4.html", problem=False)


 #########################################################################################################



 ## Division ###################

# ----------------------------
# Division Problem Generator
# ----------------------------
def generate_problem_div(max_number):
    while True:
        b = random.randint(1, max_number)  # avoid division by zero
        a = random.randint(0, max_number * b)
        return (a, b)

# ----------------------------
# Division Route
# ----------------------------
@app.route('/div', methods=["GET", "POST"])
def division():
    if request.method == "POST":
        action = request.form.get("action", "")

        # Initialize problems
        if "max_number" in request.form and "num_questions" in request.form:
            max_number = int(request.form["max_number"])
            total_questions = int(request.form["num_questions"])

            problems = [generate_problem_div(max_number) for _ in range(total_questions)]
            session["problems"] = problems
            session["current"] = 0
            session["results"] = []
            session["max_number"] = max_number
            session["total_questions"] = total_questions

        # Safety check
        if "problems" not in session or session["current"] >= len(session["problems"]):
            return render_template("quhack5.html", problem=False, results=session.get("results", []))

        current_index = session["current"]
        a, b = session["problems"][current_index]

        # -------------------
        # Hint requested
        # -------------------
        if action == "hint":
            quotient = a // b
            low = max(quotient - 5, 0)
            high = quotient + 5
            hint_text = f"The answer(quotient) is between {low} and {high}."
            return render_template("quhack5.html", problem_str=f"{a} ÷ {b} = ?", hint=hint_text)

        # -------------------
        # User submitted answer
        # -------------------
        if "user_answer" in request.form:
            user_answer_str = request.form.get("user_answer", "").strip()
            if not user_answer_str.isdigit():
                return render_template(
                    "quhack5.html",
                    problem_str=f"{a} ÷ {b} = ?",
                    message="Enter a valid integer."
                )
            user_answer = int(user_answer_str)
            correct_answer = a // b

            # Record result
            results = session.get("results", [])
            results.append({
                "problem": f"{a} ÷ {b} = ?",
                "your_answer": user_answer,
                "correct_answer": correct_answer,
                "status": "Correct" if user_answer == correct_answer else "Incorrect"
            })
            session["results"] = results

            # Move to next question
            session["current"] += 1

            # If all done, show summary
            if session["current"] >= session["total_questions"]:
                return render_template("quhack5.html", problem=False, results=results)

        # -------------------
        # Show current problem
        # -------------------
        if session["current"] < len(session["problems"]):
            a, b = session["problems"][session["current"]]
            return render_template("quhack5.html", problem_str=f"{a} ÷ {b} = ?")

    # GET request → show start form
    return render_template("quhack5.html", problem=False)


 #########################################################################################################

 ## ALL ###################
@app.route('/quhack6.html', methods =["GET", "POST"])
@app.route('/all', methods=['GET', 'POST'])
def index_all():
    if request.method == 'POST':
        # Distinguish between setting max_number and checking answer
        if 'max_number' in request.form:
            max_str = request.form['max_number'].strip()
            if not max_str.isdigit():
                return render_template('quhack6.html', problem=False, message="Please enter a valid integer for max number.") 
                                   
            max_number = int(max_str)
            # Generate the problem
            problem_str, solution = generate_problem_all(max_number)


            session['problem_str'] = problem_str
            session['solution'] = solution
            session['max_number'] = max_number
      

            return render_template('quhack6.html', 
                                   problem=True, 
                                   problem_str=problem_str,
                                   message=None)
        else:
                # User submitted an answer
                user_answer_str = request.form.get('user_answer', '').strip()
                if not user_answer_str.isdigit():
                    # Invalid input, show the same problem again
                    problem_str = session.get('problem_str')
                    return render_template('quhack6.html',
                                        problem=True,
                                        problem_str=problem_str,
                                        message="Please enter a valid integer answer.")

                user_answer = int(user_answer_str)
                correct_answer = session.get('solution')
                if user_answer == correct_answer:
                    message = "Correct!"
                else:
                    message = f"Incorrect. The correct answer was {correct_answer}."
                return render_template('quhack6.html', 
                                    problem=False, 
                                    message=message)


    # GET request: prompt for max number
    return render_template('quhack6.html', problem=False, message=None)
            
def generate_problem_all(max_number):
    # We have 3 types of problems:
    #8)


    problem_type = random.choice([1,2,3,4,5,6,7,8])
    
    for _ in range(100):
        a = random.randint(0, max_number)
        b = random.randint(0, max_number)
        
        if problem_type == 8:
            # a / b = ?
            c = int(a/b)
            if c <= max_number:
                if b != 0:    
                    return f"{a} / {b} = ?", c, 
                else:
                    pass
        elif problem_type == 7:
            # a x b = ?
            c = a * b
            if c <= max_number:
                return f"{a} x {b} = ?", c  
        elif problem_type == 1:
            # a + b = ?
            c = a + b
            if c <= max_number:
                return f"{a} + {b} = ?", c

        elif problem_type == 2:
            # a + ? = c
            c = random.randint(0, max_number)
            missing = c - a
            if missing <= max_number:
                return f"{a} + ? = {c}", missing

        elif problem_type == 3:
            # ? + b = c
            c = random.randint(0, max_number)
            missing = c - b
            if 0 <= missing <= max_number:
                return f"? + {b} = {c}", missing     
        elif problem_type == 4:
            # a - b = ?
            c = a - b
            if 0 <= c <= max_number:
                return f"{a} - {b} = ?", c

        elif problem_type == 5:
            # a - ? = c
            c = random.randint(0, max_number)
            missing = a - c
            if 0 <= missing <= max_number:
                return f"{a} - ? = {c}", missing

        elif problem_type == 6:
            # ? - b = c
            c = random.randint(0, max_number)
            missing = b + c
            if 0 <= missing <= max_number:
                return f"? - {b} = {c}", missing 

    # If no valid problem found, default to something simple
    return "2 + 2", 4

@app.route('/reset', methods=['GET'])
def reset_all():
    session.clear()
    return render_template('quhack6.html')


#########################################################################################################
## Fractions and Decimals Randomized Test ###################

def format_number(value):
    fraction = Fraction(value)
    if fraction.denominator == 1:
        return str(fraction.numerator)
    return f"{fraction.numerator}/{fraction.denominator}"


def format_decimal(value):
    text = f"{float(value):.2f}".rstrip("0").rstrip(".")
    return text if text else "0"


def format_mixed_number(value, number_type):
    if number_type == "decimal":
        return format_decimal(value)
    return format_number(value)


def parse_fraction_answer(numerator_text, denominator_text):
    numerator = int(numerator_text.strip())
    denominator = int(denominator_text.strip())
    return Fraction(numerator, denominator)


def parse_decimal_answer(answer_text):
    return Fraction(answer_text.strip())


def answers_match(user_answer, correct_answer, answer_type):
    if answer_type == "fraction":
        return user_answer == correct_answer
    return abs(float(user_answer - correct_answer)) < 0.01


def generate_fraction_operand(max_number):
    denominator = random.randint(2, 10)
    numerator = random.randint(1, max_number * denominator)
    return Fraction(numerator, denominator)


def generate_decimal_operand(max_number):
    decimal_places = random.choice([1, 2])
    scale = 10 ** decimal_places
    return Fraction(random.randint(1, max_number * scale), scale)


def generate_advanced_operand(max_number, number_mode):
    if number_mode == "both":
        number_mode = random.choice(["fraction", "decimal"])
    if number_mode == "decimal":
        return generate_decimal_operand(max_number), "decimal"
    return generate_fraction_operand(max_number), "fraction"


def generate_advanced_problem(max_number, operations, number_mode):
    operation = random.choice(operations)
    a, a_type = generate_advanced_operand(max_number, number_mode)
    b, b_type = generate_advanced_operand(max_number, number_mode)

    if operation == "addition":
        symbol = "+"
        answer = a + b
    elif operation == "subtraction":
        symbol = "-"
        answer = a - b
    elif operation == "multiplication":
        symbol = "x"
        answer = a * b
    else:
        symbol = "/"
        while b == 0:
            b, b_type = generate_advanced_operand(max_number, number_mode)
        answer = a / b

    answer_type = "decimal" if a_type == "decimal" or b_type == "decimal" else "fraction"
    problem_str = f"{format_mixed_number(a, a_type)} {symbol} {format_mixed_number(b, b_type)} = ?"
    return {
        "problem": problem_str,
        "answer": str(answer),
        "answer_type": answer_type,
        "display_answer": format_decimal(answer) if answer_type == "decimal" else format_number(answer),
        "decimal_answer": format_decimal(answer)
    }


@app.route('/advanced', methods=["GET", "POST"])
def advanced_test():
    if request.method == "GET":
        return render_template("quhack10.html", problem=False)

    action = request.form.get("action", "")

    if "max_number" in request.form and "num_questions" in request.form:
        max_str = request.form.get("max_number", "").strip()
        count_str = request.form.get("num_questions", "").strip()
        number_mode = request.form.get("number_mode", "both")
        operations = request.form.getlist("operations")

        if "all" in operations:
            operations = ["addition", "subtraction", "multiplication", "division"]

        if not max_str.isdigit() or not count_str.isdigit():
            return render_template("quhack10.html", problem=False, message="Please enter valid numbers.")

        if not operations:
            return render_template("quhack10.html", problem=False, message="Please choose at least one operation.")

        max_number = int(max_str)
        total_questions = int(count_str)

        if max_number < 1 or total_questions < 1:
            return render_template("quhack10.html", problem=False, message="Please enter numbers greater than 0.")

        problems = [generate_advanced_problem(max_number, operations, number_mode) for _ in range(total_questions)]
        session["advanced_problems"] = problems
        session["advanced_current"] = 0
        session["advanced_results"] = []
        session["advanced_total"] = total_questions

    if "advanced_problems" not in session or session["advanced_current"] >= len(session["advanced_problems"]):
        return render_template("quhack10.html", problem=False, results=session.get("advanced_results", []))

    current_problem = session["advanced_problems"][session["advanced_current"]]
    correct_answer = Fraction(current_problem["answer"])

    if action == "hint":
        hint_text = f"The answer is about {current_problem['decimal_answer']} as a decimal."
        return render_template(
            "quhack10.html",
            problem=True,
            problem_str=current_problem["problem"],
            answer_type=current_problem["answer_type"],
            hint=hint_text
        )

    if current_problem["answer_type"] == "decimal" and "user_answer_decimal" in request.form:
        user_answer_str = request.form.get("user_answer_decimal", "").strip()
        try:
            user_answer = parse_decimal_answer(user_answer_str)
        except ValueError:
            return render_template(
                "quhack10.html",
                problem=True,
                problem_str=current_problem["problem"],
                answer_type=current_problem["answer_type"],
                message="Enter a valid decimal."
            )
    elif current_problem["answer_type"] == "fraction" and "answer_numerator" in request.form and "answer_denominator" in request.form:
        numerator_str = request.form.get("answer_numerator", "").strip()
        denominator_str = request.form.get("answer_denominator", "").strip()
        try:
            user_answer = parse_fraction_answer(numerator_str, denominator_str)
        except (ValueError, ZeroDivisionError):
            return render_template(
                "quhack10.html",
                problem=True,
                problem_str=current_problem["problem"],
                answer_type=current_problem["answer_type"],
                message="Enter a valid numerator and denominator."
            )

        user_answer_str = f"{numerator_str}/{denominator_str}"
    else:
        return render_template(
            "quhack10.html",
            problem=True,
            problem_str=current_problem["problem"],
            answer_type=current_problem["answer_type"]
        )

    if "user_answer_decimal" in request.form or "answer_numerator" in request.form:
        results = session.get("advanced_results", [])
        results.append({
            "problem": current_problem["problem"],
            "your_answer": user_answer_str,
            "correct_answer": current_problem["display_answer"],
            "status": "Correct" if answers_match(user_answer, correct_answer, current_problem["answer_type"]) else "Incorrect"
        })
        session["advanced_results"] = results
        session["advanced_current"] += 1

        if session["advanced_current"] >= session["advanced_total"]:
            return render_template("quhack10.html", problem=False, results=results)

    current_problem = session["advanced_problems"][session["advanced_current"]]
    return render_template(
        "quhack10.html",
        problem=True,
        problem_str=current_problem["problem"],
        answer_type=current_problem["answer_type"]
    )


def parse_test_answer(problem, form_data, index):
    if problem["answer_type"] == "decimal":
        answer_text = form_data.get(f"decimal_answer_{index}", "").strip()
        if not answer_text:
            raise ValueError
        return parse_decimal_answer(answer_text), answer_text

    numerator_text = form_data.get(f"answer_numerator_{index}", "").strip()
    denominator_text = form_data.get(f"answer_denominator_{index}", "").strip()
    if not numerator_text or not denominator_text:
        raise ValueError
    return parse_fraction_answer(numerator_text, denominator_text), f"{numerator_text}/{denominator_text}"


@app.route('/test', methods=["GET", "POST"])
def full_test():
    if request.method == "GET":
        return render_template("quhack11.html", test=False)

    if "max_number" in request.form and "num_questions" in request.form:
        max_str = request.form.get("max_number", "").strip()
        count_str = request.form.get("num_questions", "").strip()
        number_mode = request.form.get("number_mode", "both")
        operations = request.form.getlist("operations")

        if "all" in operations:
            operations = ["addition", "subtraction", "multiplication", "division"]

        if not max_str.isdigit() or not count_str.isdigit():
            return render_template("quhack11.html", test=False, message="Please enter valid numbers.")

        if not operations:
            return render_template("quhack11.html", test=False, message="Please choose at least one operation.")

        max_number = int(max_str)
        total_questions = int(count_str)

        if max_number < 1 or total_questions < 1:
            return render_template("quhack11.html", test=False, message="Please enter numbers greater than 0.")

        test_questions = [generate_advanced_problem(max_number, operations, number_mode) for _ in range(total_questions)]
        session["test_questions"] = test_questions
        return render_template("quhack11.html", test=True, questions=test_questions)

    if request.form.get("action") == "submit_test":
        test_questions = session.get("test_questions", [])
        if not test_questions:
            return render_template("quhack11.html", test=False, message="Please start a test first.")

        results = []
        correct_count = 0

        for index, problem in enumerate(test_questions):
            correct_answer = Fraction(problem["answer"])
            try:
                user_answer, user_answer_text = parse_test_answer(problem, request.form, index)
                is_correct = answers_match(user_answer, correct_answer, problem["answer_type"])
            except (ValueError, ZeroDivisionError):
                user_answer_text = "No valid answer"
                is_correct = False

            if is_correct:
                correct_count += 1

            results.append({
                "problem": problem["problem"],
                "your_answer": user_answer_text,
                "correct_answer": problem["display_answer"],
                "status": "Correct" if is_correct else "Incorrect"
            })

        incorrect_count = len(test_questions) - correct_count
        add_to_stats(len(test_questions), correct_count, incorrect_count)
        session["last_test_results"] = results

        return render_template(
            "quhack11.html",
            test=False,
            results=results,
            summary={
                "answered": len(test_questions),
                "correct": correct_count,
                "incorrect": incorrect_count
            },
            session_stats=get_session_stats()
        )

    return render_template("quhack11.html", test=False)


@app.route('/account', methods=["GET", "POST"])
def account():
    message = None

    if request.method == "POST":
        action = request.form.get("action", "")

        if action == "logout":
            session.pop("user_id", None)
            session.pop("username", None)
            message = "Logged out."
        else:
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "").strip()

            if not username or not password:
                message = "Enter a username and password."
            elif action == "register":
                connection = get_db_connection()
                try:
                    cursor = connection.execute(
                        "INSERT INTO users (username, password) VALUES (?, ?)",
                        (username, generate_password_hash(password))
                    )
                    connection.commit()
                    session["user_id"] = cursor.lastrowid
                    session["username"] = username
                    message = "Account created."
                except sqlite3.IntegrityError:
                    message = "That username already exists."
                connection.close()
            elif action == "login":
                connection = get_db_connection()
                user = connection.execute(
                    "SELECT * FROM users WHERE username = ?",
                    (username,)
                ).fetchone()
                connection.close()

                if user and check_password_hash(user["password"], password):
                    session["user_id"] = user["id"]
                    session["username"] = user["username"]
                    message = "Logged in."
                else:
                    message = "Username or password did not match."

    return render_template(
        "quhack12.html",
        user=get_account_stats(),
        site_stats=get_site_stats(),
        message=message
    )



if __name__=='__main__':
   app.run(debug=True)

  
