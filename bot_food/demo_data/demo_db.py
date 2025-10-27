import os
import json

def load_json_files(folder_path):
    result = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            path = os.path.join(folder_path, filename)
            with open(path, 'r', encoding="utf-8") as f:
                result = json.load(f)
    return result 
folder_path = "demo_data"
data = load_json_files(folder_path)  
# print(data) 
# def load_images_from_database(json_file_path, images_folder):
#     """
#     Функция для загрузки данных из JSON-файла и возврата полного пути к изображениям.
    
#     :param json_file_path: Путь к JSON-файлу с данными о блюдах.
#     :param images_folder: Папка с изображениями.
#     :return: Словарь с результатами (ID блюда и путь к изображению).
#     """
#     # 1. Читаем данные из JSON-файла
#     with open(json_file_path, 'r', encoding='utf-8') as f:
#         menu_data = json.load(f)

#     # 2. Обрабатываем данные
#     results = {}
#     for dish in menu_data['dishes']:
#         # Формируем полный путь к изображению
#         image_name = dish['Image']
#         full_image_path = os.path.join(images_folder, image_name)
        
#         # Проверяем наличие изображения
#         if os.path.isfile(full_image_path):
#             results[dish['pk']] = full_image_path
#         else:
#             print(f"Изображение {image_name} не найдено.")

#     return results  

# json_file_path = "demo_data/database.json" 
# images_folder = "demo_data/static" 
# Images = load_images_from_database(json_file_path, images_folder)