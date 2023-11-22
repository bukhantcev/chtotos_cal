import datetime


def get_tomorow():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow_date = f'{str(tomorrow).split("-")[2]}-{str(tomorrow).split("-")[1]}-{str(tomorrow).split("-")[0]}'
    return tomorrow_date

