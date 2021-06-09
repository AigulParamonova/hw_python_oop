import datetime as dt
from typing import Optional


class Record:
    def __init__(self, amount, comment, date: Optional[str] = None):
        self.amount = amount
        self.comment = comment
        date_format: str = '%d.%m.%Y'
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for record in self.records:
            if record.date == dt.date.today():
                today_stats += record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        for record in self.records:
            during_week = dt.date.today() - dt.timedelta(days=7)
            during_day = dt.date.today()
            if during_week < record.date <= during_day:
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        day_spend = self.get_today_stats()
        calories_difference = self.limit - day_spend
        if calories_difference > 0:
            return(
                'Сегодня можно съесть что-нибудь ещё, '
                f'но с общей калорийностью не более {calories_difference} кКал'
            )
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1.0

    def __init__(self, limit):
        super().__init__(limit)

    def get_today_cash_remained(self, currency):
        day_spend = self.get_today_stats()
        debt = self.limit - day_spend
        cash_dict = {
            'rub': [self.RUB_RATE, 'руб'],
            'usd': [self.USD_RATE, 'USD'],
            'eur': [self.EURO_RATE, 'Euro']
        }
        if self.limit > day_spend:
            cash = round((debt) / cash_dict[currency][0], 2)
            return f'На сегодня осталось {cash} {cash_dict[currency][1]}'
        elif self.limit == day_spend:
            return 'Денег нет, держись'
        elif self.limit < day_spend:
            debt = abs(round((debt) / cash_dict[currency][0], 2))
            return (
                'Денег нет, держись: твой долг - '
                f'{debt} {cash_dict[currency] [1]}'
            )
        return None
