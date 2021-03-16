from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

from telegram import Update

import logging
from app.config import Config
import random

from app.firestore_service import get_questions, set_answer, get_answers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


ANSWERS = []
id_question = 0


def start(update, context) -> None:
    """Inform user about what this bot can do"""
    global ANSWERS, id_question
    ANSWERS = []

    id_question = 0
    update.message.reply_text(
        'Please select /question to get the poll'
    )


def question(update, context) -> None:
    global id_question
    # get the questions objects from db
    questions_obj = get_questions()

    # get list ids from the objects questions
    question_id_list = [q_id for q_id in questions_obj]

    # get list from the objects questions
    questions = [q.to_dict()['question'] for q in questions_obj]

    if update.message.text != '/question':
        # get id from the current question
        question_id = question_id_list[id_question].id

        # get the answers from the user
        ANSWERS.append(update.message.text)
        set_answer(question_id, update.message.text)
        id_question += 1

    try:
        update.message.reply_text(questions[id_question])

    except:
        update.message.reply_text('Hemos terminado la preguntas, Gracias!')


def main() -> None:

    config = Config()
    # Create the Updater and pass it your bot's token.
    updater = Updater(config.BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('question', question))
    dispatcher.add_handler(MessageHandler(Filters.text, question))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
