import pandas as pd
from path_ import *
import numpy as np
import datetime

class DataManager:
    """
    """
    def __init__(self):
        self.df=pd.read_csv(abs_path+"dataset_SCL.csv", sep=',')

    
    def format(self):
        new = self.df["Fecha-I"].str.split(" ", n = 1, expand = True)
        # self.df["Fecha-I"]= new[0]# making separate first name column from new data frame
        # self.df["Hora-I"]= new[1]# making separate last name column from new data frame
        # new = self.df["Fecha-O"].str.split(" ", n = 1, expand = True)
        # self.df["Fecha-O"]= new[0]
        # self.df["Hora-O"]= new[1]
        # self.delay_df=self.df[["Fecha-I","Hora-I","Fecha-O","Hora-O"]]


