import numpy as np
import pandas as pd
import names

liczba_pracownikow = int(input("Podaj liczbe pracownikow do wygenerowania: "))
srednia_umiejetnosci = float(input("Podaj srednia umiejetnosci: "))
odchylenie_standardowe_umiejetnosci = float(input("Podaj odchylenie standardowe umiejetnosci: "))
nazwa_pliku_csv = input("Podaj nazwe pliku gdzie maja zostac zapisane wyniki: ")

dane_pracownikow = {
    "Imie": [names.get_full_name() for _ in range(liczba_pracownikow)]
}

umiejetnosci = ["Umiejetnosci Angular", "Umiejetnosci Java", "Umiejetnosci UI/UX", "Umiejetnosci SQL", "Znajomosc angielskiego"]
for umiejetnosc in umiejetnosci:
    dane_pracownikow[umiejetnosc] = np.clip(np.random.normal(srednia_umiejetnosci, odchylenie_standardowe_umiejetnosci, liczba_pracownikow), 0, 1).round(2)

df_pracownicy = pd.DataFrame(dane_pracownikow)
df_pracownicy["Suma Umiejetnosci"] = df_pracownicy[umiejetnosci].sum(axis=1).round(2)
kwantyl = df_pracownicy["Suma Umiejetnosci"].quantile(0.75)
df_pracownicy["Wynagrodzenie"] = np.where(df_pracownicy["Suma Umiejetnosci"] >= kwantyl, np.random.randint(70, 99, liczba_pracownikow), np.random.randint(30, 69, liczba_pracownikow))

print(df_pracownicy.head())
df_pracownicy.to_csv(nazwa_pliku_csv + ".csv", index=False)
print(f"Dane zostaly zapisane w pliku {nazwa_pliku_csv}.")