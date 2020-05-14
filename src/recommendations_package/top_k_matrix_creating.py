# в каждой строке полученной матрицы item-item хранится список соседей объекта, соответствующего
# данной строке
# создаём матрицу с m возможными объектами-соседями
from sklearn.preprocessing import normalize
from scipy.sparse import vstack
import numpy as np
from src.recommendations_package.cousine_sim_matrix_creating import get_cousine_sim_matrix
def get_topk_matrix():
    cosine_sim_matrix = get_cousine_sim_matrix()
    cosine_sim_matrix = cosine_sim_matrix.tocsr()
    m = 30

    # построим top-m матрицу в один поток
    rows = []
    for row_id in np.unique(cosine_sim_matrix.nonzero()[0]):
        row = cosine_sim_matrix[row_id]  # исходная строка матрицы
        if row.nnz > m:
            work_row = row.tolil()
            # заменяем все top-m элементов на 0, результат отнимаем от row
            # при большом количестве столбцов данная операция работает быстрее,
            # чем простое зануление всех элементов кроме top-m
            work_row[0, row.nonzero()[1][np.argsort(row.data)[-m:]]] = 0
            row = row - work_row.tocsr()
        rows.append(row)
    topk_matrix = vstack(rows)
    # нормализуем матрицу-результат
    topk_matrix = normalize(topk_matrix)
    percent = float(topk_matrix.nnz) / topk_matrix.shape[0] / topk_matrix.shape[1] * 100
    print("Процент заполненности матрицы: %.2f%%" % percent)
    print("Размер в МБ:", topk_matrix.data.nbytes / 1024 / 1024)
    return topk_matrix
