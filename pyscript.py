import json
from flask import Flask, request, render_template, request, jsonify, redirect, url_for,render_template_string
import pyodbc
# import mysql.connector
from jinja2 import Template
from waitress import serve
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import  QUrl
from threading import Thread
from werkzeug.formparser import parse_form_data
from datetime import date
from fpdf import FPDF
from pdf2image import convert_from_path

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
    def __init__(self, initial_total):
        self.amount_paid=" "
        self.result=""                              # transcript / string of all transaction
        self.change=""
    #Custom Service
        self.custom_quantity=0
        self.custom_price = 0
        self.custom_code=6
        self.custom_servCheck=''
    #Transaction database
        self.total = initial_total
        self.customer_id=""
        self.transactions= []                       #the BT-HC00 something
        self.transaction_date = date.today().strftime("%d/%m/%Y")
        self.employee_name=""

        self.customer_name = ""
        self.customer_address = "//"

        self.filter_date = ""

    def get_total(self):
        return self.total

    def set_total(self, new_total):
        self.total = new_total

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
    print("1ERROR",e)


def display_transactions():
    # BUY PART
    partial_total=0
    buy = "<center><strong><br>BUY</strong></center><br>"
    for v_id in buy_qty_Dict:
        dBase_cursor.execute(f"select Vehicle_Make,Vehicle_Model,Buy_Price from vehicle_info where Vehicle_ID='{v_id}'")
        car_row = dBase_cursor.fetchone()
        buy_price_Dict[v_id] = buy_qty_Dict[v_id] * int(car_row[2])
        partial_total = partial_total + buy_price_Dict[v_id]
        price = f"{buy_price_Dict[v_id]:,}"
        buy += f"  <center><p style=\"font-size:13px\">{car_row[0]} {car_row[1]} x{buy_qty_Dict[v_id]}.........Php {price} </p></center> <br> "
    # RENT PART
    rent = "<center><strong>RENT</strong></center><br>"
    for v_id in rent_qty_Dict:
        dBase_cursor.execute(f"select Vehicle_Make,Vehicle_Model,Rent_Price from vehicle_info where Vehicle_ID='{v_id}'")
        car_row = dBase_cursor.fetchone()
        rent_price_Dict[v_id] = rent_qty_Dict[v_id] * int(car_row[2])
        partial_total=partial_total + rent_price_Dict[v_id]

        price = f"{rent_price_Dict[v_id]:,}"
        rent += f"  <center><p style=\"font-size:13px\">{car_row[0]} {car_row[1]} x{rent_qty_Dict[v_id]}.........Php {price} </p></center> <br> "
    # SERVICES PART
    services = "<center><strong>SERVICES</strong></center><br>"
    print(services_qty_Dict)
    for m_id in services_qty_Dict:
        try:
            dBase_cursor.execute(f"select    maintenance_Name,maintenance_Price from maintenance_services where maintenance_ID='{m_id}'")
        except Exception as e:
            print("2Error: ",e)
        car_row = dBase_cursor.fetchone()
        services_price_Dict[m_id] = services_qty_Dict[m_id] * int(car_row[1])
        partial_total=partial_total + services_price_Dict[m_id]
        price = f"{services_price_Dict[m_id]:,}"  # Put comma in Money every 3 digits
        services += f"  <center><p style=\"font-size:13px\">{car_row[0]}   x{services_qty_Dict[m_id]}.........Php {price}</p> </center> <br> "

    if buy_qty_Dict == {}:
        buy =" "
    if rent_qty_Dict == {}:
        rent =" "
    if services_qty_Dict == {}:
        services =" "
    result = f"""
                {buy}
                <br>
                {rent}
                <br>
                {services}
            """
    var.set_total(partial_total)
    return result

