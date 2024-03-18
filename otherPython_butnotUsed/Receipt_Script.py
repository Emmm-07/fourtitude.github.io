from fpdf import FPDF

my_pdf=FPDF() 
my_pdf.add_page()

my_pdf.set_font("Arial",size=14)

divider = "********************************************************************************   "
title = " O F F I C I A L   R E C E I P T "
TY = " T H A N K   Y O U "
address=""" 11th Floor Room 3, Far Eastern Univeristy
Institue Of Technology , Paredes Street , Sampaloc Manila """
Einfo=""" Employee Name:
Date:
Transaction ID:
"""
Cinfo=""" Sold To
Customer Name:
Address:
"""
item_line = " Item Name                     Amount             Qty             Subtotal "
str=""
for i in range(10):
    #str+=f"{i}\n"
    str+=" Item Name                     Amount             Qty             Subtotal \n"
print(str)
multi_line=f"""

{str}

"""
my_pdf.cell(200,6,txt=" Fourtitude Garage ", ln=1, align="C")

my_pdf.cell(200,6,txt=" (Group 4) ", ln=2, align="C")

my_pdf.multi_cell(200,6, txt=address, align="C")

my_pdf.cell(200,6,txt=divider, ln=5, align="C")

my_pdf.cell(200,6,txt=title, ln=6, align="C")

my_pdf.cell(200,6,txt=divider, ln=7, align="C")


my_pdf.multi_cell(60,6, txt=Einfo, align="R")

my_pdf.cell(200,6,txt="  " , ln=10, align="L")
my_pdf.cell(200,6,txt=item_line, ln=11, align="C")

my_pdf.multi_cell(200,6, txt=multi_line, align="C")
my_pdf.cell(200,10,txt="________________________________________________", ln=14, align="C")
my_pdf.cell(200,6,txt="                                     Total: ", ln=15, align="C")
my_pdf.cell(200,6,txt="                         Amount Paid: ", ln=15, align="C")
my_pdf.cell(200,6,txt="                                Change: ", ln=15, align="C")
my_pdf.cell(200,6,txt="  " , ln=10, align="L")
my_pdf.multi_cell(60,6, txt=Cinfo, align="R")

my_pdf.cell(200,6,txt=divider, ln=16, align="C")
my_pdf.cell(200,6,txt=TY, ln=17, align="C")
my_pdf.cell(200,6,txt=divider, ln=18, align="C")



my_pdf.output("official_receipt.pdf")