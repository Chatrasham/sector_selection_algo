import os
import pandas as pd
import jalali_pandas
import math
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.ensemble import VotingRegressor
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")
from sector_slc.settings import BASE_DIR
data_path = os.path.join(BASE_DIR, "dataset")
dataset_path = os.path.join(data_path, "dataset")
dataset_df = pd.read_csv(dataset_path + "\\" + "dataset.csv")
dataset_df = dataset_df.drop("Unnamed: 0",axis=1)
list_of_sectors = dataset_df.sector.unique().tolist()


def do_optimize(month_to_predict, year_to_predict, method, target):
    if method == "Decision Tree":
        regressor = DecisionTreeRegressor(random_state = 0, max_depth=5, criterion="absolute_error", min_samples_split=300, min_samples_leaf= 150)
    elif method == "Random Forest Regressor":
        regressor = RandomForestRegressor(n_estimators = 100, random_state = 0,criterion="absolute_error",max_depth=4,min_samples_split=300,min_samples_leaf= 150)
    elif method == "K Neighbors Regressor":
        regressor = KNeighborsRegressor(n_neighbors=10)
    elif method == "Kernel Ridge":
        regressor = KernelRidge(alpha=1.0, kernel="rbf")
    elif method == "Support Vector Regressor":
        regressor = SVR(kernel="rbf")
    elif method == "Neural Network":
        regressor = MLPRegressor(hidden_layer_sizes =[8,4], random_state=1, max_iter=5000, activation="identity")

    elif method == "Combine Decision Tree and K Neighbors and Kernel Ridge":
        regressor1 = DecisionTreeRegressor(random_state = 0, max_depth=5, criterion="absolute_error", min_samples_split=300, min_samples_leaf= 150)
        regressor2 = KNeighborsRegressor(n_neighbors=10)
        regressor3 = KernelRidge(alpha=1.0, kernel="rbf")
        regressor = VotingRegressor(estimators=[('DT', regressor1), ('KN', regressor2), ('KR', regressor3)])

    elif method == "Combine Decision Tree and SVR and Neural Network":
        regressor1 = DecisionTreeRegressor(random_state = 0, max_depth=5, criterion="absolute_error", min_samples_split=300, min_samples_leaf= 150)
        regressor2 = SVR(kernel="rbf")
        regressor3 = MLPRegressor(hidden_layer_sizes =[8,4], random_state=1, max_iter=5000, activation="identity")
        regressor = VotingRegressor(estimators=[('DT', regressor1), ('SV', regressor2), ('NN', regressor3)])

    elif method == "Combine K Neighbors and Kernel Ridge and Neural Network":
        regressor1 = KNeighborsRegressor(n_neighbors=10)
        regressor2 = KernelRidge(alpha=1.0, kernel="rbf")
        regressor3 = MLPRegressor(hidden_layer_sizes =[8,4], random_state=1, max_iter=5000, activation="identity")
        regressor = VotingRegressor(estimators=[('KN', regressor1), ('KR', regressor2), ('NN', regressor3)])



    list_of_features = [
            'P/E-ttm','market_pe', 'diff_nima_usd', 'inflation',
            'change_in_money_supply', 'last_6m_return','last_3m_return', 'last_1m_return',
            'last_6m_usd_return', 'last_3m_usd_return', 'last_1m_usd_return',
            'last_6m_index_return', 'last_3m_index_return', 'last_1m_index_return',
            'relative_trade_value','market_relative_trade_value']


    first_occurence = dataset_df[(dataset_df.month == month_to_predict) & (dataset_df.year == year_to_predict)].iloc[0].name
    train_set = dataset_df[:first_occurence]


    X = train_set[list_of_features]
    y = train_set[target]
    regressor.fit(X, y)

    result_df = pd.DataFrame(columns=["sector", "predicted_excess_return","realized_excess_return"])
    for sector in list_of_sectors:
        row = dataset_df[(dataset_df.month == month_to_predict) & (dataset_df.year == year_to_predict) & (dataset_df.sector == sector)].iloc[0]
        row_input = row[list_of_features]
        predicted_excess_return = regressor.predict([row_input])
        realized_excess_return = row[target] 
        new_row = [sector, predicted_excess_return[0]*100, realized_excess_return*100]
        result_df.loc[len(result_df)] = new_row
    result_df = result_df.sort_values(by="predicted_excess_return",ascending=False).reset_index().drop("index",axis=1)
    long_leg_return = result_df.realized_excess_return.iloc[:3].mean()
    short_leg_return = result_df.realized_excess_return.iloc[-3:].mean()
    #index_return = row.next_3m_index_return * 100
    print(long_leg_return,short_leg_return)
    


    return  [result_df, long_leg_return, short_leg_return]