def receipt(transactions_list,transaction_id):
    my_pdf = FPDF()
    my_pdf.add_page()

    divider = "*****************************************************************************"
    title = " O F F I C I A L   R E C E I P T "
    TY = " T H A N K   Y O U "
    address = """ 11th Floor Room 3, Far Eastern Univeristy
    Institue Of Technology , Paredes Street , Sampaloc Manila """
    Einfo = f""" Employee Name: {var.employee_name}
    Date: {var.transaction_date}
    Transaction ID: {transaction_id}
    """
    Cinfo = f""" Sold To
    Customer Name: {var.customer_name}
    Address: {var.customer_address}
    """

    space = """
      
    """
    my_pdf.set_font("Arial", size=19)
    my_pdf.multi_cell(200, 6, txt=space , align="C")
    my_pdf.set_font("Arial", size=21,style="B")
    my_pdf.cell(200, 6, txt=" Fourtitude Garage ", ln=3, align="C")
    my_pdf.set_font("Arial", size=17)
    my_pdf.cell(200, 6, txt=" (Group 4) ", ln=5, align="C")

    my_pdf.multi_cell(200, 6, txt=address, align="C")

    my_pdf.cell(200, 6, txt=divider, ln=8, align="C")

    my_pdf.cell(200, 6, txt=title, ln=9, align="C")

    my_pdf.cell(200, 6, txt=divider, ln=10, align="C")

    # my_pdf.multi_cell(60, 6, txt=Einfo, align="R")
    my_pdf.cell(10, 10, txt=" ", align="C", border=0)
    my_pdf.cell(60, 6, txt=f"Employee Name: {var.employee_name}", align="L", border=0)
    my_pdf.ln()
    my_pdf.cell(10, 10, txt=" ", align="C", border=0)
    my_pdf.cell(60,6, txt=f"Date: {var.transaction_date}", align="L", border=0)
    my_pdf.ln()
    my_pdf.cell(10, 10, txt=" ", align="C", border=0)
    my_pdf.cell(60, 6, txt=f"Transaction ID: {transaction_id}", align="L", border=0)
    my_pdf.ln()

    my_pdf.cell(200, 6, txt="  ", ln=13, align="L")
    my_pdf.set_font("Arial", size=17, style='B')

    my_pdf.cell(10, 10, txt=" ", align="C", border=0)
    my_pdf.cell(80, 10, txt="Item Name", align="L", border=0)
    my_pdf.cell(40, 10, txt="Amount", align="L", border=0)
    my_pdf.cell(20, 10, txt="Qty ", align="L", border=0)
    my_pdf.cell(20, 10, txt="Subtotal", align="L", border=0)
    my_pdf.ln()

    my_pdf.set_font("Arial", size=14)
    for transaction in transactions_list:
            my_pdf.cell(10, 10, txt=" ", align="C", border=0)
            my_pdf.cell(80,10,txt=transaction[0],align="L",border=0)
            my_pdf.cell(40, 10, txt=f"{transaction[1]}.00", align="L", border=0)
            my_pdf.cell(20, 10, txt=transaction[2], align="L", border=0)
            my_pdf.cell(20, 10, txt=f"{transaction[3]}.00", align="L", border=0)
            my_pdf.ln()
    # my_pdf.multi_cell(200, 6, txt=multi_line, align="C")
    my_pdf.multi_cell(200, 6, txt=space, align="C")
    my_pdf.multi_cell(200, 6, txt=space, align="C")
    my_pdf.cell(10, 10, txt=" ", align="C", border=0)
    my_pdf.set_font("Arial", size=17,style='B')
    my_pdf.cell(60, 10, txt="______________________________________________________",  align="L",border=0)
    my_pdf.ln()
    my_pdf.cell(130, 10, txt=" ", align="C", border=0)
    my_pdf.cell(30, 6, txt=f"Total: {var.get_total():,}.00", border=0, align="L")
    my_pdf.set_font("Arial", size=17)
    my_pdf.ln()
    my_pdf.cell(130, 10, txt=" ", align="C", border=0)
    my_pdf.cell(30, 6, txt=f"Amount Paid: {int(var.amount_paid):,}.00", border=0, align="L")
    my_pdf.ln()
    my_pdf.cell(130, 10, txt=" ", align="C", border=0)
    my_pdf.cell(30, 6, txt=f"Change: {var.change}.00", border=0, align="L")
    my_pdf.ln()

    my_pdf.cell(200, 6, txt="  ", ln=13, align="L")
    # my_pdf.multi_cell(60, 6, txt=Cinfo, align="R")
    my_pdf.cell(10, 10, txt=" ", align="C", border=0)
    my_pdf.cell(60, 6, txt="Sold To", align="L", border=0)
    my_pdf.ln()
    my_pdf.cell(10, 10, txt=" ", align="C", border=0)
    my_pdf.cell(60, 6, txt=f"Customer Name: {var.customer_name}", align="L", border=0)
    my_pdf.ln()
    my_pdf.cell(10, 10, txt=" ", align="C", border=0)
    my_pdf.cell(60, 6, txt=f"Address: {var.customer_address}", align="L", border=0)
    my_pdf.ln()
    my_pdf.cell(200, 6, txt=divider, ln=19, align="C")
    my_pdf.cell(200, 6, txt=TY, ln=20, align="C")
    my_pdf.cell(200, 6, txt=divider, ln=21, align="C")
    receipt_num = transaction_id[3:]
    my_pdf.output(f"receipts/official_receipt{receipt_num}.pdf")
    images = convert_from_path(f'receipts/official_receipt{receipt_num}.pdf',500,poppler_path=r'C:\Program Files\Release-24.02.0-0\poppler-24.02.0\Library\bin')
    img_name=f"receipt_image{receipt_num}.jpg"
    images[0].save(f"static/{img_name}","JPEG")
    return img_name


