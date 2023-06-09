import pandas as pd
import datetime


def readExpenseData(inputFile):
    '''
    read the input file, validate the data, and return a pandas data frame

    :param inputFile: The path to the input file.
    :return: A pandas data frame containing the expense data.
    
    '''
    # define the column names
    columnNames = ['EmployeeID', 'EmployeeName', 'ExpenseCategory', 'ExpenseDate', 'Amount', 'Description']

    # read the csv file into pandas data frame
    df = pd.read_csv(inputFile, names=columnNames, header=0)

    # validate the input data

    # expected columns
    expectedColumns = set(columnNames)
    if not expectedColumns.issubset(df.columns):
        raise ValueError(f"Unexpected columns: {df.columns}. Expected columns: {expectedColumns}.")

    # missing values or NaNs
    if df.isnull().values.any():
        raise ValueError("Missing values or NaNs in the input data.")

    # values in each column fall within the expected range or meet certain criteria

    # positive amounts
    if (df['Amount'] < 0).any():
        raise ValueError("Amount should be positive.")

    # duplicate rows
    if df.duplicated().any():
        raise ValueError("Duplicate rows found in the input data.")

    # total amount spent is reasonable and not weirdly high or low
    totalAmount = df['Amount'].sum()
    if totalAmount < 0 or totalAmount > 100000: 
        raise ValueError("Total amount spent is a weird number.")

    # return the data frame
    return df

