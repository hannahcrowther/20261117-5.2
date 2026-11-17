import pandas as pd
import os.path

data = pd.read_csv("data/03_Library Systembook.csv")

data['Book checkout'] = data['Book checkout'].str.replace(r'"', '')

data['Books'] = data['Books'].str.replace('the kind', 'the king')

data.to_csv(os.path.join('silver_data', 'library_systembook_silver'))
