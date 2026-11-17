import pandas as pd
import os.path

data = pd.read_csv("data/03_Library SystemCustomers.csv")

data = data[data['Customer ID'].notna()]

data.to_csv(os.path.join('silver_data', 'library_systemcustomers_silver'))
