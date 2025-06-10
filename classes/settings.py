import os
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        load_dotenv()
        self.mdir = os.getenv('MDIR')
        self.source_dir = os.path.join(self.mdir, 'source')
        self.fi_filename = 'bank_mapp.csv'
        self.repfield_filename = 'field_mapp.csv'
        
        