@app.route('/checkout',methods=['POST'])
def checkout():
    transaction_list=[]
    list2=[]                                    #List for Receipt
    partial_total = 0
    #BUY
    for v_id in buy_qty_Dict:
        dBase_cursor.execute(f"select Vehicle_Make,Vehicle_Model,Buy_Price from vehicle_info where Vehicle_ID='{v_id}'")
        car_row = dBase_cursor.fetchone()
        buy_price_Dict[v_id] = buy_qty_Dict[v_id] * int(car_row[2])
        partial_total = partial_total + buy_price_Dict[v_id]
        price = f"{buy_price_Dict[v_id]:,}"
        buylist=[f"B{v_id}",var.customer_id,var.transaction_date,var.employee_name,buy_price_Dict[v_id]]
        transaction_list.append(buylist)
            # T_id -  -Customer_id  - transaction date  -employee name - subtotal
        list2.append([f"{car_row[0]} {car_row[1]} (BUY)",f"Php {int(car_row[2]):,}",f"{buy_qty_Dict[v_id]}",f"{buy_price_Dict[v_id]:,}"])
            # Item mane     -   Amount      -       Qty     -       Subtotal
    # RENT
    for v_id in rent_qty_Dict:
        dBase_cursor.execute(f"select Vehicle_Make,Vehicle_Model,Rent_Price from vehicle_info where Vehicle_ID='{v_id}'")
        car_row = dBase_cursor.fetchone()
        rent_price_Dict[v_id] = rent_qty_Dict[v_id] * int(car_row[2])
        partial_total = partial_total + rent_price_Dict[v_id]
        price = f"{rent_price_Dict[v_id]:,}"
        #rentlist = ["RENT", var.customer_id, v_id, var.transaction_date, rent_qty_Dict[v_id], rent_price_Dict[v_id]]
        rentlist = [f"R{v_id}", var.customer_id, var.transaction_date,var.employee_name,rent_price_Dict[v_id]]
        transaction_list.append(rentlist)
        list2.append([f"{car_row[0]} {car_row[1]} (RENT)", f"Php {int(car_row[2]):,}", f"{rent_qty_Dict[v_id]}", f"{rent_price_Dict[v_id]:,}"])

    # SERVICES
    print(services_qty_Dict)
    for m_id in services_qty_Dict:
        try:
            dBase_cursor.execute( f"select    maintenance_Name,maintenance_Price from maintenance_services where maintenance_ID='{m_id}'")
        except Exception as e:
            print("2Error: ", e)
        car_row = dBase_cursor.fetchone()
        services_price_Dict[m_id] = services_qty_Dict[m_id] * int(car_row[1])
        partial_total = partial_total + services_price_Dict[m_id]
        price = f"{services_price_Dict[m_id]:,}"  # Put comma in Money every 3 digits
        #servicelist = ["Service", var.customer_id, m_id, var.transaction_date, services_qty_Dict[m_id], services_price_Dict[m_id]]
        servicelist = [f"S{m_id}", var.customer_id, var.transaction_date, var.employee_name, services_price_Dict[m_id]]
        transaction_list.append(servicelist)
        list2.append([f"{car_row[0]} (Service)", f"{int(car_row[1]):,}", f"{services_qty_Dict[m_id]}", f"{services_price_Dict[m_id]:,}"])

    dBase_cursor.execute("SELECT Transaction_ID FROM transaction ORDER BY Transaction_ID DESC ")
    first_row = dBase_cursor.fetchone()
    if first_row is None:
        t_id = "T_01"
    else:
        t_id =f"{first_row[0][:3]}{int(first_row[0][2:])+1}"

    print(transaction_list)
    for list in transaction_list:
        dBase_cursor.execute(f"INSERT INTO transaction (Transaction_ID,Item_Code, Customer_ID, Transaction_Date, Employee_Name,Subtotal) VALUES ('{t_id}','{list[0]}', '{list[1]}', '{list[2]}', '{list[3]}',{list[4]})")
        connection.commit()
        print(list)
    # var.transactions=transaction_list.copy()
    img_name = receipt(list2,t_id)
    buy_qty_Dict.clear()
    rent_qty_Dict.clear()
    services_qty_Dict.clear()
    return jsonify({'None':"none",'img_file':img_name})

