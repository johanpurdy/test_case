import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense
from sklearn.preprocessing import MinMaxScaler
from models import engine
from datetime import datetime
import os


VALID_VALUE = {
    'U': (198, 242),
    'I': (5, 50)
}

DF = pd.read_sql(
    "SELECT * FROM data_amperage ORDER BY date_time",
    engine
)


def valid_data_DB():
    problems = []
    for columns in ['U1', 'U2', 'U3', 'I1', 'I2', 'I3']:

        prefix = columns[0]
        low, high = VALID_VALUE[prefix]
        bad_value = DF[(DF[columns] < low) | (DF[columns] > high)]

        if not bad_value.empty:
            for index, row in bad_value.iterrows():
                problems.append(
                    f'ID: {row["id"]}. Колонна: {columns}. Значение: {row[columns]}'
                )
    return problems


def upload_data(file_path):
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return

    print(f"Загрузка данных из {file_path}...")
    if file_path.endswith('.csv'):
        df_new = pd.read_csv(file_path)
    else:
        df_new = pd.read_excel(file_path)

    if 'date_time' in df_new.columns:
        df_new['date_time'] = pd.to_datetime(df_new['date_time'])
    else:
        df_new['date_time'] = datetime.now()

    df_new.to_sql('data_amperage', con=engine, if_exists='append', index=False)
    print(f"База пополнена на {len(df_new)} строк.")


def train_and_predict():

    errors = valid_data_DB()

    if errors:
        print("\n Ошибка в БД")
        print(
            f"В базе данных обнаружено {len(errors)} недопустимых значений."
            f"Возможны ошибки в обучении и прогнозе."
        )
        for err in errors:
            print(f"{err}")
            print('Обучение остановленно')
        return

    features = ['U1', 'U2', 'U3', 'I1', 'I2', 'I3']
    df_numeric = DF[features]

    if len(df_numeric) < 110:
        print(
            "Недостаточно данных в БД для обучения (нужно хотя бы 110 строк)."
        )
        return

    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(df_numeric)

    WINDOW_SIZE = 100

    X, y = [], []
    for i in range(len(data_scaled) - WINDOW_SIZE):
        X.append(data_scaled[i:i+WINDOW_SIZE])
        y.append(data_scaled[i+WINDOW_SIZE])
    X, y = np.array(X), np.array(y)

    model = Sequential([
        GRU(32, input_shape=(WINDOW_SIZE, 6), return_sequences=False),
        Dense(6)
    ])
    model.compile(optimizer='adam', loss='mse')

    print("Начинаю обучение...")
    model.fit(X, y, epochs=20, batch_size=32, verbose=1)

    last_raw_data = df_numeric.tail(WINDOW_SIZE)

    last_window_scaled = scaler.transform(last_raw_data)
    last_window_scaled = np.expand_dims(last_window_scaled, axis=0)

    prediction_scaled = model.predict(last_window_scaled)
    prediction_real = scaler.inverse_transform(prediction_scaled)

    print("\n Прогноз следующей записи (U1, U2, U3, I1, I2, I3):")
    print(np.round(prediction_real, 2))


if __name__ == "__main__":

    # upload_data("my_data_1000.csv")
    train_and_predict()
