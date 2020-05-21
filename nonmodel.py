import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dash.dependencies import Input, Output, State
import paho.mqtt.client as mqtt
import time
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime,timedelta
import os
from flask import render_template

from collections import OrderedDict 

FA ="https://use.fontawesome.com/releases/v5.8.1/css/all.css"

from influxdb import InfluxDBClient
from influxdb import DataFrameClient

#server = Flask(__name__)
#server.config['INFLUXDB_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'influxdb:///plan.db')
##server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(server)
#db_URI = os.environ.get('DATABASE_URL', 'influxdb:///plan.db')
#engine = create_engine(db_URI)


client1 = InfluxDBClient(host='127.0.0.1', port=8086)#(host='0.0.0.0', port=8086)

#client = InfluxDBClient(host='mydomain.com', port=8086, username='myuser', password='mypass', ssl=True, verify_ssl=True)

client1.create_database('plan')

#client.get_list_database()

client1.switch_database('plan')

#[{'fields': {'message': 'hii'}, 'measurement': 'table', 'tags': {'chat': <paho.mqtt.client.Client object at 0x7f196754ff10>}, 'time': '2020-05-20 14:27:27.884088'}]



def insert(messa):
    print("insert=",messa)
    client1.write_points(messa)
    print(byenbiibbb)


#query3 = client1.query('select * from ' + 'hi'  + ' where time < now()-' + '1d', chunked=True)
#print(query3)

#query1 = client.query('SELECT "duration" FROM "chatting"."autogen"."brushEvents" WHERE time > now() - 4d GROUP BY "user"')

#print(query1)

def on_connect(client, userdata, flags, rc):
    print("Connected!", rc)
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(granted_qos))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

def on_publish(client, userdata, mid):
    print("Publish:", client)


def on_message(client, userdata, message):
    print("on_message=",message,userdata)
    print("messa=",message.payload.decode("utf-8"))
    messa=[    
            {
        "measurement": "message_table3",
        "tags": 
        {
            "user": 234,#str(userdata),
            "Id":123,# str(client),
        },
        "time":str(datetime.today()), 
        "fields": 
        {
            "message":str(message.payload.decode("utf-8"))
        }
    }
 ]
    print("messa=",message)
    print("messa=",messa)

    client1.write_points(messa)
    #insert(messa)
    
#results=client.query('SELECT "duration" FROM "pyexample"."autogen"."brushEvents" WHERE time > now() - 4d GROUP BY "user"') 
#print(results.raw)
#points = results.get_points(tags={'user':'Carol'})
#for point in points:
#    print("Time: %s, Duration: %i" % (point['time'], point['duration']))
#brush_usage_total = 0
#for point in points:
#     brush_usage_total = brush_usage_total + point['duration']
 
#if brush_usage_total > 350:
#     print("You've used your brush head for %s seconds, more than the recommended amount! Time to replace your brush head!" % brush_usage_total)


client = mqtt.Client()
client.on_subscribe = on_subscribe
#client.on_unsubscribe = on_unsubscribe
client.on_connect = on_connect
client.on_message = on_message
time.sleep(1) # Sleep for a beat to ensure things occur in order

subtop="tracker/device/sub"
pubtop="tracker/device/pub"

#client.username_pw_set("foogpegu:foogpegu", "UodafP1juFtY9qpMy7VeW9VCwTJ0Z3cU")
# client.connect('lion.rmq.cloudamqp.com', 1883)

client.username_pw_set("cbocdpsu", "3_UFu7oaad-8")
client.connect('soldier.cloudmqtt.com', 14035,60)
#client.connect("192.168.43.163", 500)
client.loop_start()
client.subscribe(subtop)
#print("subscribe")
#chatinput=input()
#client.publish(pubtop,chatinput)
client.loop()


PLOTLY_LOGO =""#https://i2.wp.com/corecommunique.com/wp-content/uploads/2015/09/smarttrak1.png"

#app = dash.Dash(__name__,server=server,external_stylesheets=[dbc.themes.BOOTSTRAP, FA])
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP, FA])

navbar = dbc.Navbar(html.Div(
    # Use row and col to control vertical alignment of logo / brand
            dbc.Row([dbc.Col(html.Img(src=PLOTLY_LOGO, height="50px")),
                     dbc.Col(dbc.NavbarBrand( html.H2("RMK Chat",style={"align":"center",'padding-right':'30rem','fontSize':'40px','align':'center','font-style': 'Georgia', 'font-weight': 'bold','color':'#610572'}))),],), ),color="#C3C489")

page_4_write=html.Div([dbc.Row([html.Div(id='receive'),html.Div(id='sent')]),
#html.H4('Using these you can write the commands for setting the values in the device'),
html.Div(dcc.Input(id="input chat", type="text",className="mr-1")),
                dbc.Button("Send", id="chat button",color='primary',outline=True)])

app.config['suppress_callback_exceptions']=True

app.layout=html.Div([navbar,page_4_write])


"""@app.callback(Output('receive', 'children'),
                [Input('receive', 'value')])
def display(x):
    #connectionmess=engine
    #df=pd.read_sql("select * from datatable",connectionmess)
    #dfdata=df[df.idxmax(axis = 1, skipna = True)]
    #dfdata=df[df.id==(len(df)-1)]
    #print(dfdata)
    #return "{}".format([chatdict['message']])
    #return "{}---{}".format(dfdata.stamp ,dfdata.message)
    results=client1.query('SELECT "message" FROM "chatting"."autogen"."message_table2" WHERE time > now() - 4d GROUP BY "user"') 
    return "{}".format(results)"""


@app.callback(
    dash.dependencies.Output('sent','children'),
    [dash.dependencies.Input('chat button','n_clicks')],
    [dash.dependencies.State('input chat','value')])
def update_output(x,value2):
    #if((value2 != None) and (x is not None)):
    if((value2 != None) and (x)):
        print(value2)
        print(x)
        #client.publish(pubtop,"{}".format(value2))
        client.publish(pubtop,value2)
        x=0
        return "{}".format(value2)
        print("bye")
      
CONTENT_STYLE = {
    "bottom": "0rem",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding-right": "10rem",
}
content = html.Div(id="page-content", style=CONTENT_STYLE)

#@server.route('/')
def main():
    return html.Div([navbar,page_4_write,dcc.Location(id='url', refresh=False),content])

#@server.route('/')
def base1():
    return render_template('base.html',name=None)

if __name__ == '__main__':
    app.run_server(port=5000,debug=False, use_reloader=False,#processes=4,
            threaded=False)#,threaded=True, use_reloader=True)
