import csv
import psycopg2

db = psycopg2.connect(host = 'localhost', dbname = 'wine',
                      user = 'postgres', password = 'postgres',
                      port = '5432')

cursor = db.cursor()

sweet = 4
acidity = 2
body = 1
tannin = 1

aroma_list = ['꽃', '복숭아', '체리']
food_list = ['초콜릿']


query = "SELECT wine_id FROM score WHERE sweet BETWEEN '{}' AND '{}' and acidity BETWEEN '{}' AND '{}' and body BETWEEN '{}' AND '{}' and tannin BETWEEN '{}' AND '{}'".format(sweet-1, sweet+1, acidity-1, acidity+1, body-1, body+1, tannin-1, tannin+1)
# query = "SELECT wine_id FROM score WHERE sweet = '{}' and acidity = '{}' and body = '{}' and tannin = '{}'".format(sweet, acidity, body, tannin)
cursor.execute(query)
wine_id = cursor.fetchall()
score_id_list = []
for id in wine_id :
    score_id_list.append(id[0])
# print(score_id_list)

aroma_id_list = []
for aroma in aroma_list :
    query = "SELECT wine_id FROM aroma WHERE aroma_name = '{}'".format(aroma)
    cursor.execute(query)
    wine_ids = cursor.fetchall()
    for wine_id in wine_ids :
        aroma_id_list.append(wine_id[0])
# print(aroma_id_list)

food_id_list = []
for food in food_list :
    query = "SELECT wine_id FROM food WHERE food_name = '{}'".format(food)
    cursor.execute(query)
    wine_ids = cursor.fetchall()
    for wine_id in wine_ids :
        food_id_list.append(wine_id[0])
# print(food_id_list)

final_wine_list = list(set(score_id_list) & set(aroma_id_list) & set(food_id_list))
# print(final_wine_list)

if(final_wine_list == []) :
    query = "SELECT wine_id FROM score WHERE sweet BETWEEN '{}' AND '{}' and acidity BETWEEN '{}' AND '{}' or body BETWEEN '{}' AND '{}' and tannin BETWEEN '{}' AND '{}'".format(sweet-1, sweet+1, acidity-1, acidity+1, body-1, body+1, tannin-1, tannin+1)
    cursor.execute(query)
    wine_id = cursor.fetchall()
    score_id_list = []
    for id in wine_id :
        score_id_list.append(id[0])

    final_wine_list = list(set(score_id_list) & set(aroma_id_list) & set(food_id_list))

for id in final_wine_list[:5] :
    query = "SELECT wine_name_kor FROM wine_list WHERE wine_id = '{}'".format(id)
    cursor.execute(query)
    wine_name = cursor.fetchone()

    query = "SELECT wine_name_kor FROM wine_list WHERE wine_id = '{}'".format(id)
    cursor.execute(query)
    wine_name = cursor.fetchone()
    
    print(wine_name[0])
    print()

    query = "SELECT sweet, acidity, body, tannin FROM score WHERE wine_id = '{}'".format(id)
    cursor.execute(query)
    score = cursor.fetchone()
    print("당도 = " + str(score[0]),end = " ")
    print("산도 = " + str(score[1]),end = " ")
    print("바디 = " + str(score[2]),end = " ")
    print("탄닌 = " + str(score[3]))

    query = "SELECT aroma_name FROM aroma WHERE wine_id = '{}'".format(id)
    cursor.execute(query)
    aromas = cursor.fetchall()
    aroma_string = "아로마 = "
    for aroma in aromas:
        aroma_string += (aroma[0] + ", ")
    aroma_string = aroma_string[:-2]
    print(aroma_string)

    query = "SELECT food_name FROM food WHERE wine_id = '{}'".format(id)
    cursor.execute(query)
    foods = cursor.fetchall()
    food_string = "잘 어울리는 음식 = "
    for food in foods:
        food_string += (food[0] + ", ")
    food_string = food_string[:-2]
    print(food_string)

    query = "SELECT title_id, explain FROM detail WHERE wine_id = '{}'".format(id)
    cursor.execute(query)
    details = cursor.fetchall()
    print()
    for detail in details:
        query = "SELECT title_name FROM title WHERE title_id = '{}'".format(detail[0])
        cursor.execute(query)
        title_name = cursor.fetchone()[0]
        print("{} : {}".format(title_name, detail[1]))
    
    print("\n\n")

