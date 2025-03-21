import urllib.request
import os
from datetime import datetime
import hashlib
import pandas as pd

def calculate_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def download_data(region_ID):
    url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={region_ID}&year1=1981&year2=2024&type=Mean"
    current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    csv_file_path = f'{dir_for_data}/NOAA_ID_{region_ID}_{current_datetime}.csv'
    
    try:
        vhi_url = urllib.request.urlopen(url)
        # Записуємо нові дані у файл
        with open(csv_file_path, 'wb') as new_file:
            new_file.write(vhi_url.read())

        # Обчислюємо хеш нового файлу
        new_file_hash = calculate_file_hash(csv_file_path)

        # Перевіряємо, чи існує csv-файл з ідентичним вмістом
        region_file_found = False
        for existing_file in os.listdir(dir_for_data):
            existing_file_path = f"{dir_for_data}/{existing_file}"

            if os.path.isfile(existing_file_path):
                if existing_file_path != csv_file_path:
                    existing_file_hash = calculate_file_hash(existing_file_path)

                    if existing_file_hash == new_file_hash:
                        print(f"VHI for region {region_ID} is already up to date in {existing_file_path}")
                        os.remove(csv_file_path)  # Видаляємо новий файл, якщо знайдений файл з ідентичним хешем
                        region_file_found = True
                        break

        # Якщо дані нові, створюємо новий файл
        if not region_file_found:
            print(f"Created csv-file for VHI in path: {csv_file_path}")
                
    except Exception as e:
        print(f"Error downloading VHI for region {region_ID}: {e}")

dir_for_data = "VHI_data"
if not os.path.exists(dir_for_data):
    os.makedirs(dir_for_data)

# Завантажуємо дані кожної адмін. одиниці України, з індексом 1-27
for i in range(1, 28):
    download_data(i)

import os
import pandas as pd

def load_data_from_directory(dir_for_data):
    # Імена стовпців повинні бути зрозумілими та без спеціальних символів
    column_names = ["Year", "Week", "SMN", "SMT", "VCI", "TCI", "VHI", "Region"]
    combined_data = pd.DataFrame(columns=column_names)

    # Ініціалізуємо лічильники початкової кількості рядків і кінцевої
    total_initial_rows = 0
    total_final_rows = 0
    
    # Зчитаємо файли з директорії
    filenames = os.listdir(dir_for_data)

    for filename in filenames:
        # Перевіряємо, чи є файл CSV
        if not filename.endswith(".csv"):
            continue

        file_path = os.path.join(dir_for_data, filename)

        # Читання CSV файлу, пропускаємо перші 2 рядки
        df = pd.read_csv(file_path, skiprows=2, names=column_names)

        # Очищення стовпця "Year" від небажаних тегів
        df["Year"] = df["Year"].astype(str).str.replace('<tt><pre>', '').str.replace('</pre></tt>', '')
        
        # Перетворюємо стовпець Year на числовий тип
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

        # Дістаємо Region_ID з імені файлу
        parts = filename.split('_')
        if len(parts) > 2 and parts[2].isdigit():
            region_id = int(parts[2])
        else:
            print(f"\nSkipped file: {filename}\n")
            continue  # Якщо ID не є числом, пропускаємо файл

        df["Region"] = region_id

        # Кількість початкових рядків
        initial_rows = len(df)
        total_initial_rows += initial_rows
        
        # Видаляємо записи, де у колонці VHI значення NaN
        df = df.drop(df.loc[df['VHI'] == -1].index).dropna()
        
        # Кількість рядків після очищення
        final_rows = len(df)
        total_final_rows += final_rows
        
        # Об'єднуємо дані
        combined_data = pd.concat([combined_data, df], ignore_index=True)
            
    # Обчислення відсотка видалених даних
    removed_percentage = ((total_initial_rows - total_final_rows) / total_initial_rows) * 100
    print(f"Removed {removed_percentage:.2f}% corrupted data\n")

    return combined_data

# Завантажуємо дані з директорії
combined_data = load_data_from_directory(dir_for_data)
combined_data_sorted = combined_data.sort_values(by=["Year", "Region"], ascending=[True, True])

# Зберігаємо результат у CSV файл
output_path = f"{dir_for_data}/NOAA_Ukraine.csv"
combined_data_sorted.to_csv(output_path, index=False)

# Відповідність старих індексів (NOAA) новим українським
region_index_eng_to_ukr = {
    1: 24,  # Cherkasy -> Черкаська
    2: 26,  # Chernihiv -> Чернігівська
    3: 25,  # Chernivtsi -> Чернівецька
    4: 27,  # Crimea -> Республіка Крим
    5: 3,   # Dnipropetrovs'k -> Дніпропетровська
    6: 4,   # Donets'k -> Донецька
    7: 8,   # Ivano-Frankivs'k -> Івано-Франківська
    8: 21,  # Kharkiv -> Харківська
    9: 22,  # Kherson -> Херсонська
    10: 23, # Khmelnyts'kyi -> Хмельницька
    11: 10, # Kiev -> Київська
    12: 9,  # Kiev City -> Київ
    13: 11, # Kirovohrad -> Кіровоградська
    14: 12, # Luhans'k -> Луганська
    15: 13, # L'viv -> Львівська
    16: 14, # Mykolaiv -> Миколаївська
    17: 15, # Odessa -> Одеська
    18: 16, # Poltava -> Полтавська
    19: 17, # Rivne -> Рівненська
    20: 18, # Sevastopol' -> Севастополь
    21: 19, # Sumy -> Сумська
    22: 20, # Ternopil' -> Тернопільська
    23: 6,  # Transcarpathia (Zakarpattia) -> Закарпатська
    24: 1,  # Vinnytsia -> Вінницька
    25: 2,  # Volyn -> Волинська
    26: 7,  # Zaporizhzhia -> Запорізька
    27: 5   # Zhytomyr -> Житомирська
}

def update_region_indexes(df):
    df["Region"] = df["Region"].map(region_index_eng_to_ukr)
    return df

# Оновлення індексів областей
combined_data_updated = update_region_indexes(combined_data)
combined_data_updated_sorted = combined_data.sort_values(by=["Year", "Region"])

# Збереження оновлених даних
combined_data_updated_sorted.to_csv(f"{dir_for_data}/NOAA_Ukraine_Updated.csv", index=False)



