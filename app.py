from flask import Flask,render_template,request
import wiki
from copy import deepcopy

app = Flask(__name__)
pageTup = wiki.initPages()
startPage=pageTup[0]
copy = deepcopy(pageTup)
currPage=copy[0]
endPage=pageTup[1]
pathHist=[startPage.title]
@app.route("/",methods=['GET', 'POST'])
def hello():
    global currPage
    global pathHist
    if request.method == "POST":
        title = request.form.get("submit")
        nextPage = wiki.wikiJSON("https://en.wikipedia.org/w/api.php?action=query&titles=%s&explaintext=true&prop=extracts|links&pllimit=500&exintro=1&exsentences=1&explaintext=true&format=json"%(title,))
        currPage.title = wiki.getTitle(nextPage)
        currPage.description = wiki.getDescr(nextPage)
        currPage.links = wiki.getLinks(nextPage)
    return render_template("index.html",start=startPage,curr=currPage,end=endPage)

if __name__ == '__main__':
    app.debug = True
    app.run()
