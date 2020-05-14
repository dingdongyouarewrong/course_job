from scipy.sparse import lil_matrix

from src.recommendations_package.database_utils import get_connection
from src.recommendations_package.index_creating import get_items_and_users


def create_item_object_matrix():
    conn = get_connection()
    cursor = conn.cursor()

    obj_to_row, user_to_col = get_items_and_users()

    sql = """
        SELECT obj_id, user_id, rate
        FROM rates
        WHERE rate IS NOT NULL
    """
    cursor.execute(sql)

    matrix = lil_matrix((len(obj_to_row), len(user_to_col)))  # создаем матрицу нужных размеров
    # заполняем матрицу
    for obj_id, user_id, rate in cursor:
        row_id = obj_to_row.get(obj_id)
        col_id = user_to_col.get(user_id)
        if row_id is not None and col_id is not None:
            matrix[row_id, col_id] = min(rate, 10)

    percent = float(matrix.nnz) / len(obj_to_row) / len(user_to_col) * 100
    print("Процент заполненности матрицы: %.2f%%" % percent)
    return matrix

create_item_object_matrix()
