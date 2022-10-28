# Solar Radiation Clustering

## Instalación de requerimientos
**Instalación para cualquier plataforma: Windows, linux, MacOs**

Hay dos formas de instalar las dependencias, por anaconda y por pip. Por pip es un método más sencillo pero en este caso suele dar problemas por lo que recomiendo instalar por anaconda.

### Por anaconda
Anaconda se encargará de instalar de forma sencilla todas las dependencias en la plataforma en la que estemos.

1. Instalar  Anaconda o miniconda <br>
    Si no se tiene ya alguno de los dos, recomiendo instalar miniconda, en el siguiente link podrás encontrar el instalador que necesitas según tu plataforma: <br> 
    📌 https://docs.conda.io/en/latest/miniconda.html

2. Descargar este repositorio y descomprimir el .zip

3. Instalamos las librerías requeridas <br>
Para evitar conflictos con otras librerías crearemos un entorno por separado para el repositorio. <br>

   En una consola (o powershell en windows) abierta dentro de la carpeta del repositorio descomprimido y escribimos

    ```
    conda env create --file=environment.yml

    ```

    Este creará un entorno llamado "SRC" con las dependencias indicadas en el archivo environment.yml, para entrar
    a nuestro entorno recién creado escribimos

    ```
    canda activate SRC
    ```

    Y ya estaremos listos de empezar a usar el repositorio 🎉

    ⚠ Nota: En el caso de querer volver al entorno por defecto solo escribimos

    ```
    canda activate
    ```

### Por pip

1. Tenemos que tener descargado e instalado previamente python. <br>
📌 https://www.python.org/downloads/

2. Descargamos y descomprimimos el .zip del repositorio.

3. En una consola (o powershell en windows) en nuestro repositorio descomprimido ingresamos:

    ```
    pip install -r requeriments.txt 
    ```
Y ya estarían todas las dependecias instaladas! 🎉 <br>

⚠ La instalación de la librería geopandas suele causar problemas en algunas plataformas, si es el caso recomiendo hacer la instalación por anaconda.
