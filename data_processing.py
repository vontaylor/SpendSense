import pandas as pd

def processExpenseData(df):
    """
    Process the parsed expense data and return a dictionary of data frames.

    :param df: The original DataFrame containing the expense data.
    :return: A dictionary containing the processed data frames.

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

    # Get the top 5 expense transactions
    top5Transactions = df.nlargest(5, 'Amount')

    
    # convert the ExpenseDate column to datetime
    df['ExpenseDate'] = pd.to_datetime(df['ExpenseDate'])

    # df['Month'] = df['ExpenseDate'].dt.to_period('M')
    # totalByMonth = df.groupby('Month')['Amount'].sum().reset_index()
    # # sort expenses by descending order for each month
    # totalByMonth = totalByMonth.sort_values(by='Amount', ascending=False)

    # # calculate the percentage of expenses for each month
    # totalByMonth['Percentage'] = (totalByMonth['Amount'] / totalExpenses) * 100

    # return the processed data
    processedExpenseData = {
        'totalByCategory': totalByCategory,
        'totalByEmployee': totalByEmployee,
        'totalExpenses': totalExpenses,
        'top5Transactions': top5Transactions,
        # 'totalByMonth': totalByMonth
    }

    return processedExpenseData
    
