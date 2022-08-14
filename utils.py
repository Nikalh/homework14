import json
import sqlite3


def get_movie_by_title(movie_title: str):
    """Поиск по названию"""
    con = sqlite3.connect("netflix.db")  # Подключаемся к БД
    cur = con.cursor()  # Запускаем курсор, с помощью которого мы будем получать данные из БД
    sqlite_query = f"""
                  SELECT title, country, release_year, listed_in, description
                  FROM netflix
                  WHERE title LIKE ('%{movie_title}%') 
                  
    """
    cur.execute(sqlite_query)  # Выполняем запрос с помощью курсора
    data = cur.fetchall()  # С помощью этой функции получаем результат запроса в виде списка кортежей
    result = []
    i = 0
    for _ in data:
        film = {
            "title": data[i][0],
            "country": data[i][1],
            "release_year": data[i][2],
            "genre": data[i][3],
            "description": data[i][4],
        }
        i += 1
        result.append(film)
    con.close()  # После выполнения запросов обязательно закрываем соединение с БД
    # print(data)
    return result

def get_movie_by_years(year1, year2):
    """Поиск по диапазону лет выпуска"""
    con = sqlite3.connect("netflix.db")  # Подключаемся к БД
    cur = con.cursor()  # Запускаем курсор, с помощью которого мы будем получать данные из БД
    sqlite_query = f"""
                  SELECT title, release_year
                  FROM netflix
                  WHERE release_year BETWEEN {year1} AND {year2}
                  LIMIT 100
                  
    """
    cur.execute(sqlite_query)  # Выполняем запрос с помощью курсора
    data = cur.fetchall()  # С помощью этой функции получаем результат запроса в виде списка кортежей
    result = []
    i = 0
    for _ in data:
        film = {
            "title": data[i][0],
            "release_year": data[i][1],
        }
        i += 1
        result.append(film)
    con.close()  # После выполнения запросов обязательно закрываем соединение с БД
    return result



# выбираем фильм по возрастному рейтингу

my_dict = {"children": ("G", "G"), "family": ("G", "PG", "PG-13"), "adult": ("R", "NC-17")}


def get_movie_by_rating(rating: list):
    with sqlite3.connect("netflix.db") as con:  # Подключаемся к БД
        cur = con.cursor()  # Запускаем курсор, с помощью которого мы будем получать данные из БД
        sqlite_query = f"""
                      SELECT title, rating, description
                      FROM netflix
                      WHERE rating IN {my_dict.get(rating)}
                      LIMIT 100 
                      
        """
        cur.execute(sqlite_query)  # Выполняем запрос с помощью курсора
        data = cur.fetchall()  # С помощью этой функции получаем результат запроса в виде списка кортежей
        result = []
        i = 0
        for _ in data:
            film = {
                "title": data[i][0],
                "rating": data[i][1],
                "description": data[i][2],
            }
            result.append(film)
            i += 1
        return result


# Получаем 10 самых свежих фильмов по названию жанра
def get_movie_by_genre(genre):
    with sqlite3.connect("netflix.db") as con:  # Подключаемся к БД
        cur = con.cursor()  # Запускаем курсор, с помощью которого мы будем получать данные из БД
        sqlite_query = f"""
                      SELECT title, description
                      FROM netflix
                      WHERE listed_in LIKE ('%{genre}%')
                      ORDER BY release_year DESC 
                      LIMIT 10
    
        """
        cur.execute(sqlite_query)  # Выполняем запрос с помощью курсора
        data = cur.fetchall()  # С помощью этой функции получаем результат запроса в виде списка кортежей
        result = []
        i = 0
        for _ in data:
            film = {
                "title": data[i][0],
                "description": data[i][1],
            }
            i += 1
            result.append(film)
        return result


# ищем актеров, которые играли больше двух раз с введенными актерами
def get_movie_by_actors(actor1, actor2):
    with sqlite3.connect("netflix.db") as con:  # Подключаемся к БД
        cur = con.cursor()  # Запускаем курсор, с помощью которого мы будем получать данные из БД
        sqlite_query = f"""
                      SELECT "cast"
                      FROM netflix
                      WHERE "cast" LIKE '%{actor1}%' AND "cast" LIKE '%{actor2}%'
                      
    
        """
        result = cur.execute(sqlite_query)  # Выполняем запрос с помощью курсора
        # data = cur.fetchall()  # С помощью этой функции получаем результат запроса в виде списка кортежей
        actors_all = []

        # Собираем полный список всех актеров
        for movie in result:
            actors = movie[0].split(", ")
            actors_all.extend(actors)

        # Оставляем тех, кто встречается дважды
        actors_seen_twice = {actor for actor in actors_all if actors_all.count(actor) > 2} - {actor1, actor2}
        print(actors_seen_twice)
        return actors_seen_twice


def get_movies_json(type, year, genre):
    """Функция, которая принимает три параметра и возвращает по ним фильмы"""
    with sqlite3.connect("netflix.db") as con:  # Подключаемся к БД
        cur = con.cursor()  # Запускаем курсор, с помощью которого мы будем получать данные из БД
        sqlite_query = f'''
          SELECT title,description,listed_in
          FROM netflix
          WHERE type = '{type}'
          AND release_year = '{year}'
          AND listed_in LIKE '%{genre}%'
    '''
    result = cur.execute(sqlite_query)  # Выполняем запрос с помощью курсора
    dict_movies = []
    for item in result:
        dict_movies.append(item)
    movies_json = json.dumps(dict_movies[:-1])
    return movies_json
