import pandas as pd
import re

class Downstream():
  def __init__(self, df, thresh):
    self.df = df
    self.thresh = thresh

  def _trim_taxa_names(self, x):
    '''Removes leading characters before taxa ID e.g. s__ '''
    match = re.sub(r'^[kpcofgs]__',"",str(x))
    return match
 
  def _get_taxa_columns(self,df,rank):
    '''Splits ID into taxanomic ranks to make taxa table''' 
    df_taxa = df['ID'].str.split('|',expand=True)
    taxa_cols = ["Kingdom","Phylum","Class","Order","Family","Genus","Species","Strain"]
    taxa_dict = {'Kingdom':1,"Phylum":2,"Class":3,"Order":4,"Family":5,"Genus":6,"Species":7,"Strain":8}
    value = taxa_dict.get(rank)
    taxa_cols=taxa_cols[0:value]
    df_taxa.columns=taxa_cols
    for col in df_taxa.columns:
        df_taxa[col]=df_taxa[col].apply(self._trim_taxa_names)    
    otu_index = []
    for i in range(0, len(df)):
        otu_index.append("Otu"+str(i))
    df_taxa['Otu']=otu_index 
    taxa_cols=[col for col in df_taxa.columns if 'Otu' not in col]
    for col in taxa_cols:
        df_taxa.at[df_taxa.index[-1], col] = 'Other'
    return df_taxa

  
  def _create_other(self,df,thresh):
    '''
    Creates other classification, for species below the given threshold and returns a new df
    '''
    # grab id column
    id_col = df['ID']
    less_than_thresh=df[(df.select_dtypes(include='float64') <= thresh)].drop(columns='ID').dropna()
    less_than_thresh.reset_index(drop=True, inplace=True)

    greater_than_thresh=df[(df.select_dtypes(include='float64') > thresh)].dropna(how='all').fillna(0).drop(columns='ID')
    greater_than_thresh['ID'] = id_col
    greater_than_thresh.reset_index(drop=True, inplace=True)
    other_row = pd.DataFrame([less_than_thresh.sum()])
    other_row['ID'] = 'Other'
    new_df = pd.concat([greater_than_thresh, other_row])
    new_df.reset_index(drop=True, inplace=True)

    return new_df

  def _create_species_col(self,df):
    '''
    Grabs taxa from species, converts it to alist
    '''
    taxa = self._get_taxa_columns(df, 'Species')
    species = taxa['Species'].to_list()
    df.drop('ID', axis=1, inplace=True)
    df['Species'] = species
    df.set_index('Species', inplace=True)
    return df
  
  def run(self):
    df = self._create_other(self.df, self.thresh)
    final_df = self._create_species_col(df)
    return final_df
