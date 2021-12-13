"""CSC110 Fall 2020: Final Project

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of Lemeng Dai, Arthur Iliescu,
Jiaxin Li, Maisarah Zulkefli. Arthur All forms of distribution of this code,
whether as given or with any changes, are expressly prohibited.

This file is Copyright (c) 2021 Lemeng Dai, Arthur Iliescu, Jiaxin Li, Maisarah Zulkefli.
"""
import clean_data
import employment_rate


def prediction_employment_rate(filename: str) -> dict[str, dict[tuple[int, int], float]]:
    """Return a dictionary of difference number of covid cases mapping to differences of employment
    rate"""
    x = employmentdata.return_data(filename)
    prediction = {}
    for provinces in x:
        date_to_employment = {}
        for date in x[provinces]:
            if date == (2020, 1):
                date_to_employment[date] = 0
            elif date == (2021, 1):
                old_date = (2020, 12)
                date_to_employment[date] = x[provinces][date] - x[provinces][old_date]
            else:
                old_date = (date[0], date[1] - 1)
                date_to_employment[date] = ((x[provinces][date]) - (x[provinces][old_date]))
        prediction[provinces] = date_to_employment

    return prediction

