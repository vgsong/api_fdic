import csv
import os
import requests
import re
import time

from classes.settings import Settings
from collections import defaultdict


class FieldManager(Settings):
    def __init__(self):
        super().__init__()
        
        self.userinput_cert = '14' 
        self.userinput_daterange = '20221231'  # YYYYMMDD
        
        self.ficert_list = self.load_bank_mapp()  # loads code numbers for FDIC banks
        self.fireport_list = self.load_field_mapp()  # loads field mapping for request
        
        
        self.main_url = 'https://banks.data.fdic.gov/api/financials' 
        self.params = {'filters':'REPDTE:20220930&CERT=14',
                       'fields': 'CERT,RSSDHCR,NAMEFULL,CITY,STALP,ZIP,REPDTE,BKCLASS,NAMEHCR,OFFDOM,SPECGRP,SUBCHAPS,ESTYMD,INSDATE,EFFDATE,MUTUAL,PARCERT,TRUST,REGAGNT,INSAGNT1,FDICDBS,FDICSUPV,FLDOFF,FED,OCCDIST,OTSREGNM,OFFOA,CB,OBSDIR,NACDIR,CTDERGTY,CTDERBEN,RT,RTNVS,RTFFC,RTWOC,RTPOC,FX,FXNVS,FXFFC,FXSPOT,FXWOC,FXPOC,EDCM,OTHNVS,OTHFFC,OTHWOC,OTHPOC,UC,UCLOC,UCCRCD,UCCOMRE,UCCOMRES,UCCOMREU,UCSC,UCOTHER,UCOVER1,SCLENT,OTHOFFBS,PARTCONV,LOCFPSB,LOCFPSBK,LOCFSB,LOCFSBK,LOCPSB,LOCPSBK,LOCCOM',
                       'sort_order':'[DESC]',
                       }
        
        
        
        # self.url = ('https://banks.data.fdic.gov/api/financials?filters=ACTIVE:1 AND !(BKCLASS:NC) AND REPDTE:20220930&CERT=14' 
        #             'fields=CERT,RSSDHCR,NAMEFULL,CITY,STALP,ZIP,REPDTE,BKCLASS,NAMEHCR,OFFDOM,SPECGRP,SUBCHAPS,ESTYMD,INSDATE,EFFDATE,MUTUAL,PARCERT,TRUST,REGAGNT,INSAGNT1,FDICDBS,FDICSUPV,FLDOFF,FED,OCCDIST,OTSREGNM,OFFOA,CB,OBSDIR,NACDIR,CTDERGTY,CTDERBEN,RT,RTNVS,RTFFC,RTWOC,RTPOC,FX,FXNVS,FXFFC,FXSPOT,FXWOC,FXPOC,EDCM,OTHNVS,OTHFFC,OTHWOC,OTHPOC,UC,UCLOC,UCCRCD,UCCOMRE,UCCOMRES,UCCOMREU,UCSC,UCOTHER,UCOVER1,SCLENT,OTHOFFBS,PARTCONV,LOCFPSB,LOCFPSBK,LOCFSB,LOCFSBK,LOCPSB,LOCPSBK,LOCCOM&'
        #             'sort_by=REPDTE&sort_order=DESC'
        #             )

        # response = requests.get(self.url)
        # print(response.status_code)
        

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
        fresult = defaultdict()
        
        for x, y in fdata:
            fresult[x] = y
        
        return fresult

    def lookup_fi(self):
        while True:
            result = []
            
            userinput_cert = input('Please enter cert number or state name for FI lookup\n' \
                                   'or type exit to quit\n'
                                  )
            
            if userinput_cert == 'exit':
                return

            else:
                result = [x for x in self.ficert_list if userinput_cert in x]      

                print('found {} result(s)'.format(len(result)))
                print('Returning first 10 results:\n')
                print('CERT, FINAME, LOCATION')
                print('---------------------')
                
                for x in result[:10]:
                    print(x)
                print('-----------------')
                     
                continue

    def set_daterange(self):
        return

    def get_data(self):
        response = requests.get(self.main_url, params=self.params)
        time.sleep(3)
        print(response.url)
        
        return

def main():
    fm = FieldManager()
    # fm.load_field_mapp()
    # fm.lookup_fi()
    # print(fm)
    # print(x for x in str(fm))
if __name__ == '__main__':
    main()
    
        