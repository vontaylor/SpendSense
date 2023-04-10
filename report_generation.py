from data_visualization import generateVisualizations
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle, Paragraph, PageBreak, Image
import io
import os
import pandas as pd


# defining the styles to be used in the report
styles = getSampleStyleSheet()

titleStyle = ParagraphStyle(
    name="Title",
    fontName="Helvetica",
    fontSize=24,
    textColor=colors.HexColor(0x00008B),
    alignment=1,
    spaceAfter=inch/2
)

sectionHeaderStyle = ParagraphStyle(
    name="SectionHeader",
    fontName="Times-Bold",
    fontSize=16,
    textColor=colors.HexColor(0x00008B),
    spaceBefore=inch/2,
    spaceAfter=inch/4
)

subheaderStyle = ParagraphStyle(
    name="Subheader",
    fontName="Times-Bold",
    fontSize=12,
    textColor=colors.HexColor(0x00008B),
    spaceBefore=inch/4,
    spaceAfter=inch/8
)

bodyStyle = ParagraphStyle(
    name="Body",
    fontName="Times-Roman",
    fontSize=12,
    spaceBefore=inch/8,
    spaceAfter=inch/8
)

# function that takes the processed data as input


def generateReport(processedExpenseData, df):
    """
    Generate the expense report PDF.
    """
    # use reportlab library to create a new PDF document to hold the report
    doc = SimpleDocTemplate("expenseReport.pdf", pagesize=letter,
                            leftMargin=inch/2, rightMargin=inch/2,
                            topMargin=inch/2, bottomMargin=inch/2)

    # Get the data frames from the expense data dictionary
    totalByCategory = processedExpenseData['totalByCategory']
    totalByEmployee = processedExpenseData['totalByEmployee']
    totalExpenses = processedExpenseData['totalExpenses']

    # Initialize the story list for the PDF
    story = []

    # Add the cover page to the PDF
    story.append(Paragraph("Expense Report", titleStyle))
    story.append(Spacer(1, 0.5 * inch))
    # story.append(Image("totalExpensesByCategoryPieChart.png", width=5*inch, height=5*inch))
    story.append(Spacer(1, 0.5 * inch))
    story.append(
        Paragraph("Date Range: [Insert Date Range Here]", styles["Normal"]))
    story.append(
        Paragraph("Company Name: [Insert Company Name Here]", styles["Normal"]))
    story.append(PageBreak())

    # Add the table of contents to the PDF
    story.append(Paragraph("Table of Contents", sectionHeaderStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<u>Summary</u>", subheaderStyle))
    story.append(Paragraph("<u>Expense Details</u>", subheaderStyle))
    story.append(Paragraph("<u>Charts and Graphs</u>", subheaderStyle))
    story.append(PageBreak())

    # Add the summary section to the PDF
    story.append(Paragraph("Summary", sectionHeaderStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<b>Executive Summary</b>", subheaderStyle))
    story.append(Paragraph("[Insert Executive Summary Here]", bodyStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<b>Total Amount Spent</b>: $%.2f" %
                 totalExpenses, bodyStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<b>Top 5 Expenses</b>", subheaderStyle))
    story.append(Spacer(1, 0.25 * inch))

    # Add the top 5 expenses to the PDF
    top5Expenses = totalByCategory.head(5)  # get the top 5 expenses
    # get the columns we want
    top5Expenses = top5Expenses[['ExpenseCategory', 'Amount', 'Percentage']]
    top5Expenses = top5Expenses.rename(columns={
                                       'ExpenseCategory': 'Category', 'Amount': 'Amount Spent', 'Percentage': 'Percentage of Total'})  # rename the columns
    top5Expenses = top5Expenses.round(
        {'Amount Spent': 2, 'Percentage of Total': 2})  # round the values
    # convert the data frame to a string
    top5Expenses = top5Expenses.to_string(index=False)
    story.append(Paragraph(top5Expenses, bodyStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<b>Total Number of Employees Included</b>: %d" %
                 len(totalByEmployee), bodyStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(
        Paragraph("<b>Top 5 Expense Categories by Total Spend</b>", subheaderStyle))
    story.append(Spacer(1, 0.25 * inch))

    # Add the top 5 expense categories to the PDF
    top5Categories = totalByCategory.head(
        5)  # get the top 5 expense categories
    # get the columns we want
    top5Categories = top5Categories[[
        'ExpenseCategory', 'Amount', 'Percentage']]
    top5Categories = top5Categories.rename(
        columns={'ExpenseCategory': 'Category', 'Amount': 'Total Spent', 'Percentage': 'Percentage of Total'})  # rename the columns
    top5Categories = top5Categories.round(
        {'Total Spent': 2, 'Percentage of Total': 2})  # round the values
    top5Categories = top5Categories.to_string(
        index=False)  # convert the data frame to a string

    story.append(Paragraph(top5Categories, bodyStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<b>Trends in Expense Data</b>", subheaderStyle))
    story.append(Spacer(1, 0.25 * inch))

    # Add the trends in expense data to the PDF
    story.append(Paragraph("[Insert Trends in Expense Data Here]", bodyStyle))
    story.append(PageBreak())

    # Add the expense details section to the PDF
    story.append(Paragraph("Expense Details", sectionHeaderStyle))
    story.append(Spacer(1, 0.25 * inch))

    # Add the expense category breakdowns to the PDF
    # get the list of expense expenseCategories
    expenseCategories = totalByCategory['ExpenseCategory'].tolist()
    for expenseCategory in expenseCategories:
        story.append(Paragraph("<b>%s</b>" % expenseCategory, subheaderStyle))
        story.append(Spacer(1, 0.25 * inch))

        # Get the data frame for the current expenseCategory
        categoryData = df[df['ExpenseCategory'] == expenseCategory]
        categoryData = categoryData[['EmployeeName', 'Amount', 'Percentage']]
        categoryData = categoryData.rename(columns={
                                           'EmployeeName': 'Employee', 'Amount': 'Amount Spent', 'Percentage': 'Percentage of Total'})
        categoryData = categoryData.round(
            {'Amount Spent': 2, 'Percentage of Total': 2})
        categoryData = categoryData.to_string(index=False)

        story.append(Paragraph(categoryData, bodyStyle))
        story.append(Spacer(1, 0.25 * inch))
        story.append(PageBreak())

    # call generateVisualizations function and add the charts and graphs to the PDF
    generateVisualizations(processedExpenseData)
    story.append(Paragraph("Charts and Graphs", sectionHeaderStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<b>Total Expenses by Category</b>", subheaderStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Image("totalExpensesByCategoryPieChart.png",
                 width=5*inch, height=5*inch))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<b>Total Expenses by Employee</b>", subheaderStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Image("totalExpensesByEmployeePieChart.png",
                 width=5*inch, height=5*inch))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<b>Total Expenses by Month</b>", subheaderStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Image("totalExpensesByMonthBarChart.png",
                 width=5*inch, height=5*inch))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<b>Total Expenses by Day of the Week</b>", subheaderStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Image("totalExpensesByDayOfWeekBarChart.png",
                 width=5*inch, height=5*inch))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("<b>Total Expenses by Hour of the Day</b>", subheaderStyle))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Image("totalExpensesByHourOfDayBarChart.png",
                 width=5*inch, height=5*inch))
    story.append(Spacer(1, 0.25 * inch))
    story.append(PageBreak())
    
    # add a SpendSense thank you image to the PDF
    story.append(Image('SpendSense.png', width=2*inch, height=2*inch))

    # save the PDF aka build the document
    doc.build(story)

    pdfFilePath = "ExpenseReport.pdf"

    return pdfFilePath
