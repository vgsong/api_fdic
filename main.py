import csv
import os
import requests
import time
import re
import json

from classes.settings import Settings

class FieldManager(Settings):
    def __init__(self):
        super().__init__()
        
        self.ficert_list = self.load_bank_mapp()  # loads code numbers for FDIC banks
        self.fireport_list = self.load_field_mapp()  # loads field mapping for request
        
        self.main_url = 'https://banks.data.fdic.gov/api/financials' 
        
        self.main_menu = {1:['GETDATA', self.get_data],
                          2:['LOOKUPCERT', self.lookup_fi],
                          9:['OPENDIR', self.open_mdir],
                          0:['QUIT', exit],
                          }


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

    def get_data(self):
        
        def get_report_name():
            fi_mapp = dict(enumerate(self.fireport_list.keys()))
            while True:
                print('\n----REPORT LIST----')
                for k, v in fi_mapp.items():
                    print('{}: {}'.format(k, v))
                try:
                    user_input = input('\nPlease select Report Name:\n')
                    return fi_mapp[int(user_input)]
                except Exception as e:
                    print(e)

        def get_cert_num():
            while True:
                try:
                    user_input = input('\nPlease select cert number:\n')
                    return user_input
                except Exception as e:
                    print(e)
        
        def get_date_range():
            while True:
                try:
                    user_input = input('\nPlease enter YYYYMMDD date or\n ' \
                                       'YYYYMMDDtoYYYYMMDD for date range:\n' \
                                       'Ex: 20220930\n'
                                       )
                                     
                    if re.match(r'20\d{2}\d{2}\d{2}|20\d{2}\d{2}\d{2}to20\d{2}\d{2}\d{2}', user_input) is None:
                        raise ValueError('Please enter date in correct format!')
                    else:
                        return user_input
                except Exception as e:
                    print(e)
            return
        
        print('Starting API request...')
        time.sleep(1)
        
        report_name = get_report_name()
        cert_num = get_cert_num()
        date_range = get_date_range()

        print('Obtaining report {}...'.format(report_name))
        print('For Bank Number: {}'.format(cert_num))        
        print('For the period: {}'.format(date_range))

        params = {'filters':'REPDTE:{} AND CERT:{}'.format(date_range, cert_num),
                  'fields': self.fireport_list[report_name],
                  'sort_order':'DESC',
                  'offset':'0',
                  'format':'csv',
                  'download':'true',
                  'filename':'data_file',                       
                  }
        
        response = requests.get(self.main_url, params=params)
        time.sleep(3)
        
        print(response.status_code)
        data = response.text.split('\n')
        
        with open(os.path.join(self.output_dir, 'data.csv'), 'w', newline='', encoding='utf-8') as cf:
            writer = csv.writer(cf, quoting=csv.QUOTE_ALL)
            for x in data:
                writer.writerow([x])
            
    def lookup_fi(self):
        while True:
            result = []
            userinput_cert = input('Please enter cert number or ' \
                                   'state name for FI lookup\n' \
                                   'or type exit to return to main menu\n'
                                   )
            
            if userinput_cert == 'exit':
                return
            else:
                result = [x for x in self.ficert_list if userinput_cert.upper() in x]
                print('found {} result(s)'.format(len(result)))
                if len(result) > 0:
                    print('Returning first 20 results:\n')
                    print('CERT, FINAME, LOCATION')
                    print('---------------------')
                    for x in result[:20]:
                        print(x)
                    print('-----------------')
                else:
                    continue

    def open_mdir(self):
        os.startfile(self.mdir)
        return

    def start_menu(self):
        while True:
            print('----MAIN MENU----')
            for k, v in self.main_menu.items():
                print('{}: {}'.format(k, v[0]))
            user_input = input('Please enter index num\n')
            try:
                self.main_menu.get(int(user_input),'')[1]()
            except ValueError as e:
                print(e)
                print('Please enter valid index number\n')

    def requests_test(self):
        # url = 'https://banks.data.fdic.gov/api/financials?filters=REPDTE:20220930&fields=CERT,RSSDHCR,NAMEFULL,CITY,STALP,ZIP,REPDTE,BKCLASS,NAMEHCR,OFFDOM,SPECGRP,SUBCHAPS,ESTYMD,INSDATE,EFFDATE,MUTUAL,PARCERT,TRUST,REGAGNT,INSAGNT1,FDICDBS,FDICSUPV,FLDOFF,FED,OCCDIST,OTSREGNM,OFFOA,CB,ASSET,CHBAL,CHBALNI,CHBALI,CHCIC,CHITEM,CHCOIN,CHUS,CHNUS,CHFRB,SC,SCUS,SCUST,SCUSO,SCASPNSUM,SCFMN,SCGNM,SCCOL,SCCPTG,SCCMOG,SCMUNI,SCDOMO,SCRMBPI,SCCMOS,SCABS,SCSFP,SCODOT,SCFORD,SCEQNFT,SCEQ,SCEQFV,SCHTMRES,SCTATFR,SCPLEDGE,SCMTGBK,SCGTY,SCODPC,SCODPI,SCCMPT,SCCMOT,SCHA,SCAF,SCRDEBT,SCPT3LES,SCPT3T12,SCPT3T5,SCPT5T15,SCPTOV15,SCO3YLES,SCOOV3Y,SCNM3LES,SCNM3T12,SCNM1T3,SCNM3T5,SCNM5T15,SCNMOV15,SC1LES,SCSNHAA,SCSNHAF,TRADE,TRREVALSUM,TRLREVAL,FREPO,LNLSNET,LNATRES,LNLSGR,LNCONTRA,LNLSGRS,LNRE,LNREDOM,LNRECONS,LNRENRES,LNREMULT,LNRERES,LNREAG,LNREFOR,LNAG,LNCI,LNCON,LNCRCD,LNCONRP,LNAUTO,LNCONOTH,LNOTCI,LNFG,LNMUNI,LNSOTHER,LS,LNCOMRE,LNRENUS,LNPLEDGE,RB2LNRES,LNLSSALE,LNEXAMT,LNRENROW,LNRENROT,LNRERSFM,LNRERSF2,LNRELOC,LNRERSF1,LNRECNFM,LNRECNOT,RSLNLTOT,RSLNREFM,RSLNLS,P3RSLNLT,P3RSLNFM,P3RSLNLS,P9RSLNLT,P9RSLNFM,P9RSLNLS,NARSLNLT,NARSLNFM,NARSLNLS,LNLSGRF,UNINCFOR,LNLSFOR,LNDEPAOBK,LNDEPCBF,LNDEPUSF,LNDEPFCF,LNAGFOR,LNCIFOR,LNCINUSF,LNCONFOR,LNFGFOR,LNMUNIF,LNOTHERF,LSFOR,LNRS3LES,LNRS3T12,LNRS1T3,LNRS3T5,LNRS5T15,LNRSOV15,LNOT3LES,LNOT3T12,LNOT1T3,LNOT3T5,LNOT5T15,LNOTOV15,LNRENR4,LNRENR1,LNRENR2,LNRENR3,LNCI4,LNCI1,LNCI2,LNCI3,LNREAG4,LNREAG1,LNREAG2,LNREAG3,LNAG4,LNAG1,LNAG2,LNAG3,LNRENR4N,LNRENR1N,LNRENR2N,LNRENR3N,LNCI4N,LNCI1N,LNCI2N,LNCI3N,LNREAG4N,LNREAG1N,LNREAG2N,LNREAG3N,LNAG4N,LNAG1N,LNAG2N,LNAG3N,PPPLNNUM,PPPLNBAL,PPPLNPLG,PPPLF1LS,PPPLFOV1,AVPPPPLG,MMLFBAL,AVMMLF,BKPREM,ORE,OREINV,OREOTH,ORERES,OREMULT,ORENRES,ORECONS,OREAG,OREOTHF,INTAN,INTANGW,INTANMSR,INTANOTH,AOA&sort_by=REPDTE&sort_order=DESC&limit=10&offset=0&format=csv&download=true&filename=data_file'
        url = 'https://banks.data.fdic.gov/api/financials?filters=REPDTE:20220930&fields=CERT,RSSDHCR,NAMEFULL,CITY,STALP,ZIP,REPDTE,BKCLASS,NAMEHCR,OFFDOM,SPECGRP,SUBCHAPS,ESTYMD,INSDATE,EFFDATE,MUTUAL,PARCERT,TRUST,REGAGNT,INSAGNT1,FDICDBS,FDICSUPV,FLDOFF,FED,OCCDIST,OTSREGNM,OFFOA,CB,ASSET,CHBAL,CHBALNI,CHBALI,CHCIC,CHITEM,CHCOIN,CHUS,CHNUS,CHFRB,SC,SCUS,SCUST,SCUSO,SCASPNSUM,SCFMN,SCGNM,SCCOL,SCCPTG,SCCMOG,SCMUNI,SCDOMO,SCRMBPI,SCCMOS,SCABS,SCSFP,SCODOT,SCFORD,SCEQNFT,SCEQ,SCEQFV,SCHTMRES,SCTATFR,SCPLEDGE,SCMTGBK,SCGTY,SCODPC,SCODPI,SCCMPT,SCCMOT,SCHA,SCAF,SCRDEBT,SCPT3LES,SCPT3T12,SCPT3T5,SCPT5T15,SCPTOV15,SCO3YLES,SCOOV3Y,SCNM3LES,SCNM3T12,SCNM1T3,SCNM3T5,SCNM5T15,SCNMOV15,SC1LES,SCSNHAA,SCSNHAF,TRADE,TRREVALSUM,TRLREVAL,FREPO,LNLSNET,LNATRES,LNLSGR,LNCONTRA,LNLSGRS,LNRE,LNREDOM,LNRECONS,LNRENRES,LNREMULT,LNRERES,LNREAG,LNREFOR,LNAG,LNCI,LNCON,LNCRCD,LNCONRP,LNAUTO,LNCONOTH,LNOTCI,LNFG,LNMUNI,LNSOTHER,LS,LNCOMRE,LNRENUS,LNPLEDGE,RB2LNRES,LNLSSALE,LNEXAMT,LNRENROW,LNRENROT,LNRERSFM,LNRERSF2,LNRELOC,LNRERSF1,LNRECNFM,LNRECNOT,RSLNLTOT,RSLNREFM,RSLNLS,P3RSLNLT,P3RSLNFM,P3RSLNLS,P9RSLNLT,P9RSLNFM,P9RSLNLS,NARSLNLT,NARSLNFM,NARSLNLS,LNLSGRF,UNINCFOR,LNLSFOR,LNDEPAOBK,LNDEPCBF,LNDEPUSF,LNDEPFCF,LNAGFOR,LNCIFOR,LNCINUSF,LNCONFOR,LNFGFOR,LNMUNIF,LNOTHERF,LSFOR,LNRS3LES,LNRS3T12,LNRS1T3,LNRS3T5,LNRS5T15,LNRSOV15,LNOT3LES,LNOT3T12,LNOT1T3,LNOT3T5,LNOT5T15,LNOTOV15,LNRENR4,LNRENR1,LNRENR2,LNRENR3,LNCI4,LNCI1,LNCI2,LNCI3,LNREAG4,LNREAG1,LNREAG2,LNREAG3,LNAG4,LNAG1,LNAG2,LNAG3,LNRENR4N,LNRENR1N,LNRENR2N,LNRENR3N,LNCI4N,LNCI1N,LNCI2N,LNCI3N,LNREAG4N,LNREAG1N,LNREAG2N,LNREAG3N,LNAG4N,LNAG1N,LNAG2N,LNAG3N,PPPLNNUM,PPPLNBAL,PPPLNPLG,PPPLF1LS,PPPLFOV1,AVPPPPLG,MMLFBAL,AVMMLF,BKPREM,ORE,OREINV,OREOTH,ORERES,OREMULT,ORENRES,ORECONS,OREAG,OREOTHF,INTAN,INTANGW,INTANMSR,INTANOTH,AOA&sort_by=REPDTE&sort_order=DESC&limit=10&offset=0&format=csv&download=true&filename=data_file'
        
        main_url = 'https://banks.data.fdic.gov/api/financials' 
        
        fields = 'CERT,RSSDHCR,NAMEFULL,CITY,STALP,ZIP,REPDTE,BKCLASS,NAMEHCR,OFFDOM,SPECGRP,SUBCHAPS,ESTYMD,INSDATE,EFFDATE,MUTUAL,PARCERT,TRUST,REGAGNT,INSAGNT1,FDICDBS,FDICSUPV,FLDOFF,FED,OCCDIST,OTSREGNM,OFFOA,CB,ASSET,CHBAL,CHBALNI,CHBALI,CHCIC,CHITEM,CHCOIN,CHUS,CHNUS,CHFRB,SC,SCUS,SCUST,SCUSO,SCASPNSUM,SCFMN,SCGNM,SCCOL,SCCPTG,SCCMOG,SCMUNI,SCDOMO,SCRMBPI,SCCMOS,SCABS,SCSFP,SCODOT,SCFORD,SCEQNFT,SCEQ,SCEQFV,SCHTMRES,SCTATFR,SCPLEDGE,SCMTGBK,SCGTY,SCODPC,SCODPI,SCCMPT,SCCMOT,SCHA,SCAF,SCRDEBT,SCPT3LES,SCPT3T12,SCPT3T5,SCPT5T15,SCPTOV15,SCO3YLES,SCOOV3Y,SCNM3LES,SCNM3T12,SCNM1T3,SCNM3T5,SCNM5T15,SCNMOV15,SC1LES,SCSNHAA,SCSNHAF,TRADE,TRREVALSUM,TRLREVAL,FREPO,LNLSNET,LNATRES,LNLSGR,LNCONTRA,LNLSGRS,LNRE,LNREDOM,LNRECONS,LNRENRES,LNREMULT,LNRERES,LNREAG,LNREFOR,LNAG,LNCI,LNCON,LNCRCD,LNCONRP,LNAUTO,LNCONOTH,LNOTCI,LNFG,LNMUNI,LNSOTHER,LS,LNCOMRE,LNRENUS,LNPLEDGE,RB2LNRES,LNLSSALE,LNEXAMT,LNRENROW,LNRENROT,LNRERSFM,LNRERSF2,LNRELOC,LNRERSF1,LNRECNFM,LNRECNOT,RSLNLTOT,RSLNREFM,RSLNLS,P3RSLNLT,P3RSLNFM,P3RSLNLS,P9RSLNLT,P9RSLNFM,P9RSLNLS,NARSLNLT,NARSLNFM,NARSLNLS,LNLSGRF,UNINCFOR,LNLSFOR,LNDEPAOBK,LNDEPCBF,LNDEPUSF,LNDEPFCF,LNAGFOR,LNCIFOR,LNCINUSF,LNCONFOR,LNFGFOR,LNMUNIF,LNOTHERF,LSFOR,LNRS3LES,LNRS3T12,LNRS1T3,LNRS3T5,LNRS5T15,LNRSOV15,LNOT3LES,LNOT3T12,LNOT1T3,LNOT3T5,LNOT5T15,LNOTOV15,LNRENR4,LNRENR1,LNRENR2,LNRENR3,LNCI4,LNCI1,LNCI2,LNCI3,LNREAG4,LNREAG1,LNREAG2,LNREAG3,LNAG4,LNAG1,LNAG2,LNAG3,LNRENR4N,LNRENR1N,LNRENR2N,LNRENR3N,LNCI4N,LNCI1N,LNCI2N,LNCI3N,LNREAG4N,LNREAG1N,LNREAG2N,LNREAG3N,LNAG4N,LNAG1N,LNAG2N,LNAG3N,PPPLNNUM,PPPLNBAL,PPPLNPLG,PPPLF1LS,PPPLFOV1,AVPPPPLG,MMLFBAL,AVMMLF,BKPREM,ORE,OREINV,OREOTH,ORERES,OREMULT,ORENRES,ORECONS,OREAG,OREOTHF,INTAN,INTANGW,INTANMSR,INTANOTH,AOA'
        
    
        params_test = {'filters':'REPDTE:{} AND CERT:{}'.format('20220930','14'),
                       'fields': fields,
                       'sort_order':'DESC',
                    #    'limit':'10000',
                       'offset':'0',
                       'format':'csv',
                       'download':'true',
                       'filename':'data_file',                       
                    }
        

        # response = [json.loads(line) for line in .text.splitlines()]
        response = requests.get(url)
        # response = response.text.split('\n')
        response = response.text.split('\n')
        # response = requests.get(main_url, params=params_test)
        print(response)
        with open(os.path.join(self.output_dir, 'data_test.csv'), 'w', encoding='utf-8', newline='') as cf:
            writer = csv.writer(cf, quoting= csv.QUOTE_ALL)
            for x in response:
                writer.writerow([x])
        # print(response.text)
        
        
def main():
    fm = FieldManager()
    fm.start_menu()
    # fm.requests_test()
    
if __name__ == '__main__':
    main()
    
        