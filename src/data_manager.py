import pandas as pd
from path_ import *
import numpy as np
import datetime
import datetime as dt

class DataManager:
    """
    Trabaja con los csv filtrando y dando el formato necesario.

    ...

    Attributos
    ----------
    df : DataFrame
        csv entregado en el challenge para posteriormente ser filtrado y ordenado.
    df_latam : DataFrame
        Contendrá los datos solicitados por latam para el synthetic_features.csv.
    df_original : DataFrame
        csv original entregado por latam (dataset_SCL.csv).
    aux_list : list
        Lista auxiliar en la que se posicionarán elementos que se introducirán como columnas a dataframe, no debería
        ser atributo pero se hizo de esta forma por temas de debuggin.
    y_data : list
        columna ['dif_min'] del dataframe df_latam que se ocupará para entrenar el modelo.
    x_concat : 
        columnas del dataframe df_latam sin incluir y_data concatenadas como texto con sus elementos separados por
        un espacio, esta es la 'columna de ordenadas' que se le entrega al modelo.
    

    Methods
    -------
    __splitter()
        Separa columnas.
    format()
        Aplica el metodo __splitter() para dar un formato util a los datos.
    latam_petitions(maxprod='fixed')
        genera el Dataframe que se exportara como synthetic_features.csv
    pre_processing()
        Da el formato correcto y extrae los datos necesarios para entrenar el modelo.


    """
    def __init__(self):
        self.df=pd.read_csv(abs_path+"dataset_SCL.csv", sep=',')
        self.df_latam = pd.DataFrame()
        self.df_original = self.df.copy(deep=True)

    def __splitter(self, to_split, n, splited=[], sep=' ', typ = ''):
        new = self.df[to_split].str.split(sep, n = n, expand = True)
        for i in range(n+1):
            if typ == 'int':
                self.df[splited[i]]=list(map(int,new[i]))
            elif typ == 'str':
                self.df[splited[i]]=new[i]

    def format(self):
        self.df['dif_min']=[((dt.datetime.strptime(self.df['Fecha-O'][i], '%Y-%m-%d %H:%M:%S')-dt.datetime.strptime(self.df['Fecha-I'][i], '%Y-%m-%d %H:%M:%S')).total_seconds()/60) for i in range(len(self.df))]
        self.__splitter("Fecha-O", 1, ["Fecha-O","Hora-O"], ' ', 'str')
        self.__splitter("Fecha-I", 1, ["Fecha-I","Hora-I"], ' ', 'str')
        self.__splitter("Fecha-I", 2, ['Anno-I', 'Mes-I', 'Dia-I'], '-', 'int')
        self.__splitter("Fecha-O", 2, ['Anno-O', 'Mes-O', 'Dia-O'], '-', 'int')
        #self.df = self.df[['Vlo-I', 'Des-I', 'Emp-I', 'Vlo-O', 'Des-O', 'Emp-O', 'DIANOM', 'TIPOVUELO','dif_min',"Hora-I","Hora-O",'Anno-I','Mes-I','Dia-I','Anno-O','Mes-O','Dia-O']]#['Fecha-I', 'Vlo-I', 'Des-I', 'Emp-I', 'Fecha-O', 'Vlo-O', 'Des-O', 'Emp-O', 'DIANOM', 'TIPOVUELO','diff_[m]',"Hora-I","Hora-O",'Anno-I','Mes-I','Dia-I','Anno-O','Mes-O','Dia-O']]

    def latam_petitions(self):
        # En el metodo format se agrega la diferencia entre la hora programada y en la que realmente sucedio el vuelo.
        # Determinar si los vuelos son de temporada alta o no.
        self.df_latam = self.df_original.copy(deep=True)
        self.df_latam['dif_min'] = self.df['dif_min']
        self.aux_list = [0]*len(self.df )
        for cont in range(len(self.df )):
            if self.df .iloc[cont]['Mes-I']==12 and self.df .iloc[cont]['Dia-I']>=15:
                self.aux_list[cont] = 1
            elif self.df .iloc[cont]['Mes-I'] in [1,2,8]:
                self.aux_list[cont] = 1
            elif self.df .iloc[cont]['Mes-I']==3 and self.df .iloc[cont]['Dia-I']<=3:
                self.aux_list[cont] = 1
            elif self.df .iloc[cont]['Mes-I']==7 and self.df .iloc[cont]['Dia-I']>=15:
                self.aux_list[cont] = 1
            elif self.df .iloc[cont]['Mes-I']==9 and self.df .iloc[cont]['Dia-I']<=31:
                self.aux_list[cont] = 1
            else:
                self.aux_list[cont] = 0
        self.df_latam ['temporada_alta']=self.aux_list
        # Determinar si el atraso es mayor a 15 mins
        self.aux_list = [0]*len(self.df )
        for cont in range(len(self.df )):
            if self.df .iloc[cont]['dif_min']>15:
                self.aux_list[cont]=1
            else:
                self.aux_list[cont]=0
        self.df_latam ['atraso_15']=self.aux_list
        # Determinar periodo del dia
        self.aux_list = []
        for hr in self.df ['Hora-I']:
            hr_list = hr.split(':')
            if int(hr_list[0])>=5 and int(hr_list[0])<12:
                self.aux_list.append('mañana')
            elif int(hr_list[0])>=12 and int(hr_list[0])<19:
                self.aux_list.append('tarde')
            else:
                self.aux_list.append('noche')
        self.df_latam ['periodo_dia'] = self.aux_list
    def pre_processing(self):
        self.df = self.df[self.df['dif_min']>0]
        self.y_data = list(self.df['dif_min'])
        self.x_concat = [" ".join([str(i) for i in self.df.iloc[j]]) for j in range(len(self.df))]
    


