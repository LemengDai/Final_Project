"""CSC110 Fall 2020: Final Project

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of Lemeng Dai, Arthur Iliescu,
Jiaxin Li, Maisarah Zulkefli. Arthur All forms of distribution of this code,
whether as given or with any changes, are expressly prohibited.

This file is Copyright (c) 2021 Lemeng Dai, Arthur Iliescu, Jiaxin Li, Maisarah Zulkefli.
"""
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import clean_data
import employment_rate


def transform_data(data: dict) -> pd.DataFrame:
    """transform the dictionary mapping the sum of new cases each month to the differences
    in employment rate between two consecutive months."""
    data = pd.DataFrame(data)
    return data


def predict(data: pd.DataFrame) -> None:
    """split data into training and testing sets to train the linear model, then test how the model
    works."""
    cases = data['cases']
    employment_rate = data['employment rate']
    x_train, x_test, y_train, y_test = train_test_split(cases, employment_rate, test_size=0.2)
    model = linear_model.LinearRegression()
    model.fit(x_train, y_train)
    # y_pred = model.predict(x_test)
    model.score(x_test, y_test)


def draw_diagram(data: pd.DataFrame) -> None:
    """draw a scatter diagram to visualize the dataset with the number of covid 19 cases as
    independent variable and employment rate as dependent variable."""
    fig = px.scatter(data, x='cases', y='employment rate')
    fig.show()


if __name__ == '__main__':
    """create data frame for graphing."""
    covid_data = clean_data.return_data('covid19-download.csv')
    new_covid_data = transform_data(covid_data)
    employment_data = employment_rate.return_data('Employment combined.csv')
    new_employment_data = transform_data(employment_data)
    # I need for each month dict[covid_data: difference of employment_rate]
