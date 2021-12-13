""" Employment Data file"""
import csv
from dataclasses import dataclass
import datetime


@dataclass
class EmploymentData:
    """A bundle of data on employment statistics for each province.

    Instance Attributes:
        - province: 'Ontario'
        - date: datetime.date(2021, 1, 1)
        - labour_force_statistics: 'Population'
        - data_type: 'Persons'
        - value: 10.2


    Representation Invariants:
        - province_name in ['Alberta', 'Ontario', 'Quebec', 'British Columbia', 'Manitoba', 'New Bruswick', 'Saskatchewan', 'Prince Edward Island', 'Newfoundland and Labrador', 'Nova Scotia']
        - data.year in [2020, 2021]
        - date.month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    """
    province: str
    date: datetime.date
    labour_force_statistics: str
    data_type: str
    value: float
        
        
def return_data(filename: str):
    """A function to run and return the data for the filename.
    """
    lst_provinces = ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan', 'Prince Edward Island',
                     'New Brunswick', 'Nova Scotia', 'Quebec', 'Newfoundland and Labrador']

    lst_years = [2020, 2021]
    lst_months = [i for i in range(1, 13)]
    input = load_data_employment(filename)
    data = employment_rate_total(input, lst_months, lst_years, lst_provinces)
    return data
        

def load_data_employment(filename: str) -> list[EmploymentData]:
    """Return a list containing the data for each entry in the file"""

    # ACCUMULATOR inputs_so_far: The CasesData passed from the filename so far

    inputs_so_far = []

    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)  # skip the header
        for row in reader:
            assert len(row) == 19, 'Expected every row to contain 19 elements.'
            split_date = str.split(str(row[0]), '-')
            new_inputs = EmploymentData(str(row[1]), datetime.date(int(split_date[0]), int(split_date[1]), 1),
                                        str(row[3]), str(row[8]), float(row[14]))
            inputs_so_far.append(new_inputs)

    return inputs_so_far


def population_num(input: list[EmploymentData], month: int, year: int, province: str) -> float:
    """Return the population in thousands of the province during set month and year."""

    for row in input:
        if year == 2021 and month != 12:
            if row.province == province and row.date.month == month and row.date.year == year and \
                    row.labour_force_statistics == 'Population' and row.data_type == 'Persons':
                return row.value
        elif year == 2020:
            if row.province == province and row.date.month == month and row.date.year == year and \
                    row.labour_force_statistics == 'Population' and row.data_type == 'Persons':
                return row.value


def employment_num(input: list[EmploymentData], month: int, year: int, province: str) -> float:
    """Return the number of people employed in thousands of the province during set month and year."""

    for row in input:
        if year == 2021 and month != 12:
            if row.province == province and row.date.month == month and row.date.year == year and \
                    row.labour_force_statistics == 'Employment' and row.data_type == 'Persons':
                return row.value
        elif year == 2020:
            if row.province == province and row.date.month == month and row.date.year == year and \
                    row.labour_force_statistics == 'Employment' and row.data_type == 'Persons':
                return row.value


def employment_rate_per_month(input: list[EmploymentData], month: int, year: int, province: str) -> float:
    """Return the employment rate for set month and year of the province."""

    if year == 2021 and month != 12:
        population = population_num(input, month, year, province)
        employment = employment_num(input, month, year, province)

        rate = (employment / population) * 100
        return round(rate, 1)

    elif year == 2020:
        population = population_num(input, month, year, province)
        employment = employment_num(input, month, year, province)

        rate = (employment / population) * 100
        return round(rate, 1)
    

def employment_rate_to_date(input: list[EmploymentData], months: list[int], years: list[int], province: str)\
        -> dict[tuple[int, int], float]:
    """Return a dictionary mapping each date in months and years to the employment rate of province."""
    dict_years_so_far = {}
    for year in years:
        for month in months:
            rate = employment_rate_per_month(input, month, year, province)
            dict_years_so_far[(year, month)] = rate
    return dict_years_so_far


def employment_rate_total(input: list[EmploymentData], months: list[int], years: list[int], provinces: list[str]) -> \
        dict[str, dict[tuple[int, int], float]]:
    """Return a dictionary mapping each province to another dictionary with date mapped to employment rate for
    that province."""
    dict_so_far = {}
    for province in provinces:
        rate = employment_rate_to_date(input, months, years, province)
        dict_so_far[province] = rate
    return dict_so_far
