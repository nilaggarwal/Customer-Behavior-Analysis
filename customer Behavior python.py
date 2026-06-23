import pandas as pd
from sqlalchemy import create_engine
df= pd.read_csv('customer_shopping_behavior.csv')

#print(df.head())

#print(df.describe())

#print(df.isnull().sum())

df['Review Rating']= df.groupby('Category')['Review Rating'].transform(lambda x:x.fillna(x.median()))
#print(df.isnull().sum())

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')
df = df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
#print(df.columns)

#create a column age_group
labels = ['Young Adult', 'Adult', 'Middle-aged','Senior']
df['age_group']= pd.qcut(df['age'], q=4, labels = labels)
#print(df[['age','age_group']].head(10))

#create columns purchase_frequency_days
frequency_mapping = {
    'Fortnightly':14,
    'weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annualy': 365,
    'Every 3 Months': 90,
}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
#print(df[['purchase_frequency_days','frequency_of_purchases']].head(10))

#print(df[['discount_applied','promo_code_used']].head(10))

#print((df['discount_applied']== df['promo_code_used']).all())

df=df.drop('promo_code_used',axis=1)
#print(df.columns)


#step 1: Connect to PostgreSQL
#Replace placeholders with your actual details
username = "postgres"
password = "123"
host = "localhost"
port = "5432"
database = "customer_behavior"

engine = create_engine(
    f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'
)

#step 2: Load Dataframe into Postgresql
table_name = "customer"   #choose any table name
df.to_sql(table_name, engine, if_exists = "replace", index = False)

print(f"Data successfully loaded into table'{table_name}' in database '{database}'.")




    
