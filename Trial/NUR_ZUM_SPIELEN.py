from os import listdir
from os.path import isfile, join

mypath = 'C:/Users/Tom/OneDrive/Dokumente/Thomas/Aktien/datas/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

onlyfiles