from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *
import pdb

app = Flask(__name__)

RESP = 'responses'

app.config['SECRET_KEY'] = '12345'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def start():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("home.html", title = title, instructions = instructions)

@app.route('/begin', methods=["POST"])
def start_survey():
    """Clear reponses list."""
    session[RESP] = []
    return redirect('/questions/0')


@app.route('/answer', methods=["POST"])
def get_answer():
   
    answer = request.form['answer']
    responses = session[RESP]
    responses.append(answer)
    session[RESP] = responses

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect ('/finished')
    return  redirect(f"/questions/{len(responses)}")


@app.route('/questions/<int:qid>')
def show_question(qid):
    responses = session.get(RESP)

    if (responses is None):
        return redirect ('/')

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect ('/finished')

    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[qid]
    return render_template(
    'questions.html', question=question)

@app.route('/finished')
def complete():
    responses =  session[RESP]
    questions =  satisfaction_survey.questions
    return render_template('finished.html', responses = responses, questions = questions)


