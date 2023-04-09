# Import necessary libraries
import data_import
import data_processing
import data_visualization
import report_generation

# constant of input file path:
inputFile = "testdata/sampleinput.csv"

def main():
    """
    The main function of the script, which coordinates the different components
    of the system: data import, data processing, visualization, and report generation.
    """
    try:
        # read the input data from the CSV file
        df = data_import.readExpenseData(inputFile)

        # process the expense data (df) to calculate various statistics and group the data by categories, employees, and months
        processedExpenseData = data_processing.processExpenseData(df)

        # generate the report with visualizations and save it to a PDF file
        pdfFile = report_generation.generateReport(processedExpenseData)

        # print the path to the PDF file
        print('Report generated at: ' + pdfFile)

    except Exception as e:
        print('An error occurred while generating the report: ' + str(e))


