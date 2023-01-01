import os
import pandas as pd
import math
import numpy as np
from sklearn.linear_model import LinearRegression
from sector_slc.settings import BASE_DIR

def return_calculator(df):
    period_return = 1
    li = list(df)
    for day, _ in df.iteritems():
        idx = df.index.get_loc(day)
        elem = li[idx]
        if (math.isnan(elem)):
            elem = outlier_handler(elem)
            if elem == False:
                continue
        period_return = period_return * (1+elem)
    period_return = period_return - 1
    return period_return

def outlier_handler(ret):
    if (math.isnan(ret)):
        return False

def do_performance(first_years_month, first_year):

    processed_data_path = os.path.join(BASE_DIR ,"processed_data")
    list_of_files = os.listdir(processed_data_path)
    list_of_files = list_of_files[1:]

    data = pd.read_csv(processed_data_path+ "\\" + list_of_files[0])
    last_years_month = data["month"].iloc[-1]
    last_year = data["year"].iloc[-1]

    performance_df = pd.DataFrame(columns=["month","year","long_leg_return","short_leg_return","portfolio_return"])

    for year_to_predict in range(first_year, last_year + 1):

        if (year_to_predict == first_year) and (first_year != last_year) :
            for month_to_predict in range(first_years_month, 13):
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
                long_leg_return = resutl_df["realized_return"].iloc[0:3].mean()
                short_leg_return = resutl_df["realized_return"].iloc[-3:].mean()
                portfolio_return = long_leg_return - short_leg_return
                new_row_performance_df = [month_to_predict, year_to_predict, long_leg_return , short_leg_return, portfolio_return]
                performance_df.loc[len(performance_df)] = new_row_performance_df

        elif year_to_predict == last_year:
            for month_to_predict in range(1, last_years_month + 1):
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
                long_leg_return = resutl_df["realized_return"].iloc[0:3].mean()
                short_leg_return = resutl_df["realized_return"].iloc[-3:].mean()
                portfolio_return = long_leg_return - short_leg_return
                new_row_performance_df = [month_to_predict, year_to_predict, long_leg_return , short_leg_return, portfolio_return]
                performance_df.loc[len(performance_df)] = new_row_performance_df

        else:
            for month_to_predict in range(1, 13):
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
                long_leg_return = resutl_df["realized_return"].iloc[0:3].mean()
                short_leg_return = resutl_df["realized_return"].iloc[-3:].mean()
                portfolio_return = long_leg_return - short_leg_return
                new_row_performance_df = [month_to_predict, year_to_predict, long_leg_return , short_leg_return, portfolio_return]
                performance_df.loc[len(performance_df)] = new_row_performance_df



    total_long_leg_ret =  return_calculator(performance_df["long_leg_return"]/100) * 100
    total_short_leg_ret = return_calculator(performance_df["short_leg_return"]/100) * 100
    total_portfolio_ret = total_long_leg_ret - total_short_leg_ret
    new_row_performance_df = ["total", "return", total_long_leg_ret , total_short_leg_ret, total_portfolio_ret]
    performance_df.loc[len(performance_df)] = new_row_performance_df

    return  performance_df