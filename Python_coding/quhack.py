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


max_number = 0
#########################################################################################################



 ## Subtraction ###################

 

@app.route('/quhack3.html', methods =["GET", "POST"])
@app.route('/sub', methods=['GET', 'POST'])
def index_sub():
    if request.method == 'POST':
        # Distinguish between setting max_number and checking answer
        if 'max_number' in request.form:
            max_str = request.form['max_number'].strip()
            if not max_str.isdigit():
                return render_template('quhack3.html', problem=False, message="Please enter a valid integer for max number")
                       
            max_number = int(max_str)
            # Generate the problem
            problem_str, solution = generate_problem_sub(max_number)

            session['problem_str'] = problem_str
            session['solution'] = solution
            session['max_number'] = max_number

            return render_template('quhack3.html', 
                                   problem=True, 
                                   problem_str=problem_str,
                                   message=None)
        else:
            # User submitted an answer
            user_answer_str = request.form.get('user_answer', '').strip()
            if not user_answer_str.isdigit():
                # Invalid input, show the same problem again
                problem_str = session.get('problem_str')
                return render_template('quhack3.html',
                                       problem=True,
                                       problem_str=problem_str,
                                       message="Please enter a valid integer answer.")

            user_answer = int(user_answer_str)
            correct_answer = session.get('solution')
            if user_answer == correct_answer:
                message = "Correct!"
            else:
                message = f"Incorrect. The correct answer was {correct_answer}."
            return render_template('quhack3.html', 
                                   problem=False, 
                                   message=message)

    # GET request: prompt for max number
    return render_template('quhack3.html', problem=False, message=None)
            
def generate_problem_sub(max_number):
    # We have 6 types of problems:
    # 1) a + b = ?
    # 2) a + ? = c
    # 3) ? + b = c
    # 4) a - b = ?
    # 5) a - ? = c
    # 6) ? - b = c

    problem_type = random.choice([4,5,6])
    
    for _ in range(100):
        a = random.randint(0, max_number)
        b = random.randint(0, max_number)

               
        if problem_type == 4:
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
    return "4-2 = ?", 2

 

@app.route('/reset', methods=['GET'])
def reset_sub():
    session.clear()
    return render_template('quhack3.html')



#########################################################################################################



 ## Adition ###################
