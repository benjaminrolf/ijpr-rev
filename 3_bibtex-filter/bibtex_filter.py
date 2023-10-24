import pandas as pd
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

'''creates a new bibtex file that only contains publications that are relevant
   according to the stage 2 decision'''

# read excel and bibtex files
pubs = pd.read_excel('2023-10-13 PUBLICATIONS JOURNALDATA.xlsx')

with open('0_resources/2023-10-06 Scopus Export.bib', encoding='utf8') as f:
    parser = BibTexParser()
    parser.customization = convert_to_unicode
    scopus_bib = bibtexparser.load(f, parser=parser)

with open('0_resources/2023-10-06 Web of Science Export 1.bib', encoding='utf8') as f:
    parser = BibTexParser()
    parser.customization = convert_to_unicode
    wos_bib = bibtexparser.load(f, parser=parser)

# filter relevant publications
pubs_include = pubs[pubs['Relevant'] == 'yes']

# create new bibtex database
bibtex_keep = BibDatabase()
bibtex_keep.entries = []

# iterate included publications
for pub in pubs_include.iterrows():
    key = pub[1]['Bibtex Key']
    source = pub[1]['Source']

    # choose source
    if source == 'Scopus':
        entry = scopus_bib.entries_dict[key]
    elif source == 'Web of Science':
        entry = wos_bib.entries_dict[key]
    
    # append to new bibtex database
    bibtex_keep.entries.append(entry)

# save new bibtex file
writer = BibTexWriter()
with open('0_resources/Stage2_Bib.bib', 'w', encoding='utf8') as f:
    f.write(writer.write(bibtex_keep))