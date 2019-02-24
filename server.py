#!/usr/bin/env python

import web
from web import form
import webbrowser


import subprocess
import sys
import os

import requests 
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
import numpy as np
import seaborn as sns
import pandas as pd
import xlrd

web.config.debug = False
web.config.session_parameters['cookie_path'] = '/'
        

urls = ("/", "start",
        "/filters(.*)", "filters",
        "/result(.*)", "result",
        "/process(.*)", "process",
       "/upload", "upload",
       "/get_result", "get_result",
       "/anal", "anal")

app = web.application(urls, globals())
render = web.template.render('templates/', cache = False)


if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'filter_url': "", 'origin_url': ""})
    web.config._session = session
else:
    session = web.config._session


myform = form.Form( 
    form.Textbox("Enter URL:", 
        form.notnull,
        form.Validator('Не должно быть пустой строкой', lambda x: str(x) != ''))) 

class get_result:
    def GET(self):
        with open("start.png","w") as f:
            lines = f.readlines()
            lines = [l for l in lines if "ROW" in l]
            with open("C:/Users//Mvideo//Desktop//URAAAA.png","w")  as f1:
                f1.writelines(lines)
        return render.get_result()

class anal:
    def GET(self):
        df = pd.read_csv('roma_final_output.csv', header = None)
        df.columns = ['machine', 'begin_time', 'end_time', 'name']
        max_time = df['end_time'].max()
        for t in range(max_time):
                df[str(t)] = np.array(t >= df['begin_time'], dtype=int) * np.array(t <= df['end_time'] , dtype=int)
        df_list = []
        col_list = []
        for i in range(max_time):
            col_list += [str(i)]

        col_list.append('name')

        for mach in range(1, 11):
            df_machine = df[df['machine']==mach][col_list]
            df_list += [df_machine]
        height = []
        for i in range(10):
            height += [ df_list[i].sum()[:-1].sum()]
        plt.figure(figsize=(16,8))
        plt.bar(range(1,11), height, color='darkgreen')
        plt.title('Распределение времени работы по станкам', fontsize=20)
        plt.xlabel('Номер станка', fontsize=16)
        plt.ylabel('Минуты работы', fontsize=16)
        plt.savefig('plot1.png')
        plt.clf()
        plt.figure(figsize=(16,8))
        plt.plot(df.sum()[4:][::200], color='darkgreen')
        plt.title('Зависимость нагруженности станков от времени', fontsize=20)
        plt.xlabel('Время', fontsize=16)
        plt.ylabel('Количество работающих станков', fontsize=16)
        plt.savefig('plot2.png')
        
        file_object1  = open('plot1.png', "r")
        file_object2 = open('plot2.png', "r")
        
        return render.anal(file_object1, file_object2)

       
class upload:
    def GET(self): 
        form = myform()
        # make sure you create a copy of the form by calling it (line above)
        # Otherwise changes will appear globally
        return render.formtest(form)

    def POST(self): 
        form = myform() 
        if not form.validates(): 
            return render.formtest(form)
        else:
            # form.d.boe and form['boe'].value are equivalent ways of
            # extracting the validated arguments from the form.
            str_url = form["Enter URL:"].value
            r = requests.get(str_url)
            with open("get_data.xlsx",'wb') as f:
                    f.write(r.content) 
        return render.get_result()
  
class start:
    def GET(self):
        return render.start()
        
class filters:
    def GET(self, url):
        if not session['origin_url'].startswith('http') or url != 'fromprocess':
            session['origin_url'] = "http://" + url
        return render.filters()

class process:
    def GET(self, filter_url):
        session['filter_url'] = filter_url
        return render.process("", "", "hidden", "", 'true')
        
class result:
    def GET(self, dummy_url):
     
        filter_url = session['filter_url']
        origin_url = session['origin_url']
        
        after = subprocess.check_output(["bash", "script.sh", origin_url, filter_url])
        # catch error
        if not after.startswith('http'):
            after = '/static/PhLab1.jpg'
        return render.process("", after, "", "hidden", 'false')

    
        
if __name__ == "__main__":
    app.run()


