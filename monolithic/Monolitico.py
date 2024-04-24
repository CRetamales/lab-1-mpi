'''
Laboratorio 1 - MPI
Sistemas Distribuidos
Profesor: Manuel Ignacio Manríquez
Ayudante: Ariel Madariaga
Nombres: Carlos Retamales (19.839.974-4); David Valero (20.636.919-1)
'''
#------------------------- Import
import pandas as pd
from flask import Flask, request, jsonify, render_template
from concurrent.futures import ThreadPoolExecutor
#import os
from pathlib import Path

#------------------------- Const
filename = "data.csv"
output = "output.csv"
global_results = None
app = Flask(__name__)

#------------------------- Functions

"""
This function is the main function of the program, it is the one that will be executed when the program is run.
Input: Nothing
Output: Nothing
"""
@app.route('/', methods=['GET'])
def index():
    try: 
        return render_template('index.html')
    except:
        return "Error al cargar la pagina"
"""

"""
def calculate_statistics(data):
    return data.groupby('station')['temperature'].agg(['min', 'max', 'mean']).reset_index()


"""
This function is the one that will be executed when the user wants to upload a file with the data to be processed.
Input: Nothing
Output: Nothing
"""
@app.route('/upload', methods=['POST'])
def upload_data():
    global global_results
    file = request.files['file']
    if not file:
        return "Archivo no encontrado", 400
    try:
        data = pd.read_csv(file, names=["station", "temperature"], sep=';')
        global_results = process_data_with_thread(data)
        return "Datos procesados exitosamente", 200
    except Exception as e:
        return str(e), 500


"""
This function is the one that will be executed when the user wants to see the results of the data processing, using threads.
Input: data as <class 'pandas.core.frame.DataFrame'> with the data.
Output: <class 'pandas.core.frame.DataFrame'> with the results of the data processing.
"""
def process_data_with_thread(data):
    num_hilos = 4
    chunk_size = len(data) // num_hilos + 1
    chunks = [data.iloc[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    with ThreadPoolExecutor(max_workers=num_hilos) as executor:
        results = list(executor.map(calculate_statistics, chunks))
    final_result = pd.concat(results)
    return final_result.groupby('station').agg({'min': 'min', 'max': 'max', 'mean': 'mean'}).reset_index()

"""
This function is the one that will be executed when the user wants to see the results of the data processing, without using threads.
Input: data as <class 'pandas.core.frame.DataFrame'> with the data.
Output: <class 'pandas.core.frame.DataFrame'> with the results of the data processing.
"""
def process_data(data):
    return data.groupby('station')['temperature'].agg(['min', 'max', 'mean']).reset_index()


"""
This function to save the result in a file with .csv extension.
Input: <class 'pandas.core.frame.DataFrame'> with the data, output file path as String.
Output: write in output.csv of the results, that being "station, min temp, max temp, mean temp".
"""
def save(data,output_filepath):
    data.to_csv(output_filepath, index=False)
    print(f"Resultados guardados en {output_filepath}")


"""


"""
@app.route('/results', methods=['GET'])
def get_results():
    global global_results
    if global_results is None:
        return "No hay resultados disponibles", 404
    return global_results.to_json(orient='records')

#------------------------- Main
def main():
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()