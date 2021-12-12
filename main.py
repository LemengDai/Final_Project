"""CSC110 Fall 2021: Final Project

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of Lemeng Dai, Arthur Iliescu,
Jiaxin Li, Maisarah Zulkefli. All forms of distribution of this code, whether as given or 
with any changes, are expressly prohibited.

This file is Copyright (c) 2021 Lemeng Dai, Arthur Iliescu, Jiaxin Li, Maisarah Zulkefli.
"""
import datetime
from dataclasses import dataclass
import csv


@dataclass
class CasesData:
    """A bundle of data on covid-19 for each province.

    Instance Attributes:
        -


    Representation Invariants:
        -

    """
    province_id: int
    province_name: str
    date: datetime.date
    number_confirmed: int
    number_total: int
    number_today: int


lst_provinces = ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan', 'Prince Edward Island',
                 'New Brunswick', 'Nova Scotia', 'Quebec', 'Newfoundland and Labrador']

lst_years = [2020, 2021]
lst_months = [i for i in range(1, 13)]


def return_data(filename: str):
    """A function to run and return the data for the filename."""
    input = load_data(filename)
    data = total_cases_per_years(input, lst_months, lst_years, lst_provinces)
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
            assert len(row) == 6, 'Expected every row to contain 6 elements.'
            split_date = str.split(str(row[2]), '/')
            new_inputs = CasesData(int(row[0]), str(row[1]), datetime.date(int(split_date[2]),
                                                                           int(split_date[0]), 
                                                                           int(split_date[1])), 
                                   int(row[3]),
                                   int(row[4]), int(row[5]))

            inputs_so_far.append(new_inputs)

    return inputs_so_far


def cases_per_month(input: list[CasesData], month: int, year: int, province: str) -> int:
    """Return the monthly cases for the given province.

    preconditions
    """
    cases_so_far = 0
    for row in input:
        if row.province_name == province and row.date.month == month and row.date.year == year:
            cases_so_far = cases_so_far + row.number_today

    return cases_so_far


def cases_per_month_province(input: list[CasesData], months: list[int], year: int, province: str):
    """Return a dictionary matching the month in a calendar year to the number of cases in that month for province."""
    dict_so_far = {}
    for month in months:
        if year == 2021 and month != 12:
            number = cases_per_month(input, month, year, province)
            dict_so_far[month] = number
        elif year == 2020:
            number = cases_per_month(input, month, year, province)
            dict_so_far[month] = number
    return dict_so_far


def total_cases_per_years(input: list[CasesData], months: list[int], years: list[int], provinces: list[str]):
    """Return the Provinces mapped to the years mapped to the total cases per month.""
    province_cases_so_far = {}
    for province in provinces:
        dict_so_far_years = {}
        for year in years:
            cases = cases_per_month_province(input, months, year, province)
            dict_so_far_years[year] = cases

        province_cases_so_far[province] = dict_so_far_years
    return province_cases_so_far
