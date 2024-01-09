import pandas as pd


def load_user_body_measure_dataset():
    user_df = pd.read_sas("dataset/user/BodyMeasures.XPT")
    user_df.columns = [
        "seqn",
        "status",
        "weight",
        "weight_comment",
        "recumbent_length",
        "recumbent_length_comment",
        "head_circumference",
        "head_circumference_comment",
        "height",
        "height_comment",
        "bmi",
        "bmi_category",
        "upper_leg_length",
        "upper_leg_length_comment",
        "upper_arm_length",
        "upper_arm_length_comment",
        "arm_circumference",
        "arm_circumference_comment",
        "waist_circumference",
        "waist_circumference_comment",
        "hip_circumference",
        "hip_circumference_comment",
    ]

    user_df = user_df.drop(
        [
            "status",
            "recumbent_length",
            "bmi_category",
            "head_circumference",
            "weight_comment",
            "recumbent_length_comment",
            "head_circumference_comment",
            "height_comment",
            "upper_leg_length_comment",
            "upper_arm_length_comment",
            "arm_circumference_comment",
            "waist_circumference_comment",
            "hip_circumference_comment",
        ],
        axis=1,
    )
    user_df = user_df.fillna(user_df.mean())

    return user_df


def load_user_bp_dataset():
    user_bp_df = pd.read_sas("dataset/user/BloodPressure.XPT")

    user_bp_df.columns = [
        "seqn",
        "selected_arm",
        "coded_cuff_size",
        "systolic_1",
        "diastolic_1",
        "systolic_2",
        "diastolic_2",
        "systolic_3",
        "diastolic_3",
        "pulse_1",
        "pulse_2",
        "pulse_3",
    ]

    numeric_cols = [
        "coded_cuff_size",
        "systolic_1",
        "diastolic_1",
        "systolic_2",
        "diastolic_2",
        "systolic_3",
        "diastolic_3",
        "pulse_1",
        "pulse_2",
        "pulse_3",
    ]

    user_bp_df[numeric_cols] = user_bp_df[numeric_cols].fillna(
        user_bp_df[numeric_cols].mean()
    )
    user_bp_df["systolic"] = user_bp_df[
        ["systolic_1", "systolic_2", "systolic_3"]
    ].mean(axis=1)
    user_bp_df["diastolic"] = user_bp_df[
        ["diastolic_1", "diastolic_2", "diastolic_3"]
    ].mean(axis=1)
    user_bp_df["pulse"] = user_bp_df[["pulse_1", "pulse_2", "pulse_3"]].mean(axis=1)

    user_bp_df = user_bp_df.drop(
        [
            "coded_cuff_size",
            "systolic_1",
            "systolic_2",
            "systolic_3",
            "diastolic_1",
            "diastolic_2",
            "diastolic_3",
            "pulse_1",
            "pulse_2",
            "pulse_3",
            "selected_arm",
        ],
        axis=1,
    )

    return user_bp_df


def load_users_health():
    user_df = load_user_body_measure_dataset()
    user_bp_df = load_user_bp_dataset()
    users = pd.merge(user_df, user_bp_df, on="seqn")

    return users


def load_food_pref_dataset():
    main_food_df = pd.read_excel("dataset/food/MainFoodDesc.xlsx")
    user_food_pref = pd.read_sas("dataset/user/IndividualFoods.XPT")
    user_food_pref.columns = [
        "seqn",
        "dietary_day_one_sample_weight",
        "dietary_day_two_sample_weight",
        "food_component_number",
        "dietary_recall_status",
        "interviewer_id_code",
        "breast_fed_infant",
        "number_of_days_of_intake",
        "number_of_days_bn_intake_and_interview",
        "intake_day_of_week",
        "respondent_language",
        "combination_food_number",
        "combination_food_type",
        "time_of_eating_occasion",
        "name_of_eating_occasion",
        "source_of_food",
        "location_of_food_home",
        "usda_food_code",
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

    user_food_pref.drop(
        [
            "dietary_day_one_sample_weight",
            "dietary_day_two_sample_weight",
            "food_component_number",
            "dietary_recall_status",
            "interviewer_id_code",
            "respondent_language",
            "combination_food_number",
            "number_of_days_bn_intake_and_interview",
            "number_of_days_of_intake",
            "time_of_eating_occasion",
            "combination_food_type",
            "breast_fed_infant",
        ],
        inplace=True,
        axis=1,
    )

    user_food_pref["usda_food_code"] = user_food_pref["usda_food_code"].apply(int)

    user_food_pref["seqn"] = user_food_pref["seqn"].apply(int)

    user_data = pd.merge(
        user_food_pref, main_food_df, left_on="usda_food_code", right_on="Food code"
    )

    source_of_food = {
        1: "Store - grocery/supermarket",
        2: "Restaurant with waiter/waitress",
        3: "Restaurant fast food/pizza",
        4: "Bar/tavern/lounge",
        5: "Restaurant no additional information",
        6: "Cafeteria NOT in a K-12 school",
        7: "Cafeteria in a K-12 school",
        8: "Child/Adult care center",
        9: "Child/Adult home care",
        10: "Soup kitchen/shelter/food pantry",
        11: "Meals on Wheels",
        12: "Community food program - other",
        13: "Community program no additional information",
        14: "Vending machine",
        15: "Common coffee pot or snack tray",
        16: "From someone else/gift",
        17: "Mail order purchase",
        18: "Residential dining facility",
        19: "Grown or caught by you or someone you know",
        20: "Fish caught by you or someone you know",
        24: "Sport, recreation, or entertainment facility",
        25: "Street vendor, vending truck",
        26: "Fundraiser sales",
        27: "Store - convenience type",
        28: "Store - no additional info",
        91: "Other, specify",
        99: "Don't know",
    }

    name_of_occasion = {
        1: "Breakfast",
        2: "Lunch",
        3: "Dinner",
        4: "Supper",
        5: "Brunch",
        6: "Snack",
        7: "Drink",
        8: "Infant feeding",
        9: "Extended consumption",
        10: "Desayano",
        11: "Almuerzo",
        12: "Comida",
        13: "Merienda",
        14: "Cena",
        15: "Entre comida",
        16: "Botana",
        17: "Bocadillo",
        18: "Tentempie",
        19: "Bebida",
        91: "Other",
        99: "Don't know",
    }

    days = [
        "",
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    ]

    location_of_food_home = {1: "Yes", 2: "No", 7: "Refused", 9: "Don't know"}

    user_data.dropna(inplace=True)

    user_data["intake_day_of_week"] = user_data["intake_day_of_week"].apply(
        lambda x: days[int(x)]
    )
    user_data["name_of_eating_occasion"] = user_data["name_of_eating_occasion"].apply(
        lambda x: name_of_occasion[int(x)]
    )
    user_data["source_of_food"] = user_data["source_of_food"].apply(
        lambda x: source_of_food[int(x)]
    )
    user_data["location_of_food_home"] = user_data["location_of_food_home"].apply(
        lambda x: location_of_food_home[int(x)]
    )

    return user_data
