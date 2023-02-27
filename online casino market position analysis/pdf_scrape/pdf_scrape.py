import PyPDF2 as pdf2
import re

# Open the PDF file
pdf_file = open('annual_reports/pointsbet2021.pdf', 'rb')
pdf_reader = pdf2.PdfReader(pdf_file)

# Extract text from each page of the PDF
text = ""
for page_num in range(pdf_reader.numPages):
    page = pdf_reader.getPage(page_num)
    text += page.extractText()

# Search for the revenue information in the text
financial_info = ''

# revenue_all = []
lines = text.split('\n')
for line in lines:
    if r'207' in line.lower() and bool(re.search(r'\d', line)):
        financial_info += line
    # if 'margin' in line.lower():
       
    #     margin += [int(s) for s in line.split() if s.isdigit()]

# Write the revenue information to a file
with open('financial_info/pointbet_financial_info.txt', 'w') as f:
    f.write(financial_info)

# Close the PDF file
pdf_file.close()
