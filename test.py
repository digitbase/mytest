import os
import sys
from modbus_tk import modbus_tcp
import telnetlib
import mysql.connector
import config


st=['~','#','@','#','$','%','^','&','*','_','-','+','\\']
def prm(a,p=0):
    prf(a, 'a')
    
    print(type(a),end='\n\n')
    
    if type(a) == list:
        for row in a:
            print(row,'\n')
    else :
        print('  =>> ',(a))
    if p>0:
        s=st[p-1]*20
        print(s)


def prd(a,p=0):
    prf(a, 'w')
    prm(a,p)
    print('======= prd end =========')
    os._exit(0)
    

def prf(a, type='w') :
    fileName='res.html'
    if type == 'w':
        with open(fileName,'w') as file:
                file.write(str(a))
    else :
        with open(fileName,'a') as file:
            file.write(str(a))

def main():
    cursor = None
    cnx = None
    try:
        cnx = mysql.connector.connect(**config.myems_system_db)
        cursor = cnx.cursor()

        query = (" SELECT version "
                 " FROM tbl_versions  "
                 " WHERE id = 1 ")
        cursor.execute(query)
        row = cursor.fetchone()
        if row is not None and len(row) > 0:
            print("The database version is : ", str(row[0]))
    except Exception as e:
        print("There is something wrong with database :", str(e))
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()



if __name__ == "__main__":
    main()
