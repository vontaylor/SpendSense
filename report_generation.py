from data_visualization import generateVisualizations # used to generate charts and graphs visuals
from reportlab.lib.pagesizes import letter # used to set the page size of the report
from reportlab.lib.units import inch # used to set the margins of the report
from reportlab.pdfgen import canvas # used to create PDF canvas
from reportlab.lib import colors # used to set the colors for tables and text
# used to create the document template, spacing, tables, table styles, paragraphs, page breaks, and images.
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle, Paragraph, PageBreak, Image 

import io # used for file handling
import os # used for interacting with my operating system
import pandas as pd # used for data manipulation
# used to import the styles from the styles.py file
from styles import titleStyle, sectionHeaderStyle, subheaderStyle, bodyStyle, tableOfContentsHeader 

# function to generate report
def generateReport(processedExpenseData, df):
    def formatAmount(amount):
        return "${:,.2f}".format(amount)
    def formatPercentage(value):
        return "{:.2f}%".format(value)
    """
    Generate the expense report PDF.

    :param processedExpenseData: A dictionary containing processed expense data.
    :param df: The original DataFrame containing the expense data.
    :return: The path to the generated PDF report.

    """
    # create a new PDF document to hold the report
    doc = SimpleDocTemplate("expenseReport.pdf", pagesize=letter,
                            leftMargin=inch, rightMargin=inch,
                            topMargin=inch, bottomMargin=inch)

    # get the data frames from the expense data dictionary
    totalByCategory = processedExpenseData['totalByCategory']
    totalByEmployee = processedExpenseData['totalByEmployee']
    totalExpenses = processedExpenseData['totalExpenses']

    # initialize story list for PDF
    story = []

    # add the cover page to the PDF
    story.append(Spacer(1, 3 * inch))
    story.append(Paragraph("April's", titleStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("Expense", titleStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("Report", titleStyle))
    story.append(Spacer(1, 0.25 * inch))
    #TODO: hmmm i wonder for future feature to add company name and logo
    # story.append(Paragraph("Company Name: ", bodyStyle)) 
    # story.append(Image("totalExpensesByCategoryPieChart.png", width=5*inch, height=5*inch)) 
    story.append(PageBreak())

    # add the table of contents to PDF 
    # TODO: clickable links to each section is also a future feature idea
    story.append(Spacer(1, 3.25 * inch))
    story.append(Paragraph("Table of Contents", tableOfContentsHeader))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<u>Summary</u>", subheaderStyle))
    story.append(Paragraph("<u>Expense Details</u>", subheaderStyle))
    story.append(Paragraph("<u>Charts and Graphs</u>", subheaderStyle))
    story.append(PageBreak())

    # add the summary section 
    story.append(Paragraph("Summary", titleStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<b>Executive Summary</b>", subheaderStyle))
    story.append(Paragraph("[Insert Executive Summary Here]", bodyStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<b>Total Amount Spent</b>: %s" % formatAmount(totalExpenses), bodyStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<b>Top 5 Expense Categories by Total Spend</b>", subheaderStyle))
    story.append(Spacer(1, 0.25 * inch))

    # add the top 5 expenses to the PDF
    # get the top 5 expenses, the columns i'll want, rename those columns, round the values, and format the amount
    top5Expenses = totalByCategory.head(5)
    top5Expenses = top5Expenses[['ExpenseCategory', 'Amount', 'Percentage']]
    top5Expenses = top5Expenses.rename(columns={
                                       'ExpenseCategory': 'Category', 'Amount': 'Amount Spent', 'Percentage': 'Percentage of Total'}) 
    top5Expenses = top5Expenses.round(
        {'Amount Spent': 2, 'Percentage of Total': 2}) 
    top5Expenses['Amount Spent'] = top5Expenses['Amount Spent'].apply(formatAmount)

    # add the top 5 expenses as a table
    top5ExpensesData = [['Category', 'Amount Spent', 'Percentage of Total']] + top5Expenses.values.tolist()
    top5ExpensesTable = Table(top5ExpensesData)
    top5ExpensesTable.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F1F1F')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#E7E6E6')),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ]))
    story.append(top5ExpensesTable)
    story.append(Spacer(1, 0.25 * inch))

    # add the total number of employees included in the report
    story.append(Paragraph("<b>Total Number of Employees Included</b>: %d" %
                 len(totalByEmployee), bodyStyle))
    story.append(Spacer(1, 0.25 * inch))

    # add the top 5 transactions
    story.append(Paragraph("<b>Top 5 Expense Transactions</b>", subheaderStyle))
    story.append(Spacer(1, 0.25 * inch))
    # get the top 5 transactions, the columns I want, rename those columns, and format the amount
    top5Transactions = df.nlargest(5, 'Amount')
    top5Transactions = top5Transactions[['ExpenseDate', 'EmployeeName', 'ExpenseCategory', 'Amount']]
    top5Transactions = processedExpenseData['top5Transactions']
    top5Transactions['Amount'] = top5Transactions['Amount'].apply(formatAmount)

    # add the top 5 transactions as a table
    top5TransactionsData = [['Emp#', 'Employee', 'Category', 'Date', 'Amount', 'Details' ]] + top5Transactions.values.tolist()
    top5TransactionsTable = Table(top5TransactionsData)
    top5TransactionsTable.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F1F1F')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#E7E6E6')),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ]))
    story.append(top5TransactionsTable)
    story.append(Spacer(1, 0.25 * inch))
    story.append(PageBreak())

    # TODO: feature i can add, example can be if the meal expense is over a certain amount, then it will be flagged and reported within the trends section
    # # add the trends in expense section
    # story.append(Paragraph("<b>Trends in Expense Data</b>", subheaderStyle))
    # story.append(Spacer(1, 0.25 * inch))
        # TODO trend calculations can be added to the data processing section and then added to the story here   
    # story.append(PageBreak())

    # add the expense details section
    story.append(Paragraph("Expense Details", titleStyle))
    story.append(Spacer(1, 0.25 * inch))
    # add the expense category breakdowns
    expenseCategories = totalByCategory['ExpenseCategory'].tolist()
    for expenseCategory in expenseCategories:
        story.append(Paragraph("<b>%s</b>" % expenseCategory, subheaderStyle))
        story.append(Spacer(1, 0.25 * inch))

        # get the data frame for the current expenseCategory
        categoryData = df[df['ExpenseCategory'] == expenseCategory].copy() # Mr. Brown, this piece of code was causing me a lot of trouble. ultimately, it was causing the data to be modified in the original data frame so I had to copy it
        categoryData['Amount'] = categoryData['Amount'].apply(formatAmount) 
        # add the expense category data as a table
        categoryDataData = [['Emp#', 'Employee', 'Category', 'Date', 'Amount', 'Details' ]] + categoryData.values.tolist()
        categoryDataTable = Table(categoryDataData)
        categoryDataTable.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F1F1F')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#E7E6E6')),
            ('GRID', (0, 0), (-1, -1), 1, colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.aliceblue, colors.lavender])
        ]))
        story.append(categoryDataTable)        
    story.append(PageBreak())

    # add the charts and graphs
    # first, generate the visualizations using the function i made from 'data_visualization' module
    generateVisualizations(processedExpenseData) 

    # add the titles
    story.append(Spacer(1, 3 * inch))
    story.append(Paragraph("Charts", titleStyle))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("& Graphs", titleStyle))
    story.append(Spacer(1, 0.2 * inch))
    story.append(PageBreak())

    # add title and pie chart
    story.append(Paragraph("<b>Total Expenses by Category</b>", subheaderStyle))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Image("expenseByCategoryPieChart.png", width=7*inch, height=7*inch))
    story.append(Spacer(1, 0.25 * inch))
    story.append(PageBreak())

    # add title and bar chart
    story.append(Paragraph("<b>Total Expenses by Employee</b>", subheaderStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Image("expenseByEmployeeBarChart.png", width=5*inch, height=8*inch))
    story.append(Spacer(1, 0.25 * inch))
    story.append(PageBreak())

    #TODO: add a SpendSense thank you image to the PDF
    # add a SpendSense thank you image to the PDF
    # story.append(Image('SpendSense.png', width=2*inch, height=2*inch))

    # save the PDF, aka build the document
    doc.build(story)

    # set the path to the generated PDF report and return it
    pdfFilePath = "ExpenseReport.pdf"
    return pdfFilePath
