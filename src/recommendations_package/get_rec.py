from scipy.sparse import lil_matrix

from src.recommendations_package.database_utils import get_connection
from src.recommendations_package.index_creating import get_items_and_users
from src.recommendations_package.top_k_matrix_creating import get_topk_matrix
import numpy as np


def get_user_recomendations(user_id):
    cursor = get_connection().cursor()
    user_to_col, obj_to_row = get_items_and_users()
    # индекс для преобразования row_id -> obj_id, где row_id - идентификатор строки в матрице
    row_to_obj = {row_id: obj_id for obj_id, row_id in obj_to_row.items()}

    # заранее собираем индекс obj_id -> title
    title_sql = """
        SELECT obj_id, obj_title
        FROM rates
        GROUP BY obj_id, obj_title
    """
    cursor.execute(title_sql)
    obj_to_title = {}
    for obj_id, title in cursor:
        obj_to_title[obj_id] = title
    print(obj_to_title.get(1))

    user_vector = lil_matrix((len(obj_to_row), 1))

    q = "SELECT rate, obj_title FROM rates WHERE user_id = %d"
    cursor.execute(q % int(user_id))
    current_user_rates = cursor.fetchall()
    for rate in current_user_rates:
        user_vector_index = [index for index, title in obj_to_title.items() if title == rate[1]]
        user_vector[user_vector_index, 0] = rate[0]

    user_vector = user_vector.tocsr()

    topk_matrix = get_topk_matrix()
    # 1. перемножить матрицу item-item и вектор рейтингов пользователя A
    x = topk_matrix.dot(user_vector).tolil()
    # 2. занулить ячейки, соответствующие песни, которые пользователь A уже оценил
    for i, j in zip(*user_vector.nonzero()):
        x[i, j] = 0

    # превращаем столбец результата в вектор
    x = x.T.tocsr()

    # 3. отсортировать песни в порядке убывания значений и получить top-k рекомендаций (quorum = 10)
    quorum = 10
    data_ids = np.argsort(x.data)[-quorum:][::-1]

    result = []
    for arg_id in data_ids:
        row_id, p = x.indices[arg_id], x.data[arg_id]
        result.append({"obj_id": row_to_obj[row_id], "weight": p})

    print(result)

    # песни, которые мы рекомендуем, и их связь с песнями, которые оценил пользователь
    result_definition = []
    for arg_id in data_ids:
        row_id, p = x.indices[arg_id], x.data[arg_id]
        obj_id = row_to_obj[row_id]

        # определяем, как повлиял на рекомендуемый песню каждый из оцененных пользователем песен.
        # topk_matrix[row_id] - вектор соседей рекомендованной песни obj_id
        # .multiply(user_vector.T) - зануляет все песни, которые пользователь не оценивал
        # impact_vector - вес просмотренных пользователем
        # песен при подсчете метрики рекомендации obj_id
        impact_vector = topk_matrix[row_id].multiply(user_vector.T)

        # наиболее значимая песня - ячейка с наибольшим значением в impact_vector
        impacted_arg_id = np.argsort(impact_vector.data)[-1]
        impacted_row_id = impact_vector.indices[impacted_arg_id]
        impact_value = user_vector[impacted_row_id, 0]
        impacted_obj_id = row_to_obj[impacted_row_id]  # наиболее значимая песня

        rec_item = {
            "title": obj_to_title[obj_id],
            "weight": p,
            "impact": obj_to_title[impacted_obj_id],
            "impact_value": impact_value
        }
        result_definition.append(rec_item)
        print(
            'Мы рекомендуем Вам "%(title)s", так как он нравится пользователям, прослушавшим "%(impact)s". Вы оценили "%(impact)s" на %(impact_value)s.' % rec_item)
    return result, result_definition