@app.route('/database')                                 # Transaction history
def database():
    if var.filter_date == "//":
        print("yes")
        dBase_cursor.execute(f"select * from transaction ORDER BY Transaction_ID DESC")
        all_transac = dBase_cursor.fetchall()
    else:
        print("no")
        dBase_cursor.execute(f"select * from transaction where Transaction_Date='{var.filter_date}' ORDER BY Transaction_ID DESC")
        all_transac = dBase_cursor.fetchall()

    transac_dict = [{'t_id':t_id,'i_code':i_code,'c_id':c_id,'t_date':t_date,'emp_name':emp_name,'subtotal':f"Php {int(subtotal):,}"}for(t_id,i_code,c_id,t_date,emp_name,subtotal)in all_transac]
    var.filter_date="//"
    return render_template('fg_THistory.html',transactions=transac_dict)

@app.route('/filter_history',methods=['POST'])
def filter_history():
        date = request.form.get('date')
        date=date[8:]+"/"+date[5:7]+"/"+date[0:4]
        var.filter_date=date
        print(date)
        dBase_cursor.execute(f"select * from transaction where Transaction_Date='{var.filter_date}' ORDER BY Transaction_ID DESC")
        all_transac = dBase_cursor.fetchall()
        if all_transac:
            return jsonify({'exist': True})
        else:
            return jsonify({'exist': False})



@app.route('/')
def first():
    return render_template('fg_UserLogin.html')
# ------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/employees')
def employees():
    dBase_cursor.execute(f"select * from employee")
    all_employee = dBase_cursor.fetchall()
    emp_dict  = [{'e_id':e_id,'e_name':e_name,'e_pass':e_pass,'add':add,'contact':contact}for(e_id,e_name,e_pass,add,contact) in all_employee]
    return render_template('fg_EProfile.html',emp_list=emp_dict)


@app.route('/delete_data',methods=['POST'])
def delete_data():
    checkedList = request.form.getlist('checkedList[]')
    for item in checkedList:
        print(type(item))
        print(item)
        dBase_cursor.execute("DELETE FROM employee WHERE Employee_ID=?", (item,))
        dBase_cursor.commit()
    return jsonify({'nodata':"nodata"})

@app.route('/edit_data',methods=['POST'])
def edit_data():
    checkedData = request.form.get('checkedData')
    newPass = request.form.get('newPass')
    print(checkedData,"   ",newPass)
    dBase_cursor.execute(f"UPDATE employee set Employee_Pass='{newPass}' where Employee_ID='{checkedData}'")
    dBase_cursor.commit()
    return jsonify({'nodata':"nodata"})

@app.route('/add_data',methods=['POST'])
def add_data():
    name = request.form.get('name')
    id = request.form.get('id')
    password = request.form.get('pass')
    add = request.form.get('add')
    contact = request.form.get('contact')
    print(id)

    dBase_cursor.execute(f"INSERT INTO employee(Employee_ID,Employee_Name,Employee_Pass,Address,Contact) VAlUES ('{id}','{name}','{password}','{add}','{contact}')")
    dBase_cursor.commit()
    return jsonify({'nodata':"nodata"})

# ----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/login',methods=['POST'])
def login():
    emp_id = request.form.get('emp_id')
    password = request.form.get('pass')
    if request.method == 'POST':
        print("SUCCESSSSS")
    else:
        print("Failed")
    dBase_cursor.execute(f"select Employee_Name from employee where Employee_ID='{emp_id}' AND Employee_Pass='{password}'")
    exists = dBase_cursor.fetchone()
    if exists:
        var.employee_name = exists[0]
        print(var.employee_name)
        return jsonify({'isSuccess':True,'redirect_to':'/home'})
    elif emp_id=="admin" and password=="admin123":
        return jsonify({'isSuccess': True,'redirect_to':'/employees'})
    else:
        return jsonify({'isSuccess': False})



