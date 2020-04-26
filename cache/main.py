import sys
from datetime import date, timedelta


class Example:
    cache: dict = {}
    max_cache_size: int = 5000

    def __init__(self):
        self.data = open("cache/owid-covid-data.csv", "r").readlines()

    @staticmethod
    def get_key(country, date) -> str:
        return f"{country}-{date}"

    def remove_oldest(self) -> None:
        oldest_key: str = list(self.cache.keys())[0]
        self.cache.pop(oldest_key)

    def set_cache(self, key, data):
        if self.size > self.max_cache_size:
            self.remove_oldest()
        self.cache[key] = data

    def get_data(self, country, date):
        for item in self.data:
            split_data = item.split(",")
            if split_data[1] == country and split_data[2] == str(date):
                return split_data[4]  # new_case
        return

    def collect_data(self, country: str, start_date: str, end_date: str):
        s_year, s_month, s_day = start_date.split("-")
        e_year, e_month, e_day = end_date.split("-")
        s_date = date(int(s_year), int(s_month), int(s_day))
        e_date = date(int(e_year), int(e_month), int(e_day))
        delta = e_date - s_date
        result = {}
        for i in range(delta.days + 1):
            d = s_date + timedelta(days=i)
            key = self.get_key(country, d)
            if self.cache.get(key):
                result[key] = self.cache[key]
            else:
                data = self.get_data(country, d)
                result[key] = data
                self.set_cache(key, data)
        return result

    @property
    def size(self) -> int:
        return sys.getsizeof(self.cache)


if __name__ == "__main__":
    c = Example()
    while True:
        print("Which country")
        country = input()
        print("Start date")
        start_date = input()
        print("End date")
        end_date = input()
        print(c.collect_data(country, start_date, end_date))


