"""CSC110 Fall 2020: Final Project

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of Lemeng Dai, Arthur Iliescu,
Jiaxin Li, Maisarah Zulkefli. Arthur All forms of distribution of this code,
whether as given or with any changes, are expressly prohibited.

This file is Copyright (c) 2021 Lemeng Dai, Arthur Iliescu, Jiaxin Li, Maisarah Zulkefli.
"""
import datetime
from dataclasses import dataclass
import csv


@dataclass
class CasesData:
    """A bundle of data on covid-19 for each province.
    Instance Attributes:
        - province_id: 35
        - province_name: 'Ontario'
        - date: datetime.date(2020, 1, 2)
        - number_confirmed: 12
        - number_total: 20
        - number_today: int
        
    Representation Invariants:
        - province_id in [35, 59, 24, 48, 43, 17, 61, 62, 12, 60, 99, 46, 47, 11]
        - province_name in ['Alberta', 'Ontario', 'Quebec', 'British Columbia', 'Manitoba', \
                            'New Brunswick', 'Saskatchewan', 'Prince Edward Island', \
                            'Newfoundland and Labrador', 'Nova Scotia']
        - data.year in [2020, 2021]
        - date.month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    """
    province_id: int
    province_name: str
    date: datetime.date
    number_confirmed: int
    number_total: int
    number_today: int
    number_tests: int
    rate_total: float


def return_data_cases(filename: str) -> dict[str, dict[tuple[int, int], int]]:
    """A function to run and return the data for the filename.
    """
    lst_provinces = ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan', 'Prince Edward Island',
                     'New Brunswick', 'Nova Scotia', 'Quebec', 'Newfoundland and Labrador']

    lst_years = [2020, 2021]
    lst_months = [i for i in range(1, 13)]
    inputs = load_data(filename)
    data = total_cases_per_years(inputs, lst_months, lst_years, lst_provinces)
    return data


def return_data_tests(filename: str) -> dict[str, dict[tuple[int, int], int]]:
    """A function to run and return the data for the filename.
    """
    lst_provinces = ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan', 'Prince Edward Island',
                     'New Brunswick', 'Nova Scotia', 'Quebec', 'Newfoundland and Labrador']

    lst_years = [2020, 2021]
    lst_months = [i for i in range(1, 13)]
    inputs = load_data(filename)
    data = total_tests_per_years(inputs, lst_months, lst_years, lst_provinces)
    return data


def load_data(filename: str) -> list[CasesData]:
    """Return a list containing the data for each entry in the file
    """
    # ACCUMULATOR inputs_so_far: The CasesData passed from the filename so far
    inputs_so_far = []

    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)  # skip the header

        for row in reader:
            assert len(row) == 40, 'Expected every row to contain 40 elements.'
            split_date = str.split(str(row[3]), '-')
            new_inputs = CasesData(int(row[0]), str(row[1]), datetime.date(int(split_date[0]),
                                                                           int(split_date[1]),
                                                                           int(split_date[2])),
                                   int(row[5]),
                                   int(row[8]), int(row[15]), int(row[10]), float(row[17]))

            inputs_so_far.append(new_inputs)

    return inputs_so_far


def cases_per_month(inputs: list[CasesData], month: int, year: int, province: str) -> int:
    """Return the monthly cases for the given province.
    Preconditions:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
        - province in ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan', 'Prince Edward Island',
                     'New Brunswick', 'Nova Scotia', 'Quebec', 'Newfoundland and Labrador']
    >>> method = [CasesData(province_id=35, province_name='Ontario', \
    date=datetime.date(2020, 1, 31), number_confirmed=3, number_total=3, number_today=3, number_tests=0, \
    rate_total=0.0)]
    >>> cases_per_month(method, 1, 2020, 'Ontario')
    3
    """
    cases_so_far = 0
    for row in inputs:
        if row.province_name == province and row.date.month == month and row.date.year == year:
            cases_so_far = cases_so_far + row.number_today

    return cases_so_far


def cases_per_month_province(inputs: list[CasesData], months: list[int], years: list[int],
                             province: str) -> dict[tuple[int, int], int]:
    """Return a dictionary matching the month in a calendar year to the number of cases in that month for province.
    
    Preconditions:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
        - province in ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan', 'Prince Edward Island',
                     'New Brunswick', 'Nova Scotia', 'Quebec', 'Newfoundland and Labrador']
    >>> method = [CasesData(province_id=35, province_name='Ontario', \
    date=datetime.date(2020, 1, 31), number_confirmed=40, number_total=40, number_today=40, number_tests=0, \
    rate_total=0.0)]
    >>> lst_months = [1]
    >>> lst_years = [2020]
    >>> cases_per_month_province(method, lst_months, lst_years, 'Ontario')
    {(2020, 1): 40}
    """
    dict_so_far = {}
    for year in years:
        for month in months:
            if year == 2021 and month != 12:
                number = cases_per_month(inputs, month, year, province)
                dict_so_far[(year, month)] = number
            elif year == 2020:
                number = cases_per_month(inputs, month, year, province)
                dict_so_far[(year, month)] = number
    return dict_so_far


