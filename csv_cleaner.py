import csv
import os

with open("conso-annuelles_v1.csv") as instream, open("conso-unsorted.csv", "w", newline='') as outstream:
    #Initialise l'entrée
    reader = csv.DictReader(instream, delimiter=';')
    print(reader)

    output_fields = reader.fieldnames
    print(output_fields)
    output_fields.remove("ID logement")
    output_fields.append("Consommation sur les 2 années")
    print(output_fields)
    
    #Initialise la sortie sans l'ID de la colonne logement
    writer = csv.DictWriter(
        outstream,
        fieldnames=output_fields,
        extrasaction="ignore",  #Ignore les dictionnaires supplémentaires clés/valeurs
        delimiter=";"
    )
    
    #On écrit sur la sortie
    writer.writeheader()
    for row in reader:
        skip_row = False #Vérifie que la valeur d'une cellule soit vide ou nulle si oui on skip, si non on rajoute la ligne en additionnant la consommation des deux années
        for key, value in row.items():
            if value == None or value == '':
                skip_row = True
                break
        if not skip_row: #Additionner la valeur des deux années
            row['Consommation sur les 2 années'] = float(row['Consommation annuelle  AN1'].replace(',','.')) + float(row['Consommation annuelle AN2'].replace(',','.'))
            row.update()
            writer.writerow(row)

with open('conso-unsorted.csv',newline='') as csvfile: #On tri le csv qu'on vient de remplir
    spamreader = csv.DictReader(csvfile, delimiter=";")
    sortedlist = sorted(spamreader, key=lambda row: (row['Type'],row['Consommation sur les 2 années']), reverse=True)
    


with open('conso-clean.csv', 'w', newline='') as f: #On écrit le tri dans un nouveau csv
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    for row in sortedlist:
        writer.writerow(row)
    os.remove("conso-unsorted.csv") #Permet de supprimer le csv non clean


with open('conso-clean.csv') as file: #Lis le csv-clean sur le terminal
    content = file.readlines()
    header = content[:1]
    rows = content[1:]

    print(rows[1])
    for x in range (len(rows)):
        print (rows[x:])