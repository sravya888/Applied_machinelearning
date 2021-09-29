from flask import Flask,render_template, request, session, Response
# from werkzeug import secure_filename
# from flask_session import Session
import io
import random
from algorithms import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import json
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model, metrics

app = Flask(__name__)
app.secret_key = "any random string"

@app.route('/')
def upload_file():
   return render_template('fileupload.html')
	
@app.route('/uploader', methods = ['GET','POST'])
def uploader():

    fname=request.form.get("filename")
    print(fname.split("."))
    MLtype=request.form.get("algotype")
    if(fname.split(".")[1]!="txt"):
        return render_template('fileupload.html', filetxt=1) 
    df = pd.read_csv(fname,header=None)
    session["df"]=df.to_json()
    # print(df.to_json()) 
    session["MLtype"]=MLtype
    print(fname)
    print(MLtype)
#    if request.method == 'POST':
#       f = request.files['file']
#     #   f.save(secure_filename(f.filename))
    return render_template('SecondPage.html')


# @app.route('/linear',  methods = ['GET','POST'])
# def linear():
#     automate=request.form.get("automate")
#     session["automate"]=automate
#     print(session["automate"])
#     return render_template('linear.html',auto=automate)

@app.route('/linearregression',  methods = ['GET','POST'])
def linearregression():
    automate=request.form.get("automate")
    # automate=session["automate"]
    # if(automate=="yes"):
    #     alpha=0.2
    #     epochs=30
    # else:
    #     alpha = request.form.get("alpha")
    #     epochs = request.form.get("epoch")
    #     print(alpha, epochs)
    
    # session["testdata"]=data.to_json()
    df=session["df"]
    df=pd.read_json(df)
    df = pd.concat([pd.Series(1,index = df.index,name='00'),df],axis=1)
    drop_col = len(df.columns)-2
    X = df.drop(columns=drop_col)
    y = df.iloc[:,-1]
    # for i in range(1,len(X.columns)):
    #     X[i-1] = X[i-1]/np.max(X[i-1])
    # theta = np.array([0]*len(X.columns))
    print("--------- linear regression ---------------")
    reg = linear_model.LinearRegression()
    reg.fit(X,y)
    # data = session['testdata']
    test_file=request.form.get("filename")
    data = pd.read_csv(test_file,header=None)
    data_n2 = data.values
    m2 = len(data_n2)
    data = pd.concat([pd.Series(1,index = data.index,name='00'),data],axis=1)
    # data = pd.read_json(data)
    ypred = reg.predict(data)
    data = pd.DataFrame(data)   
    # print(session["automate"])
    if(request.method == ['GET']):
        output = io.BytesIO()
        FigureCanvas(plt).print_png(output)
        img=Response(output.getvalue(), mimetype='image/png')
        return render_template('linear.html',img=img)

    x=data.values.tolist()
    print("-------- x value = ",x)
    print("------- y value = ",y)
    return render_template('linear.html',auto=automate,xy = zip(x,ypred))

@app.route('/classi', methods = ['GET','POST'])
def classi():
    x=request.form.get("classi")
    y=request.form.get("automate")
    # print(x,y)
    return render_template('fileupload.html')


@app.route('/select', methods = ['GET','POST'])
def select():
    x=request.form.get("select")
    if(x=="shape"):
        df=session["df"]
       
        df=pd.read_json(df)
        # print(":////////////",df.shape)
        y=df.shape
        return render_template('SecondPage.html', tup=str(y),flag=1)
        # return str(y)
    if(x=="desc"):
        df=session["df"]
       
        df=pd.read_json(df)
        x=df.values.tolist()
        
    #     y=df.describe()
    #     print("://////////// describe",y)
    #     print(len(y))
    #     print(len(y.columns))
    #     for i i
        return render_template('SecondPage.html',table1=x, flag=2)
    if(x=="plot"):
        df=session["df"]
       
        df=pd.read_json(df)
        drop_col = len(df.columns)-2
        X = df.drop(columns=drop_col)
        y = df.iloc[:,-1]
        if len(df.columns)==2:
            plt.scatter(X[0],y,c="blue")
            plt.show()
        else:
            return render_template('SecondPage.html',flag=5)

            
    if(x=="predict"):
        return render_template('SecondPage.html',flag=6)
        if(session["MLtype"]=="Classification"):
            return render_template('SecondPage.html',flag=3) 
        else:
            return render_template('SecondPage.html',flag=4)


    # print(x)
    # return x
@app.route('/plot', methods = ['GET','POST'])
def plot():
    df=session["df"]
       
    df=pd.read_json(df)
    drop_col = len(df.columns)-2
    X = df.drop(columns=drop_col)
    y = df.iloc[:,-1]
    col=int(request.form.get("colvalue"))-1
    # col = int(input("Enter the Independent column number to plot = "))
    plt.scatter(X[col],y,c="blue")
    plt.show()
    return render_template('SecondPage.html',flag=5)
@app.route('/predict', methods = ['GET','POST'])
def predict():
    automate=request.form.get("automate")
    session["automate"]=automate
    print(session["automate"])
    if(automate=="yes"):
        return render_template('SecondPage.html',flag=4) 
    # else:

    
if __name__ == '__main__':
   app.run(debug = True)