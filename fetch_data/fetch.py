import os
from pytse_client.download import download_financial_indexes
import pandas as pd
import jalali_pandas
import math
import numpy as np
from scipy.stats.mstats import winsorize
from sector_slc.settings import BASE_DIR
industry_indices_path = os.path.join(BASE_DIR, "industry_indices")
processed_data_path = os.path.join(BASE_DIR, "processed_data")
limit = 3000

data_path = os.path.join(BASE_DIR, "dataset")
sectors_data_path = os.path.join(data_path, "sectors")
market_data_path = os.path.join(data_path, "market")
market_other_data_path = os.path.join(data_path, "market_other_data")
list_of_sector_files = os.listdir(sectors_data_path)
list_of_market_files = os.listdir(market_data_path)
list_of_market_other_data_files = os.listdir(market_other_data_path)
market_data_processed_path = os.path.join(data_path, "market_data_processed")
sectors_data_processed_path = os.path.join(data_path, "sectors_data_processed")
list_of_sector_processed_files = os.listdir(sectors_data_processed_path)
list_of_sector_processed_files = list_of_sector_processed_files[1:]
list_of_market_processed_files = os.listdir(market_data_processed_path)
list_of_market_processed_files = list_of_market_processed_files[1:]
dataset_path = os.path.join(data_path, "dataset")



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


