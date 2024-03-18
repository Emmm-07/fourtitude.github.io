import json
from flask import Flask, request, render_template, request, jsonify, redirect, url_for,render_template_string
import pyodbc
import mysql.connector
from jinja2 import Template
from waitress import serve
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import  QUrl
from threading import Thread
from werkzeug.formparser import parse_form_data

amt_Stack =[]                       # datastruct Stack
# Quantity Dictionaries
buy_qty_Dict = {}
rent_qty_Dict = {}
services_qty_Dict = {}
# Price Dictionaries
buy_price_Dict = {'T-C001': 0, 'T-H001': 0, 'T-G001': 0,'H-CV001':0,'H-CR001':0,'H-CH001':0,'F-T001':0,'F-RR001':0,'F-M001':0}
rent_price_Dict = {'T-C001': 0, 'T-H001': 0, 'T-G001': 0,'H-CV001':0,'H-CR001':0,'H-CH001':0,'F-T001':0,'F-RR001':0,'F-M001':0}
services_price_Dict = {'M_01':0,'M_02':0,'M_03':0,'M_04':0,'M_05':0,}

class Variables:
    def __init__(self, initial_qty):
        self.qty = initial_qty

    def get_qty(self):
        return self.qty

    def set_qty(self, new_qty):
        self.qty = new_qty

var=Variables(0)



app = Flask(__name__)



try:
    # connection = mysql.connector.connect(
    #    host="localhost",
    #    user="root",
    #    password="",
    #    database="project"
    # )
    con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\jmbal\PycharmProjects\templates\database_fourtitude.accdb;'
    connection = pyodbc.connect(con_str)
    dBase_cursor = connection.cursor()
    print("CONNECTED")
except Exception as e:
    print("ERROR",e)


@app.route('/')
def fg_home():
    return render_template('fg_home.html')

##################################################################################################################################
def index():
    return 'Hello from Flask!'

def start_flask_app():
    app.run()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fourtitude Garage")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        self.load_flask_app()

    def load_flask_app(self):
        url = QUrl("http://127.0.0.1:5000/")  # Create a QUrl object
        self.web_view.setUrl(url)


def main():
    # Start Flask app in a separate thread
    from threading import Thread
    flask_thread = Thread(target=start_flask_app)
    flask_thread.start()

    # Create PyQt application
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
################################################################################################


@app.route('/customer_info', methods=['POST'])
def customer_info():
    name=request.form['name']
    address=request.form['address']
    contact=request.form['contact']

    dBase_cursor.execute(f"SELECT COUNT(*) FROM customer_profile")                                                    # To know the number of rows
    row_count = dBase_cursor.fetchone()[0]                                                                         #


    dBase_cursor.execute(f"INSERT INTO customer_profile (Customer_ID, Name, Address, Contact) VALUES ('CID{row_count}', '{name}', '{address}', '{contact}')")
    connection.commit()

    dBase_cursor.execute('select * from customer_profile')
    for row in dBase_cursor.fetchall():
        print(row)

    print(f"Name:{name} \nAddress:{address} \nContact Number:{contact}")

   # time.sleep(50000)
    return render_template('fg_cta.html')                                            #BABAGUHIN PA TO, ilink sa ibang window



# from fg_Cta to fg_STMenu
@app.route('/menu')
def menu():
    return render_template('fg_STMenu.html',placeholder=" ")


# Getting value from javascript
@app.route('/test',methods=['POST','GET'])
def test():
    output = request.get_json()
    if request.method == 'POST':
        output = request.get_json()
        amt_Stack.append(output)
        print("AFTER:", amt_Stack, " SIZE: ", len(amt_Stack))
        return jsonify({"redirect_url": "/compute"})



@app.route('/buy')
def buy():
    # data = request.json  # Get JSON data from the request body
    # amt_paid = data.get('amt_paid')  # Extract the 'amt_paid' value
    # print("Received amt_paid from JavaScript:", amt_paid)
    # # You can process the 'amt_paid' value here as needed
    # return jsonify({'message': 'Data received successfully'})

    # return render_template('fg_STMenu.html',total=total,change=change)
    # ot = request.args.get('ot')  # Get the value from test()
    return render_template('fg_STBuy1.html')

