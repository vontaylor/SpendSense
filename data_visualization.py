import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd

def generateVisualizations(processedExpenseData):
    """
    Generate visualizations for the expense data and return a dictionary of
    the visualizations.
    """

    # style the visualizations
    colors = mcolors.TABLEAU_COLORS
    plt.style.use('ggplot')

    # dictionary to store the visualizations
    visualizations = {}

    # Pie chart for total expenses by category
    totalByCategory = processedExpenseData['totalByCategory']
    categoryLabels = totalByCategory['ExpenseCategory']
    categoryAmounts = totalByCategory['Amount']
    plt.pie(categoryAmounts, labels=categoryLabels, autopct='%1.1f%%', colors=colors.values(), textprops={'fontsize': 12})
    plt.title('Total Expenses by Category', fontsize=16)
    plt.axis('equal')
    plt.tight_layout(pad=1.5)
    plt.savefig('expenseByCategoryPieChart.png')
    plt.clf()
    visualizations['expenseByCategoryPieChart'] = 'expenseByCategoryPieChart.png'

    # Bar chart for total expenses by employee
    totalByEmployee = processedExpenseData['totalByEmployee']
    employeeLabels = totalByEmployee['EmployeeName']
    employeeAmounts = totalByEmployee['Amount']
    fig, ax = plt.subplots()

    bar_width = 0.6
    bar_positions = np.arange(len(employeeLabels))

    ax.bar(bar_positions, employeeAmounts, bar_width, color=colors.values())

    ax.set_xlabel('Employee', fontsize=14)
    ax.set_ylabel('Amount Spent', fontsize=14)
    ax.set_title('Total Expenses by Employee', fontsize=16)
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(employeeLabels, fontsize=12, rotation=45)

    plt.tight_layout()
    plt.savefig('expenseByEmployeeBarChart.png', bbox_inches='tight')
    plt.clf()
    plt.bar(employeeLabels, employeeAmounts)
    plt.xlabel('Employee')
    plt.ylabel('Amount Spent')
    plt.title('Total Expenses by Employee')
    plt.xticks(rotation=45)
    plt.savefig('expenseByEmployeeBarChart.png', bbox_inches='tight')
    plt.clf()
    visualizations['expenseByEmployeeBarChart'] = 'expenseByEmployeeBarChart.png'

    # # Bar chart for total expenses by month
    # totalByMonth = processedExpenseData['totalByMonth']
    # monthLabels = totalByMonth['Month']
    # monthAmounts = totalByMonth['Amount']
    # plt.bar(monthLabels, monthAmounts)
    # plt.xlabel('Month')
    # plt.ylabel('Amount Spent')
    # plt.title('Total Expenses by Month')
    # plt.xticks(rotation=45)
    # plt.savefig('expenseByMonthBarChart.png', bbox_inches='tight')
    # plt.clf()
    # visualizations['expenseByMonthBarChart'] = 'expenseByMonthBarChart.png'

    return visualizations
