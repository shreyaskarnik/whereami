import os
import urllib

print("Downloading Dataset")
path = 'https://s3.amazonaws.com/mmcommons-tutorial/models/'
model_path = './model/'
if not os.path.exists(model_path):
    os.mkdir(model_path)
urllib.urlretrieve(path + 'RN101-5k500-symbol.json',
                   model_path + 'RN101-5k500-symbol.json')
urllib.urlretrieve(path + 'RN101-5k500-0012.params',
                   model_path + 'RN101-5k500-0012.params')
print("Download finished")
