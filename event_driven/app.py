'''
Laboratorio 1 - MPI
Sistemas Distribuidos
Profesor: Manuel Ignacio Manríquez
Ayudante: Ariel Madariaga
Nombres: Carlos Retamales (19.839.974-4); David Valero (20.636.919-1)
Solution: Event Driven
'''
#------------------------- Import
from flask import Flask, request, jsonify, render_template, Response, redirect, url_for
import subprocess
from database import Database
import pandas as pd
import time
import os
from dotenv import load_dotenv

#------------------------- Const
load_dotenv()
db_name = os.getenv('DB_NAME', 'distributed_systems')
user = os.getenv('DB_USER', 'postgres')
password = os.getenv('DB_PASSWORD', 'postgres')
host = os.getenv('DB_HOST', 'localhost')
port = os.getenv('DB_PORT', '5432')
app = Flask(__name__)
db = Database(dbname=db_name, user=user, password=password, host=host, port=port)

#------------------------- Functions

"""
This function tis the main funcion of the program, it is the one that will be executed when the program is run.
Input: Nothing
Output: Nothing
"""
@app.route('/')
def index():
    return render_template('index.html')

"""
This function is the one that will be executed when the user wants to see the information of the program.
Input: Nothing
Output: Nothing
""" 
@app.route('/info', methods=['GET'])
def info():
    try:
        return render_template('info.html')
    except:
        return "Error al cargar la pagina"

"""
This function is the one that will be executed when the user wants to see the information of the program.
Input: Nothing
Output: Nothing
"""
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        file_path = f"temp_data_{timestamp}.csv"
        file.save(file_path)
        # Start the MPI process
        process = subprocess.Popen(['mpiexec', '-n', '4', 'python', 'mpi_event_handler.py', file_path])
        # Remove the files after processing
        #process.wait()
        #os.remove(file_path)
        return "Archivo cargado exitosamente, los resultados estarán disponibles en unos minutos."
    return "No se pudo cargar el archivo", 400

"""
This function is the one that will be executed when the user wants to see the information of the program.
Input: Nothing
Output: Nothing
"""
@app.route('/results', methods=['GET'])
def results():
    try:
        data = db.fetch_data()
        return jsonify(data)
    except Exception as e:
        return str(e), 500

"""
This function is the one that will be executed when the user wants to see the information of the program.
Input: Nothing
Output: Nothing
"""
@app.route('/save', methods=['GET'])
def download():
    try:
        data = db.fetch_data()
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False)
        return Response(
            csv,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=temperature_data" + str(pd.Timestamp.now()) + ".csv"}
        )
    except Exception as e:
        return str(e), 500

#------------------------- Main
if __name__ == '__main__':
    app.run(debug=True, port=5000)
