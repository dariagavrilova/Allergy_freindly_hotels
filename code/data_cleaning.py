import pandas as pd
import re

bcn = pd.read_csv('data/barcelona_data.csv')
amst = pd.read_csv('data/amsterdam_data.csv')
lis = pd.read_csv('data/lisbon_data.csv')
prs = pd.read_csv('data/paris_data.csv')
rome = pd.read_csv('data/rome_data.csv')


def data_cleaning(data):
    data.drop(data[data['Price'] == '€\xa0666666'].index, inplace=True)
    data.drop(data[data['Pets'] == '0'].index, inplace=True)
    bcn_list = data['Pets'].tolist()
    symbol = '\n'
    bcn_list_clean = [item.translate(symbol).strip() for item in bcn_list]
    data.drop(['Pets'], axis=1, inplace=True)
    data['Pets'] = bcn_list_clean
    data.drop(['Unnamed: 0'], axis=1, inplace=True)
    bcn_prices = data['Price'].tolist()
    clean_prices = []
    for i in bcn_prices:
        clean_prices.append(re.findall(r"\b[0-9]+\b", i)[0])
    data.drop(['Price'], axis=1, inplace=True)
    data['Price'] = clean_prices
    data = data[['Name', 'Score', 'Price', 'Pets', 'Link']]


data_cleaning(bcn)
data_cleaning(amst)
data_cleaning(lis)
data_cleaning(prs)
data_cleaning(rome)


bcn.insert(0, 'City', 'Barcelona')
amst.insert(0, 'City', 'Amsterdam')
lis.insert(0, 'City', 'Lisbon')
prs.insert(0, 'City', 'Paris')
rome.insert(0, 'City', 'Rome')


bcn_amst = bcn.append(amst)
bcn_amst_lis = bcn_amst.append(lis)
bcn_amst_lis_prs = bcn_amst_lis.append(prs)
appended_data = bcn_amst_lis_prs.append(rome)


# appended_data.to_csv('booking_pets_data.csv')
