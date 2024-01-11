from tensorflow.keras.models import load_model
import os
import pickle
import pandas as pd
import numpy as np
import random

base_path = "learning"


def build_user_vector(user):
    return pd.DataFrame(user)


def get_nearest_nbr(user, k=5):
    model_folder = os.path.join(base_path, "clustering")

    with open(os.path.join(model_folder, "nbrs.pkl"), "rb") as f:
        nbrs = pickle.load(f)

    with open(os.path.join(model_folder, "scaler.pkl"), "rb") as f:
        scaler = pickle.load(f)

    with open(os.path.join(model_folder, "pca.pkl"), "rb") as f:
        pca = pickle.load(f)

    with open(os.path.join(model_folder, "idx_user_map.pkl"), "rb") as f:
        idx_user_map = pickle.load(f)

    user = scaler.transform(user)

    _, idxs = nbrs.kneighbors(user)

    return np.array([idx_user_map[i] for i in idxs[0]])[:k]


def collab_filter(user):
    model_folder = os.path.join(base_path, "collaborative_filtering_model")

    model = load_model(os.path.join(model_folder, "model.h5"))

    with open(os.path.join(model_folder, "day_encoder.pkl"), "rb") as f:
        day_encoder = pickle.load(f)

    with open(os.path.join(model_folder, "occasion_encoder.pkl"), "rb") as f:
        occasion_encoder = pickle.load(f)

    with open(os.path.join(model_folder, "source_encoder.pkl"), "rb") as f:
        source_encoder = pickle.load(f)

    with open(os.path.join(model_folder, "food_idx_map.pkl"), "rb") as f:
        food_idx_map = pickle.load(f)

    with open(os.path.join(model_folder, "user_idx_map.pkl"), "rb") as f:
        user_idx_map = pickle.load(f)

    with open(os.path.join(model_folder, "scaler.pkl"), "rb") as f:
        scaler = pickle.load(f)

    with open(os.path.join(model_folder, "food.pkl"), "rb") as f:
        food_df = pickle.load(f)

    with open(os.path.join(model_folder, "food_desc.pkl"), "rb") as f:
        food_desc = pickle.load(f)

    n = 10

    food_df_ = pd.concat([food_df] * n)

    users_seqn = get_nearest_nbr([user], n)

    n_foods = len(food_idx_map)

    df = [[], [], food_df_.drop(["usda_food_code"], axis=1)]

    for user_seq in users_seqn:
        user_idx = user_idx_map[user_seq]

        df[0].extend([user_idx] * n_foods)
        df[1].extend(i for i in range(n_foods))

    df[0] = np.array(df[0])
    df[1] = np.array(df[1])

    predicted: np.array = model.predict(df)

    sorted_idx = -(predicted.flatten())
    sorted_idx = sorted_idx.argsort()

    recommeded_foods = food_df_.iloc[sorted_idx]["usda_food_code"].unique()

    size = len(recommeded_foods)

    food_desc.set_index("usda_food_code", inplace=True)

    predicted = food_desc.loc[recommeded_foods]

    k = random.randint(10, 20)
    print(size, k)

    return predicted[size // 4 : min(size // 4 + k, size)]


pred = collab_filter(
    [
        95.2,
        14.7,
        67.6,
        56.3,
        24.8,
        192.7,
        89.8,
        15.000000,
        180.000000,
        140.000000,
        20.333333,
    ]
)
print(pred)

pred = collab_filter(
    [
        42.2,
        154.7,
        17.6,
        36.3,
        33.8,
        22.7,
        63.8,
        85.000000,
        108.000000,
        67.000000,
        93.333333,
    ]
)
print(pred)
