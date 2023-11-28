import datetime


def get_tomorow():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow_date = f'{str(tomorrow).split("-")[2]}-{str(tomorrow).split("-")[1]}-{str(tomorrow).split("-")[0]}'
    return tomorrow_date


def get_today():
    today = datetime.date.today()
    today_date = f'{str(today).split("-")[2]}-{str(today).split("-")[1]}-{str(today).split("-")[0]}'
    return today_date



def future(date: str):
    try:
        year = date.split('-')[2]
        month = date.split('-')[1]
        day = date.split('-')[0]
        today_year = datetime.date.today().year
        today_month = datetime.date.today().month
        today_day = datetime.date.today().day


        if int(year) - int(today_year) > 0 or (int(year) - int(today_year) >= 0 and int(month) -
                                               int(today_month) > 0) or (int(year) -
                                                                         int(today_year) >= 0 and int(month) -
                                                                         int(today_month) >= 0 and int(day) - int(today_day) >= 0):

                    return True
        else:
            return False


    except:
        pass

