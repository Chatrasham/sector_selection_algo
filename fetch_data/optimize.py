import os
import pandas as pd
import math
import numpy as np
from sklearn.linear_model import LinearRegression
from sector_slc.settings import BASE_DIR

def do_optimize(month_to_predict, year_to_predict):

    processed_data_path = os.path.join(BASE_DIR ,"processed_data")
    list_of_files = os.listdir(processed_data_path)
    list_of_files = list_of_files[1:]
    resutl_df = pd.DataFrame(columns=["sector","predicted_excess_return","realized_excess_return","realized_return"])

    for file in list_of_files:
        data = pd.read_csv(processed_data_path+ "\\" + file)
        idx = data[(data["month"] == month_to_predict ) & (data["year"] == year_to_predict)].index[0]
        X = data[["1month_return","1m_3m","1m_6m"]][0:idx]
        y = data[["month_excess_return"]][0:idx]
        reg = LinearRegression().fit(X, y)
        reg.predict(data[(data.month == month_to_predict ) & (data.year == year_to_predict)][["1month_return","1m_3m","1m_6m"]])
        predicted_return = reg.predict(data[(data.month == month_to_predict ) & (data.year == year_to_predict)][["1month_return","1m_3m","1m_6m"]])[0][0]
        realized_excess_return = data[(data.month == month_to_predict ) & (data.year == year_to_predict)][["month_excess_return"]].iloc[0].item()
        realized_return = data[(data.month == month_to_predict ) & (data.year == year_to_predict)][["return"]].iloc[0].item()
        new_row = [file, predicted_return, realized_excess_return ,realized_return]
        resutl_df.loc[len(resutl_df)] = new_row
        
    resutl_df = resutl_df.sort_values("predicted_excess_return", ascending=False).reset_index()
    resutl_df = resutl_df.drop(["index"],axis=1)
    return  resutl_df