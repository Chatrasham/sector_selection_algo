import os
from pytse_client.download import download_financial_indexes
import pandas as pd
import jalali_pandas
import math
import numpy as np
from sector_slc.settings import BASE_DIR
industry_indices_path = os.path.join(BASE_DIR, "industry_indices")
processed_data_path = os.path.join(BASE_DIR, "processed_data")
limit = 3000



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

    download_financial_indexes(symbols="all", write_to_csv=True, base_path=industry_indices_path)

    list_of_files = os.listdir(industry_indices_path)
    to_delete_indices = ["شاخص 30 شركت بزرگ.csv","شاخص آزاد شناور.csv","شاخص بازار اول.csv","شاخص بازار دوم.csv",
                "شاخص بازده نقدي قيمت.csv", "شاخص صنعت.csv", "شاخص قيمت (هم وزن).csv", "شاخص قيمت 50 شركت.csv",
                "شاخص قيمت(وزنيارزشي).csv", "شاخص50شركت فعالتر.csv", "شاخص كل.csv", "شاخص كل (هم وزن).csv"
                ]
    defunct_sectors = ["مبلمان.csv", "ابزار پزشكي.csv" , "پيمانكاري.csv"]
    sectors_li = [item for item in list_of_files if item not in to_delete_indices]
    sectors_li = [item for item in sectors_li if item not in defunct_sectors]
    for f in sectors_li:
        data = pd.read_csv(industry_indices_path+ "\\" + f)
        if len(data) < limit:
            sectors_li.remove(f)

    for sector_item in sectors_li:
        data = pd.read_csv(industry_indices_path+ "\\" + sector_item)
        data['date'] = pd.to_datetime( data['date'],    format='%Y-%m-%d')
        data["jdate"] = data["date"].jalali.to_jalali()
        data["month"] = data["jdate"].jalali.month
        data["year"] = data["jdate"].jalali.year
        data["weekday"] = data["jdate"].jalali.weekday
        #data.set_index('date' ,inplace=True)
        data['value'] = data['value'].pct_change()
        data['value'].values[data['value'].values > 0.05] = 0.05
        data['value'].values[data['value'].values < -0.05] = -0.05
        #weekly_data = data.resample("W").sum()

        first_years_month = data["month"][0]
        first_year = data["year"][0]
        last_years_month = data["month"].iloc[-1]
        last_year = data["year"].iloc[-1]

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

        monthly_data = pd.DataFrame(columns=["return","year","month","return_1m","return_3m","return_6m"])
        monthly_data["year"] = empty_li_year
        monthly_data["month"] = empty_li_month

        for year in range(first_year, last_year + 1):

            if year == first_year:
                for month in range(first_years_month, 13):
                    idx = monthly_data[(monthly_data.year == year) & (monthly_data.month == month)].index.item()
                    ret = return_calculator(data[(data["month"] == month) & (data["year"] == year)]["value"])
                    monthly_data["return"][idx] = ret

            elif year == last_year:
                for month in range(1, last_years_month + 1):
                    idx = monthly_data[(monthly_data.year == year) & (monthly_data.month == month)].index.item()
                    ret = return_calculator(data[(data["month"] == month) & (data["year"] == year)]["value"])
                    monthly_data["return"][idx] = ret

            else:
                for month in range(1, 13):
                    idx = monthly_data[(monthly_data.year == year) & (monthly_data.month == month)].index.item()
                    ret = return_calculator(data[(data["month"] == month) & (data["year"] == year)]["value"])
                    monthly_data["return"][idx] = ret

        monthly_data["return"] = monthly_data["return"] * 100
        monthly_data["return_1m"] = monthly_data["return"].shift(1)
        monthly_data["return_3m"] = monthly_data["return"].shift(3)
        monthly_data["return_6m"] = monthly_data["return"].shift(6)
        monthly_data = monthly_data.dropna().reset_index()
        monthly_data = monthly_data.drop(['index'], axis=1)


        index_data = pd.read_csv(industry_indices_path+ "\\" + "شاخص كل.csv")

        index_data['date'] = pd.to_datetime( index_data['date'],    format='%Y-%m-%d')
        index_data["jdate"] = index_data["date"].jalali.to_jalali()
        index_data["month"] = index_data["jdate"].jalali.month
        index_data["year"] = index_data["jdate"].jalali.year
        index_data["weekday"] = index_data["jdate"].jalali.weekday
        #data.set_index('date' ,inplace=True)
        index_data['value'] = index_data['value'].pct_change()
        index_data['value'].values[index_data['value'].values > 0.05] = 0.05
        index_data['value'].values[index_data['value'].values < -0.05] = -0.05
        #weekly_data = data.resample("W").sum()

        first_years_month = index_data["month"][0]
        first_year = index_data["year"][0]
        last_years_month = index_data["month"].iloc[-1]
        last_year = index_data["year"].iloc[-1]

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

        index_monthly_data = pd.DataFrame(columns=["index_return","year","month","index_return_1m","index_return_3m","index_return_6m"])
        index_monthly_data["year"] = empty_li_year
        index_monthly_data["month"] = empty_li_month

        for year in range(first_year, last_year + 1):

            if year == first_year:
                for month in range(first_years_month, 13):
                    idx = index_monthly_data[(index_monthly_data.year == year) & (index_monthly_data.month == month)].index.item()
                    ret = return_calculator(index_data[(index_data["month"] == month) & (index_data["year"] == year)]["value"])
                    index_monthly_data["index_return"][idx] = ret

            elif year == last_year:
                for month in range(1, last_years_month + 1):
                    idx = index_monthly_data[(index_monthly_data.year == year) & (index_monthly_data.month == month)].index.item()
                    ret = return_calculator(index_data[(index_data["month"] == month) & (index_data["year"] == year)]["value"])
                    index_monthly_data["index_return"][idx] = ret

            else:
                for month in range(1, 13):
                    idx = index_monthly_data[(index_monthly_data.year == year) & (index_monthly_data.month == month)].index.item()
                    ret = return_calculator(index_data[(index_data["month"] == month) & (index_data["year"] == year)]["value"])
                    index_monthly_data["index_return"][idx] = ret

        index_monthly_data["index_return"] = index_monthly_data["index_return"] * 100
        index_monthly_data["index_return_1m"] = index_monthly_data["index_return"].shift(1)
        index_monthly_data["index_return_3m"] = index_monthly_data["index_return"].shift(3)
        index_monthly_data["index_return_6m"] = index_monthly_data["index_return"].shift(6)
        index_monthly_data = index_monthly_data.dropna().reset_index()
        index_monthly_data = index_monthly_data.drop(['index'], axis=1)

        merged_data = monthly_data.merge(index_monthly_data, on=["month","year"])
        merged_data["month_excess_return"] = merged_data["return"] - merged_data["index_return"]
        merged_data["1month_return"] = merged_data["return_1m"] - merged_data["index_return_1m"]
        merged_data["3month_return"] = merged_data["return_3m"] - merged_data["index_return_3m"]
        merged_data["6month_return"] = merged_data["return_6m"] - merged_data["index_return_6m"]
        merged_data["1m_3m"] = np.array((merged_data["1month_return"] + merged_data["3month_return"])/150,dtype=float)
        merged_data["1m_3m"] = 1000 * ((1/(1 + np.exp(-merged_data["1m_3m"]))) - 0.5) 
        merged_data["1m_6m"] = np.array((merged_data["1month_return"] + merged_data["6month_return"])/150,dtype=float)
        merged_data["1m_6m"] = 1000 * ((1/(1 + np.exp(-merged_data["1m_6m"]))) - 0.5) 
        merged_data = merged_data[["month","year","return","month_excess_return","1month_return","1m_3m","1m_6m"]]

        merged_data.to_csv(processed_data_path +"\\" +sector_item)

    return