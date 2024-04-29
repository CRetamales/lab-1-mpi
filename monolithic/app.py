'''
Laboratorio 1 - MPI
Sistemas Distribuidos
Profesor: Manuel Ignacio Manríquez
Ayudante: Ariel Madariaga
Nombres: Carlos Retamales (19.839.974-4); David Valero (20.636.919-1)
Solution: Monolithic
'''
#------------------------- Import
import pandas as pd
from flask import Flask, request, jsonify, render_template, Response
from concurrent.futures import ThreadPoolExecutor
import os
#from pathlib import Path
from database import Database
import time # For testing purposes

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
Function to calculate the statistics of the data.
Input: data as <class 'pandas.core.frame.DataFrame'> with the data.
Output: <class 'pandas.core.frame.DataFrame'> with the results of the data processing.
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
    file = request.files['file']
    if not file:
        return "Archivo no encontrado", 400
    try:
        data = pd.read_csv(file, names=["station", "temperature"], sep=';')
        results = process_data_with_thread(data)
        for _, row in results.iterrows():
            db.insert_data(row['station'], row['min'], row['max'], row['mean'])
        return "Datos procesados exitosamente", 200
    except Exception as e:
        return str(e), 500


"""
Function to save the time of the test
Input: time as <class 'float'> with the time of the test.
Output: Nothing
"""
def save_test(time):
    #Save the time in a file 'time.csv'
    with open('time.csv', 'a') as f:
        f.write(str(time) + '\n')
    


"""
This function is the one that will be executed when the user wants to see the results of the data processing, using threads.
Input: data as <class 'pandas.core.frame.DataFrame'> with the data.
Output: <class 'pandas.core.frame.DataFrame'> with the results of the data processing.
"""
def process_data_with_thread(data):
    #Time initialization
    start_time = time.time()
    num_hilos = 4
    chunk_size = len(data) // num_hilos + 1
    chunks = [data.iloc[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    with ThreadPoolExecutor(max_workers=num_hilos) as executor:
        results = list(executor.map(calculate_statistics, chunks))
    final_result = pd.concat(results)
    final_result = final_result.groupby('station').agg({'min': 'min', 'max': 'max', 'mean': 'mean'}).round(1).reset_index()
    #Time finalization
    elapsed_time = time.time() - start_time
    print("Elapsed time: ", elapsed_time)
    #save_test(elapsed_time)
    return final_result


"""
This function is the one that will be executed when the user wants to see the results of the data processing, without using threads.
Input: data as <class 'pandas.core.frame.DataFrame'> with the data.
Output: <class 'pandas.core.frame.DataFrame'> with the results of the data processing.
"""
def process_data(data):
    return data.groupby('station')['temperature'].agg(['min', 'max', 'mean']).reset_index()


"""
This function gives the user the option to save the results of the data processing in a file.
Input: Nothing
Output: Response(csv, mimetype="text/csv", headers={"Content-disposition": "attachment; filename=temperature_data" + str(pd.Timestamp.now()) + ".csv"})
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
This function is the one that will be executed when the user wants to see the results of the data processing.
Input: Nothing
Output: jsonify(data) as <class 'dict'> with the results of the data processing.
"""
@app.route('/results', methods=['GET'])
def get_results():
    try:
        data = db.fetch_data()
        return jsonify(data)
    except Exception as e:
        return str(e), 500

#------------------------- Main
def main():
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()