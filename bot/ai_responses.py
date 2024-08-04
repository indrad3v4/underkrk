import os
from openai import OpenAI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from logs import logging, error_logger

# Initialize OpenAI client
MODEL = "gpt-4o-mini"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AIResponses:
    def __init__(self, rave_model):
        self.rave_model = rave_model

    def generate_ai_response(self, role, user_message):
        try:
            completion = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": f"You are AI-Powered Rave Coordinator Bot who helps roles in the rave get an ideal rave experience. You base your juicy yet funny tone of voice on values of peace, love, unity, respect. The rave details are: Insight: {self.rave_model.insight}, Sound System: {self.rave_model.soundsystem}, Lineup: {self.rave_model.lineup}, Place: {self.rave_model.place}, Time: {self.rave_model.time}, style='ravecore', bpm=150, Role: {role}"},
                    {"role": "user", "content": user_message}
                ]
            )
            response = completion.choices[0].message.content
            logging.info(f"AI response generated for role {role} with message: {user_message}")
            return response
        except Exception as e:
            error_logger.error("Exception occurred while generating AI response", exc_info=True)
            return "Sorry, I encountered an error while generating a response. Please try again later."

    async def handle_message(self, update: Update, context: CallbackContext) -> None:
        user_message = update.message.text
        user = update.message.from_user
        user_nickname = user.username if user.username else user.first_name

        role = context.bot_data.get('roles', {}).get(user.id, "rave participant")
        response = self.generate_ai_response(role, user_message)

        await update.message.reply_text(f"<b>{response}</b>", parse_mode='HTML')

        # Add button for further actions
        keyboard = [
            [InlineKeyboardButton("Ask a question to AI about rave", callback_data=f'ask_question_{update.message.message_id}')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_html("What next?", reply_markup=reply_markup)

    async def handle_ai_question(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        user_id = query.from_user.id
        user_nickname = query.from_user.username if query.from_user.username else query.from_user.first_name

        role = context.bot_data.get('roles', {}).get(user_id, "rave participant")
        response = self.generate_ai_response(role, "I have a question about the rave")

        await query.edit_message_text(f"<b>{response}</b>", parse_mode='HTML')

        # Add button for further actions to continue the game
        keyboard = [
            [InlineKeyboardButton("Ask another question", callback_data=f'ask_question_{query.message.message_id}')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_html("Want to ask something else?", reply_markup=reply_markup)
