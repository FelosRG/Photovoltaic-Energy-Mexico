"""
Modulo para la administración de los datos.
"""
import os
import h5py
import datetime
import numpy as np

from pathlib import Path

# Paths base
script_path = Path(os.path.realpath(__file__))
script_dir  = script_path.parent.absolute()
DIR_ROOT    = script_dir.parent.absolute()

# Paths programas
PATH_DATOS = str(DIR_ROOT / "Data" / "data.h5")

class Datos:
    def __init__(self,array):
        self.temp = array[:,0]
        self.GHI  = array[:,1]

class DatosDiarios:
    def __init__(self,array):
        self.energia_diaria    = array[:,1]
        self.prom_temp_diaria  = array[:,0]

class DatosEstadisticos:
    def __init__(self,array):
        self.prom_energia_diaria = array[0,:,1]
        self.std_energia_diaria  = array[1,:,1]
        self.prom_temp_diaria    = array[0,:,0]


class Explorador:
    def __init__(self,):
        self.path_datos = PATH_DATOS

        # Metadatos grid
        self.mask = None
        self.x = None
        self.y = None
        self._obtener_metadatos()
        self.X , self.Y = np.meshgrid(self.x,self.y)

        self.resolucion_grid = 50

        # Obtenemos una lista de los nombres de las keys asociadas 
        # a cada uno de los 738 puntos.
        self.lista_keys = self._obtener_lista_keys()

        # Columnas según la categoría
        self.columnas_completo = ["Temperature","GHI"]
        self.columnas_diarios  = ["Temp prom","Energía"]
        self.columnas_estadisticos = ["Temp prom","Energía prom","Energía std"]

    
    def _obtener_metadatos(self,):
        with h5py.File(self.path_datos,"r") as file:
            self.mask = file["Metadatos/mask"][:]
            self.x = file["Metadatos/x"][:]
            self.y = file["Metadatos/y"][:]
    
    def _obtener_lista_keys(self,):
        lista_keys = []
        for i in range(self.resolucion_grid):
            for j in range(self.resolucion_grid):
                if self.mask[i,j]:
                    lat , lon = self.Y[i,j] , self.X[i,j]
                    key = self.obtener_key(lat,lon)
                    lista_keys.append(key)
        return lista_keys

    def extraer_datos(self,año,key):
        with h5py.File(self.path_datos,"r") as file:
            array = file[f"Datos/{año}/{key}"][:]
        objeto = Datos(array)
        return objeto

    def extraer_datos_diarios(self,año,key):
        with h5py.File(self.path_datos,"r") as file:
            array = file[f"DatosDiarios/{año}/{key}"][:]
        objeto = DatosDiarios(array)
        return objeto

    def extraer_datos_estadisticos(self,key):
        with h5py.File(self.path_datos,"r") as file:
            array = file[f"DatosEstadisticos/{key}"][:]
        objeto = DatosEstadisticos(array)
        return objeto

    def punto_cercano(self,lat,lon):
        """
        Devuelve el punto más cercano de los datos que se tiene
        """
        # Reacomodamos para usar con argmin
        Y = self.Y.reshape(-1)
        X = self.X.reshape(-1)
        mask = self.mask.reshape(-1)
        
        dif_lat = self.Y - lat
        dif_lon = self.X - lon

        idx_cercano = np.argmin(dif_lat**2 + dif_lon**2)

        # Si se ingresa una coordenada fuera del los puntos de los datos
        # entonces el punto más cercano será alguno que no esté marcado
        # por el mask, por lo que en ese caso soltamos un error.
        if mask[idx_cercano] == False: raise ValueError("Coordenada no válida!")

        lat_cercano , lon_cercano = Y[idx_cercano] , X[idx_cercano]

        return lat_cercano , lon_cercano

    def obtener_key(self,lat,lon):
        lat = str(round(lat,3))
        lon = str(round(lon,3))
        return f"{lat}__{lon}"

    def fecha2idx_completo(fecha:datetime.datetime):
        """
        Dado un objeto datetime devuelve el índice al que le
        corresponde.

        [Datos completos]
        """
        pass

    def fecha2idx_diarios(fecha:datetime.datetime):
        pass


    def lista2grid(self,lista,default=-1):
        """
        Transforma una lista de keys en un array con el
        grid.
        """

        # Se establece una cantidad por default.
        array = np.ones(shape=(self.resolucion_grid,self.resolucion_grid))*default

        # Se rellena el resto
        idx = 0
        for i in range(self.resolucion_grid):
            for j in range(self.resolucion_grid):
                if self.mask[i,j]:
                    array[i,j] = lista[idx]
                    idx += 1
    
        return array
    
    def _print_contenido(self):
        with h5py.File(self.path_datos,"r") as file:
            keys = list(file.keys())
        for key in keys:
            print(key)



if __name__ == "__main__":
    print("")
    print("----------")
    print("   TEST   ")
    print("----------")
    print("")

    admin = Explorador()
    print(admin.x)
    print(admin.y)
    print(admin.punto_cercano(20,-100))

    print("Ok")

