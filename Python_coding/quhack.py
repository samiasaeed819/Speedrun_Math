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

@app.route("/sub", methods=["GET", "POST"])
def subtraction():
    if "problems" not in session:
        session["problems"] = [(random.randint(20, 60), random.randint(1, 20)) for _ in range(10)]
        session["current"] = 0
        session["score"] = 0
        session["results"] = []

    if request.method == "POST":
        action = request.form.get("action")
        a, b = session["problems"][session["current"]]

        # Hint action
        if action == "hint":
            answer = a - b
            low = answer - 5
            high = answer + 5
            hint_text = f"The correct answer is between {low} and {high}."
            return render_template("quhack3.html", problem_str=f"{a} - {b} = ?", 
                                   current=session["current"]+1, score=session["score"], hint=hint_text)

        # Answer submitted
        user_answer = request.form.get("user_answer")
        if user_answer and user_answer.isdigit():
            user_answer = int(user_answer)
            correct_answer = a - b
            status = "Correct" if user_answer == correct_answer else "Incorrect"
            session["results"].append({
                "problem": f"{a} - {b} = ?",
                "your_answer": user_answer,
                "correct_answer": correct_answer,
                "status": status
            })
            if user_answer == correct_answer:
                session["score"] += 1

        session["current"] += 1

        if session["current"] >= len(session["problems"]):
            final_results = session["results"]
            score = session["score"]
            session.clear()
            return render_template("quhack3_result.html", results=final_results, score=score)

    a, b = session["problems"][session["current"]]
    return render_template("quhack3.html", problem_str=f"{a} - {b} = ?", 
                           current=session["current"]+1, score=session["score"])

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

@app.route("/mul", methods=["GET", "POST"])
def multiplication():
    if "problems" not in session:
        session["problems"] = [(random.randint(2,12), random.randint(2,12)) for _ in range(10)]
        session["current"] = 0
        session["score"] = 0
        session["results"] = []

    if request.method == "POST":
        action = request.form.get("action")
        a, b = session["problems"][session["current"]]

        if action == "hint":
            answer = a * b
            low = answer - 5
            high = answer + 5
            hint_text = f"The correct answer is between {low} and {high}."
            return render_template("quhack4.html", problem_str=f"{a} × {b} = ?", 
                                   current=session["current"]+1, score=session["score"], hint=hint_text)

        user_answer = request.form.get("user_answer")
        if user_answer and user_answer.isdigit():
            user_answer = int(user_answer)
            correct_answer = a * b
            status = "Correct" if user_answer == correct_answer else "Incorrect"
            session["results"].append({
                "problem": f"{a} × {b} = ?",
                "your_answer": user_answer,
                "correct_answer": correct_answer,
                "status": status
            })
            if user_answer == correct_answer:
                session["score"] += 1

        session["current"] += 1
        if session["current"] >= len(session["problems"]):
            final_results = session["results"]
            score = session["score"]
            session.clear()
            return render_template("quhack4_result.html", results=final_results, score=score)

    a, b = session["problems"][session["current"]]
    return render_template("quhack4.html", problem_str=f"{a} × {b} = ?", 
                           current=session["current"]+1, score=session["score"])


 #########################################################################################################



 ## Division ###################


@app.route("/div", methods=["GET", "POST"])
def division():
    if "problems" not in session:
        problems = []
        for _ in range(10):
            b = random.randint(2,12)
            answer = random.randint(2,12)
            a = b * answer  # ensures clean division
            problems.append((a, b))
        session["problems"] = problems
        session["current"] = 0
        session["score"] = 0
        session["results"] = []

    if request.method == "POST":
        action = request.form.get("action")
        a, b = session["problems"][session["current"]]

        if action == "hint":
            answer = a // b
            low = answer - 5
            high = answer + 5
            hint_text = f"The correct answer is between {low} and {high}."
            return render_template("quhack5.html", problem_str=f"{a} ÷ {b} = ?", 
                                   current=session["current"]+1, score=session["score"], hint=hint_text)

        user_answer = request.form.get("user_answer")
        if user_answer and user_answer.isdigit():
            user_answer = int(user_answer)
            correct_answer = a // b
            status = "Correct" if user_answer == correct_answer else "Incorrect"
            session["results"].append({
                "problem": f"{a} ÷ {b} = ?",
                "your_answer": user_answer,
                "correct_answer": correct_answer,
                "status": status
            })
            if user_answer == correct_answer:
                session["score"] += 1

        session["current"] += 1
        if session["current"] >= len(session["problems"]):
            final_results = session["results"]
            score = session["score"]
            session.clear()
            return render_template("quhack5_result.html", results=final_results, score=score)

    a, b = session["problems"][session["current"]]
    return render_template("quhack5.html", problem_str=f"{a} ÷ {b} = ?", 
                           current=session["current"]+1, score=session["score"])

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

  