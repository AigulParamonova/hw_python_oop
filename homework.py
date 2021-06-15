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
        return sum(
            record.amount
            for record in self.records if record.date == today
        )

    def get_week_stats(self):
        during_day = dt.date.today()
        during_week = during_day - dt.timedelta(days=7)
        return sum(
            record.amount
            for record in self.records
            if during_week < record.date <= during_day
        )

    def difference(self):
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    KEEP_EATING = (
        'Сегодня можно съесть что-нибудь ещё, '
        'но с общей калорийностью не более {difference} кКал'
    )

    def get_calories_remained(self):
        difference = self.difference()
        if difference > 0:
            return self.KEEP_EATING.format(difference=self.difference())
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1.0
    CASH_DICT = {
        'rub': (RUB_RATE, 'руб'),
        'usd': (USD_RATE, 'USD'),
        'eur': (EURO_RATE, 'Euro')
    }

    BALANCE = 'На сегодня осталось {cash} {type_of_currency}'
    CREDIT = 'Денег нет, держись: твой долг - {debt} {type_of_currency}'
    NOTICE = 'Недопустимое значение валюты {currency}'
    NO_MONEY = 'Денег нет, держись'

    def get_today_cash_remained(self, currency):
        if currency not in self.CASH_DICT:
            raise ValueError(self.NOTICE.format(currency=currency))
        selected_currency, type_of_currency = self.CASH_DICT[currency]
        day_spend = self.get_today_stats()
        difference = self.difference()
        cash = round(difference / selected_currency, 2)
        debt = abs(cash)
        if self.limit > day_spend:
            return self.BALANCE.format(
                cash=cash, type_of_currency=type_of_currency
            )
        elif self.limit < day_spend:
            return self.CREDIT.format(
                debt=debt, type_of_currency=type_of_currency
            )
        else:
            return self.NO_MONEY
