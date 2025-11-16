import time
import random

# importing Flask and other modules
from flask import Flask, render_template, request, session, redirect, url_for
 
# Flask constructor
app = Flask(__name__)   
app.secret_key = "a_very_secret_key_for_session"  # Replace with a secure key in production 


######FLASK####
@app.route('/')
def home():
    return render_template('quhack.html')

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



max_number = 0
#########################################################################################################



 ## Subtraction ###################

# --------------------------------------------------------
# PROBLEM GENERATOR  (MUST COME BEFORE ROUTES)
# --------------------------------------------------------
def generate_problem_sub(max_number):
    # Types:
    # 4) a - b = ?
    # 5) a - ? = c
    # 6) ? - b = c

    problem_type = random.choice([4, 5, 6])

    for _ in range(100):
        a = random.randint(0, max_number)
        b = random.randint(0, max_number)

        if problem_type == 4:
            c = a - b
            if 0 <= c <= max_number:
                return f"{a} - {b} = ?", c

        elif problem_type == 5:
            c = random.randint(0, max_number)
            missing = a - c
            if 0 <= missing <= max_number:
                return f"{a} - ? = {c}", missing

        elif problem_type == 6:
            c = random.randint(0, max_number)
            missing = b + c
            if 0 <= missing <= max_number:
                return f"? - {b} = {c}", missing

    return "4 - 2 = ?", 2


# --------------------------------------------------------
# SUBTRACTION ROUTE
# --------------------------------------------------------
@app.route('/quhack3.html', methods=["GET", "POST"])
@app.route('/sub', methods=["GET", "POST"])
def index_sub():

    # ----------------------------------------------------
    # USER JUST SUBMITTED max_number + num_questions
    # ----------------------------------------------------
    if request.method == "POST" and "max_number" in request.form and "num_questions" in request.form:
        max_str = request.form['max_number'].strip()
        count_str = request.form['num_questions'].strip()

        if not max_str.isdigit() or not count_str.isdigit():
            return render_template("quhack3.html", problem=False,
                                   message="Please enter valid whole numbers.")

        max_number = int(max_str)
        total_questions = int(count_str)

        # Initialize session tracking
        session['max_number'] = max_number
        session['total_questions'] = total_questions
        session['questions_answered'] = 0
        session['results'] = []

        # Generate first problem
        p_str, sol = generate_problem_sub(max_number)
        session['problem_str'] = p_str
        session['solution'] = sol

        return render_template("quhack3.html", problem=True, problem_str=p_str)

    # ----------------------------------------------------
    # USER ANSWERS A PROBLEM
    # ----------------------------------------------------
    if request.method == "POST" and "user_answer" in request.form:
        answer_str = request.form.get("user_answer", "").strip()

        if not answer_str.isdigit():
            return render_template("quhack3.html",
                                   problem=True,
                                   problem_str=session.get("problem_str"),
                                   message="Enter a valid integer.")

        user_answer = int(answer_str)
        correct_answer = session.get("solution")
        problem_str = session.get("problem_str")

        # Record result
        results = session.get("results", [])
        results.append({
            "problem": problem_str,
            "your_answer": user_answer,
            "correct_answer": correct_answer,
            "status": "Correct" if user_answer == correct_answer else "Incorrect"
        })
        session['results'] = results

        # Increment count
        session['questions_answered'] += 1

        # If done → show summary
        if session['questions_answered'] >= session['total_questions']:
            return render_template("quhack3.html", 
                                   problem=False, 
                                   results=results)

        # Otherwise, generate next problem
        max_number = session.get("max_number")
        p_str, sol = generate_problem_sub(max_number)
        session['problem_str'] = p_str
        session['solution'] = sol

        return render_template("quhack3.html", problem=True, problem_str=p_str)

    # ----------------------------------------------------
    # GET request (first page load)
    # ----------------------------------------------------
    return render_template("quhack3.html", problem=False, message=None)


