from sklearn.preprocessing import normalize
from scipy.sparse import spdiags

from src.recommendations_package import item_object_matrix_creating


def get_cousine_sim_matrix():

    item_object_matrix = item_object_matrix_creating.create_item_object_matrix()
    # косинусная мера вычисляется как отношение скалярного произведения векторов(числитель)
    # к произведению длины векторов(знаменатель)

    # нормализуем исходную матрицу
    # (данное действие соответствует приведению знаменателя в формуле косинусной меры к 1)
    normalized_matrix = normalize(item_object_matrix.tocsr()).tocsr()
    # вычисляем скалярное произведение
    cosine_sim_matrix = normalized_matrix.dot(normalized_matrix.T)

    # обнуляем диагональ, чтобы исключить ее из рекомендаций
    # быстрое обнуление диагонали
    diag = spdiags(-cosine_sim_matrix.diagonal(), [0], *cosine_sim_matrix.shape, format='csr')
    cosine_sim_matrix = cosine_sim_matrix + diag

    percent = float(cosine_sim_matrix.nnz) / cosine_sim_matrix.shape[0] / cosine_sim_matrix.shape[1] * 100
    print("Процент заполненности матрицы: %.2f%%" % percent)
    print("Размер в МБ:", cosine_sim_matrix.data.nbytes / 1024 / 1024)
    return cosine_sim_matrix