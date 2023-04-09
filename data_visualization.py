import matplotlib.pyplot as plt
import pandas as pd

def generateVisualizations(processedExpenseData):
    """
    Generate visualizations for the expense data and return a dictionary of
    the visualizations.
    """

    # style the visualizations
    plt.style.use('ggplot')

    # dictionary to store the visualizations
    visualizations = {}

    # Pie chart for total expenses by category
    totalByCategory = processedExpenseData['totalByCategory']
    categoryLabels = totalByCategory['ExpenseCategory']
    categoryAmounts = totalByCategory['Amount']
    plt.pie(categoryAmounts, labels=categoryLabels, autopct='%1.1f%%')
    plt.title('Total Expenses by Category')
    plt.axis('equal')
    plt.savefig('expenseByCategoryPieChart.png')
    plt.clf()
    visualizations['expenseByCategoryPieChart'] = 'expenseByCategoryPieChart.png'

    # Bar chart for total expenses by employee
    totalByEmployee = processedExpenseData['totalByEmployee']
    employeeLabels = totalByEmployee['EmployeeName']
    employeeAmounts = totalByEmployee['Amount']
    plt.bar(employeeLabels, employeeAmounts)
    plt.xlabel('Employee')
    plt.ylabel('Amount Spent')
    plt.title('Total Expenses by Employee')
    plt.xticks(rotation=45)
    plt.savefig('expenseByEmployeeBarChart.png', bbox_inches='tight')
    plt.clf()
    visualizations['expenseByEmployeeBarChart'] = 'expenseByEmployeeBarChart.png'

    # Bar chart for total expenses by month
    totalByMonth = processedExpenseData['totalByMonth']
    monthLabels = totalByMonth['Month']
    monthAmounts = totalByMonth['Amount']
    plt.bar(monthLabels, monthAmounts)
    plt.xlabel('Month')
    plt.ylabel('Amount Spent')
    plt.title('Total Expenses by Month')
    plt.xticks(rotation=45)
    plt.savefig('expenseByMonthBarChart.png', bbox_inches='tight')
    plt.clf()
    visualizations['expenseByMonthBarChart'] = 'expenseByMonthBarChart.png'

    return visualizations
