import pyodbc

msa_drivers = [x for x in pyodbc.drivers() if 'ACCESS' in x.upper()]
print(f'MSA DRIVERS: {msa_drivers}')

try:
    con_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\jmbal\PycharmProjects\templates\myDB.accdb;'
    conn = pyodbc.connect(con_str)
    print('SUCCESSFUL CONNECTION')

except pyodbc.Error as e:
    print('CONNECTION ERROR: ',e)

dBase_cursor =  conn.cursor()