# --------------------------------------------------------
# RESET ROUTE
# --------------------------------------------------------
@app.route('/reset')
def reset_sub():
    session.clear()
    return render_template('quhack3.html')

#########################################################################################################


 ## Adition ###################

@app.route("/add", methods=["GET", "POST"])
def add():
    # setup game if no session
    if "problems" not in session:
        session["problems"] = []
        session["current"] = 0
        session["results"] = []
        session["max_number"] = None
        session["num_questions"] = None

    # If GET → just show page
    if request.method == "GET":
        return render_template("quhack2.html")

    # POST logic
    action = request.form.get("action")   # "check" or "hint"

    # If starting the game
    if session["max_number"] is None:
        try:
            max_num = int(request.form["max_number"])
            num_q = int(request.form["num_questions"])
        except:
            return render_template("quhack2.html",
                                   message="Please enter valid numbers.")

        # generate problems
        import random
        session["problems"] = [(random.randint(0, max_num), random.randint(0, max_num))
                               for _ in range(num_q)]
        session["max_number"] = max_num
        session["num_questions"] = num_q
        session["current"] = 0
        session["results"] = []

        a, b = session["problems"][0]
        return render_template("quhack2.html",
                               problem=True,
                               problem_str=f"{a} + {b}",
                               hint=None)

    # If HINT was pressed
    if action == "hint":
        a, b = session["problems"][session["current"]]
        # Simple useful hint:
        # Show the tens-break addition
        tens = a + (10 - (a % 10)) if a % 10 != 0 else a  # next round number
        hint_text = f"Try adding to the nearest 10 first: {a} + {b} → {tens} + (remaining)."

        a, b = session["problems"][session["current"]]
        return render_template("quhack2.html",
                               problem=True,
                               problem_str=f"{a} + {b}",
                               hint=hint_text)

    # Otherwise, user clicked CHECK
    user_answer = request.form.get("user_answer", "").strip()

    # Validate
    if not user_answer.isdigit():
        a, b = session["problems"][session["current"]]
        return render_template("quhack2.html",
                               message="Please enter a number.",
                               problem=True,
                               problem_str=f"{a} + {b}")

    user_answer = int(user_answer)
    a, b = session["problems"][session["current"]]
    correct = a + b

    # record result
    session["results"].append({
        "problem": f"{a} + {b}",
        "your_answer": user_answer,
        "correct_answer": correct,
        "status": "Correct" if user_answer == correct else "Incorrect"
    })

    session["current"] += 1

    # Game finished?
    if session["current"] >= session["num_questions"]:
        results = session["results"]
        session.clear()
        return render_template("quhack2.html", results=results)

    # next problem
    a, b = session["problems"][session["current"]]
    return render_template("quhack2.html",
                           problem=True,
                           problem_str=f"{a} + {b}")



 #########################################################################################################



 ## Multiplication###################
@app.route('/mul', methods=['GET', 'POST'])
@app.route('/quhack4.html', methods=['GET', 'POST'])
def index_mul():
    if request.method == 'POST':

        if 'max_number' in request.form:
            max_str = request.form['max_number'].strip()
            num_str = request.form['num_questions'].strip()

            if not max_str.isdigit() or not num_str.isdigit():
                return render_template('quhack4.html', problem=False,
                                       message="Enter valid integers.",
                                       results=None)

            max_number = int(max_str)
            num_questions = int(num_str)

            session['max_number'] = max_number
            session['num_questions'] = num_questions
            session['current_q'] = 0
            session['results'] = []

            problem_str, solution = generate_problem_mul(max_number)
            session['problem_str'] = problem_str
            session['solution'] = solution

            return render_template('quhack4.html', problem=True,
                                   problem_str=problem_str)

        else:
            ans_str = request.form.get('user_answer', '').strip()

            if not ans_str.isdigit():
                return render_template('quhack4.html',
                                       problem=True,
                                       problem_str=session['problem_str'],
                                       message="Enter a valid integer.")

            user_answer = int(ans_str)
            correct = session['solution']

            session['results'].append({
                "problem": session['problem_str'],
                "your_answer": user_answer,
                "correct_answer": correct,
                "status": "Correct" if user_answer == correct else "Incorrect"
            })

            session['current_q'] += 1

            if session['current_q'] >= session['num_questions']:
                return render_template("quhack4.html",
                                       problem=False,
                                       results=session['results'])

            problem_str, solution = generate_problem_mul(session['max_number'])
            session['problem_str'] = problem_str
            session['solution'] = solution

            return render_template("quhack4.html",
                                   problem=True,
                                   problem_str=problem_str)

    return render_template("quhack4.html", problem=False)


