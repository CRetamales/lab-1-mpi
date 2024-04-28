'''
Laboratorio 1 - MPI
Sistemas Distribuidos
Profesor: Manuel Ignacio Manríquez
Ayudante: Ariel Madariaga
Nombres: Carlos Retamales (19.839.974-4); David Valero (20.636.919-1)
Solution: Services
'''
#------------------------- Import
import pandas as pd
from flask import Flask, request, jsonify, render_template, Response
from concurrent.futures import ThreadPoolExecutor
from database import Database
from mpi4py import MPI
import numpy

#------------------------- Const
app = Flask(__name__)
db = Database(dbname='dis2', user='postgres', password='postgres', host='localhost', port='5432')
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

"""
Function to calculate the statistics of the data
Input: data (DataFrame)
Output: DataFrame with the statistics of the data
"""
def calculate_statistics(data):
    return data.groupby('station')['temperature'].agg(['min', 'max', 'mean']).reset_index()

"""
Function to distribute the data to the different processes
Input: data (DataFrame)
Output: DataFrame with the statistics of the data
"""
def distribute_data(data):
    try:
        if rank == 0:
            chunks = numpy.array_split(data, size)
            for i in range(1, size):
                comm.send(chunks[i].to_dict('records'), dest=i, tag=11)
            master_results = calculate_statistics(chunks[0])
            results = [master_results]
            for i in range(1, size):
                result = comm.recv(source=i, tag=12)
                results.append(pd.DataFrame(result))
            final_result = pd.concat(results)
            return final_result
        else:
            data_chunk = comm.recv(source=0, tag=11)
            processed_data = calculate_statistics(pd.DataFrame(data_chunk))
            comm.send(processed_data.to_dict('records'), dest=0, tag=12)
    except Exception as e:
        print(f"Error en el proceso {rank}: {str(e)}")

"""
Function to start the Flask application
Input: None
Output: None
"""
@app.route('/')
def index():
    return render_template('index.html')

"""
Function to upload the data to the application
Input: None
Output: None
"""
@app.route('/upload', methods=['POST'])
def upload_data():
    file = request.files['file']
    if not file:
        return "Archivo no encontrado", 400
    try:
        data = pd.read_csv(file, names=["station", "temperature"], sep=';')
        if rank == 0:
            results = distribute_data(data)
            for _, row in results.iterrows():
                db.insert_data(row['station'], row['min'], row['max'], row['mean'])
            return "Datos procesados correctamente", 200
        else:
            return "Proceso no maestro, espera datos", 200
    except Exception as e:
        return str(e), 500

"""
Function to get the results of the data
Input: None
Output: JSON with the results of the data
"""
@app.route('/results', methods=['GET'])
def get_results():
    try:
        data = db.fetch_data() 
        return jsonify(data)
    except Exception as e:
        return str(e), 500

"""
Function to save the data to a CSV file
Input: None
Output: CSV file with the data
"""
@app.route('/save', methods=['GET'])
def save_data():
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

"""
Function to start the application
Input: None
Output: None
"""
def main():
    if rank == 0:
        app.run(debug=True, port=5000)

if __name__ == "__main__":
    main()