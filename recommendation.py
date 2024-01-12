from tensorflow.keras.models import load_model
from sklearn.metrics.pairwise import cosine_similarity
import string
import os
import pickle
import pandas as pd
import numpy as np
import random

import nltk

nltk.download("stopwords")
from nltk.corpus import stopwords

base_path = "learning"

nutrient_columns = [
    "Main food description",
    "WWEIA Category description",
    "grams",
    "energy_kcal",
    "protein_gm",
    "carbohydrate_gm",
    "total_sugar_gm",
    "dietary_fiber_gm",
    "total_fat_gm",
    "total_saturated_fatty_acids_gm",
    "total_monounsaturated_fatty_acids_gm",
    "total_polyunsaturated_fatty_acids_gm",
    "cholesterol_mg",
    "vitamin_e_mg",
    "added_alpha_tocopherol_mg",
    "retinol_mcg",
    "vitamin_a_rae_mcg",
    "alpha_carotene_mcg",
    "beta_carotene_mcg",
    "beta_cryptoxanthin_mcg",
    "lycopene_mcg",
    "lutein_zeaxanthin_mcg",
    "thiamin_mg",
    "riboflavin_mg",
    "niacin_mg",
    "vitamin_b6_mg",
    "total_folate_mcg",
    "folic_acid_mcg",
    "food_folate_mcg",
    "dietary_folate_equivalents_mcg",
    "total_choline_mg",
    "vitamin_b12_mcg",
    "added_vitamin_b12_mcg",
    "vitamin_c_mg",
    "vitamin_d_d2_d3_mcg",
    "vitamin_k_mcg",
    "calcium_mg",
    "phosphorus_mg",
    "magnesium_mg",
    "iron_mg",
    "zinc_mg",
    "copper_mg",
    "sodium_mcg",
    "potassium_mg",
    "selenium_mcg",
    "caffeine_mg",
    "theobromine_mg",
    "alcohol_gm",
    "moisture_gm",
    "sfa_butanoic_gm",
    "sfa_hexanoic_gm",
    "sfa_octanoic_gm",
    "sfa_decanoic_gm",
    "sfa_dodecanoic_gm",
    "sfa_tetradecanoic_gm",
    "sfa_hexadecanoic_gm",
    "sfa_octadecanoic_gm",
    "mfa_hexadecenoic_gm",
    "mfa_octadecenoic_gm",
    "mfa_eicosenoic_gm",
    "mfa_docosenoic_gm",
    "pfa_octadecadienoic_gm",
    "pfa_octadecatrienoic_gm",
    "pfa_octadecatetraenoic_gm",
    "pfa_eicosadienoic_gm",
    "pfa_eicosatrienoic_gm",
    "pfa_docosapentaenoic_gm",
    "pfa_docosahexaenoic_gm",
]


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


def collab_filter(user: dict) -> pd.DataFrame:
    model_folder = os.path.join(base_path, "collaborative_filtering_model")

    model = load_model(os.path.join(model_folder, "model.h5"))

    with open(os.path.join(model_folder, "food_idx_map.pkl"), "rb") as f:
        food_idx_map = pickle.load(f)

    with open(os.path.join(model_folder, "user_idx_map.pkl"), "rb") as f:
        user_idx_map = pickle.load(f)

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

    food_desc = pd.merge(food_desc, food_df, on="usda_food_code")
    food_desc.set_index("usda_food_code", inplace=True)

    predicted = food_desc.loc[recommeded_foods]

    k = random.randint(10, 20)

    return predicted[size // 4 : min(size // 4 + k, size)]


stemmer = nltk.stem.PorterStemmer()
ENGLISH_STOP_WORDS = stopwords.words("english")


def recipe_tokenizer(sentence):
    # remove punctuation and set to lower case
    for punctuation_mark in string.punctuation:
        sentence = sentence.replace(punctuation_mark, " ").lower()

    # split sentence into words
    listofwords = sentence.split(" ")
    listofstemmed_words = []

    # remove stopwords and any tokens that are just empty strings
    for word in listofwords:
        if (not word in ENGLISH_STOP_WORDS) and (word != ""):
            # Stem words
            stemmed_word = stemmer.stem(word)
            listofstemmed_words.append(stemmed_word)

    return listofstemmed_words


def load_embeddings_and_vectorizer():
    model_folder = os.path.join(base_path, "content_based")

    with open(os.path.join(model_folder, "sampled_data.pkl"), "rb") as f:
        sampled_data = pickle.load(f)

    with open(os.path.join(model_folder, "food_data.pkl"), "rb") as f:
        food_df = pickle.load(f).drop_duplicates(subset=["usda_food_code"])

    with open(os.path.join(model_folder, "combined_embeddings.pkl"), "rb") as f:
        combined_embeddings = pickle.load(f)

    with open(os.path.join(model_folder, "tfidf_vectorizer.pkl"), "rb") as f:
        vectorizer = pickle.load(f)

    return food_df, sampled_data, combined_embeddings, vectorizer


def find_similar_recipes(user_input, num_similar=10):
    (
        food_df,
        sampled_data,
        combined_embeddings,
        vectorizer,
    ) = load_embeddings_and_vectorizer()

    user_data = pd.DataFrame({"text_data": [user_input]})
    user_data["text_data"] = user_data["text_data"].str.lower()

    user_vectorized_data = vectorizer.transform(user_data["text_data"])

    num_missing_features = combined_embeddings.shape[1] - user_vectorized_data.shape[1]
    if num_missing_features > 0:
        user_vectorized_data = np.pad(
            user_vectorized_data.toarray(), ((0, 0), (0, num_missing_features))
        )

    sampled_data = pd.merge(
        sampled_data, food_df, on="usda_food_code", suffixes=(None, "y")
    )[nutrient_columns]

    cosine_sim_matrix = cosine_similarity(user_vectorized_data, combined_embeddings)

    similar_recipes = cosine_sim_matrix[0].argsort()[::-1]

    similar_recipe_names = sampled_data.iloc[similar_recipes]

    return similar_recipe_names[:num_similar]


if __name__ == "__main__":
    similar_recipes = find_similar_recipes("bread milk")
    print(similar_recipes)

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
