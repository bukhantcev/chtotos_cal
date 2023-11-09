




class Klients:
    tg_id = int
    first_name = str
    last_name = str
    tg_username = str
    last_procedure = str
    status_recording = str
    date_recording = str
    date_vizit = str
    status_news = str
    def __init__(self, tg_id: int, first_name: str, last_name = str, tg_username = str):
        self.tg_id = tg_id
        self.first_name = first_name
        self.last_name = last_name
        self.tg_username = tg_username


