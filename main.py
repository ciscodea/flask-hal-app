from app import create_app
from app.forms import QuestionForm

from flask import render_template, redirect, url_for, flash
from app.firestore_service import get_questions, set_question, delete_question, get_answers


app = create_app()


@app.route('/', methods=['GET', 'POST'])
def home():
    """ This is the home directory """
    question_form = QuestionForm()
    questions = get_questions()

    context = {
        'questions': questions,
        'question_form': question_form,

    }

    if question_form.validate_on_submit():
        set_question(question=question_form.question.data)
        flash('Se agrego la pregunta')
        return redirect(url_for('home'))

    return render_template('home.html', **context)


@app.route('/questions/delete/<question_id>', methods=['POST', 'GET'])
def delete(question_id):
    """ Delete questions passing arg question id """
    delete_question(question_id=question_id)

    return redirect(url_for('home'))
