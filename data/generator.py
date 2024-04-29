import numpy as np
import pandas as pd

def generate_station_data(num_samples):
    station_names = ['Station' + str(i) for i in range(1, 51)]  
    random_stations = np.random.choice(station_names, num_samples) 
    random_temperatures = np.round(np.random.uniform(5.0, 40.0, num_samples), 2)
    data_frame = pd.DataFrame({
        'Station': random_stations,
        'Temperature': random_temperatures
    })
    return data_frame

def save_in_chunks(data_frame, file_path, chunk_size=500):
    with open(file_path, 'w', newline='') as f: 
        for i in range(0, len(data_frame), chunk_size):
            if i == 0:
                data_frame.iloc[i:i+chunk_size].to_csv(f, index=False, sep=';', header=False, mode='w')
            else:
                data_frame.iloc[i:i+chunk_size].to_csv(f, index=False, sep=';', header=False, mode='a')

sizes = [500,5000,50000,500000,5000000,50000000]

for size in sizes:
    data = generate_station_data(size)
    file_name = f'data_{size}.csv'
    save_in_chunks(data, file_name, chunk_size=500) 

print("Archivos generados exitosamente")
