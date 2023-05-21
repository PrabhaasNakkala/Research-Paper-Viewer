from bs4 import BeautifulSoup
import os
import prompt

list = dict()
testString = prompt.response
testString = str(testString)

# print('testString:', testString)

hold = 0
colon = 0
testString = ' ' + testString
for i in range(0, len(testString)):
    if(testString[i] == ':'):
        colon = i
    if(testString[i] == '.'):
        list[testString[hold + 1:colon].replace('\n', '')] = testString[colon + 2:i]
        hold = i + 1

# list = {"Cronbach's Alpha": 'A statistical measure of the reliability of a survey or questionnaire', 'Kuala Lumpur': 'The capital city of Malaysia', 'Halal': 'A term used to describe items which are permissible under Islamic law', 'IPTS': 'A type of higher educational institution in Malaysia', 'IPTA': 'A type of higher educational institution in Malaysia', 'Hypothesis': 'A proposed explanation for a phenomenon or a logical conjecture made in order to draw out and test its consequences', 'Regression': 'A statistical technique for determining the relationship between a dependent variable and one or more independent variables', 'Phenomenon': 'Something that exists or occurs in reality, especially something remarkable', 'JAKIM': 'A government body in Malaysia responsible for Halal certification'}



# for key in list:
#     if len(key) < 3:
#         list.pop(key)

print('List: ', list)

curr = os.getcwd()
soup = BeautifulSoup(open(curr+"/website.html"), "html.parser")

styleTags = '''
    .popup {
        position: relative;
    } 

    .popup::after {
      content: attr(data-popup-content);
      visibility: hidden;
      opacity: 0;
      position: absolute;
      top: -30px;
      left: 0;
      width: 200px;
      padding: 10px;
      background-color: #fff;
      border: 1px solid #ccc;
      border-radius: 5px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
      z-index: 1;
      transition: visibility 0.3s, opacity 0.3s;
    }
    
    .popup:hover::after {
        visibility: visible;
        opacity: 1;
    } 
'''

body = soup.body
soupText = str(soup)
origString = str(body)
bodyString = str(body)

soupText = soupText[:soupText.find('<style>') + 8] + styleTags + soupText[soupText.find('<style>') + 8:]

for word in list:    
    if len(word) < 3:
        continue
    rep = '<a class="popup" href="#" data-popup-content=\"' + list[word] + '\">' + word + '</a>'
    bodyString = bodyString.replace(word, rep)
    bodyString = bodyString.replace(word.lower(), rep)

soupText = soupText.replace(origString, bodyString)
file = open('website.html', 'w')
file.write(soupText)
file.close()




