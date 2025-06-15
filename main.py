import csv
import os
import requests
import time
import re
import json

from classes.settings import FieldManager

class MainMenu(FieldManager):
    def __init__(self):
        super().__init__()
        
        self.main_url = 'https://banks.data.fdic.gov/api/financials' 
        
        self.main_menu = {1:['GETDATA', self.get_data],
                          2:['LOOKUPCERT', self.lookup_fi],
                          9:['OPENDIR', self.open_mdir],
                          0:['QUIT', exit],
                          }
        
        self.ficert_list = self.load_bank_mapp()  # loads code numbers for FDIC banks
        self.fireport_list = self.load_field_mapp()  # loads field mapping for request
        
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

        
        
def main():
    main_menu = MainMenu()
    main_menu.start_menu()
    
if __name__ == '__main__':
    main()
    
        