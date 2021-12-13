"""Comparison between Covid-19 Cases and Employment Rate"""

import clean_data
import employmentdata


def differences_employment_rate(filename: str, month: int, year: int, province: str) -> float:
    """Return differences of employment rate between month in year and the month before"""
    x = employmentdata.return_data(filename)
    if province in x:
        if (year, month) in x[province]:
            employment_rate_now = x[province][(year, month)]
            if month == 1 and year == 2020:
                return employment_rate_now
            else:
                employment_rate_before = x[province][(year, month - 1)]
                return employment_rate_now - employment_rate_before


def differences_covid_cases(filename: str, month: int, year: int, province: str) -> float:
    """Return differences of employment rate between month in year and the month before"""
    y = clean_data.return_data(filename)
    if province in y:
        if (year, month) in y[province]:
            covid_cases_now = y[province][(year, month)]
            if month == 1 and year == 2020:
                return covid_cases_now
            else:
                covid_cases_before = y[province][(year, month - 1)]
                return covid_cases_now - covid_cases_before


def prediction_employment_rate(month: int, year: int, filename_1: str, filename_2: str) -> dict[str, dict[int, int]]:
    """Return a dictionary of difference number of covid cases mapping to differences of employment
    rate"""
    provinces = ['Ontario', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan', 'Prince Edward Island',
                 'New Brunswick', 'Nova Scotia', 'Quebec', 'Newfoundland and Labrador']
    prediction = {}
    for province in provinces:
        covid_to_employment = {}
        covid = differences_covid_cases(filename_1, month, year, province)
        employment = differences_employment_rate(filename_2, month, year, province)
        covid_to_employment[covid] = employment
        prediction[province] = covid_to_employment
    return prediction
