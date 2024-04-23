'''
Laboratorio 1 - MPI
Sistemas Distribuidos
Profesor: Manuel Ignacio Manríquez
Ayudante: Ariel Madariaga
Nombres: Carlos Retamales (19.839.974-4); David Valero (20.636.919-1)
'''
#------------------------- Import
import pandas as pd
#import os
from pathlib import Path

#------------------------- Const
filename = "data.csv"
output = "output.csv"

#------------------------- Functions

"""
This function reads the data from a file .csv with the information of the stations and their respective temperature 
separated with ";".
Input: file path as String 
Output: <class 'pandas.core.frame.DataFrame'> with the data of the station and their respective temperature indented
"""
def reading(filepath=""):
    try:
        return pd.read_csv(filepath, names=["station", "temperature"], sep=";")
    except:
        print("Ocurrio un problema con el archivo o la libreria panda, por favor revise que ambos estén en orden")
    finally:
        print("(╯°□°）╯︵ ┻━┻")

"""
This function calculate the temperature minimum, maximum and mean of all stations in Dataframe
Input: <class 'pandas.core.frame.DataFrame'> with the data of the station and their respective temperature indented
Output: <class 'pandas.core.frame.DataFrame'> with the data calculated 
"""
def calculate(data):
    metrics = data.groupby('station')['temperature'].agg(['min','max','mean']).reset_index()
    metrics.columns = ['station','Min Temp','Max Temp','Mean Temp']
    return metrics

"""
This function to save the result in a file with .csv extension.
Input: <class 'pandas.core.frame.DataFrame'> with the data, output file path as String.
Output: write in output.csv of the results, that being "station, min temp, max temp, mean temp".
"""
def save(data,output_filepath):
    data.to_csv(output_filepath, index=False)
    print(f"Resultados guardados en {output_filepath}")

"""
This function acts like a menu in the console of the user, 
Input: Nothing, but during the process the menu asks the user to write un te console a number between 0 and 1. 
Output: Nothing
"""
def menu():
    while True:
        print('''
        Bienvenido al programa de calculo de temperatura por estacion, 
        por favor ingresa el numero de una de las sig. opciones:
        0.- Cerrar el programa
        1.- Calcular datos sobre la temperatura por estacion
        ''')
        try:
            choice = int(input("Ingresa el numero de tu eleccion: "))
        except ValueError:
            print("Lo ingresado no es un numero")
            continue
        except:
            print("¡ostia chaval, ha ocurrido un error inesperado!")
            continue

        if choice == 0:
            exit(0)
        elif choice == 1:
            path = Path(filename)
            data = reading(path)
            print(type(data))

            # print(data)
            metrics = calculate(data)
            print(metrics)
            print(type(metrics))

            save(metrics, output)
        else:
            print("Por favor ingresa un numero valido")


#------------------------- Main
def main():
    menu()


if __name__ == "__main__":
    main()