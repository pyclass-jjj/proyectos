import pandas as pd
from os import path
from datetime import datetime, timedelta

class COVID:

    def __init__(self):
        self.descarga_datos()
        self.get_estado()
        #self.grafica_matplot()
        self.grafica_plotly()

    def descarga_datos(self):

        hoy = datetime.now() - timedelta(1)
        fecha = hoy.strftime("%Y%m%d")
        file_confirmados = f'Casos_Diarios_Estado_Nacional_Confirmados_{fecha}.csv'
        file_defunciones = f'Casos_Diarios_Estado_Nacional_Defunciones_{fecha}.csv'
        url1 = f'https://datos.covid-19.conacyt.mx/Downloads/Files/{file_confirmados}'
        url2 = f'https://datos.covid-19.conacyt.mx/Downloads/Files/{file_defunciones}'
        print(url1)

        if not path.exists(file_confirmados):
            df = pd.read_csv(url1)
            df.to_csv(file_confirmados)
            print(f'Archivo {file_confirmados} descargado')
            df = pd.read_csv(url2)
            df.to_csv(file_defunciones)
            print(f'Archivo {file_defunciones} descargado')
        else:
            print('Archivos previamente descargados')

        self.df_conf = pd.read_csv(file_confirmados, parse_dates=True)
        self.df_def  = pd.read_csv(file_defunciones, parse_dates=True)

    def get_estado(self):
        estados = list(self.df_conf['nombre'])
        print(estados)
        estado = input('Seleccione un estado o Nacional (default Nacional): ')

        if estado is None or estado == '':
            self.estado = 'Nacional'
        else:
            self.estado = estado.upper()

        df_filtered_conf = self.df_conf.query(f"nombre == '{self.estado}'")
        self.data_conf = df_filtered_conf.sum()[4:]

        df_filtered_def = self.df_def.query(f"nombre == '{self.estado}'")
        self.data_def = df_filtered_def.sum()[4:]

    def grafica_plotly(self):
        pd.options.plotting.backend = "plotly"
        data1 = self.data_conf
        data2 = self.data_def
        data = pd.concat([data1, data2], axis=1)
        fig = data.plot(title=f'Contagios COVID-19 ({self.estado})', template="simple_white", labels=dict(index="Fecha", value="Cantidad", variable=""))
        fig.data[0].name = 'Contagios'
        fig.data[1].name = 'Defunciones'
        fig.show()

    def grafica_matplot(self):
        import matplotlib.pyplot as plt
        data1 = self.data_conf
        data2 = self.data_def

        plt.title(f'Contagios COVID-19 ({self.estado})')
        plt.xlabel(f'Fecha')
        plt.rc('xtick', labelsize=8)
        plt.xticks(fontsize=6)
        plt.xticks(rotation=70)
        plt.grid(True)
        plt.ticklabel_format(useOffset=False)
        ax = data1.plot()
        data2.plot(ax=ax)
        plt.show()

covid = COVID()
