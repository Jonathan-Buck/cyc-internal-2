import os
from pathlib import Path

dirpath =  os.path.dirname(os.path.realpath(__file__))

# Change the current working directory
os.chdir(dirpath)

os.system("gdown https://drive.google.com/drive/folders/1LEjAo7Oz7yse8YlzSHes9kp_rwCw8qny?usp=share_link -O interview_data --folder")

os.system("python new.py")