@app.route('/home')
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

    var.customer_name = name
    var.customer_address = address
    dBase_cursor.execute(f"SELECT COUNT(*) FROM customer_profile")                                                    # To know the number of rows
    row_count = dBase_cursor.fetchone()[0]                                                                         #

    var.customer_id=f"CID{row_count}"
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

# ---------------------------------------------------------------------------------------------------------------------------------
# Getting values from javascript
@app.route('/test',methods=['POST','GET'])
def test():
    output = request.get_json()
    if request.method == 'POST':
        output = request.get_json()
        amt_Stack.append(output)
        print("AFTER:", amt_Stack, " SIZE: ", len(amt_Stack))

        total = var.get_total()  # ito yung ieedit sa db
        try:  # check if stack is empty
            amt_p = int(amt_Stack.pop())
        except Exception as e:
            amt_p = 0

        if amt_p >= total:
            change = f"{(amt_p - total):,}"
        else:
            change = "Insufficient amount "

        if total == 0:
            amt_p = " "
            total = " "
            change = " "
        print(total, ' : ', amt_p, ' : ', change)
        var.amount_paid = amt_p
        total=f" Php {total:,}"
        var.change=change
        return jsonify({"redirect_url": "/compute",'total':total, 'change':change})


# ---------------------------------------------------------------------------------------------------------------------------------
@app.route('/buy')
def buy():
    if buy_qty_Dict=={} and rent_qty_Dict=={} and services_qty_Dict=={}:
        return render_template('fg_STBuy1.html')
    else:
        return render_template('fg_STBuy1.html',transcript=var.result,total=f" Php  {var.get_total():,}",placeholder="Enter_Amount")
    # data = request.json  # Get JSON data from the request body
    # amt_paid = data.get('amt_paid')  # Extract the 'amt_paid' value
    # print("Received amt_paid from JavaScript:", amt_paid)
    # # You can process the 'amt_paid' value here as needed
    # return jsonify({'message': 'Data received successfully'})

    # return render_template('fg_STMenu.html',total=total,change=change)
    # ot = request.args.get('ot')  # Get the value from test()
@app.route('/rent')
def rent():
    if buy_qty_Dict == {} and rent_qty_Dict == {} and services_qty_Dict == {}:
        return render_template('fg_STRent1.html')
    else:
        return render_template('fg_STRent1.html', transcript=var.result,total=f" Php  {var.get_total():,}",placeholder="Enter_Amount")

@app.route('/services')
def services():
    var.custom_code = dBase_cursor.execute(f"SELECT COUNT(*) FROM maintenance_services").fetchone()[0]  # initializing, this will be used in /transaction
    if buy_qty_Dict == {} and rent_qty_Dict == {} and services_qty_Dict == {}:
        return render_template('fg_STServices1.html')
    else:
        return render_template('fg_STServices1.html', transcript=var.result,total=f" Php  {var.get_total():,}",placeholder="Enter_Amount")



 # ---------------------------------------------------------------------------------------------------------------------------------


                # Condier tanggalin yung '/buy/' pati sa HTML if may nagugulo sa process
@app.route('/buy/toyota')
def toyota_buy():
    if buy_qty_Dict == {} and rent_qty_Dict == {} and services_qty_Dict == {}:
        return render_template('fg_BToyota.html')
    else:
        return render_template('fg_BToyota.html', transcript=var.result,total=f" Php  {var.get_total():,}",placeholder="Enter_Amount")

@app.route('/buy/honda')
def honda_buy():
    if buy_qty_Dict == {} and rent_qty_Dict == {} and services_qty_Dict == {}:
        return render_template('fg_BHonda.html')
    else:
        return render_template('fg_BHonda.html', transcript=var.result, total=f" Php  {var.get_total():,}",placeholder="Enter_Amount")

@app.route('/buy/ford')
def ford_buy():
    if buy_qty_Dict == {} and rent_qty_Dict == {} and services_qty_Dict == {}:
        return render_template('fg_BFord.html')
    else:
        return render_template('fg_BFord.html', transcript=var.result, total=f" Php  {var.get_total():,}",placeholder="Enter_Amount")


