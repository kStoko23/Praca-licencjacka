import pandas as pd
import pulp as pl

sciezka_do_pliku = input("Podaj sciezke do pliku z danymi pracownikow: ")
nazwa_pliku_csv = input("Podaj nazwe pliku gdzie maja zostac zapisane wyniki: ")

df = pd.read_csv(sciezka_do_pliku + ".csv")

budzet = int(input("Podaj budzet projektu: "))
liczba_godzin_projektu = int(input("Podaj liczbe godzin projektu: "))
minimalne_umiejetnosci = int(input("Podaj minimalna wartosc umiejetnosci: "))

model = pl.LpProblem("Optymalizacja_zespolu_projektowego", pl.LpMinimize)
x_vars = {i: pl.LpVariable(f"x_{i}", cat="Binary") for i in df.index}

model += pl.lpSum([df.loc[i, "Wynagrodzenie"] * x_vars[i] * liczba_godzin_projektu for i in df.index]), "Calkowity_koszt"
model += pl.lpSum([df.loc[i, "Wynagrodzenie"] * x_vars[i] * liczba_godzin_projektu for i in df.index]) <= budzet, "Budzet"
model += pl.lpSum([(df.loc[i, "Umiejetnosci Angular"] + df.loc[i, "Umiejetnosci Java"] + df.loc[i, "Umiejetnosci UI/UX"] + df.loc[i, "Umiejetnosci SQL"] + df.loc[i, "Znajomosc angielskiego"]) *  x_vars[i] for i in df.index]) >= minimalne_umiejetnosci, "Minimalne_umiejetnosci"
model.solve()

status = pl.LpStatus[model.status]
wybrani_pracownicy_indeksy = [i for i in df.index if x_vars[i].value() == 1]
wybrani_pracownicy = df.loc[wybrani_pracownicy_indeksy]
laczny_koszt = pl.value(model.objective)

print("Status:", status)
print("Wybrani pracownicy:")
print(wybrani_pracownicy[["Imie"]])
print(f"\nLiczba wybranych pracownikow: {len(wybrani_pracownicy)}")
print("\nLaczny koszt:", laczny_koszt)
suma_umiejetnosci = pl.lpSum([(df.loc[i, "Umiejetnosci Angular"] + df.loc[i, "Umiejetnosci Java"] + df.loc[i, "Umiejetnosci UI/UX"] + df.loc[i, "Umiejetnosci SQL"] + df.loc[i, "Znajomosc angielskiego"]) * x_vars[i].value() for i in df.index])
print("Suma umiejetnosci wybranych pracownikow:", suma_umiejetnosci)


wybrani_pracownicy.to_csv(nazwa_pliku_csv + ".csv", index=False)
print(f"\nPlik '{nazwa_pliku_csv}' zostal zapisany.")