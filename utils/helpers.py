import arrow

def set_time_to_save(hours_to_save, days_to_save, weeks_to_save, years_to_save, current_time_to_save):
    """
    Sets the time of comments or submissions to save and 
    updates the UI to show what its currently set to.
    :param hours_to_save: input received from the UI - how many hours of items to save
    :param days_to_save: input received from the UI - how many days of items to save
    :param weeks_to_save: input received from the UI - how many weeks of items to save
    :param years_to_save: input received from the UI - how many years of items to save
    :param current_time_to_save: text shown to user in UI so they know how much time will be saved
    :return: The formatted time to save for storing in state dictionaries
    """
    total_hours = int(hours_to_save) + (int(days_to_save) * 24) + \
        (int(weeks_to_save) * 168) + (int(years_to_save) * 8736)

    def get_text(time, text):
        return '' if time == '0' else time + text

    hours_text = get_text(hours_to_save, 'hours')
    days_text = get_text(days_to_save, 'days')
    weeks_text = get_text(weeks_to_save, 'weeks')
    years_text = get_text(years_to_save, 'years')

    if hours_to_save == '0' and days_to_save == '0' and weeks_to_save == '0' and years_to_save == '0':
        current_time_to_save.set(f'Currently set to save: [nothing]')
    else:
        current_time_to_save.set(
            f'Currently set to save: [{years_text} {weeks_text} {days_text} {hours_text}] of items')

    return arrow.now().replace(hours=-total_hours)


def set_max_score(max_score, current_max_score, item_string):
    """
    Sets the maximum score level, any items above this store will be skipped over
    updates the UI to show what its currently set to.
    :param max_score: the input received from the UI - any comments greater than or equal to this will be saved
    :param current_max_score: text to display for the user in the UI - current max_score
    :param state_key: the key used to identify this value in the state
    :param ui_string: what will be shown to the user (upvotes, tweets,)
    :return max_score: the updated score for the state
    """
    if max_score == '':
        max_score = 0
    elif max_score == 'Unlimited':
        max_score = 9999999999
    else:
        max_score = int(max_score)

    current_max_score.set(f'Currently set to: {str(max_score)} upvotes')

    return max_score


def format_snippet(text, length):
    """
    Helper function to format the snippets displayed in UI
    :param text: full text of item
    :param length: how many chars the snippet should be
    :return: formatted snippet with '...' if needed
    """
    snippet = ''

    if len(text) > length:
        snippet = text[0:length] + '...'
    else:
        snippet = text
    for char in snippet:
        # tkinter can't handle certain unicode characters,
        # so we strip them
        if ord(char) > 65535:
            snippet = snippet.replace(char, '')
    return snippet
