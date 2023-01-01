from django.shortcuts import render
from .fetch import do_fetch
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


#def clean_page(request):
    #files = glob.glob(industry_indices_path)
    #for f in files:
        #os.remove(f)
    #files = glob.glob(processed_data_path)
    #for f in files:
        #os.remove(f)
    #return render(request, 'clean.html')

