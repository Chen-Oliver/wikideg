from flask import Flask,render_template
import wiki
import page as pg


app = Flask(__name__)

@app.route("/")
def hello():
    pageTup = wiki.initPages()
    startPage=currPage = pageTup[0]
    endPage = pageTup[1]
    pathHist = [startPage.title]
    return(render_template("index.html",start=startPage,curr=currPage,end=endPage))

if __name__ == '__main__':
    app.debug = True
    app.run()
