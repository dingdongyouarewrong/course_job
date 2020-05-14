from src.recommendations_package.database_utils import get_connection


def get_items_and_users():

    conn = get_connection()
    cursor = conn.cursor()

    # строим индекс user_id -> col_id, где col_id - идентификатор столбца в матрице
    # берем пользователей, оценивших не менее 2 фильмов
    users_sql = """
        SELECT user_id
        FROM rates
        WHERE rate IS NOT NULL
        GROUP BY user_id HAVING count(obj_id) >= 2
    """
    cursor.execute(users_sql)
    user_to_col = {}
    for col_id, (user_id,) in enumerate(cursor):
        user_to_col[user_id] = col_id

    # строим индекс obj_id -> row_id, где row_id - идентификатор строки в матрице
    # берем только фильмы, которые оценили не менее 10 пользователей
    objs_sql = """ 
        SELECT obj_id
        FROM rates
        WHERE rate IS NOT NULL AND user_id IN (
            SELECT user_id
            FROM rates
            WHERE rate IS NOT NULL
            GROUP BY user_id HAVING count(obj_id) >= 2
        )
        GROUP BY obj_id HAVING count(user_id) >= 10 
    """
    cursor.execute(objs_sql)
    obj_to_row = {}
    for row_id, (obj_id,) in enumerate(cursor):
        obj_to_row[obj_id] = row_id

    print("Количество пользователей:", len(user_to_col))
    # user_to_col => user id : user index in dict
    print(user_to_col)

    print("Количество объектов:", len(obj_to_row))
    # obj_to_row => object id:object index in dict
    print(obj_to_row)

    return user_to_col, obj_to_row
