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
