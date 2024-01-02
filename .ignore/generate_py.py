import os

files = os.listdir()

for filename in files:
    if filename.endswith(".ipynb"):
        os.system(f"jupyter nbconvert --to script {filename}")

        
