import pandas as pd
import numpy as np
import pickle

data_path = 'datasets'

import os
def load_data(dat_path = data_path):
    csv_path = os.path.join(dat_path, 'adult.csv')
    features = ['age', 'wkclss', 'fnlwgt', 'educa', 'educa_n', 'marit_st', 'occupa', 'relatnshp', 'race', 'sex', 'cap_gn', 'cap_lss', 'hrwkwk', 'nativ_cntry', 'income']
    return pd.read_csv(csv_path, header = None, sep = ',', names=features)

adult_df = load_data()

adult_df_cat = adult_df[['income']]


from sklearn.preprocessing import OrdinalEncoder
ord_encoder = OrdinalEncoder()
adult_df_income_Ordi = ord_encoder.fit_transform(adult_df_cat)


num_income_df = pd.DataFrame(adult_df_income_Ordi, columns=['num_income'])

adult_df = pd.concat([adult_df, num_income_df], sort=True, axis=1)

adult_df['new_feature'] = (adult_df['hrwkwk'])*(adult_df['educa_n'])*adult_df['age'] + 0.223013*adult_df['cap_gn'] - 0.147554*adult_df['cap_lss']

from sklearn.model_selection import train_test_split

train_set, test_set = train_test_split(adult_df, test_size=0.2, random_state=77)

cal_attributes = ['new_feature', 'educa_n', 'age', 'hrwkwk']

train_labels = train_set['num_income']
train_features = train_set[cal_attributes]

test_labels = test_set['num_income']
test_features = test_set[cal_attributes]


from sklearn.linear_model import LogisticRegression
clf = LogisticRegression()
clf.fit(train_features, train_labels)


pickle.dump(clf, open('model.pkl', 'wb'))

model = pickle.load(open('model.pkl', 'rb'))

# Sample input
cap_gn = 0
cap_lss = 0
hrwkwk = 84
educa_n = 15
age = 24
new_feature = hrwkwk*educa_n*age + 0.223013*cap_gn - 0.147554*cap_lss
X_input = [[new_feature, educa_n, age, hrwkwk]]
print(X_input)
# end Sample input

model.predict(X_input)
