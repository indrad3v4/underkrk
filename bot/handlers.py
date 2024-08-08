from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext, ChatMemberHandler
from bot.messages import (
    WELCOME_MESSAGE,
    ROLE_INSTRUCTIONS,
    VERIFICATION_PENDING_MESSAGE,
    VERIFICATION_APPROVED_MESSAGE,
    VERIFICATION_DENIED_MESSAGE,
    NEW_GUEST_MESSAGE,
    NEW_PARTICIPANT_MESSAGE,
    RAVE_DETAILS_MESSAGE,
    NEW_CHAT_MEMBER_MESSAGE,
    MEMBER_LEFT_MESSAGE,
    DONATION_ACKNOWLEDGMENT,
    DONATION_NOTIFICATION,
    ERROR_MESSAGE
)
from bot.ai_responses import AIResponses
from bot.payments import setup_payment_handlers
from app.models import Rave
from logs.logs import log_error
import os


class RaveBot:
    def __init__(self, rave_model, group_chat_id, verification_chat_id):
        self.roles = {}
        self.pending_verifications = {}
        self.group_chat_id = group_chat_id
        self.verification_chat_id = verification_chat_id
        self.rave_model = rave_model

    async def start(self, update: Update, context: CallbackContext) -> None:
        user = update.effective_user
        user_nickname = user.username if user.username else user.first_name
        keyboard = [
            [InlineKeyboardButton("Join as Sound System Provider", callback_data='sound_system')],
            [InlineKeyboardButton("Join as DJ", callback_data='dj')],
            [InlineKeyboardButton("Join as a Decorator", callback_data='decorator')],
            [InlineKeyboardButton("Join as a Contributor", callback_data='contributor')],
            [InlineKeyboardButton("Join as a Guest", callback_data='guest')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_html(
            WELCOME_MESSAGE.format(username=user_nickname),
            reply_markup=reply_markup,
        )

    async def button(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        await query.answer()
        choice = query.data
        user_id = query.from_user.id
        user_nickname = query.from_user.username if query.from_user.username else query.from_user.first_name

        if choice in ROLE_INSTRUCTIONS:
            role_instruction = ROLE_INSTRUCTIONS[choice]
            await query.edit_message_text(
                text=f"{role_instruction}\n\nYour input will be reviewed by the organizers. If approved, you will receive an invite link to the group here in the bot. All relevant information will be in the pinned messages. Remember that this rave will be a day rave from morning near 11 till night, and we have a free lineup for the entire event.",
                parse_mode='HTML'
            )
            context.user_data['role_choice'] = choice
        elif choice == 'guest':
            keyboard = [
                [InlineKeyboardButton("Donate with @wallet", url="https://t.me/wallet")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                text=ROLE_INSTRUCTIONS['guest'],
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
            self.add_user(user_id, 'guest')
            await context.bot.send_message(
                chat_id=self.group_chat_id,
                text=NEW_GUEST_MESSAGE.format(username=user_nickname),
                parse_mode='HTML'
            )
            await context.bot.send_message(chat_id=user_id, text=RAVE_DETAILS_MESSAGE, parse_mode='HTML')

    async def handle_link(self, update: Update, context: CallbackContext) -> None:
        user_id = update.message.from_user.id
        role = context.user_data.get('role_choice')
        link = update.message.text

        if role and link:
            self.store_pending_verification(user_id, role, link)
            keyboard = [
                [InlineKeyboardButton("Approve", callback_data=f'approve_{user_id}'),
                 InlineKeyboardButton("Send message in TG", url=f"tg://user?id={user_id}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(
                chat_id=self.verification_chat_id,
                text=f"New {role} request from {update.message.from_user.name}: {link}",
                reply_markup=reply_markup
            )
            await update.message.reply_text(VERIFICATION_PENDING_MESSAGE)
            await context.bot.send_message(
                chat_id=self.group_chat_id,
                text=NEW_PARTICIPANT_MESSAGE.format(username=update.message.from_user.name, role=role),
                parse_mode='HTML'
            )
        else:
            await update.message.reply_text("Oops. Please start again with /start.")

    async def verify_user(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        action, user_id = query.data.split('_')
        user_id = int(user_id)

        if action == 'approve':
            role = self.get_role(user_id)
            link = self.get_link(user_id)
            self.add_user(user_id, role, link)
            await context.bot.send_message(chat_id=user_id, text=VERIFICATION_APPROVED_MESSAGE.format(role=role))
            await context.bot.send_message(chat_id=self.group_chat_id, text=f"A new {role} has been added to the event! Welcome!")
            self.remove_pending_verification(user_id)
        else:
            await context.bot.send_message(chat_id=user_id, text=VERIFICATION_DENIED_MESSAGE)
            self.remove_pending_verification(user_id)

    async def new_chat_member(self, update: Update, context: CallbackContext) -> None:
        for member in update.message.new_chat_members:
            role = self.get_role(member.id)
            await update.message.reply_text(NEW_CHAT_MEMBER_MESSAGE.format(full_name=member.full_name, role=role))

    async def member_left(self, update: Update, context: CallbackContext) -> None:
        member = update.message.left_chat_member
        await update.message.reply_text(MEMBER_LEFT_MESSAGE.format(full_name=member.full_name))

    def add_user(self, user_id, role, link=None):
        self.roles[user_id] = {'role': role, 'link': link}
        if role == 'sound_system':
            self.update_soundsystem(link)
        elif role == 'dj':
            self.update_lineup(link)
        application.bot.add_chat_member(chat_id=self.group_chat_id, user_id=user_id)

    def get_role(self, user_id):
        return self.roles.get(user_id, {}).get('role')

    def get_link(self, user_id):
        return self.roles.get(user_id, {}).get('link')

    def store_pending_verification(self, user_id, role, link):
        self.pending_verifications[user_id] = {'role': role, 'link': link}

    def remove_pending_verification(self, user_id):
        if user_id in self.pending_verifications:
            del self.pending_verifications[user_id]

    def update_soundsystem(self, link):
        new_soundsystem = f"New sound system provided: {link}"
        self.rave_model.add_soundsystem(new_soundsystem, self.rave_model.id)
        self.announce_update("soundsystem")

    def update_lineup(self, link):
        new_lineup = f"New DJ added: {link}"
        self.rave_model.add_lineup(new_lineup, self.rave_model.id)
        self.announce_update("lineup")

    def announce_update(self, update_type):
        if update_type == "soundsystem":
            message = f"Updated Soundsystem: {self.rave_model.get_soundsystem(self.rave_model.id)}"
        elif update_type == "lineup":
            message = f"Updated Lineup: {self.rave_model.get_lineup(self.rave_model.id)}"
        else:
            message = "Unknown update type"
        application.bot.send_message(chat_id=self.group_chat_id, text=message)

def setup_handlers(application: Application, rave_model):
    group_chat_id = os.getenv("GROUP_CHAT_ID")
    verification_chat_id = os.getenv("VERIFICATION_CHAT_ID")

    rave_bot = RaveBot(rave_model, group_chat_id, verification_chat_id)
    ai_responses = AIResponses(rave_model)

    application.add_handler(CommandHandler("start", rave_bot.start))
    application.add_handler(CallbackQueryHandler(rave_bot.button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_responses.handle_message))
    application.add_handler(MessageHandler(filters.TEXT & filters.COMMAND, rave_bot.handle_link))
    application.add_handler(ChatMemberHandler(rave_bot.new_chat_member, ChatMemberHandler.CHAT_MEMBER))
    application.add_handler(ChatMemberHandler(rave_bot.member_left, ChatMemberHandler.MY_CHAT_MEMBER))
    application.add_handler(CallbackQueryHandler(rave_bot.verify_user, pattern=r'approve_\d+'))
    application.add_handler(CallbackQueryHandler(rave_bot.verify_user, pattern=r'deny_\d+'))
    application.add_handler(CallbackQueryHandler(ai_responses.handle_ai_question, pattern=r'ask_question_\d+'))

    setup_payment_handlers(application)
