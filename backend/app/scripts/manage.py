from app.scripts.process import Process
from app.scripts.downstream import Downstream
import shutil
import pandas as pd

class Manage():
    def __init__(self, jobs, uploads_dir, results_dir, thresh):
        self.jobs = jobs
        self.uploads_dir = uploads_dir
        self.results_dir = results_dir
        self.results = []
        self.thresh = thresh
    
    def read(self,filename, skip=3, delimeter='\t'):
        '''
        reads in mpa output, and returns species only relative abundance
        '''
        df = pd.read_table(filename, sep=delimeter, skiprows=skip)
        sample_name = filename.split('.')[0]
        df.rename(columns={'#clade_name': 'ID', 'relative_abundance':sample_name},      inplace=True)
        df = df[(df['ID'].str.lower().str.contains('s__'))]
        df.reset_index(drop=True,inplace=True)
        df.drop(columns={'NCBI_tax_id', 'additional_species'}, inplace=True)
        return df

    def merge(self, df_lst):
        '''
        merges dataframes
        '''
        df = pd.concat(df_lst)
        df.reset_index(drop=True,inplace=True)
        df.fillna(0,inplace=True)
        return df
    
    def process_dfs(self, dfs):
        '''
        takes a list of dfs and merges them
        '''
        if len(dfs) >1:
          df_lst = []
          for df in dfs:
            segment = self.read(df)
            df_lst.append(segment)
          return self.merge(df_lst)
        else:
          segment = self.read(dfs[0])
          return segment
    
    async def run(self):
        for job in self.jobs:
            process = Process(job['inp'], self.results_dir, job['input_type'], job['filename'])
            await process.run()
            self.results.append(process.mpa_out)

        shutil.rmtree(self.uploads_dir)

        samples = [x['inp'] for x in self.jobs]
        matrx = self.process_dfs(samples)
        downstream = Downstream(matrx, self.thresh)

        data = downstream.run()
        return data