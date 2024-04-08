from datetime import date, timedelta
import random
import datetime

class DateWorker:

    @staticmethod
    async def get_dates_between(start_date, end_date) -> list[date]:
        """
        Return the list of dates between start_date and end_date
        """
        delta = end_date - start_date
        # Generate a list of dates between start_date and end_date
        dates_between = list()
        for i in range(delta.days + 1):
            date = start_date + timedelta(days=i)
            dates_between.append(date.strftime("%Y-%m-%d"))

        return dates_between
    

    @staticmethod
    async def set_random_mm_ss_msms(dt: datetime, hours: int):
        mm = random.randint(0, 60)
        ss = random.randint(0, 60)
        msms = random.randint(0, 999)

        