import requests
import os
import csv

from dotenv import load_dotenv

class LPA:
    def __init__(self):
        load_dotenv()
        self.mdir = os.getenv('MDIR')
        
        self.source_dir = os.path.join(self.mdir, 'source')
        self.fi_filename = 'bank_mapp.csv'
        self.repfield_filename = 'field_mapp.csv'
        
        self.main_url = 'https://banks.data.fdic.gov/api/financials?filters'
        
        self.userinput_cert = ''
        self.userinput_daterange = ''
        self.ficert_list = self.load_fi_data()
    
        # self.url = ('https://banks.data.fdic.gov/api/financials?filters=ACTIVE:1 AND !(BKCLASS:NC) AND REPDTE:20220930&CERT=14' 
        #             'fields=CERT,RSSDHCR,NAMEFULL,CITY,STALP,ZIP,REPDTE,BKCLASS,NAMEHCR,OFFDOM,SPECGRP,SUBCHAPS,ESTYMD,INSDATE,EFFDATE,MUTUAL,PARCERT,TRUST,REGAGNT,INSAGNT1,FDICDBS,FDICSUPV,FLDOFF,FED,OCCDIST,OTSREGNM,OFFOA,CB,OBSDIR,NACDIR,CTDERGTY,CTDERBEN,RT,RTNVS,RTFFC,RTWOC,RTPOC,FX,FXNVS,FXFFC,FXSPOT,FXWOC,FXPOC,EDCM,OTHNVS,OTHFFC,OTHWOC,OTHPOC,UC,UCLOC,UCCRCD,UCCOMRE,UCCOMRES,UCCOMREU,UCSC,UCOTHER,UCOVER1,SCLENT,OTHOFFBS,PARTCONV,LOCFPSB,LOCFPSBK,LOCFSB,LOCFSBK,LOCPSB,LOCPSBK,LOCCOM&'
        #             'sort_by=REPDTE&sort_order=DESC'
        #             )

        # response = requests.get(self.url)
        # print(response.status_code)
        
    def load_fi_data(self):
        csv_mdir = os.path.join(self.source_dir, self.fi_filename)
        result = list()
        with open(csv_mdir, 'r', encoding='utf-8') as cf:
            data = cf.readlines()
            for x in data:
                result.append(x.strip())
        return result

    def load_fi_field_data(self):
        csv_mdir = os.path.join(self.source_dir, self.repfield_filename)
        result = list()
        with open(csv_mdir, 'r', encoding='utf-8') as cf:
            data = cf.readlines()
            for x in data:
                result.append(x)
        return result




    def lookup_fi_by_cert(self):
        userinput_cert = input('Please enter cert number for FI lookup\n')
        for x in self.ficert_list:
            if userinput_cert in x:
                print(x)
        return
    
    def lookup_fi_by_state(self):
        userinput_cert = input('Please enter state name for FI lookup\n')
        for x in self.ficert_list:
            if userinput_cert in x:
                print(x)
        return
    
    def set_daterange(self):
        return

def main():
    lpa = LPA()
    # lpa.load_fi_data()
    # lpa.lookup_fi_by_cert()
    lpa.load_fi_field_data()
    

if __name__ == '__main__':
    main()
    
        
