from flask import Flask,render_template,request
import wiki
from copy import deepcopy
import page as pg
app = Flask(__name__)
pageTup = wiki.initPages()
startPage=pageTup[0]
currPage=pg.Page(startPage.title,startPage.description,startPage.links)
endPage=pageTup[1]
@app.route("/",methods=['GET', 'POST'])
def hello():
    global currPage
    global startPage
    global endPage
    if request.method == "POST":
        submitValue = request.form.get("submit")
        if submitValue==endPage.title:
            return render_template("win.html")
        else:
            nextPage = wiki.wikiJSON("https://en.wikipedia.org/w/api.php?action=query&titles=%s&explaintext=true&prop=extracts|links&pllimit=500&exintro=1&exsentences=3&explaintext=true&format=json"%(submitValue,))
            currPage.title = wiki.getTitle(nextPage)
            currPage.description = wiki.getDescr(nextPage)
            currPage.links = wiki.getLinks(nextPage)
    elif request.method == "GET":
        submitValue = request.args.get("submit")
        searchValue = request.args.get("search")
        if submitValue== "new":
            pageTup = wiki.initPages()
            startPage=pageTup[0]
            copy = deepcopy(pageTup)
            currPage=copy[0]
            endPage=pageTup[1]
        elif submitValue == "restart":
            currPage.title = startPage.title
            currPage.description=startPage.description
            currPage.links=startPage.links

    return render_template("index.html",start=startPage,curr=currPage,end=endPage)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
