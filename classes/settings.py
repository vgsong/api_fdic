import csv
import os
import re
import time

import requests

from dotenv import load_dotenv


class Settings:
    def __init__(self):
        load_dotenv()
        self.mdir = os.getenv('MDIR')
        self.source_dir = os.path.join(self.mdir, 'source')
        self.output_dir = os.path.join(self.mdir, 'output')
        self.fi_filename = 'bank_mapp.csv'
        self.repfield_filename = 'field_mapp.csv'
        
class FieldManager(Settings):
    def __init__(self):
        super().__init__()
        self.ficert_list = self.load_bank_mapp()  # loads code numbers for FDIC banks
        self.fireport_list = self.load_field_mapp()  # loads field mapping for request
        
    def load_bank_mapp(self):
        # loads source/bank_mapp.csv
        csv_mdir = os.path.join(self.source_dir, self.fi_filename)
        result = list()
        with open(csv_mdir, 'r', encoding='utf-8') as cf:
            data = cf.readlines()
            for x in data:
                result.append(x.strip())
        return result

    def load_field_mapp(self):
        csv_mdir = os.path.join(self.source_dir, self.repfield_filename)
        category_list = list()
        report_list = list()
        field_list = list()
        
        with open(csv_mdir, 'r', encoding='utf-8') as cf:
            data = cf.readlines()
            for x in data[1:]:
                category_list.append(x.split(',')[0])
                report_list.append(x.split(',')[1])
                field_list.append(x.split('"')[1])
        
        fdata = zip(report_list, field_list)
        fresult = {}
        
        for x, y in fdata:
            fresult[x] = y
        
        return fresult
