import os
import json


def load_json_files(folder_path):
    """Загружает все JSON-файлы из указанной папки и объединяет их в один словарь."""
    result = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            path = os.path.join(folder_path, filename)
            with open(path, 'r', encoding="utf-8") as f:
                result = json.load(f)
    return result 


folder_path = "demo_data"
data = load_json_files(folder_path)  
