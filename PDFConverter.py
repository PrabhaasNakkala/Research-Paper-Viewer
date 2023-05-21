from PyPDF2 import PdfReader
import os
from bs4 import BeautifulSoup
import pdfplumber

tableSettings = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines"
}

curr = os.getcwd()

soup = BeautifulSoup(open(curr+"/website.html"), "html.parser")

text = ''
pdf = pdfplumber.open('file4.pdf')

pageCount = len(pdf.pages)

for num in range(0, pageCount):
    page = pdf.pages[num]
    bound = [table.bbox for table in page.find_tables(table_settings=tableSettings)]
    def notInBox(obj):
        def inBox(boundBox):
            mid1 = ((obj["top"] + obj["bottom"]) / 2)
            mid2 = ((obj["x0"] + obj["x1"]) / 2)
            x0, up, x1, down = boundBox
            return (mid1 >= up) and (mid1 < down) and (mid2 >= x0) and (mid2 < x1)
        return not any(inBox(boundBox) for boundBox in bound)
    text += page.filter(notInBox).extract_text()
    
text = text.replace('\n', ' ').replace('\"b', '').replace('\'b', '')
    
body = soup.body
soupText = str(soup)
origString = str(body)
bodyString = str(body)

brLocation = bodyString.find('<br/>')


while 1:
    index = str(text.encode('utf-8')).find('\\' + 'x')
    string = str(text.encode('utf-8'))[index:index+4]
    text = str(text.encode('utf-8')).replace(string, '')
    if str(text.encode('utf-8')).find('\\' + 'x') == -1:
        break

text = text.replace('\\', ' ')

bodyString = bodyString[:brLocation + 5] + '<p class="main">' + str(text.encode('utf-8')) + '</p>' + bodyString[brLocation + 5:]
firstHalf = bodyString[:brLocation]
secondHalf = bodyString[brLocation:]
bodyString = firstHalf + '' + secondHalf
soupText = soupText.replace(origString, bodyString)

dataFile = open('data.txt', 'w')
dataFile.write(str(text.encode('utf-8')))
dataFile.close()

file = open('website.html', 'w')
file.write(str(soupText))
file.close()