from django.shortcuts import render
from .fetch import do_fetch
from .optimize import do_optimize 
from .performance import do_performance
from .forms import RankForm, PerformanceForm
import json
from django.shortcuts import HttpResponse
#from sector_slc.settings import BASE_DIR
#import os
#import glob
#industry_indices_path = os.path.join(BASE_DIR,"industry_indices")
#processed_data_path = os.path.join(BASE_DIR ,"processed_data")


def landing_page(request):
    return render(request, 'base.html')

def fetch_page(request):
    do_fetch()
    return render(request, 'fetch.html')

def optimize_page(request):
    if request.method == 'POST':
        form = RankForm(request.POST)
        if form.is_valid():
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            method = form.cleaned_data['method']
            target = form.cleaned_data['target']
            json_records = do_optimize(month,year,method,target).reset_index().to_json(orient ='records')
            data = []
            data = json.loads(json_records)
            context = {'d': data}
            return render(request, 'optimize.html', context)
    else:
        form = RankForm()
        return render(request, 'optimize_form.html', {'form': form,})

def performance_page(request):
    if request.method == 'POST':
        form = PerformanceForm(request.POST)
        if form.is_valid():
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            json_records = do_performance(month,year).reset_index().to_json(orient ='records')
            data = []
            data = json.loads(json_records)
            context = {'d': data}
            return render(request, 'performance.html', context)
    else:
        form = PerformanceForm()
        return render(request, 'performance_form.html', {'form': form,})


#def clean_page(request):
    #files = glob.glob(industry_indices_path)
    #for f in files:
        #os.remove(f)
    #files = glob.glob(processed_data_path)
    #for f in files:
        #os.remove(f)
    #return render(request, 'clean.html')