def generate_problem_mul(max_number):
    a = random.randint(0, max_number)
    b = random.randint(0, max_number)
    return f"{a} × {b} = ?", a * b


# -------------------------------------------
# MULTIPLICATION PROBLEM GENERATOR
# -------------------------------------------
def generate_multiplication_problem(max_number):
    a = random.randint(0, max_number)
    b = random.randint(0, max_number)
    c = a * b

    return f"{a} × {b} = ?", c


# -------------------------------------------
# MULTIPLICATION ROUTES
# -------------------------------------------
@app.route('/multiplication', methods=["GET", "POST"])
def multiplication():
    if request.method == "POST":
        if "max_number" in request.form:
            max_number = int(request.form["max_number"])
            problem, solution = generate_multiplication_problem(max_number)

            session["max_number"] = max_number
            session["problem"] = problem
            session["solution"] = solution

            return render_template("multiplication.html",
                                   problem=True,
                                   problem_str=problem)

        if "user_answer" in request.form:
            user_answer = int(request.form["user_answer"])
            correct = session["solution"]

            if user_answer == correct:
                message = "Correct!"
            else:
                message = f"Incorrect. The answer is {correct}."

            return render_template("multiplication.html",
                                   problem=False,
                                   message=message)

    return render_template("multiplication.html", problem=False)


 #########################################################################################################



 ## Division ###################

@app.route('/div', methods=['GET', 'POST'])
@app.route('/quhack5.html', methods=['GET', 'POST'])
def index_div():
    if request.method == 'POST':

        if 'max_number' in request.form:
            max_str = request.form['max_number'].strip()
            num_str = request.form['num_questions'].strip()

            if not max_str.isdigit() or not num_str.isdigit():
                return render_template('quhack5.html', problem=False,
                                       message="Enter valid integers.",
                                       results=None)

            max_number = int(max_str)
            num_questions = int(num_str)

            session['max_number'] = max_number
            session['num_questions'] = num_questions
            session['current_q'] = 0
            session['results'] = []

            problem_str, solution = generate_problem_div(max_number)
            session['problem_str'] = problem_str
            session['solution'] = solution

            return render_template('quhack5.html',
                                   problem=True,
                                   problem_str=problem_str)

        else:
            ans_str = request.form.get('user_answer', '').strip()

            if not ans_str.isdigit():
                return render_template('quhack5.html',
                                       problem=True,
                                       problem_str=session['problem_str'],
                                       message="Enter a valid integer.")

            user_answer = int(ans_str)
            correct = session['solution']

            session['results'].append({
                "problem": session['problem_str'],
                "your_answer": user_answer,
                "correct_answer": correct,
                "status": "Correct" if user_answer == correct else "Incorrect"
            })

            session['current_q'] += 1

            if session['current_q'] >= session['num_questions']:
                return render_template("quhack5.html",
                                       problem=False,
                                       results=session['results'])

            problem_str, solution = generate_problem_div(session['max_number'])
            session['problem_str'] = problem_str
            session['solution'] = solution

            return render_template("quhack5.html",
                                   problem=True,
                                   problem_str=problem_str)

    return render_template("quhack5.html", problem=False)


def generate_problem_div(max_number):
    b = random.randint(1, max_number)      # divisor
    c = random.randint(0, max_number)      # quotient
    a = b * c                              # dividend
    return f"{a} ÷ {b} = ?", c

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



if __name__=='__main__':
   app.run(debug=True)

  