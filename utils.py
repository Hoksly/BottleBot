from telebot.types import Message, Location, Contact


def convert_contact(message: Message):
    """
    :param message: message which has contact
    :return: string which will be stored in DB
    """
    pass


def convert_location(message: Message):
    """
    :param message: message which has location
    :return: string which will be stored in DB
    """
    pass


def create_location(stored: str):
    # receive string from database return Location
    pass


def create_contact(stored: str):
    # receive string from database return Contact
    pass