import re, os

# Load the files
ignoreFiles = set([".DS_Store","LICENSE","README.md"])
qts_texts = {}
for root, dirs, files in os.walk("QTS_authors_clean"):
    for filename in files:
        if filename not in ignoreFiles:
            with open(os.path.join(root,filename)) as rf:
                title = filename[:-4] # Remove the file extension
                corpus = rf.read()
                qts_texts[title] = corpus

qts_authors = qts_texts.keys()

# Get a list of the authors' corpora
corpora = []
for i, title in enumerate(qts_authors):
    corpora.append(qts_texts[title])

# Get length of corpora
length = [len(text.replace('、', '')) for text in corpora]

# Find instances of double draft (雙擬), or 'dds'.
regex = r'、.{0,5}([^、\s]+)[^、]{1,6}\1.{0,5}、'
    
dds =[]
for i in corpora:
    result = re.finditer(regex, i)
    temp_dds = []
    for match in result:
        temp_dds.append(match.group())
    dds.append(temp_dds)

total_dds = [len(dd) for dd in dds]

#double draft ratio
dd_ratio = [int(r)/int(l) for r,l in zip(total_dds, length)]

#export to CSV
write_strings = [f"{qts_authors}, {total_dds}, {length}, {dd_ratio}"
    for qts_authors, total_dds, length, dd_ratio
    in zip(qts_authors, total_dds, length, dd_ratio)]
with open('QTS_DD_Ratio.csv', 'w') as wf:
    wf.write('\n'.join(write_strings))