def total_cases_per_years(inputs: list[CasesData], months: list[int], years: list[int], provinces: list[str]) -> \
        dict[str, dict[tuple[int, int], int]]:
    """Return the Provinces mapped to the years mapped to the total cases per month.
    
    Preconditions:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
        - province in ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan', 'Prince Edward Island',
                     'New Brunswick', 'Nova Scotia', 'Quebec', 'Newfoundland and Labrador']
    >>> method = [CasesData(province_id=35, province_name='Ontario', \
    date=datetime.date(2020, 1, 31), number_confirmed=40, number_total=40, number_today=40, number_tests=0, \
    rate_total=0.0), CasesData(province_id=35, province_name='Alberta', date=datetime.date(2020, 2, 10), \
    number_confirmed=20, number_total=20, number_today=20, number_tests=0, rate_total=0.0)]
    >>> lst_months = [1,2]
    >>> lst_years = [2020]
    >>> lst_provinces = ['Ontario', 'Alberta']
    >>> total_cases_per_years(method, lst_months, lst_years, lst_provinces)
    {'Ontario': {(2020, 1): 40, (2020, 2): 0}, 'Alberta': {(2020, 1): 0, (2020, 2): 20}}

    """
    province_cases_so_far = {}
    for province in provinces:
        a = cases_per_month_province(inputs, months, years, province)
        province_cases_so_far[province] = a
    return province_cases_so_far


def total_tests_per_month(inputs: list[CasesData], month: int, year: int, province: str) -> int:
    """Return the total number of tests for the month of the province.

    Preconditions:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
        - province in ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan', 'Prince Edward Island',
                     'New Brunswick', 'Nova Scotia', 'Quebec', 'Newfoundland and Labrador']
    >>> method = [CasesData(province_id=35, province_name='Ontario', \
    date=datetime.date(2020, 1, 31), number_confirmed=5, number_total=5, number_today=5, number_tests=2,\
     rate_total=0.0)]
    >>> total_tests_per_month(method, 1, 2020, 'Ontario')
    2
    """
    tests_so_far = 0
    for row in inputs:
        if row.province_name == province and row.date.month == month and row.date.year == year:
            tests_so_far = tests_so_far + row.number_tests

    return tests_so_far


def tests_per_month_province(inputs: list[CasesData], months: list[int], years: list[int], province: str) -> \
        dict[tuple[int, int], int]:
    """Return the date of each month in months for each year in years mapped to the total number
    of tests for that month.

    Preconditions:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
        - province in ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan', 'Prince Edward Island',
                     'New Brunswick', 'Nova Scotia', 'Quebec', 'Newfoundland and Labrador']

     >>> method = [CasesData(province_id=35, province_name='Ontario', \
    date=datetime.date(2020, 1, 31), number_confirmed=40, number_total=40, number_today=40, number_tests=20, \
    rate_total=0.0)]
    >>> lst_months = [1]
    >>> lst_years = [2020]
    >>> tests_per_month_province(method, lst_months, lst_years, 'Ontario')
    {(2020, 1): 20}
    """
    dict_so_far = {}
    for year in years:
        for month in months:
            if year == 2021 and month != 12:
                number = total_tests_per_month(inputs, month, year, province)
                dict_so_far[(year, month)] = number
            elif year == 2020:
                number = total_tests_per_month(inputs, month, year, province)
                dict_so_far[(year, month)] = number
    return dict_so_far


def total_tests_per_years(inputs: list[CasesData], months: list[int], years: list[int], provinces: list[str]) -> \
        dict[str, dict[tuple[int, int], int]]:
    """Return the Provinces mapped to the years mapped to the total cases per month.

    Preconditions:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
        - province in ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan', 'Prince Edward Island',
                     'New Brunswick', 'Nova Scotia', 'Quebec', 'Newfoundland and Labrador']

    >>> method = [CasesData(province_id=35, province_name='Ontario', \
    date=datetime.date(2020, 1, 31), number_confirmed=40, number_total=40, number_today=40, number_tests=25,\
     rate_total=0.0), CasesData(province_id=35, province_name='Alberta', date=datetime.date(2020, 2, 10), \
    number_confirmed=20, number_total=20, number_today=20, number_tests=15, rate_total=0.0)]
    >>> lst_months = [1,2]
    >>> lst_years = [2020]
    >>> lst_provinces = ['Ontario', 'Alberta']
    >>> total_tests_per_years(method, lst_months, lst_years, lst_provinces)
    {'Ontario': {(2020, 1): 25, (2020, 2): 0}, 'Alberta': {(2020, 1): 0, (2020, 2): 15}}

    """
    province_cases_so_far = {}
    for province in provinces:
        a = tests_per_month_province(inputs, months, years, province)
        province_cases_so_far[province] = a
    return province_cases_so_far


if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # Leave this code uncommented when you submit your files.
    import python_ta
    import doctest

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'csv', 'datetime', 'dataclass'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'R1710', 'E9998']
    })
    doctest.testmod()
