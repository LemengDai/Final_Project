"""CSC110 Fall 2021: Final Project

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of Lemeng Dai, Arthur Iliescu,
Jiaxin Li, Maisarah Zulkefli. All forms of distribution of this code, whether as given or 
with any changes, are expressly prohibited.

This file is Copyright (c) 2021 Lemeng Dai, Arthur Iliescu, Jiaxin Li, Maisarah Zulkefli.
"""
import csv
import datetime
from dataclasses import dataclass


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
            new_inputs = CasesData(int(row[0]), str(row[1]), datetime.date(int(split_date[2]), int(split_date[0]), int(split_date[1])), int(row[3]),
                                   int(row[4]), int(row[5]))

            inputs_so_far.append(new_inputs)

    return inputs_so_far




def monthly_data(cases: CasesData):
    for i in range(cases.date.month):
