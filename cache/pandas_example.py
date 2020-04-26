import pandas as pd
from pandas import DataFrame
import sys


class Example:
    cache: dict = {}
    max_cache_size: int = 5000

    def __init__(self):
        self.data = pd.read_csv("cache/owid-covid-data.csv", index_col=["date"])

    @staticmethod
    def get_key(country, start_date, end_date) -> str:
        return f"{country}-{start_date}-{end_date}"

    def remove_oldest(self) -> None:
        oldest_key: str = list(self.cache.keys())[0]
        self.cache.pop(oldest_key)

    def set_cache(self, key: str, data: DataFrame) -> None:
        if self.size > self.max_cache_size:
            self.remove_oldest()
        self.cache[key] = data.to_dict()["total_cases"]

    def get_data(self, country: str, start_date: str, end_date: str) -> DataFrame:
        key = self.get_key(country, start_date, end_date)
        if self.cache.get(key):
            return self.cache[key]
        else:
            data = self.data[self.data["location"] == country][start_date: end_date]
            self.set_cache(key, data)
            return data.to_dict()["total_cases"]

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
        print(c.get_date(country, start_date, end_date))
