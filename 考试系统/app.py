{\rtf1\ansi\ansicpg936\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from flask import Flask, request, jsonify, render_template\
from docx import Document\
import re, random, os\
\
app = Flask(__name__)\
BANK = []\
\
def parse_docx(path):\
    doc = Document(path)\
    text = "\\n".join([p.text for p in doc.paragraphs if p.text.strip()])\
    lines = text.split("\\n")\
\
    qs=[]\
    cur=None\
\
    for l in lines:\
        l=l.strip()\
        if not l: continue\
\
        if re.match(r"^\\d+[\\.\uc0\u12289 ]", l):\
            if cur: qs.append(cur)\
            cur=\{"q":"","options":[],"answer":[],"type":"single","chapter":"\uc0\u26410 \u30693 "\}\
            cur["q"]=re.sub(r"^\\d+[\\.\uc0\u12289 ]","",l)\
\
        elif "\uc0\u31532 " in l and "\u31456 " in l:\
            if cur: cur["chapter"]=l\
\
        elif re.match(r"^[A-D][\\.\uc0\u12289 ]", l):\
            cur["options"].append(l)\
\
        elif "\uc0\u27491 \u30830 \u31572 \u26696 " in l:\
            ans=l.split("\uc0\u27491 \u30830 \u31572 \u26696 \u65306 ")[-1].strip()\
            if ans in ["\uc0\u27491 \u30830 ","\u38169 \u35823 "]:\
                cur["type"]="judge"\
                cur["answer"]=["A"] if ans=="\uc0\u27491 \u30830 " else ["B"]\
            else:\
                ans=re.sub(r"[^A-D]","",ans)\
                cur["answer"]=list(ans)\
                cur["type"]="multi" if len(ans)>1 else "single"\
\
    if cur: qs.append(cur)\
    return qs\
\
\
@app.route("/")\
def index():\
    return render_template("index.html")\
\
@app.route("/upload",methods=["POST"])\
def upload():\
    global BANK\
    f=request.files["file"]\
    path="temp.docx"\
    f.save(path)\
    BANK=parse_docx(path)\
    return jsonify(\{"count":len(BANK)\})\
\
@app.route("/exam")\
def exam():\
    def pick(t,n):\
        arr=[q for q in BANK if q["type"]==t]\
        return [random.choice(arr) for _ in range(n)] if arr else []\
\
    return jsonify(\{\
        "questions":pick("single",20)+pick("multi",5)+pick("judge",5)\
    \})\
\
if __name__=="__main__":\
    app.run(debug=True)}