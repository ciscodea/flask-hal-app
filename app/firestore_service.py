import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


project_id = 'hal-project-307805'
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': project_id,
})
db = firestore.client()


def get_questions():
    return db.collection('questions').get()


def get_answers(question_id, answer_id):
    return db.collection('questions').document(question_id).collection('answers').document(answer_id).get()


def set_question(question):
    question_collection_ref = db.collection('questions')
    question_collection_ref.add({'question': question})


def set_answer(question_id, answer):
    question_collection_ref = db.collection(
        'questions').document(question_id).collection('answers')
    question_collection_ref.add({'answer': answer})


def delete_question(question_id):
    todo_ref = _get_question_ref(question_id=question_id)
    todo_ref.delete()


def _get_question_ref(question_id):
    return db.document(f'questions/{question_id}')
