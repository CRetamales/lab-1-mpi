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

#------------------------- Const
app = Flask(__name__)
db = Database(dbname='dis3', user='postgres', password='postgres', host='localhost', port='5432')

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
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        file_path = 'temp_data.csv'
        file.save(file_path)
        # Inicia el script MPI usando subprocess para manejar el procesamiento de datos
        subprocess.Popen(['mpiexec', '-n', '4', 'python', 'mpi_process.py', file_path])
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
        # Obtiene los datos de la base de datos
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
        # Descarga los resultados como CSV desde la base de datos
        data = db.fetch_data()
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False)
        return Response(
            csv,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=results.csv"}
        )
    except Exception as e:
        return str(e), 500

#------------------------- Main
if __name__ == '__main__':
    app.run(debug=True, port=5000)
