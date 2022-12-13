from datetime import timedelta
from db import connector
from handlers.change_channel_sampling.markups import decode_string


def get_row(user_id):
    connector.init_db()
    row = connector.get_row(user_id)
    connector.close_db()
    return row


def get_channels(user_id):
    row = get_row(user_id)
    return decode_string(row[1])


def get_posts_limit(user_id):
    row = get_row(user_id)
    return row[2]


def get_period(user_id):
    row = get_row(user_id)
    return timedelta(seconds=row[3])
