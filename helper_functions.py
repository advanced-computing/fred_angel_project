

def continent_filter(countries: pd.Series):
    
    #This list also captures regions specified by UN (i.e. East Asia or Carribean)
    continents = ['Africa', 'Asia', 'America', 'Ocreania', 'Europe', 'Carribean', 
                  'Total, all countries or areas']
    
    #Returns what is not in continents list (i.e. countries)
    return countries.loc[~countries.isin(continents)]
    

    