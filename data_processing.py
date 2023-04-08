import pandas as pd

def processExpenseData(df):
    """
    Process the parsed expense data and return a dictionary of data frames.
    """
    # Group expenses by category
    dfByCategory = df.groupby('ExpenseCategory')

    # Calculate total expenses by category and sort by descending order
    totalByCategory = dfByCategory['Amount'].sum().reset_index()
    totalByCategory = totalByCategory.sort_values(by='Amount', ascending=False)

    # Group expenses by employee and calculate total expenses by employee
    dfByEmployee = df.groupby(['EmployeeID', 'EmployeeName'])
    totalByEmployee = dfByEmployee['Amount'].sum().reset_index()

    # Calculate the overall total expenses
    totalExpenses = df['Amount'].sum()

    # Calculate the percentage of expenses for each category
    totalByCategory['Percentage'] = (totalByCategory['Amount'] / totalExpenses) * 100

    # Calculate the percentage of expenses for each employee
    totalByEmployee['Percentage'] = (totalByEmployee['Amount'] / totalExpenses) * 100

    # Sort expenses by descending order for each employee
    totalByEmployee = totalByEmployee.sort_values(by='Amount', ascending=False)

    # return the processed data
    processedExpenseData = {
        'totalByCategory': totalByCategory,
        'totalByEmployee': totalByEmployee,
        'totalExpenses': totalExpenses
    }

    return processedExpenseData
    
