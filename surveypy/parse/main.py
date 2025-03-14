import pandas as pd
from typing import Literal

class SourceData:
    def __init__(self, file_path: str, type: Literal['excel', 'csv']):
        self.file_path = file_path
        self.type = type
        self.encode_mapping = {}
        self.cat_cols = []
        
    def initialize(self):
        if self.type == 'excel':
            self.raw_data = pd.read_excel(self.file_path)
            self._parse()
            
    def _parse(self):
        self.cat_cols = self.raw_data.select_dtypes(include=['object']).columns
        for col in self.cat_cols:
            self.raw_data[col] = self.raw_data[col].astype('category')
            self.encode_mapping[col] = dict(enumerate(self.raw_data[col].cat.categories))
        
    def convert_df(self, to=Literal['text', 'num']):
        if to == 'num':
            for col in self.cat_cols:
                self.raw_data[col] = self.raw_data[col].cat.codes
            