# Import necessary libraries
import data_import
import data_processing
import data_visualization
import report_generation
from styles import titleStyle, sectionHeaderStyle, subheaderStyle, bodyStyle

# accept the path to the CSV input file as a command-line argument within the testdata folder like this: python main.py sampleinput , knowing that the input file is in the testdata folder and the name of the file is sampleinput.csv
# inputFile = 'testdata/' + sys.argv[1] + '.csv'
inputFile = 'testdata/sampleinput.csv'

# now you can run the script from the command line like this: python main.py sampleinput


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
        pdfFile = report_generation.generateReport(processedExpenseData, df)

        # print the path to the PDF file

        print('Report generated at: ' + pdfFile)

    except Exception as e:
        print('An error occurred while generating the report: ' + str(e))

if __name__ == "__main__":
    # Run the main function and test cases only when the script is executed as
    # the main module
    main()
