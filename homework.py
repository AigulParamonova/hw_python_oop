import datetime as dt
from typing import Optional


class Record:
    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date: Optional[str] = None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        today_stats = [
            record.amount
            for record in self.records if record.date == today
        ]
        return sum(today_stats)

    def get_week_stats(self):
        during_day = dt.date.today()
        during_week = during_day - dt.timedelta(days=7)
        week_stats = [
            record.amount
            for record in self.records
            if during_week < record.date <= during_day
        ]
        return sum(week_stats)

    def difference(self):
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        keep_eating = (
            'Сегодня можно съесть что-нибудь ещё, '
            f'но с общей калорийностью не более {self.difference()} кКал'
        )
        if self.difference() > 0:
            return keep_eating.format()
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1.0
    CASH_DICT = {
        'rub': [RUB_RATE, 'руб'],
        'usd': [USD_RATE, 'USD'],
        'eur': [EURO_RATE, 'Euro']
    }

    def __init__(self, limit):
        super().__init__(limit)

    def get_today_cash_remained(self, currency):
        day_spend = self.get_today_stats()
        selected_currency, type_of_currency = self.CASH_DICT[currency]
        cash = round(self.difference() / selected_currency, 2)
        debt = abs(cash)
        balance = f'На сегодня осталось {cash} {type_of_currency}'
        credit = f'Денег нет, держись: твой долг - {debt} {type_of_currency}'
        notice = f'Недопустимое значение валюты {currency}'
        if currency not in self.CASH_DICT:
            raise ValueError(notice.format())
        elif self.limit > day_spend:
            return balance.format()
        elif self.limit < day_spend:
            return credit.format()
        else:
            return 'Денег нет, держись'
        return None
