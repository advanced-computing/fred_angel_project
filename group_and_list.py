import pandas as pd
import os

def load_data():
    '''
    This function loads un_data
    formats columns for later use
    adds column names for empty values
    '''
    
    # absolute path
    file_path = os.path.join(os.getcwd(), "un_data.csv")

    data = pd.read_csv(file_path, 
                       encoding="ISO-8859-1", skiprows = 1, header = 0)
    

    
    data = data.rename(columns={"Region/Country/Area": "Region Code","Unnamed: 1": "Region"})
    
    return data
    
    #Validation
    print(data.columns)
    print(data.head(100))


load_data()