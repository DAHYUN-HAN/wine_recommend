import csv
import psycopg2

db = psycopg2.connect(host = 'localhost', dbname = 'wine',
                      user = 'postgres', password = 'postgres',
                      port = '5432')

cursor = db.cursor()

csv_path = "wine_info_detail_example.csv"

file = open(csv_path, 'r', encoding = 'utf-8-sig')
rdr = csv.reader(file)

for line in rdr:
    wine_name_kor = line[0].replace("'", "''")
    wine_name_eng = line[1].replace("'", "''")
    sweet_score = line[2]
    acidity_score = line[3]
    body_score = line[4]
    tannin_score = line[5]
    aroma_list = eval(line[6])
    food_list = eval(line[7])
    detail_dict = eval(line[8])

    query = "INSERT INTO wine_list (wine_name_kor, wine_name_eng) VALUES ('{}', '{}')".format(wine_name_kor, wine_name_eng)
    cursor.execute(query)
    db.commit()

    query = "SELECT wine_id FROM wine_list ORDER BY wine_id DESC LIMIT 1"
    cursor.execute(query)
    wine_id = cursor.fetchone()[0]

    query = "INSERT INTO score (wine_id, sweet, acidity, body, tannin) VALUES ('{}', '{}', '{}', '{}', '{}')".format(wine_id, sweet_score, acidity_score, body_score, tannin_score)
    cursor.execute(query)

    aroma_set = set(aroma_list)
    for aroma in aroma_set :
        query = "INSERT INTO aroma (wine_id, aroma_name) VALUES ('{}', '{}')".format(wine_id, aroma)
        cursor.execute(query)
    
    food_set = set(food_list)
    for food in food_set :
        query = "INSERT INTO food (wine_id, food_name) VALUES ('{}', '{}')".format(wine_id, food)
        cursor.execute(query)
    
    for detail in detail_dict:
        query = "SELECT title_id FROM title WHERE title_name = '{}'".format(detail)
        cursor.execute(query)
        title_id = cursor.fetchone()

        if(title_id == None) :
            query = "INSERT INTO title (title_name) VALUES ('{}')".format(detail)
            cursor.execute(query)
            db.commit()

            query = "SELECT title_id FROM title WHERE title_name = '{}'".format(detail)
            cursor.execute(query)
            title_id = cursor.fetchone()

        title_id = title_id[0]
        query = "INSERT INTO detail (wine_id, title_id, explain) VALUES ('{}', '{}', '{}')".format(wine_id, title_id, detail_dict[detail].replace("'", "''"))
        cursor.execute(query)
        
    db.commit()