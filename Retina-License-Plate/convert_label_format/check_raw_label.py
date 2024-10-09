from os import listdir
from os.path import join
from tqdm import tqdm

labeldir = './label_raw'



for labelfn in tqdm(listdir(labeldir)):
    with open(join(labeldir, labelfn), mode = 'r') as f:
        lines = f.readlines()
        if len(lines) != 5:
            print(labelfn)

print('Labels in the same format')