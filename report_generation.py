from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle, Paragraph, PageBreak
import io
import os
import pandas as pd


# Define the styles to be used in the report
styles = getSampleStyleSheet()

titleStyle = ParagraphStyle(
    name="Title",
    fontName="Arial",
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


def generateReport(processedExpenseData): # q: what is the input to this function? 
    """
    Generate the expense report PDF.
    """
    doc = SimpleDocTemplate(, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    # Create the PDF object, using the buffer as its "file."
    report = SimpleDocTemplate("expense_report.pdf", pagesize=letter, leftMargin=inch/2, rightMargin=inch/2, topMargin=inch/2, bottomMargin=inch/2)

    # Get the data frames from the expense data dictionary
    totalByCategory = processedExpenseData['totalByCategory']
    totalByEmployee = processedExpenseData['totalByEmployee']
    totalExpenses = processedExpenseData['totalExpenses']

    # Initialize the story list for the PDF
    story = []

    # Add the cover page to the PDF
    story.append(Paragraph("Expense Report", titleStyle))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("Date Range: [Insert Date Range Here]", styles["Normal"]))
    story.append(Paragraph("Company Name: [Insert Company Name Here]", styles["Normal"]))
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
    story.append(Paragraph("<b>Total Amount Spent</b>: $%.2f" % totalExpenses, bodyStyle))
   
