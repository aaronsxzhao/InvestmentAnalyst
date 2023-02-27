import requests
from bs4 import BeautifulSoup
import io
from PyPDF2 import PdfFileReader


url = "https://investors.mgmresorts.com/investors/financial-info/annual-reports/default.aspx"
read = requests.get(url)
html_content = read.content
soup = BeautifulSoup(html_content, "html.parser")
# reports = soup.find_all("a", class_="btn btn-default")

# print(reporsts)
list_of_pdf = set()
l = soup.find('p')
print(soup)
p = l.find_all('a')
# print(p)

for link in (p):
	pdf_link = (link.get('href')[:-5]) + ".pdf"
	print(pdf_link)
	list_of_pdf.add(pdf_link)

def info(pdf_path):
	response = requests.get(pdf_path)
	
	with io.BytesIO(response.content) as f:
		pdf = PdfFileReader(f)
		information = pdf.getDocumentInfo()
		number_of_pages = pdf.getNumPages()

	txt = f"""
	Information about {pdf_path}:

	Author: {information.author}
	Creator: {information.creator}
	Producer: {information.producer}
	Subject: {information.subject}
	Title: {information.title}
	Number of pages: {number_of_pages}
	"""
	print(txt)
	return information


for i in list_of_pdf:
	info(i)
