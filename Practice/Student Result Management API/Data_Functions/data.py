import json

def load_data():
    with open("student.json","r") as f:
        data = json.load(f)
    return data

def save_data():
    with open("student.json","w") as g:
        json.dump(g)
    