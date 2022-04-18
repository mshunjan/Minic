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
    
    def _read(self,file_dir, sample_name, skip=3, delimeter='\t'):
        '''
        reads in mpa output, and returns species only relative abundance
        '''
        df = pd.read_table(file_dir, sep=delimeter, skiprows=skip)
        df.rename(columns={'#clade_name': 'ID', 'relative_abundance':sample_name},      inplace=True)
        df = df[(df['ID'].str.lower().str.contains('s__'))]
        df.reset_index(drop=True,inplace=True)
        df.drop(columns={'NCBI_tax_id', 'additional_species'}, inplace=True)
        return df

    def _merge(self, df_lst):
        '''
        merges dataframes
        '''
        df = pd.concat(df_lst)
        df.reset_index(drop=True,inplace=True)
        df.fillna(0,inplace=True)
        return df
    
    def _process_files(self, files):
        '''
        takes a list of files, reads them in as dataframes and merges them
        '''
        if len(files) >1:
            df_lst = []
            for file in files:
                segment = self._read(file_dir=file['file_dir'], sample_name=file['sample_name'])
                df_lst.append(segment)
            merged =  self._merge(df_lst)
            return merged
        else:
            segment = self._read(files[0]['file_dir'], files[0]['sample_name'])
            return segment
    
    async def run(self):
        for job in self.jobs:
            process = Process(job['inp'], self.results_dir, job['input_type'], job['filename'])
            await process.run()
            self.results.append({"file_dir": process.mpa_out, "sample_name": job['filename']})
            processed = [x['sample_name'] for x in self.results]
            print(f'processed {processed} so far')

        shutil.rmtree(self.uploads_dir)

        merged = self._process_files(self.results)
        downstream = Downstream(merged, self.thresh)

        data = downstream.run()
        shutil.rmtree(self.results_dir)
        print(data)
        return data