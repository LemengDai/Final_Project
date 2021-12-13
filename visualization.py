"""CSC110 Fall 2020: Final Project

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of Lemeng Dai, Arthur Iliescu,
Jiaxin Li, Maisarah Zulkefli. Arthur All forms of distribution of this code,
whether as given or with any changes, are expressly prohibited.

This file is Copyright (c) 2021 Lemeng Dai, Arthur Iliescu, Jiaxin Li, Maisarah Zulkefli.
"""
import json
from urllib.request import urlopen
import pandas as pd
import plotly.express as px
import employment_rate as employment
import covid19_cases as cases


with urlopen('https://raw.githubusercontent.com/LemengDai/Final_Project/main/Canada2.json') as \
        response:
    provinces = json.load(response)


def return_province_emprate_cases(month: int, year: int) -> dict[str, list]:
    """Return a dictionary mapped provinces, employment rate, and number of COVID-19 cases to a
    list."""
    lst1 = employment.return_emp_for_map(month, year)
    case = cases.return_case_for_map(month, year)['cases']
    lst1['cases'] = case
    return lst1


def choropleth_map_emp(month: int, year: int) -> None:
    """Show a choropleth map containing information about the employment rate in provinces of Canada
    in the given month of the given year in explorer.
    Note that month cannot be 12 when year is 2021.

    Precondition:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
    """
    df = pd.DataFrame(employment.return_emp_for_map(month, year))
    fig = px.choropleth(df, geojson=provinces, locations='provinces',
                        color='employment_rate', range_color=(0, 70),
                        featureidkey='properties.NAME', color_continuous_scale='rdylbu',
                        labels={'employment_rate': 'employment rate(%)'})
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_geos(fitbounds="locations", visible=False)
    fig.show()


def choropleth_map_cases(month: int, year: int) -> None:
    """Show a choropleth map containing information about the covid-19 cases in provinces of Canada
    in the given month of the given year in explorer.
    Note that month cannot be 12 when year is 2021.

    Precondition:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
    """
    df = pd.DataFrame(cases.return_case_for_map(month, year))
    fig = px.choropleth(df, geojson=provinces, locations='provinces',
                        color='cases', range_color=(0, 99999),
                        featureidkey='properties.NAME', color_continuous_scale='burgyl',
                        labels={'cases': 'Covid-19 cases(month)'})
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_geos(fitbounds="locations", visible=False)
    fig.show()


def choropleth_map_cases_and_emp(month: int, year: int) -> None:
    """Show a choropleth map containing information about the employment rate and the number of
    covid-19 cases in provinces of Canada in the given month of the given year in explorer.
    Note that month cannot be 12 when year is 2021.

    Precondition:
        - month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        - year in [2020, 2021]
    """
    df = pd.DataFrame(return_province_emprate_cases(month, year))
    fig = px.choropleth(df, geojson=provinces, locations='provinces',
                        color='cases', range_color=(0, 99999),
                        featureidkey='properties.NAME', color_continuous_scale='burgyl',
                        labels={'cases': 'Covid-19 cases(month)',
                                'employment_rate': 'employment rate(%)'})
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_geos(fitbounds="locations", visible=False)
    fig.show()


if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # Leave this code uncommented when you submit your files.
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'json', 'plotly.express', 'pandas',
                          'covid_19_cases', 'employment_rate', 'urllib.request'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'E9997']
    })

    import doctest

    doctest.testmod()

# end
