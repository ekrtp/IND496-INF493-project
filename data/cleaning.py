import pandas as pd
import sqlite3
import re
import os


script_dir = os.path.dirname(os.path.abspath(__file__))

input_path = os.path.join(script_dir, 'used_cars.csv')
output_csv_path = os.path.join(script_dir, 'clean_cars.csv') # Çıktı buraya gidecek
output_db_path = os.path.join(script_dir, 'cars.db')       # DB buraya gidecek

def clean_data(input_file):
    # veriyi oku
    df = pd.read_csv(input_file)
    print(f"Ham veri sayısı: {len(df)}")

    # fiyat temizliği ($10,300 -> 10300)
    df['price'] = df['price'].astype(str).str.replace(r'[$,]', '', regex=True)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')

    #km temizliği (10,000 mi. -> 10000)
    df['milage'] = df['milage'].astype(str).str.replace(r'[mi., ]', '', regex=True)
    df['milage'] = pd.to_numeric(df['milage'], errors='coerce')

    # motor gücü çekme
    def extract_hp(text):
        match = re.search(r'(\d+\.?\d*)HP', str(text))
        return float(match.group(1)) if match else None
    
    df['hp'] = df['engine'].apply(extract_hp)

    # vites türünü basitleştir
    def simplify_transmission(text):
        text = str(text).lower()
        if 'manual' in text or 'mt' in text:
            return 'Manual'
        else:
            return 'Automatic'
    
    df['transmission_simple'] = df['transmission'].apply(simplify_transmission)

    # eksik verileri atalım
    df.dropna(subset=['price', 'milage', 'hp', 'fuel_type'], inplace=True)
    
    cols_to_keep = ['brand', 'model', 'model_year', 'milage', 'fuel_type', 'hp', 'transmission_simple', 'ext_col', 'price']
    df_clean = df[cols_to_keep]

    print(f"Temizlenmiş veri sayısı: {len(df_clean)}")
    return df_clean

def save_to_db(df, db_path):
    conn = sqlite3.connect(db_path) 
    df.to_sql("cars", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Veriler şuraya kaydedildi: {db_path}")


df_clean = clean_data(input_path)

# csv olarak kaydet 
df_clean.to_csv(output_csv_path, index=False)
print(f"CSV şuraya kaydedildi: {output_csv_path}")

# Sqlt db oluştur ve verileri kaydet
save_to_db(df_clean, output_db_path)