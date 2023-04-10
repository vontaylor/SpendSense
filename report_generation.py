from data_visualization import generateVisualizations
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle, Paragraph, PageBreak, Image


import io
import os
import pandas as pd
from styles import titleStyle, sectionHeaderStyle, subheaderStyle, bodyStyle, tableOfContentsHeader

# function that takes my processed data as input
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
    # use reportlab library to create a new PDF document to hold the report
    doc = SimpleDocTemplate("expenseReport.pdf", pagesize=letter,
                            leftMargin=inch, rightMargin=inch,
                            topMargin=inch, bottomMargin=inch)

    # get the data frames from the expense data dictionary
    totalByCategory = processedExpenseData['totalByCategory']
    totalByEmployee = processedExpenseData['totalByEmployee']
    totalExpenses = processedExpenseData['totalExpenses']
    # totalByMonth = processedExpenseData['totalByMonth']

    # initialize story list for PDF
    story = []

    # Add the cover page to the PDF
    story.append(Paragraph("April's", titleStyle))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("Expense", titleStyle))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("Report", titleStyle))
    story.append(Spacer(1, 0.5 * inch))
    # story.append(Image("totalExpensesByCategoryPieChart.png", width=5*inch, height=5*inch))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("Company Name: [Insert Company Name Here]", bodyStyle))
    story.append(PageBreak())

    # Add the table of contents to the PDF clickable links to each section
    story.append(Paragraph("Table of Contents", tableOfContentsHeader))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<u>Summary</u>", subheaderStyle))
    story.append(Paragraph("<u>Expense Details</u>", subheaderStyle))
    story.append(Paragraph("<u>Charts and Graphs</u>", subheaderStyle))
    story.append(PageBreak())

    # Add the summary section to the PDF
    story.append(Paragraph("Summary", titleStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<b>Executive Summary</b>", subheaderStyle))
    story.append(Paragraph("[Insert Executive Summary Here]", bodyStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<b>Total Amount Spent</b>: %s" % formatAmount(totalExpenses), bodyStyle))

    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<b>Top 5 Expense Categories by Total Spend</b>", subheaderStyle))
    story.append(Spacer(1, 0.25 * inch))


    # Add the top 5 expenses to the PDF
    top5Expenses = totalByCategory.head(5)  # get the top 5 expenses
    # get the columns we want
    top5Expenses = top5Expenses[['ExpenseCategory', 'Amount', 'Percentage']]
    top5Expenses = top5Expenses.rename(columns={
                                       'ExpenseCategory': 'Category', 'Amount': 'Amount Spent', 'Percentage': 'Percentage of Total'})  # rename the columns
    top5Expenses = top5Expenses.round(
        {'Amount Spent': 2, 'Percentage of Total': 2})  # round the values
    top5Expenses['Amount Spent'] = top5Expenses['Amount Spent'].apply(formatAmount)

    # Add the top 5 expenses as a table
    top5ExpensesData = [['Category', 'Amount Spent', 'Percentage of Total']] + top5Expenses.values.tolist()
    top5ExpensesTable = Table(top5ExpensesData)
    top5ExpensesTable.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F1F1F')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#E7E6E6')),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        # ('LEFTPADDING', (0, 0), (-1, -1), 15),
    ]))
    story.append(top5ExpensesTable)
    story.append(Spacer(1, 0.25 * inch))

    story.append(Paragraph("<b>Total Number of Employees Included</b>: %d" %
                 len(totalByEmployee), bodyStyle))
    story.append(Spacer(1, 0.25 * inch))

    # Get the top 5 expense transactions
    top5Transactions = df.nlargest(5, 'Amount')
    # Select the columns we want
    top5Transactions = top5Transactions[['ExpenseDate', 'EmployeeName', 'ExpenseCategory', 'Amount']]
    # Add the top 5 expense transactions to the PDF
    
    story.append(Paragraph("<b>Top 5 Expense Transactions</b>", subheaderStyle))
    story.append(Spacer(1, 0.25 * inch))

    top5Transactions = processedExpenseData['top5Transactions']
    # top5Transactions['ExpenseDate'] = top5Transactions['ExpenseDate'].dt.strftime('%Y-%m-%d')  # Format the date
    top5Transactions['Amount'] = top5Transactions['Amount'].apply(formatAmount)  # Format the amount

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

    # convert the data frame to a string
    top5Expenses = top5Expenses.to_string(index=False)

    story.append(Paragraph("<b>Trends in Expense Data</b>", subheaderStyle))
    story.append(Spacer(1, 0.25 * inch))

    # Add the trends in expense data to the PDF
    story.append(Paragraph("[Insert Trends in Expense Data Here]", bodyStyle))
    story.append(PageBreak())

    # Add the expense details section to the PDF
    story.append(Paragraph("Expense Details", titleStyle))
    story.append(Spacer(1, 0.25 * inch))
    # Add the expense category breakdowns to the PDF
    # get the list of expense expenseCategories
    expenseCategories = totalByCategory['ExpenseCategory'].tolist()

    for expenseCategory in expenseCategories:
        story.append(Paragraph("<b>%s</b>" % expenseCategory, subheaderStyle))
        story.append(Spacer(1, 0.25 * inch))

        # Get the data frame for the current expenseCategory
        categoryData = df[df['ExpenseCategory'] == expenseCategory].copy()
        categoryData['Amount'] = categoryData['Amount'].apply(formatAmount) 

        categoryData_data = [['Emp#', 'Employee', 'Category', 'Date', 'Amount', 'Details' ]] + categoryData.values.tolist()
        categoryData_table = Table(categoryData_data)
        categoryData_table.setStyle(TableStyle([
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

        story.append(categoryData_table)
        # story.append(Spacer(1, 0.25 * inch))
        

        
    story.append(PageBreak())
    # call generateVisualizations function and add the charts and graphs to the PDF
    generateVisualizations(processedExpenseData)
    story.append(Paragraph("Charts", titleStyle))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("& Graphs", titleStyle))
    story.append(Spacer(1, 0.2 * inch))
    story.append(
        Paragraph("<b>Total Expenses by Category</b>", subheaderStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Image("expenseByCategoryPieChart.png",
                 width=7*inch, height=7*inch))
    story.append(Spacer(1, 0.25 * inch))
    story.append(
        Paragraph("<b>Total Expenses by Employee</b>", subheaderStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Image("expenseByEmployeeBarChart.png",
                 width=5*inch, height=5*inch))
    story.append(Spacer(1, 0.25 * inch))
    # story.append(Paragraph("<b>Total Expenses by Month</b>", subheaderStyle))
    # story.append(Spacer(1, 0.25 * inch))
    # story.append(Image("totalExpensesByMonthBarChart.png",
    #              width=5*inch, height=5*inch))
    # story.append(Spacer(1, 0.25 * inch))
    story.append(PageBreak())

    # add a SpendSense thank you image to the PDF
    # story.append(Image('SpendSense.png', width=2*inch, height=2*inch))

    # save the PDF aka build the document
    doc.build(story)

    pdfFilePath = "ExpenseReport.pdf"

    return pdfFilePath
