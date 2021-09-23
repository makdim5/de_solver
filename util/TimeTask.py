import datetime


class Time:
    @staticmethod
    def get_data_and_time():
        return str(datetime.datetime.now())

    @staticmethod
    def get_time():
        return str(datetime.datetime.now().time())

    @staticmethod
    def get_date():
        return str(datetime.datetime.now().date())