@app.route('/quhack2.html', methods =["GET", "POST"])
@app.route('/add', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Distinguish between setting max_number and checking answer
        if 'max_number' in request.form:
            max_str = request.form['max_number'].strip()
            if not max_str.isdigit():
                return render_template('quhack2.html', problem=False, message="Please enter a valid integer for max number.") 
        
                                  
            max_number = int(max_str)
            # Generate the problem
            problem_str, solution = generate_problem(max_number)          

            session['problem_str'] = problem_str
            session['solution'] = solution
            session['max_number'] = max_number

            return render_template('quhack2.html', 
                                   problem=True, 
                                   problem_str=problem_str,
                                   message=None)

        else:
        
            # User submitted an answer
            user_answer_str = request.form.get('user_answer', '').strip()
            if not user_answer_str.isdigit():
                # Invalid input, show the same problem again
                problem_str = session.get('problem_str')
                return render_template('quhack2.html',
                                       problem=True,
                                       problem_str=problem_str,
                                       message="Please enter a valid integer answer.")

            user_answer = int(user_answer_str)
            correct_answer = session.get('solution')
            if user_answer == correct_answer:
                message = "Correct!"
            else:
                message = f"Incorrect. The correct answer was {correct_answer}."
            return render_template('quhack2.html', 
                                   problem=False, 
                                   message=message)


    # GET request: prompt for max number
    return render_template('quhack2.html', problem=False, message=None)
            
def generate_problem(max_number):
    # We have 6 types of problems:
    # 1) a + b = ?
    # 2) a + ? = c
    # 3) ? + b = c
    # 4) a - b = ?
    # 5) a - ? = c
    # 6) ? - b = c

    problem_type = random.choice([1, 2, 3])
    
    for _ in range(100):
        a = random.randint(0, max_number)
        b = random.randint(0, max_number)
        
        if problem_type == 1:
            # a + b = ?
            c = a + b
            if c <= max_number:
                return f"{a} + {b} = ?", c

        elif problem_type == 2:
            # a + ? = c
            c = random.randint(0, max_number)
            missing = c - a
            if 0 <=missing <= max_number:
                return f"{a} + ? = {c}", missing

        elif problem_type == 3:
            # ? + b = c
            c = random.randint(0, max_number)
            missing = c - b
            if 0 <= missing <= max_number:
                return f"? + {b} = {c}", missing

    # If no valid problem found, default to something simple
    return "2 + 2 = ?", 4


@app.route('/reset', methods=['GET'])
def reset():
    session.clear()
    return render_template('quhack2.html')

#########################################################################################################



 ## Multiplacation ###################

@app.route('/quhack4.html', methods =["GET", "POST"])
@app.route('/multi', methods=['GET', 'POST'])
def index_multi():
    if request.method == 'POST':
        # Distinguish between setting max_number and checking answer
        if 'max_number' in request.form:
            max_str = request.form['max_number'].strip()
            if not max_str.isdigit():
                return render_template('quhack4.html', problem=False, message="Please enter a valid integer for max number.") 
                                   
            max_number = int(max_str)
            # Generate the problem
            problem_str, solution = generate_problem_multi(max_number)


            session['problem_str'] = problem_str
            session['solution'] = solution
            session['max_number'] = max_number

            return render_template('quhack4.html', 
                                   problem=True, 
                                   problem_str=problem_str,
                                   message=None) 
        else:
                # User submitted an answer
                user_answer_str = request.form.get('user_answer', '').strip()
                if not user_answer_str.isdigit():
                    # Invalid input, show the same problem again
                    problem_str = session.get('problem_str')
                    return render_template('quhack4.html',
                                        problem=True,
                                        problem_str=problem_str,
                                        message="Please enter a valid integer answer.")

                user_answer = int(user_answer_str)
                correct_answer = session.get('solution')
                if user_answer == correct_answer:
                    message = "Correct!"
                else:
                    message = f"Incorrect. The correct answer was {correct_answer}."
                return render_template('quhack4.html', 
                                    problem=False, 
                                    message=message)


    # GET request: prompt for max number
    return render_template('quhack4.html', problem=False, message=None)
            
def generate_problem_multi(max_number):
    # We have 3 types of problems:
    #7) a * b = ?
    #8) a * ? = c
    #9) ? * b = c

    problem_type = random.choice([7])
    
    for _ in range(100):
        a = random.randint(0, max_number)
        b = random.randint(0, max_number)
        
        if problem_type == 7:
            # a x b = ?
            c = a * b
            if c <= max_number:
                return f"{a} x {b} = ?", c

    # If no valid problem found, default to something simple
    return "2 x 2 = ?", 4
    

@app.route('/reset', methods=['GET'])
def reset_mult():
    session.clear()
    return render_template('quhack4.html')


 #########################################################################################################



 ## Division ###################

 
@app.route('/quhack5.html', methods =["GET", "POST"])
@app.route('/div', methods=['GET', 'POST'])
def index_div():
    if request.method == 'POST':
        # Distinguish between setting max_number and checking answer
        if 'max_number' in request.form:
            max_str = request.form['max_number'].strip()
            if not max_str.isdigit():
                return render_template('quhack5.html', problem=False, message="Please enter a valid integer for max number.") 
                                   
            max_number = int(max_str)
            # Generate the problem
            problem_str, solution1, solution2 = generate_problem_div(max_number)


            session['problem_str'] = problem_str
            session['solution'] = solution1
            session['solution2'] = solution2
            session['max_number'] = max_number

            return render_template('quhack5.html', 
                                   problem=True, 
                                   problem_str=problem_str,
                                   message=None)
        else:
                # User submitted an answer
                user_answer_str  = request.form.get('user_answer', '').strip()
                user_answer2_str = request.form.get('user_answer2','').strip()

                if not user_answer_str.isdigit():
                    # Invalid input, show the same problem again
                    problem_str = session.get('problem_str')
                    return render_template('quhack5.html',
                                        problem=True,
                                        problem_str=problem_str,
                                        message="Please enter a valid integer answer.")
                
                
                if not user_answer2_str.isdigit():
                    # Invalid input, show the same problem again
                    problem_str = session.get('problem_str')
                    return render_template('quhack5.html',
                                        problem=True,
                                        problem_str=problem_str,
                                        message="Please enter a valid integer answer.")

                user_answer = int(user_answer_str)
                user_answer2 =int(user_answer2_str)
                correct_answer = session.get('solution')
                correct_answer2 = session.get('solution2')
                if user_answer == correct_answer and user_answer2 == correct_answer2:
                    message = "Correct!"
                else:
                    message = f"Incorrect. The correct answer was quotient = {correct_answer}, and remainder = {correct_answer2}."
                return render_template('quhack5.html', 
                                    problem=False, 
                                    message=message)


    # GET request: prompt for max number
    return render_template('quhack5.html', problem=False, message=None)
            
def generate_problem_div(max_number):
    # We have 3 types of problems:
    #8)

    problem_type = random.choice([8])
    
    for _ in range(100):
        a = random.randint(0, max_number)
        b = random.randint(0, max_number)
        
        if problem_type == 8:
            # a / b = ?
            if b!=0:
                c = int(a/b)
                d = int(a%b)
                if c <= max_number:
                    if b != 0:    
                        return f"{a} / {b} = ?", c , d
                    else:
                        pass

    # If no valid problem found, default to something simple
    return "4 / 2 = ?", 2 , 0
    

@app.route('/reset', methods=['GET'])
def reset_div():
    session.clear()
    return render_template('quhack5.html')

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

  