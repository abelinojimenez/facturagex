#from operator import truediv
import os
#from tkinter import S
from flask import Flask,jsonify,request,send_file
from dotenv import load_dotenv
from pathlib import Path
from decimal import Decimal

load_dotenv()
from flask_bcrypt import Bcrypt
from importlib_metadata import files;
import mysql.connector;
from hashlib import md5
from time import localtime
from flask_cors import CORS
import json
from sendGridEmail import SendEmail # class for sendMessage
UPLOAD_PROFILE=os.getenv("UPLOAD_PROFILE")
UPLOAD_FOLDER=os.getenv("UPLOAD_FOLDER")
UPLOAD_DOCUMENT=os.getenv("UPLOAD_DOCUMENT")
app=Flask(__name__)
bcrypt = Bcrypt(app)

CORS(app,resources={
    r'/*':{"origins":{os.getenv("DOMAIN"),os.getenv("DOMAIN2")}}
})
def consulta(query,tuplas,type="insert"):
    try:
        connection = mysql.connector.connect(host=os.getenv("DB_HOST"),
                                                database=os.getenv("DB_NAME"),
                                                password=os.getenv("DB_PASSWORD"),
                                                user=os.getenv("DB_USER"))
            #cursor = connection.cursor(prepared=True)
        cursor= connection.cursor(prepared=True)
       
        sql_insert_query =query
        if type=="insert" or type=="update": 
            list_id=[]
            for i in range(0,len(tuplas)):
                cursor.execute(sql_insert_query,tuplas[i])
                connection.commit()
                print(cursor.rowcount)
                if type=="update":
                    list_id.append(cursor.rowcount) 
                else:
                    list_id.append(cursor.lastrowid)
            return list_id
        elif type=="select":
                cursor.execute(sql_insert_query,tuplas[0])
                #return cursor.fetchall()
                row_headers=[x[0] for x in cursor.description]
                rv = cursor.fetchall()
                payload = []
                content = {}
                for result in rv:
                    #content = {row_headers[0]: result[0], row_headers[1]: result[1], row_headers[2]: result[2]}
                    for i in range(len(row_headers)):
                        content[row_headers[i]]=result[i]
                    payload.append(content)
                    content = {}
                return payload
               
        
    except mysql.connector.Error as error:
        print("parameterized query failed {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed") 


@app.route('/facturaCabeza',methods=['POST'])
def add_facturaHead():
    #fields=json.loads(request.form)
    fields = request.form.to_dict(flat=True)

    query= """ INSERT INTO factura 
                                ( idUser, nit,clientNombre,fecha) VALUES (%s,%s,%s,%s)"""
    tuples=[(fields["idUser"],fields["nit"],fields["clientNombre"],fields["fecha"])]
    consulta(query,tuples)

    return '',204

@app.route("/facturaDetalle/<string:idFactura>")
def get_detailProfile(idFactura):
    query= """ SELECT idUser,nit,clientNombre,fecha FROM factura where idFactura=%s """ 
    tuples = [(idFactura)] 
    result=consulta(query,tuples,"select")
    return jsonify(result) 

@app.route('/facturaActualizacion',methods=['POST'])
def upadate_factura():
    #fields=json.loads(request.form)
    fields = request.form.to_dict(flat=True)
    query= """ update factura SET idUser= %s, nit= %s, clientNombre = %s, fecha= %s  where idFactura = %s """
    tuples=[(fields["idFactura"])]
    consulta(query,tuples)

    return '',204

@app.route('/facturaActualizacion',methods=['DELETE'])
def  delete_factura():
    #fields=json.loads(request.form)
    fields = request.form.to_dict(flat=True)
    query= """ Delete from factura where idFactura = %s """
    tuples=[(fields["idFactura"])]
    consulta(query,tuples)

    return '',204

@app.route("/facturaDetalle/<string:idFactura>")
def get_facturaDetalle(idFactura):
    query= """ SELECT idUser,nit,clientNombre,fecha FROM factura where idFactura = %s """ 
    tuples = [(idFactura,)] 
    result=consulta(query,tuples,"select")
    return jsonify(result) 



@app.route("/facturaCompleta/<string:idFactura>")
def get_facturaCompleta(idFactura):
    query= """ SELECT idUser,nit,clientNombre,fecha FROM factura where idFactura = %s """ 
    tuples = [(idFactura,)] 
    result=consulta(query,tuples,"select")

    query= """ SELECT productoName, cantidad, descripcion, precio, (cantidad*precio) as monto FROM detalle where idFactura = %s """ 
    tuples = [(idFactura,)] 
    result2=consulta(query,tuples,"select")

    factura={"cabeza":result[0],"detalle":result2}

    return jsonify(factura) 


if __name__ =='__main__':
    app.run(debug=True)