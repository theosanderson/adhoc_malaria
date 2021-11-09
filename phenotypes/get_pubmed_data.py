from collections import defaultdict
import pandas

data = pandas.read_csv('from_rmgmdb.csv')

pubmed_ids = data['reference_pubmed1'].unique()

from Bio import Entrez

Entrez.email = "theo@theo.io"


def get_pub_date(pubmed_id):
    try:
        handle = Entrez.esummary(db="pubmed", id=pubmed_id)
        record = Entrez.read(handle)
        handle.close()
        return (record[0]["PubDate"])
    except RuntimeError:
        print("error")
        return None


import tqdm
# get date for each ID
pubmed_to_date = defaultdict(None)
for pubmed_id in tqdm.tqdm(pubmed_ids):
    pubmed_to_date[pubmed_id] = get_pub_date(pubmed_id)

data['reference_pubmed_date'] = data['reference_pubmed1'].map(pubmed_to_date)
data.to_csv('from_rmgmdb_with_pubmed_date.csv', index=False)