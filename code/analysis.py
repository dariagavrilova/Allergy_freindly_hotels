import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

data = pd.read_csv('../data/booking_pets_data_with_rome.csv')


data.drop(['Unnamed: 0'], axis=1, inplace=True)
data =[data['Price'] != 1]


# function to create Pets categories ( Allowed or Not allowed)
def pets_category(row):
    if row['Pets'] == 'Pets are not allowed.':
        return 'Not allowed'
    elif row['Pets'] == 'Free!\n\n\nAll pools are free of charge':
        return 'No info'
    else:
        return 'Allowed'


pets_groups = data.apply(lambda row: pets_category(row), axis=1)
data['Pets TF'] = pets_groups


# cleaning data after creating pets categories
data.drop(['Pets'],axis=1, inplace=True)
data.rename(columns={'Pets TF': 'Pets'}, inplace=True)
data = data[['City', 'Name', 'Score', 'Price', 'Pets', 'Link']]


# Choosing palette
sns.set_palette("crest")
pets_palette = {"Allowed": "C5", "No info": "C2", "Not allowed":"C0"}


# Preparing data to create Price categories
price = data.groupby(['City', 'Pets'])['Price'].mean()
price = data['Price'].tolist()
df_price = pd.DataFrame(price)
names = data['Name'].tolist()
df_price['Names'] = names
df_price.rename(columns={0: 'Price'}, inplace=True)


# function to create Price categories (Cheap, Normal, Expensive)
def price_category(row):
    if row['Price'] <= 50:
        return 'Cheap'
    elif 50 < row['Price'] <= 150:
        return 'Normal'
    elif row['Price'] > 150:
        return 'Expensive'


price_groups = df_price.apply(lambda row: price_category(row), axis=1)
data['Price Groups'] = price_groups


# cleaning data after creating pets categories
data.drop(['Pets'], axis=1, inplace=True)
data.rename(columns={'Pets TF': 'Pets'}, inplace=True)
data = data[['City', 'Name', 'Score', 'Price', 'Pets', 'Link']]


# After cleaning data contains 2367 hotels. Rome 496, Paris 495, Lisbon 472, Barcelona 467, Amsterdam 437
fig, ax = plt.subplots(figsize=(8, 8))
sns.countplot(ax=ax, x='City', data=data, palette="crest")
plt.title("Cities")
plt.xlabel("City")
plt.ylabel('Amount')


# There are 1430 hotels of the category 'Pets not allowed'
# 918 "Allowed"
# 19 there is no info about pets
fig, ax = plt.subplots(figsize=(5, 8))
sns.countplot(ax=ax, x='Pets', data=data, palette="crest")
plt.title("No pets Hotels")
plt.xlabel("Hotels")
plt.ylabel('Amount')
fig.savefig("allowed_vs_not_allowed.png")


""" Amount of hotels by city that allow and do not allow accommodation with pets
Amsterdam: Not allowed - 307, Allowed - 130
Barcelona: Not allowed - 293, Allowed - 1
Lisbon: Not allowed - 415, Allowed - 57
Paris: Not allowed - 178, Allowed - 317
Rome: Not allowed - 259, Allowed - 237
"""
city_pets = data.groupby(['City', 'Pets'])['Price'].count().reset_index()
plt.figure(figsize=(15,6))
sns.barplot(x='City', y='Price', hue='Pets', data=city_pets, palette=pets_palette)
plt.title("No pets Hotels")
plt.xlabel("Hotels")
plt.ylabel('Amount')
fig.savefig("allowed_vs_not_allowed_by_city.png")


""" % of hotels by city that allow and do not allow accommodation with pets
Amsterdam: Not allowed - 70% , Allowed - 30%
Barcelona: Not allowed - 63%, Allowed - 33%, No info - 4%
Lisbon: Not allowed - 88%, Allowed - 12%
Paris: Not allowed - 36%, Allowed - 64%
Rome: Not allowed - 48%, Allowed - 52%
"""
city_pets = data.groupby(['City', 'Pets'])['Price'].count().reset_index()
city_total = data['City'].value_counts().reset_index().rename(columns={'index':'City', 'City': 'Total'})
ct = city_pets.merge(right=city_total, how="left", left_on="City", right_on="City")
ct.rename(columns={'Price': 'Amount'}, inplace=True)
percents_city = round(ct['Amount']*100/ct['Total'])
ct['%'] = percents_city
fig_city, ax_city = plt.subplots(figsize=(15,6))
sns.barplot(ax=ax_city, x='City', y='%', hue='Pets', data=ct, palette=pets_palette)
plt.title("No pets Hotels")
fig.savefig("allowed_vs_not_allowed_by_city%.png")


# Creating dataset of hotels with conditions: no pets, normal price categories, score higher or equal 9
me = data[data['Pets'] == 'Not allowed']
me_price = me[me['Price Groups'] == "Normal"]
me_score = me_price[me_price['Score'] >= 9]


"""Statistical analysis
NULL hypothesis. Price of No pets hotels is equal to Pets hotels."""
stat_data = data.drop(data[data['Pets'] == 'No info'].index, inplace=False)
allowed = stat_data[stat_data['Pets'] == "Allowed"]
not_allowed = stat_data[stat_data['Pets'] == "Not allowed"]
allowed_price = allowed['Price'].tolist()
not_allowed_price = not_allowed['Price'].tolist()
print(stats.ttest_ind(allowed_price, not_allowed_price, equal_var=False))


price_pets=stat_data.groupby(['Pets'])['Price'].count().reset_index()
fig_stat_price, ax_stat_price = plt.subplots(figsize=(5,8))
sns.countplot(ax=ax_stat_price, x='Pets', data=stat_data, palette="crest")
plt.title("Price samples")
plt.xlabel("Hotels")
plt.ylabel('Price')
fig_stat_price.savefig("stat_price.png")
# This two samples differ statistically significant. Null hypothesis can be rejected.


"""Null hypothesis number 2. 
Score of No pets hotels is equal to Pets hotels"""
allowed_score = allowed['Score'].tolist()
not_allowed_score = not_allowed['Score'].tolist()
print(stats.ttest_ind(allowed_score, not_allowed_score, equal_var=False))


score_pets = stat_data.groupby(['Pets'])['Score'].count().reset_index()
fig_stat_score, ax_stat_score = plt.subplots(figsize=(5, 8))
sns.countplot(ax=ax_stat_score, x='Pets', data=stat_data, palette="crest")
plt.title("Score samples")
plt.xlabel("Hotels")
plt.ylabel('Score')
fig_stat_score.savefig("stat_score.png")
# This two samples differ statistically significant. Null hypothesis number 2 can be rejected.




