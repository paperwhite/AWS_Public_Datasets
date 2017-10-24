#code to download IRS-form-990 dataset for the years 2011 to 2015 from s3://irs-form-990

import json
from pprint import pprint
import codecs
from collections import namedtuple
import numpy as np
import urllib2
import wget
import os
import errno

def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data




for year in range(2011,2016):
    data = []

    file_loc = 'https://s3.amazonaws.com/irs-form-990/index_'+ str(year) +'.json'
    print file_loc

    response = urllib2.urlopen(file_loc)
    data_file = response.read()

    filename = 'index_'+str(year)+'.json'
    # Write data to file
    file_ = open(filename, 'w')
    file_.write(data_file)
    file_.close()

#with codecs.open('sample_index.json') as f:
    with codecs.open(filename,'rU','utf-8') as f:
        for line in f:
            data.append(json_loads_byteified(line))

    Filing = namedtuple('Filing','EIN, TaxPeriod, DLN, FormType, URL, OrganizationName, SubmittedOn, ObjectId, LastUpdated')
    dict_key = "Filings"+str(year)
    metros = [Filing(**k) for k in data[0][dict_key]]
    for i in metros:
        url = i.URL
        fname_list = url.split('/')
        fname = "/home/paperwhite/"+str(year)+"/"+fname_list[len(fname_list)-1]
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        response = urllib2.urlopen(url)
        data_file = response.read()


        # Write data to file
        file_1 = open(fname, 'w')
        file_1.write(data_file)
        file_1.close()


        #filename = wget.download(url, out='/home/paperwhite/irs-form-990-data/')
        
    
                                                                                
