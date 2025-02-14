import pandas as pd

def load_data():
    '''
    This function loads un_data
    formats columns for later use
    adds column names for empty values
    '''

    data = pd.read_csv(r'fred_angel_project\un_data.csv', 
                       encoding="ISO-8859-1", skiprows = 1, header = 0)
    

    
    data = data.rename(columns={"Region/Country/Area": "Region Code","Unnamed: 1": "Region"})
    
    #Optional validation
    print(data.columns)
    print(data)


load_data()