def do_fetch():

    for file_name in list_of_sector_files:
        
        data = pd.read_excel(sectors_data_path+ "\\" + file_name)
        first_row_with_pe_ttm = data[data["P/E-ttm"] != "-"].iloc[-1].name 
        data = data[:first_row_with_pe_ttm + 1]
        first_row_with_trade_value = data[data["ارزش معاملات"] != "-"].iloc[-1].name 
        data = data[:first_row_with_trade_value + 1]
        first_row_with_pct_change = data[data["درصد تغییر"] != "-"].iloc[-1].name 
        data = data[:first_row_with_pct_change + 1]
        data = data[["تاریخ شمسی","درصد تغییر","ارزش معاملات","P/E-ttm"]]
        data = data.replace('-', np.nan)
        data["date"] = data["تاریخ شمسی"].jalali.parse_jalali("%Y-%m-%d")
        data["month"] = data["date"].jalali.month
        data["year"] = data["date"].jalali.year
        data["quarter"] = data["date"].jalali.quarter
        data["weekday"] = data["date"].jalali.weekday
        data["day"] = data["date"].jalali.day
        data = data.drop(["تاریخ شمسی"],axis=1)
        data.rename(columns = {'درصد تغییر':'dayli_return', 'ارزش معاملات':'trade_value'}, inplace = True)
        last_years_month = data["month"][0]
        last_year = data["year"][0]
        first_years_month = data["month"].iloc[-1]
        first_year = data["year"].iloc[-1]

        empty_li_month = []
        empty_li_year = []
        for year in range(first_year, last_year + 1):

            if year == first_year:
                empty_li_month += [i for i in range(first_years_month,13)]
                empty_li_year += [year] * (13-first_years_month)

            elif year == last_year:
                empty_li_month += [i for i in range(1,last_years_month+1)]
                empty_li_year += [year] * (last_years_month)

            else:
                empty_li_month += [i for i in range(1,13)]
                empty_li_year += [year] * 12

        monthly_data = pd.DataFrame(columns=["year","quarter","month","monthly_return","monthly_trade_value","P/E-ttm"])
        monthly_data["year"] = empty_li_year
        monthly_data["month"] = empty_li_month

        for year in range(first_year, last_year + 1):

            if year == first_year:
                for month in range(first_years_month, 13):
                    idx = monthly_data[(monthly_data.year == year) & (monthly_data.month == month)].index.item()
                    ret = return_calculator(data[(data["month"] == month) & (data["year"] == year)]["dayli_return"])
                    monthly_trade_value = data[(data["month"] == month) & (data["year"] == year)]["trade_value"].mean()
                    month_pe_ttm = data[(data["month"] == month) & (data["year"] == year)]["P/E-ttm"].dropna().mean()
                    monthly_data["quarter"][idx] = data[(data["month"] == month) & (data["year"] == year)].quarter.mean()
                    monthly_data["monthly_return"][idx] = ret
                    monthly_data["monthly_trade_value"][idx] = monthly_trade_value
                    monthly_data["P/E-ttm"][idx] = month_pe_ttm

            elif year == last_year:
                for month in range(1, last_years_month + 1):
                    idx = monthly_data[(monthly_data.year == year) & (monthly_data.month == month)].index.item()
                    ret = return_calculator(data[(data["month"] == month) & (data["year"] == year)]["dayli_return"])
                    monthly_trade_value = data[(data["month"] == month) & (data["year"] == year)]["trade_value"].mean()
                    month_pe_ttm = data[(data["month"] == month) & (data["year"] == year)]["P/E-ttm"].dropna().mean()
                    monthly_data["quarter"][idx] = data[(data["month"] == month) & (data["year"] == year)].quarter.mean()
                    monthly_data["monthly_return"][idx] = ret
                    monthly_data["monthly_trade_value"][idx] = monthly_trade_value
                    monthly_data["P/E-ttm"][idx] = month_pe_ttm

            else:
                for month in range(1, 13):
                    idx = monthly_data[(monthly_data.year == year) & (monthly_data.month == month)].index.item()
                    ret = return_calculator(data[(data["month"] == month) & (data["year"] == year)]["dayli_return"])
                    monthly_trade_value = data[(data["month"] == month) & (data["year"] == year)]["trade_value"].mean()
                    month_pe_ttm = data[(data["month"] == month) & (data["year"] == year)]["P/E-ttm"].dropna().mean()
                    monthly_data["quarter"][idx] = data[(data["month"] == month) & (data["year"] == year)].quarter.mean()
                    monthly_data["monthly_return"][idx] = ret
                    monthly_data["monthly_trade_value"][idx] = monthly_trade_value
                    monthly_data["P/E-ttm"][idx] = month_pe_ttm

        monthly_data.to_excel(sectors_data_processed_path + "\\" + file_name)

    market_df = pd.DataFrame()
    for file_name in list_of_market_files:
        data = pd.read_excel(market_data_path+ "\\" + file_name)
        file_name = file_name.split(".")[0]
        data.rename(columns = {'مقدار':file_name, "تاریخ شمسی":"date"}, inplace = True)
        data = data.drop(["تاریخ میلادی"],axis=1)
        data["date"] = data["date"].jalali.parse_jalali("%Y-%m-%d")
        data["month"] = data["date"].jalali.month
        data["year"] = data["date"].jalali.year
        data["quarter"] = data["date"].jalali.quarter
        data["weekday"] = data["date"].jalali.weekday
        data["day"] = data["date"].jalali.day
        if len(market_df) == 0:
            market_df = data
        else:
            market_df = market_df.merge(data,on="date",how="inner")
        
    market_df = market_df[["date","market_pe","overall_index","trade_value","usd","nima_usd"]]
    market_df["month"] = market_df["date"].jalali.month
    market_df["year"] = market_df["date"].jalali.year
    market_df["quarter"] = market_df["date"].jalali.quarter
    market_df["weekday"] = market_df["date"].jalali.weekday
    market_df["day"] = market_df["date"].jalali.day
    market_df["diff_nima_usd"] = market_df["nima_usd"] / market_df["usd"] - 1
    market_df["usd"] = market_df["usd"].pct_change() 
    market_df["overall_index"] = market_df["overall_index"].pct_change()

    first_years_month = market_df["month"][0]
    first_year = market_df["year"][0]
    last_years_month = market_df["month"].iloc[-1]
    last_year = market_df["year"].iloc[-1]

    empty_li_month = []
    empty_li_year = []
    for year in range(first_year, last_year + 1):

        if year == first_year:
            empty_li_month += [i for i in range(first_years_month,13)]
            empty_li_year += [year] * (13-first_years_month)

        elif year == last_year:
            empty_li_month += [i for i in range(1,last_years_month+1)]
            empty_li_year += [year] * (last_years_month)

        else:
            empty_li_month += [i for i in range(1,13)]
            empty_li_year += [year] * 12

    monthly_market_data = pd.DataFrame(columns=["year","quarter","month","index_monthly_return","monthly_trade_value","monthly_usd_return","market_pe","diff_nima_usd"])
    monthly_market_data["year"] = empty_li_year
    monthly_market_data["month"] = empty_li_month

    for year in range(first_year, last_year + 1):

        if year == first_year:
            for month in range(first_years_month, 13):
                idx = monthly_market_data[(monthly_market_data.year == year) & (monthly_market_data.month == month)].index.item()
                index_ret = return_calculator(market_df[(market_df["month"] == month) & (market_df["year"] == year)]["overall_index"])
                usd_ret = return_calculator(market_df[(market_df["month"] == month) & (market_df["year"] == year)]["usd"])
                monthly_trade_value = market_df[(market_df["month"] == month) & (market_df["year"] == year)]["trade_value"].mean()
                month_pe_ttm = market_df[(market_df["month"] == month) & (market_df["year"] == year)]["market_pe"].dropna().mean()
                diff_nima_usd_monthly = market_df[(market_df["month"] == month) & (market_df["year"] == year)]["diff_nima_usd"].dropna().median()
                monthly_market_data["quarter"][idx] = market_df[(market_df["month"] == month) & (market_df["year"] == year)].quarter.mean()
                monthly_market_data["index_monthly_return"][idx] = index_ret
                monthly_market_data["monthly_usd_return"][idx] = usd_ret
                monthly_market_data["monthly_trade_value"][idx] = monthly_trade_value
                monthly_market_data["market_pe"][idx] = month_pe_ttm
                monthly_market_data["diff_nima_usd"][idx] = diff_nima_usd_monthly

        elif year == last_year:
            for month in range(1, last_years_month + 1):
                idx = monthly_market_data[(monthly_market_data.year == year) & (monthly_market_data.month == month)].index.item()
                index_ret = return_calculator(market_df[(market_df["month"] == month) & (market_df["year"] == year)]["overall_index"])
                usd_ret = return_calculator(market_df[(market_df["month"] == month) & (market_df["year"] == year)]["usd"])
                monthly_trade_value = market_df[(market_df["month"] == month) & (market_df["year"] == year)]["trade_value"].mean()
                month_pe_ttm = market_df[(market_df["month"] == month) & (market_df["year"] == year)]["market_pe"].dropna().mean()
                diff_nima_usd_monthly = market_df[(market_df["month"] == month) & (market_df["year"] == year)]["diff_nima_usd"].dropna().median()
                monthly_market_data["quarter"][idx] = market_df[(market_df["month"] == month) & (market_df["year"] == year)].quarter.mean()
                monthly_market_data["index_monthly_return"][idx] = index_ret
                monthly_market_data["monthly_usd_return"][idx] = usd_ret
                monthly_market_data["monthly_trade_value"][idx] = monthly_trade_value
                monthly_market_data["market_pe"][idx] = month_pe_ttm
                monthly_market_data["diff_nima_usd"][idx] = diff_nima_usd_monthly

        else:
            for month in range(1, 13):
                idx = monthly_market_data[(monthly_market_data.year == year) & (monthly_market_data.month == month)].index.item()
                index_ret = return_calculator(market_df[(market_df["month"] == month) & (market_df["year"] == year)]["overall_index"])
                usd_ret = return_calculator(market_df[(market_df["month"] == month) & (market_df["year"] == year)]["usd"])
                monthly_trade_value = market_df[(market_df["month"] == month) & (market_df["year"] == year)]["trade_value"].mean()
                month_pe_ttm = market_df[(market_df["month"] == month) & (market_df["year"] == year)]["market_pe"].dropna().mean()
                diff_nima_usd_monthly = market_df[(market_df["month"] == month) & (market_df["year"] == year)]["diff_nima_usd"].dropna().median()
                monthly_market_data["quarter"][idx] = market_df[(market_df["month"] == month) & (market_df["year"] == year)].quarter.mean()
                monthly_market_data["index_monthly_return"][idx] = index_ret
                monthly_market_data["monthly_usd_return"][idx] = usd_ret
                monthly_market_data["monthly_trade_value"][idx] = monthly_trade_value
                monthly_market_data["market_pe"][idx] = month_pe_ttm
                monthly_market_data["diff_nima_usd"][idx] = diff_nima_usd_monthly

    data = pd.read_excel(market_other_data_path + "//" + 'inflation.xlsx')
    data["inflation"] = data["CPI"].pct_change()
    data = data.drop(["CPI"],axis=1)
    data = data.dropna()
    data["date"] = data["date"].jalali.parse_jalali("%Y-%m")
    data["month"] = data["date"].jalali.month
    data["year"] = data["date"].jalali.year
    data["quarter"] = data["date"].jalali.quarter
    data["weekday"] = data["date"].jalali.weekday
    data["day"] = data["date"].jalali.day
    inflation_df = data

    data = pd.read_excel(market_other_data_path + "//" + 'money_supply.xlsx')
    data["change_in_money_supply"] = data["money_supply"].pct_change()
    data = data.drop(["money_supply"],axis=1)
    data = data.dropna()
    data["date"] = data["date"].jalali.parse_jalali("%Y-%m")
    data["month"] = data["date"].jalali.month
    data["year"] = data["date"].jalali.year
    data["quarter"] = data["date"].jalali.quarter
    data["weekday"] = data["date"].jalali.weekday
    data["day"] = data["date"].jalali.day
    money_supply_df = data

    monthly_market_data = monthly_market_data.merge(inflation_df,on=["year","month"],how="inner")
    monthly_market_data = monthly_market_data.merge(money_supply_df,on=["year","month"],how="inner")
    monthly_market_data = monthly_market_data.drop(["quarter_x","date_x","quarter_y","weekday_x","day_x","date_y","weekday_y","day_y","quarter"],axis=1)
    monthly_market_data.rename(columns = {'monthly_trade_value':"market_monthly_trade_value"}, inplace = True)

    monthly_market_data.to_csv(market_data_processed_path + "\\" + "market_data_processed.csv")

    dataset_df = pd.DataFrame()
    for file_name in list_of_sector_processed_files:
        data = pd.read_excel(sectors_data_processed_path+ "\\" + file_name)
        data = data.fillna(method='ffill')
        data = data.drop(["Unnamed: 0"],axis=1)
        market_data = pd.read_csv(market_data_processed_path+ "\\" + list_of_market_processed_files[0])
        market_data = market_data.drop(["Unnamed: 0"],axis=1)
        market_data = market_data.fillna(method='ffill')
        new_data = data.merge(market_data,on=["year","month"],how="inner")

        number_of_rows = len(new_data)
        new_data["sector"] = [file_name.split(".")[0]] * number_of_rows
        new_data["next_6m_return"] = [np.nan] * number_of_rows
        new_data["next_3m_return"] = [np.nan] * number_of_rows
        new_data["next_1m_return"] = [np.nan] * number_of_rows

        new_data["last_6m_return"] = [np.nan] * number_of_rows
        new_data["last_3m_return"] = [np.nan] * number_of_rows
        new_data["last_1m_return"] = [np.nan] * number_of_rows

        new_data["next_6m_usd_return"] = [np.nan] * number_of_rows
        new_data["next_3m_usd_return"] = [np.nan] * number_of_rows
        new_data["next_1m_usd_return"] = [np.nan] * number_of_rows

        new_data["last_6m_usd_return"] = [np.nan] * number_of_rows
        new_data["last_3m_usd_return"] = [np.nan] * number_of_rows
        new_data["last_1m_usd_return"] = [np.nan] * number_of_rows

        new_data["next_6m_index_return"] = [np.nan] * number_of_rows
        new_data["next_3m_index_return"] = [np.nan] * number_of_rows
        new_data["next_1m_index_return"] = [np.nan] * number_of_rows

        new_data["last_6m_index_return"] = [np.nan] * number_of_rows
        new_data["last_3m_index_return"] = [np.nan] * number_of_rows
        new_data["last_1m_index_return"] = [np.nan] * number_of_rows

        new_data["excess_next_1m_return"] = [np.nan] * number_of_rows
        new_data["excess_next_3m_return"] = [np.nan] * number_of_rows
        new_data["excess_next_6m_return"] = [np.nan] * number_of_rows

        new_data["relative_trade_value"] = [np.nan] * number_of_rows
        new_data["market_relative_trade_value"] = [np.nan] * number_of_rows

        for index, row in new_data.iterrows():
            if (index <=5) or (index > number_of_rows - 6):
                continue
            else:
                new_data["next_6m_return"].iloc[index] = return_calculator(new_data["monthly_return"].iloc[index:index+6])
                new_data["next_3m_return"].iloc[index] = return_calculator(new_data["monthly_return"].iloc[index:index+3])
                new_data["next_1m_return"].iloc[index] = return_calculator(new_data["monthly_return"].iloc[index:index+1])

                new_data["last_6m_return"].iloc[index] = return_calculator(new_data["monthly_return"].iloc[index-6:index])
                new_data["last_3m_return"].iloc[index] = return_calculator(new_data["monthly_return"].iloc[index-3:index])
                new_data["last_1m_return"].iloc[index] = return_calculator(new_data["monthly_return"].iloc[index-1:index])

                new_data["next_6m_usd_return"].iloc[index] = return_calculator(new_data["monthly_usd_return"].iloc[index:index+6])
                new_data["next_3m_usd_return"].iloc[index] = return_calculator(new_data["monthly_usd_return"].iloc[index:index+3])
                new_data["next_1m_usd_return"].iloc[index] = return_calculator(new_data["monthly_usd_return"].iloc[index:index+1])

                new_data["last_6m_usd_return"].iloc[index] = return_calculator(new_data["monthly_usd_return"].iloc[index-6:index])
                new_data["last_3m_usd_return"].iloc[index] = return_calculator(new_data["monthly_usd_return"].iloc[index-3:index])
                new_data["last_1m_usd_return"].iloc[index] = return_calculator(new_data["monthly_usd_return"].iloc[index-1:index])

                new_data["next_6m_index_return"].iloc[index] = return_calculator(new_data["index_monthly_return"].iloc[index:index+6])
                new_data["next_3m_index_return"].iloc[index] = return_calculator(new_data["index_monthly_return"].iloc[index:index+3])
                new_data["next_1m_index_return"].iloc[index] = return_calculator(new_data["index_monthly_return"].iloc[index:index+1])

                new_data["last_6m_index_return"].iloc[index] = return_calculator(new_data["index_monthly_return"].iloc[index-6:index])
                new_data["last_3m_index_return"].iloc[index] = return_calculator(new_data["index_monthly_return"].iloc[index-3:index])
                new_data["last_1m_index_return"].iloc[index] = return_calculator(new_data["index_monthly_return"].iloc[index-1:index])

                new_data["relative_trade_value"].iloc[index] = new_data["monthly_trade_value"].iloc[index] / new_data["monthly_trade_value"].iloc[index-6:index].mean() - 1
                new_data["market_relative_trade_value"].iloc[index] = new_data["market_monthly_trade_value"].iloc[index] / new_data["market_monthly_trade_value"].iloc[index-6:index].mean() - 1

        to_winsorize_list = [
            'P/E-ttm','market_pe', 'diff_nima_usd', 'inflation',
            'change_in_money_supply', 'next_6m_return', 'last_6m_return',
            'next_3m_return', 'next_1m_return', 'last_3m_return', 'last_1m_return',
            'next_6m_usd_return', 'next_3m_usd_return', 'next_1m_usd_return',
            'last_6m_usd_return', 'last_3m_usd_return', 'last_1m_usd_return',
            'next_6m_index_return', 'next_3m_index_return', 'next_1m_index_return',
            'last_6m_index_return', 'last_3m_index_return', 'last_1m_index_return',
            'excess_next_1m_return', 'excess_next_3m_return','excess_next_6m_return',
                'relative_trade_value','market_relative_trade_value']

        for column in to_winsorize_list:
            new_data[column] = winsorize(new_data[column],(0.025,0.025))    

        new_data["excess_next_1m_return"] = new_data["next_1m_return"] - new_data["next_1m_index_return"]
        new_data["excess_next_3m_return"] = new_data["next_3m_return"] - new_data["next_3m_index_return"]
        new_data["excess_next_6m_return"] = new_data["next_6m_return"] - new_data["next_6m_index_return"]

        new_data = new_data.dropna()
        

        if len(dataset_df) == 0:
            dataset_df = new_data

        else:
            dataset_df = pd.concat([dataset_df,new_data])

    
    dataset_df = dataset_df.sort_values(by = ['year', 'month'], ascending = [True, True])
    dataset_df.to_csv(dataset_path + "\\" + "dataset.csv")


    return