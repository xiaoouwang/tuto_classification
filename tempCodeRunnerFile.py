
import os
path = "/Users/becca/Documents/nlp/M2Nanterre/coursM2/coursAlice/corpus/societe"
#

for file in os.listdir(path):
    file_path = os.path.join(path, file)
    with open(file_path, "r", encoding="utf-8") as f:
        new_text = f.read()[7:]
        with open(file_path, 'w') as new_f:
            new_f.write(new_text)
