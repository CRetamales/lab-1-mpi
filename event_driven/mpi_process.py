'''
Laboratorio 1 - MPI
Sistemas Distribuidos
Profesor: Manuel Ignacio Manríquez
Ayudante: Ariel Madariaga
Nombres: Carlos Retamales (19.839.974-4); David Valero (20.636.919-1)
Solution: Event Driven
'''
#------------------------- Import
from mpi4py import MPI
import pandas as pd
import sys
from database import Database  # Asegúrate de que el módulo database está correctamente importado y configurado
import numpy

#------------------------- Const
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
db = Database(dbname='dis3', user='postgres', password='postgres', host='localhost', port='5432')  # Configura según tus necesidades

#------------------------- Functions

"""
This function is the one that will be executed when the user wants to see the information of the program.
Input: Nothing
Output: Nothing
"""
def process_data(data_chunk):
    return data_chunk.groupby('station')['temperature'].agg(['min', 'max', 'mean']).round(1).reset_index()

"""
This function is the main function of the program, it is the one that will be executed when the program is run.
Input: Nothing
Output: Nothing
"""
def main():
    if rank == 0:
        filepath = sys.argv[1]
        data = pd.read_csv(filepath, names=["station", "temperature"], sep=';')
        chunks = numpy.array_split(data, size)
        # Send data to other processes
        for i in range(1, size):
            comm.send(chunks[i].to_dict('records'), dest=i, tag=11)
        # Process data in the master process
        master_results = process_data(chunks[0])
        results = [master_results]
        # Receive data from other processes
        for i in range(1, size):
            result = comm.recv(source=i, tag=12)
            results.append(pd.DataFrame(result))
        # Concatenate all results
        final_result = pd.concat(results)
        # Insert data into the database
        for _, row in final_result.iterrows():
            db.insert_data(row['station'], row['min'], row['max'], row['mean'])
    else:
        data_chunk = comm.recv(source=0, tag=11)
        processed_data = process_data(pd.DataFrame(data_chunk))
        comm.send(processed_data.to_dict('records'), dest=0, tag=12)

if __name__ == '__main__':
    main()
