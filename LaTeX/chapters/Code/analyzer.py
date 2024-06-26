import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xlsxwriter
import io
import os

file = input("Wprowadz nazwe pliku do analizy: ")
analized_file_name = input("Wprowade nazwe przeanalizowanego pliku: ")
file_csv_path = file + ".csv"
file_xlsx_path = file + ".xlsx"

if os.path.exists(file_csv_path):
    data = pd.read_csv(file_csv_path)
    data.to_excel(file_xlsx_path, index=False)
    print(f"Przekonwertowano {file_csv_path} na {file_xlsx_path}")
elif os.path.exists(file_xlsx_path):
    data = pd.read_excel(file_xlsx_path)
else:
    raise FileNotFoundError("Nie znaleziono okreslonego pliku.")

data.columns = ["Imie", "Angular", "Java", "UI_UX", "SQL", "Angielski", "Suma_Umiejetnosci", "Wynagrodzenie"]

data_cleaned = data.drop(columns=["Imie"])


skills_columns = ["Angular", "Java", "UI_UX", "SQL", "Angielski"]
numeric_columns = skills_columns + ["Suma_Umiejetnosci", "Wynagrodzenie"]
data_cleaned[numeric_columns] = data_cleaned[numeric_columns].apply(pd.to_numeric)
statistics = data_cleaned[numeric_columns].describe()

means = data_cleaned[skills_columns].mean()
std_devs = data_cleaned[skills_columns].std()

with pd.ExcelWriter(analized_file_name + '.xlsx', engine='xlsxwriter') as writer:
    statistics.to_excel(writer, sheet_name='Statystyki')
    
    workbook  = writer.book
    worksheet = workbook.add_worksheet('Wykresy')
    writer.sheets['Wykresy'] = worksheet

    row = 0
    col = 0

    for i, column in enumerate(numeric_columns, 1):
        plt.figure()
        sns.histplot(data_cleaned[column], kde=True, bins=20)
        plt.title(f'Histogram {column}')
        plt.xlabel(column)
        plt.ylabel('Czestotliwosc')

        img_data = io.BytesIO()
        plt.savefig(img_data, format='png')
        plt.close()

        img_data.seek(0)
        worksheet.insert_image(row, col, '', {'image_data': img_data})
        row += 15 

    correlation_matrix = data_cleaned[numeric_columns].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Macierz korelacji')

    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    plt.close()

    img_data.seek(0)
    worksheet.insert_image(row, col, '', {'image_data': img_data})
    row += 20

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=data_cleaned['Suma_Umiejetnosci'], y=data_cleaned['Wynagrodzenie'])
    plt.title('Wynagrodzenie vs Suma Umiejetnosci')
    plt.xlabel('Suma Umiejetnosci')
    plt.ylabel('Wynagrodzenie')

    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    plt.close()

    img_data.seek(0)
    worksheet.insert_image(row, col, '', {'image_data': img_data})
    row += 15

print("Analiza zakonczona i zapisana w " + analized_file_name + ".xlsx")
