from settings import GROUP_ID
from loader import bot
from telebot.types import Message, Location, Contact
from database import add_user, add_content, get_random_post, update_user_language, update_user_counter
from translations import UL, MT
from utils import *


def send_random_message(destination: int):


    content_id, content_type = get_random_post()
    print(content_id, content_type)
    if content_type == 'text':
        bot.send_message(destination, content_id)

    elif content_type == 'document':
        bot.send_document(destination, content_id)

    elif content_type == 'photo':
        bot.send_photo(destination, content_id)

    elif content_type == 'video_note':
        bot.send_video_note(destination, content_id)

    elif content_type == 'animation':
        bot.send_animation(destination, content_id)

    elif content_type == 'voice':
        bot.send_voice(destination, content_id)

    elif content_type == 'location':
        bot.send_location(destination, create_location(content_id))

    elif content_type == 'contact':
        bot.send_contact(destination, create_contact(content_id))

    elif content_type == 'sticker':
        bot.send_sticker(destination, content_id)

    elif content_type == 'video':
        bot.send_video(destination, content_id)

    elif content_type == 'audio':
        bot.send_audio(destination, content_id)

def add_new_content(message: Message):

    if message.text:
        add_content(message.text, 'text')
    elif message.audio:
        add_content(message.audio.file_id, 'audio')

    elif message.document:
        add_content(message.document.file_id, 'document')

    elif message.photo:
        add_content(message.photo[0].file_id, 'photo')

    elif message.sticker:
        add_content(message.sticker.file_id, 'sticker')

    elif message.video:
        add_content(message.video.file_id, 'video')

    elif message.animation:
        add_content(message.animation.file_id, 'animation')

    elif message.video_note:
        add_content(message.video_note.file_id, 'video_note')

    elif message.voice:
        add_content(message.voice.file_id, 'voice')

    elif message.location:
        add_content(convert_location(message), 'location')
        pass

    elif message.contact:
        add_content(convert_contact(message), 'contact')


@bot.message_handler(commands=['start'])
def start(message:Message):
    add_user(message.chat.id)
    user_lang = UL[str(message.chat.id)]

    bot.send_message(message.chat.id, MT['start_message'][user_lang])


@bot.message_handler(commands=['help'])
def helpp(message: Message):
    pass


@bot.message_handler(content_types= ['text', 'audio', 'document', 'photo', 'sticker', 'video', 'animation', 'video_note', 'voice', 'location', 'contact'])
def receive_content(message: Message):
    add_new_content(message)
    send_random_message(message.chat.id)


bot.polling()

'''
Add limits for sticker. Same sticker can have different file_id
Deal with location and contact messages 
Deal with spam
'''

