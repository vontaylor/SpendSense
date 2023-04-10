import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd


def generateVisualizations(processedExpenseData):
    """
    Generate visualizations for the expense data and return a dictionary of
    the visualizations.

    :param processedExpenseData: The processed expense data.
    :return: A dictionary containing the visualizations.

    """

    # set color palette and style for the visualizations
    colors = mcolors.TABLEAU_COLORS
    plt.style.use('ggplot')

    # initialize an empty dictionary to store visualizations
    visualizations = {}

    # create a pie chart for total expenses by category
    totalByCategory = processedExpenseData['totalByCategory']
    categoryLabels = totalByCategory['ExpenseCategory']
    categoryAmounts = totalByCategory['Amount']
    plt.pie(categoryAmounts, labels=categoryLabels, autopct='%1.1f%%',
            colors=colors.values(), textprops={'fontsize': 12})
    plt.title('Total Expenses by Category', fontsize=16)
    plt.axis('equal')
    plt.tight_layout(pad=1.5)
    plt.savefig('expenseByCategoryPieChart.png')
    plt.clf()
    visualizations['expenseByCategoryPieChart'] = 'expenseByCategoryPieChart.png'

    # create a bar chart for total expenses by employee
    totalByEmployee = processedExpenseData['totalByEmployee']
    employeeLabels = totalByEmployee['EmployeeName']
    employeeAmounts = totalByEmployee['Amount']
    fig, ax = plt.subplots()

    barWidth = 0.6
    barPositions = np.arange(len(employeeLabels))

    # plot the bar chart using the Axes object
    ax.bar(barPositions, employeeAmounts, barWidth, color=colors.values())
    ax.set_xlabel('Employee', fontsize=14)
    ax.set_ylabel('Amount Spent', fontsize=14)
    ax.set_title('Total Expenses by Employee', fontsize=16)
    ax.set_xticks(barPositions)
    ax.set_xticklabels(employeeLabels, fontsize=12, rotation=45)

    plt.tight_layout()
    plt.savefig('expenseByEmployeeBarChart.png', bbox_inches='tight')
    plt.clf()
    visualizations['expenseByEmployeeBarChart'] = 'expenseByEmployeeBarChart.png'

    return visualizations
