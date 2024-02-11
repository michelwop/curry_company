import inflection
import pandas as pd

def rename_columns(dataframe):
    df = dataframe.copy()

    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")

    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))

    cols_new = list(map(snakecase, cols_old))

    df.columns = cols_new

    return df


def process_data(file_path):
    df = pd.read_csv(file_path)

    df = rename_columns(df)
    df = df.dropna()
    df = df.replace(to_replace=r'\(min\)[ ]', value='', regex=True)
    df['city'] = df['city'].str.rstrip()
    df['festival'] = df['festival'].str.rstrip()
    #df.dropna(inplace=True)
    #df.replace('NaN', pd.NA, inplace=True)
    df = df.drop_duplicates()


    #Conversoes
    # Conversao de nota para numeros float
    df['delivery_person_ratings'] = df['delivery_person_ratings'].astype( float )
    
    # Conversao de texto/categoria/string para numeros inteiros
    #df['delivery_person_age'] = df['delivery_person_age'].astype( int )
    df['time_taken(min)'] = df['time_taken(min)'].astype( int )
    
    # Conversao de texto para data
    #df['time_orderd'] = pd.to_datetime( df['time_orderd'], format='%H:%M:%S' )
    df['time_order_picked'] = pd.to_datetime( df['time_order_picked'], format='%H:%M:%S' )    
    df['order_date'] = pd.to_datetime( df['order_date'], format='%d-%m-%Y' )

    df.to_csv("./dataset/train_processed.csv", index=False)

    return df