#Bibliotecas
from utils.transform_data import process_data
from utils import entregador_data as ed

RAW_DATA_PATH = f"./dataset/train.csv"

def main():

    df = process_data(RAW_DATA_PATH)

    selected_traffic_density, values = ed.create_sidebar(df)

    linhas = df['road_traffic_density'].isin(selected_traffic_density)
    df = df.loc[linhas, :]

    linhas = df['order_date'] < values
    df = df.loc[linhas, :]
    
    ed.create_home(df)

    return None


if __name__ == "__main__":
    main()