@app.route('/toyota')
def toyota():
    return render_template('fg_BToyota.html')


@app.route('/compute')
def compute():
    total=7564                                                 # ito yung ieedit sa db

    try:                                                                        # check if stack is empty
        amt_p=int(amt_Stack.pop())
    except Exception as e:
        amt_p=0

    if amt_p>=total:
        change = f"{amt_p-total}"
    else:
        change = "insuff"

    if total==0:
        amt_p=" "
        total=" "
        change=" "
    print(total,' : ',amt_p,' : ',change)

    return render_template('fg_BToyota.html', total=f"   {total}", change=change,placeholder=amt_p)




@app.route('/transaction', methods=['POST'])
def transaction():
    # vehicle_id = request.form['v_id']
 # Get data from js
    prev_data = request.form.get('divData')
    form_data = request.form.get('formData')

    transaction_code = form_data[5:6]                           # if B, R or S     -  Buy, Rent, Services
    vehicle_id = form_data[6:]                      #String slicing

    if transaction_code=="B":
        if vehicle_id in buy_qty_Dict:
            buy_qty_Dict[vehicle_id] = buy_qty_Dict[vehicle_id] + 1
        else:
            buy_qty_Dict[vehicle_id] = 1
    elif transaction_code=="R":
        if vehicle_id in rent_qty_Dict:
            rent_qty_Dict[vehicle_id] = rent_qty_Dict[vehicle_id] + 1
        else:
            rent_qty_Dict[vehicle_id] = 1
    else:
        if vehicle_id in services_qty_Dict:
            services_qty_Dict[vehicle_id] = services_qty_Dict[vehicle_id] + 1
        else:
            services_qty_Dict[vehicle_id] = 1

#BUY PART
    buy="<center><strong><br>BUY</strong></center><br>"
    for v_id in buy_qty_Dict:
         dBase_cursor.execute(f"select Vehicle_Make,Vehicle_Model,Buy_Price from vehicle_info where Vehicle_ID='{v_id}'")
         car_row = dBase_cursor.fetchone()
         buy_price_Dict[v_id] = buy_qty_Dict[v_id]* int(car_row[2])
         price=f"{buy_price_Dict[v_id]:,}"
         buy+=f"  <center>{car_row[0]} {car_row[1]} x{buy_qty_Dict[v_id]}.........Php {price} </center> <br> "

# RENT PART
    rent = "<center><strong>RENT</strong></center><br>"
    for v_id in rent_qty_Dict:
        dBase_cursor.execute(f"select Vehicle_Make,Vehicle_Model,Rent_Price from vehicle_info where Vehicle_ID='{v_id}'")
        car_row = dBase_cursor.fetchone()
        rent_price_Dict[v_id] = rent_qty_Dict[v_id] * int(car_row[2])
        price = f"{rent_price_Dict[v_id]:,}"
        rent += f"  <center>{car_row[0]} {car_row[1]} x{rent_qty_Dict[v_id]}.........Php {price} </center> <br> "

# SERVICES PART
    services = "<center><strong>SERVICES</strong></center><br>"
    for m_id in services_qty_Dict:
        dBase_cursor.execute(f"select    maintenance_Name,maintenance_Price from maintenance_services where maintenance_ID='{m_id}'")
        car_row = dBase_cursor.fetchone()
        services_price_Dict[m_id] = services_qty_Dict[m_id] * int(car_row[1])
        price = f"{services_price_Dict[m_id]:,}"
        services += f"  <center>{car_row[0]}   x{services_qty_Dict[m_id]}.........Php {price} </center> <br> "

    result=f"""
            {buy}
            <br>
            {rent}
            <br>
            {services}
        """
    return jsonify({'result':result})                                      #Sends a dictionary



if __name__ == '__main__':
    # app.run(debug=True)
    serve(app,host='0.0.0.0',port=50100,threads=2)
    #main()