@app.route('/rent/toyota')
def toyota_rent():
    if buy_qty_Dict == {} and rent_qty_Dict == {} and services_qty_Dict == {}:
        return render_template('fg_RToyota.html')
    else:
        return render_template('fg_RToyota.html', transcript=var.result, total=f" Php  {var.get_total():,}",placeholder="Enter_Amount")


@app.route('/rent/honda')
def honda_rent():
    if buy_qty_Dict == {} and rent_qty_Dict == {} and services_qty_Dict == {}:
        return render_template('fg_RHonda.html')
    else:
        return render_template('fg_RHonda.html', transcript=var.result, total=f" Php  {var.get_total():,}",placeholder="Enter_Amount")


@app.route('/rent/ford')
def ford_rent():
    if buy_qty_Dict == {} and rent_qty_Dict == {} and services_qty_Dict == {}:
        return render_template('fg_RFord.html')
    else:
        return render_template('fg_RFord.html', transcript=var.result, total=f" Php  {var.get_total():,}",placeholder="Enter_Amount")


# ---------------------------------------------------------------------------------------------------------------------------------
# Clear Cart
@app.route('/clear', methods=['POST'])
def clear():
    data=request.form.get('no_data')
    page_url = request.form.get('page_url')
    buy_qty_Dict.clear()
    rent_qty_Dict.clear()
    services_qty_Dict.clear()
    print(buy_qty_Dict)
    return jsonify({'redirect_url': page_url})
    #return jsonify({'no_data':"No data"})

# @app.route('/compute')
# def compute():
#     total=var.get_total()                                                 # ito yung ieedit sa db
#     try:                                                                        # check if stack is empty
#         amt_p=int(amt_Stack.pop())
#     except Exception as e:
#         amt_p=0
#
#     if amt_p>=total:
#         change = f"{amt_p-total}"
#     else:
#         change = "insuff"
#
#     if total==0:
#         amt_p=" "
#         total=" "
#         change=" "
#     print(total,' : ',amt_p,' : ',change)
#     var.amount_paid = amt_p
#     return render_template('fg_BToyota.html', total=f" Php {total:,}", change=change,placeholder=amt_p)



# ---------------------------------------------------------------------------------------------------------------------------------
@app.route('/transaction', methods=['POST'])
def transaction():
    # vehicle_id = request.form['v_id']
 # Get data from js
 # prev_data = request.form.get('divData')
 #   form_data = request.form.get('formData')

    code=request.form.get('code')
    transaction_code = code[0:1]                           # if B, R or S     -  Buy, Rent, Services
    vehicle_id = code[1:]                      #String slicing

    if '5' < code[4:5] < 'B':                                 # if code is greater than M_05
        custom_service = request.form.get('custom_service')
        price = request.form.get('custom_price')
        if custom_service == var.custom_servCheck:
            services_qty_Dict[f'NM_0{var.custom_code}'] = services_qty_Dict[f'NM_0{var.custom_code}']+1
        else:
            var.custom_code=var.custom_code+1
            try:
                dBase_cursor.execute(f"INSERT INTO maintenance_services  (maintenance_ID, maintenance_Name, maintenance_Price) VALUES ('NM_0{var.custom_code}', '{custom_service}', '{price}')")
            except Exception as e:
                print("3Error: ",e)
            connection.commit()
            services_qty_Dict[f'NM_0{var.custom_code}'] = 1
            var.custom_servCheck = custom_service

    elif transaction_code=="B":
        if vehicle_id in buy_qty_Dict:
            buy_qty_Dict[vehicle_id] = buy_qty_Dict[vehicle_id] + 1
        else:
            buy_qty_Dict[vehicle_id] = 1
    elif transaction_code=="R":
        if vehicle_id in rent_qty_Dict:
            rent_qty_Dict[vehicle_id] = rent_qty_Dict[vehicle_id] + 1
        else:
            rent_qty_Dict[vehicle_id] = 1
    elif transaction_code=="S":
        if vehicle_id in services_qty_Dict:
            services_qty_Dict[vehicle_id] = services_qty_Dict[vehicle_id] + 1
        else:
            services_qty_Dict[vehicle_id] = 1


    var.result=display_transactions()
    enter_value = "Enter_Amount"
    return jsonify({'result':var.result,'total':f" Php {var.get_total():,}",'enter_value':enter_value})
    #Sends a dictionary

# ---------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    # app.run(debug=True)
    serve(app,host='0.0.0.0',port=50100,threads=2)
    #main()
