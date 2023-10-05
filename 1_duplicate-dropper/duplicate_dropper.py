import pandas as pd
import re


'''aggregates the exports from Scopus and Web of Science in a single file and
   drops duplicates'''

# import publications
scopus = pd.read_excel('0_resources/Scopus_Export.xlsx')
wos = pd.read_excel('0_resources/WoS_Export.xlsx')
base = pd.read_excel('0_resources/first_search.xlsx')

# Create consistent name space
scopus.rename(
    columns={'Title': 'Article title', 'Author Keywords': 'Keywords', 
             'Correspondence Address': 'Correspondence', 'Page start': 'Start page',
             'Page end': 'End page', 'Cited by': 'Times cited'},
    inplace=True
)

wos.rename(
    columns={'Publication Year': 'Year', 'Author Keywords': 'Keywords',
             'Email Addresses': 'Correspondence',
             'Times Cited, All Databases': 'Times cited', 'DOI Link': 'Link',
             'Cited References': 'References', 'Start Page': 'Start page',
             'End Page': 'End page', 'Article Title': 'Article title',
             'Source Title': 'Source title'},
    inplace=True
)

# Add additional information
scopus['Source'] = 'Scopus'
wos['Source'] = 'Web of Science'
scopus['Bibtex key'] = ''
wos['Bibtex key'] = ''

# create empty dataframe for publications
columns = [
        'Year', 'Authors', 'Article title', 'DOI', 'Source title', 'Volume',
        'Issue', 'Start page', 'End page', 'Keywords', 'Times cited',
        'Affiliations', 'Link', 'Correspondence', 'References', 'Source',
        'Bibtex key', 'Abstract'
]
pubs = pd.DataFrame(columns=columns)

## inclusion decision
#'Spacer 1', 'Relevant', 'Accessible', 'Full text relevant',
## topic
#'Spacer 2', 'Description',
## supply chain driver
#'Spacer 3', 'Supply chain driver', 'Subdriver', 'Aim',
## algorithm
#'Spacer 4', 'Role of algorithm', 'Algo class 1', 'Algo group 1',
#'Algo subgroup 1', 'Algo name 1', 'Algo class 2', 'Algo group 2',
#'Algo subgroup 2', 'Algo name 2', 'Algo class 3', 'Algo group 3',
#'Algo subgroup 3', 'Algo name 3', 'Algo class 4', 'Algo group 4',
#'Algo subgroup 4', 'Algo name 4', 'Algo class 5', 'Algo group 5',
#'Algo subgroup 5', 'Algo name 5', 'Algo class 6', 'Algo group 6',
#'Algo subgroup 6', 'Algo name 6', 'Algo class 7', 'Algo group 7',
#'Algo subgroup 7', 'Algo name 7',
## data source
#'Spacer 5', 'Data source', 'Data class', 'Data subclass',
## idustry
#'Spacer 6', 'ChatGPT input', 'ISIC', 'Section', 'Division', 'Group',
#'Class',
## comments
#'Spacer 7', 'Comments'

# Concatenate publications
pubs = pd.concat([scopus[columns], wos[columns]], ignore_index=True)

# Creates a string of all uppercase letters and removes special characters
# (main reason why duplicates are not recognized)
pubs['Title Upper'] = pubs['Article title'].str.upper()
pubs['Title Upper'] = pubs['Title Upper'].apply(lambda x: re.sub('[^A-Za-z0-9]+', '', x))

# Remove duplicates
pubs.drop_duplicates(
    subset=['DOI', 'Title Upper'],
    keep='first',
    inplace=True,
    ignore_index=True
)
#pubs.drop(columns=['Title Upper'], inplace=True)

# Match publications with previusly evaluated publications
pubs = pd.merge(pubs, base, on=['DOI', 'Article title'], how='left')

# Sorts publications by authors and title
pubs.sort_values(by=['Authors', 'Article title'], inplace=True, ignore_index=True)

# Print statistics
print('Number of Publications in Scopus: ', len(scopus))
print('Number of Publications in Web of Science: ', len(wos))
print('Number of Publications without Duplicates: ', len(pubs))
print('Number of Duplicates: ', len(scopus) + len(wos) - len(pubs))

# Create csv file
pubs.to_excel('0_resources/publications.xlsx', index=True)