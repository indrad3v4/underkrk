# bot/messages.py

WELCOME_MESSAGE = """Hi {username}! Welcome to the Under Krakow Events! The next 150 BPM day rave under Krakow will run on 29th of July. 30 Spots only ^^ How would you like to participate?"""

ROLE_INSTRUCTIONS = {
    'sound_system': "As a Sound System Provider, you will ensure the best audio experience for our rave. Please provide your SoundCloud link or other relevant link for verification.",
    'dj': "As a DJ, you will keep the energy high with your music. Please provide your SoundCloud link or other relevant link for verification.",
    'decorator': "As a Decorator, you will create the perfect ambiance for our event. Please provide your portfolio link or other relevant link for verification.",
    'contributor': "As a Contributor, your support will help make this event unforgettable. Please provide your relevant link for verification.",
    'guest': (
        "To join as a guest, please use @wallet to make a donation to one of the following addresses "
        "with the secret phrase <b>'underrave'</b> followed by your Telegram ID in the comments:\n\n"
        "<b>BTC:</b> 1P9V5CyAgqfQeEgkYeJ7Kr7ursq37EkMjP\n"
        "<b>TON:</b> UQBA0w-iP7gLIgemwW3i12d6n1xb8mfFbOnNw7SFcosWmmbl\n"
        "<b>USDT:</b> TFpqb8ogiTV2Re9S5V6YJr8X67GdfTAUCp\n\n"
        "After sending crypto, you will get an invite link here in the bot. While you wait, you can write anything in the bot to get more info about the event."
    )
}

VERIFICATION_PENDING_MESSAGE = "Thank you! Your request has been submitted for verification. You will be notified once approved."
VERIFICATION_APPROVED_MESSAGE = "Your role as {role} has been approved!"
VERIFICATION_DENIED_MESSAGE = "Your request has been denied."

NEW_GUEST_MESSAGE = "A new guest has joined the event! Welcome, {username}!"
NEW_PARTICIPANT_MESSAGE = "{username} wants to join the rave as a {role}."

RAVE_DETAILS_MESSAGE = (
    "<b>Welcome to Under Krakow Rave!</b>\n"
    "Date: <b>29th July</b>\n"
    "Location: <b>Scenic forest in Krakow</b>\n"
    "For more details, check the pinned messages."
)

NEW_CHAT_MEMBER_MESSAGE = "Welcome {full_name} ({role})! We're excited to have you at our rave event. Please check the pinned messages for more information."
MEMBER_LEFT_MESSAGE = "Goodbye {full_name}. We'll miss you at the rave!"

DONATION_ACKNOWLEDGMENT = "Thank you for your donation of ${amount} towards {element}, {username}!"
DONATION_NOTIFICATION = "{username} has donated ${amount} towards {element}!"

ERROR_MESSAGE = "An error occurred while processing your request. Please try again."
