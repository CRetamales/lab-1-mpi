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
from database import Database
import numpy

#------------------------- Const
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
db = Database(dbname='dis3', user='postgres', password='postgres', host='localhost', port='5432')

#------------------------- Functions

"""
This function is the one that will be executed when the user wants to upload a file with the data to be processed.
Input: Nothing
Output: Nothing
"""
def process_data(data_chunk):
    return data_chunk.groupby('station')['temperature'].agg(['min', 'max', 'mean']).reset_index()

"""
This function is the one that will be executed when the user wants to upload a file with the data to be processed.
Input: event_type as <class 'str'> with the type of event, data as <class 'dict'> with the data of the event.
Output: Nothing
"""
def handle_event(event_type, data=None):
    if event_type == 'DataUploaded':
        if rank == 0:
            filepath = data
            full_data = pd.read_csv(filepath, names=["station", "temperature"], sep=';')
            chunks = numpy.array_split(full_data, size)
            # Send data chunks to workers
            for i in range(1, size):
                comm.send({'type': 'ProcessData', 'data': chunks[i].to_dict('records')}, dest=i, tag=11)
            # Process own chunk
            master_results = process_data(chunks[0])
            results = [master_results]
            # Collect results
            for i in range(1, size):
                event = comm.recv(source=i, tag=12)
                results.append(pd.DataFrame(event['data']))
            final_result = pd.concat(results)
            # Insert into database
            for _, row in final_result.iterrows():
                db.insert_data(row['station'], row['min'], row['max'], row['mean'])
        else:
            event = comm.recv(source=0, tag=11)
            if event['type'] == 'ProcessData':
                processed_data = process_data(pd.DataFrame(event['data']))
                comm.send({'type': 'DataProcessed', 'data': processed_data.to_dict('records')}, dest=0, tag=12)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        handle_event('DataUploaded', sys.argv[1])
