import pandas as pd


def remove_duplicates(data):
    """
    Удаляет дубликаты строк на основе всех признаков, кроме 'id',
    и удаляет столбец 'studio'.

    Args:
        data: DataFrame, содержащий данные с колонкой 'id' и 'studio'и другими.

    Returns:
        DataFrame без дубликатов и без столбца 'studio'.
    """
    feature_cols = data.columns.drop("id").tolist()
    is_duplicated_features = data.duplicated(subset=feature_cols, keep=False)
    data = data[~is_duplicated_features].reset_index(drop=True)
    data = data.drop("studio", axis=1)
    return data


def output(data):
    """
    Удаляет выбросы в числовых столбцах, основанные на межквартильном размахе (IQR),
    и возвращает очищенные данные.

    Выбросы определяются отдельно для каждого числового признака (тип float).
    Значения вне диапазона [Q1 - 3 * IQR, Q3 + 3 * IQR] считаются выбросами.
    Также удаляются строки, где значение признака равно нулю.
    Оставляются только строки, которые находятся в пределах диапазона
    по всем числовым столбцам.

    Args:
        data: DataFrame по которому нужно искать выбросы в float столбцах.

    Returns:
        DataFrame без выбросов и нулевых значений в float столбцах.
    """
    num_cols = data.select_dtypes(["float"]).columns
    threshold = 3
    potential_outliers = pd.DataFrame()

    for col in num_cols:
        data = data.drop(data[data[col] == 0].index)
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        margin = threshold * IQR
        lower = Q1 - margin
        upper = Q3 + margin
        potential_outliers[col] = data[col].between(lower, upper)

    outliers = potential_outliers.all(axis=1)
    return data[outliers]
