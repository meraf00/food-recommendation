#!/usr/bin/env python
# coding: utf-8

# In[105]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[106]:


RANDOM_SEED = 42


# In[107]:


food_ing_df = pd.read_excel('dataset/food/FNDDSIngred.xlsx')
nutrient_df = pd.read_excel('dataset/food/NutDesc.xlsx')
food_nut_df = pd.read_excel('dataset/food/FNDDSNutVal.xlsx')
main_food_df = pd.read_excel('dataset/food/MainFoodDesc.xlsx')


# In[108]:


food_ing_df.head()


# In[109]:


nutrient_df.head()


# In[110]:


main_food_df.head()


# In[111]:


user_df = pd.read_sas('dataset/user/BodyMeasures.XPT')
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
user_df = user_df.drop(['status', 'recumbent_length', 'bmi_category', 'head_circumference', 'weight_comment', 'recumbent_length_comment', 'head_circumference_comment', 'height_comment', 'upper_leg_length_comment', 'upper_arm_length_comment', 'arm_circumference_comment', 'waist_circumference_comment', 'hip_circumference_comment'], axis=1)
user_df = user_df.fillna(user_df.mean())
user_df.head()


# In[112]:


user_bp_df = pd.read_sas('dataset/user/BloodPressure.XPT')

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
user_bp_df.head()


# In[113]:


user_bp_df.info()


# In[114]:


numeric_cols = ["coded_cuff_size", "systolic_1", "diastolic_1", "systolic_2", "diastolic_2", "systolic_3", "diastolic_3", "pulse_1", "pulse_2", "pulse_3"]
user_bp_df[numeric_cols] = user_bp_df[numeric_cols].fillna(user_bp_df[numeric_cols].mean())


# In[115]:


user_bp_df['systolic'] = user_bp_df[['systolic_1', 'systolic_2', 'systolic_3']].mean(axis=1)
user_bp_df['diastolic'] = user_bp_df[['diastolic_1', 'diastolic_2', 'diastolic_3']].mean(axis=1)
user_bp_df['pulse'] = user_bp_df[['pulse_1', 'pulse_2', 'pulse_3']].mean(axis=1)

user_bp_df = user_bp_df.drop(['coded_cuff_size', 'systolic_1', 'systolic_2', 'systolic_3', 'diastolic_1', 'diastolic_2', 'diastolic_3', 'pulse_1', 'pulse_2', 'pulse_3', 'selected_arm'], axis=1)
user_bp_df.head()


# In[116]:


sns.histplot(user_bp_df['systolic'])
sns.histplot(user_bp_df['diastolic'])
sns.histplot(user_bp_df['pulse'])


# In[117]:


user = pd.merge(user_df, user_bp_df, on='seqn')
user.head()


# In[118]:


user_food_pref = pd.read_sas('dataset/user/IndividualFoods.XPT')
user_food_pref.head()


# In[119]:


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


# In[120]:


user_food_pref.drop(["dietary_day_one_sample_weight", "dietary_day_two_sample_weight", "food_component_number","dietary_recall_status", "interviewer_id_code", "respondent_language", "combination_food_number","number_of_days_bn_intake_and_interview","number_of_days_of_intake", "time_of_eating_occasion"], inplace=True, axis=1)


# In[121]:


user_food_pref.head()


# In[122]:


user_food_pref['usda_food_code'] = user_food_pref['usda_food_code'].apply(int)
user_food_pref['seqn'] = user_food_pref['seqn'].apply(int)


# In[123]:


merged = pd.merge(user_food_pref, main_food_df, left_on='usda_food_code', right_on='Food code')
merged.head()


# In[124]:


source_of_food = ['Store - grocery/supermarket', 'Restaurant with waiter/waitress', 'Restaurant fast food/pizza', 'Bar/tavern/lounge', 'Restaurant no additional information',
                  'Cafeteria NOT in a K-12 school', 'Cafeteria in a K-12 school', 'Child/Adult care center', 'Child/Adult home care', 'Soup kitchen/shelter/food pantry',
                  'Meals on Wheels', 'Community food program - other', 'Community program no additional information', 'Vending machine', 'Common coffee pot or snack tray',
                  'From someone else/gift', 'Mail order purchase', 'Residential dining facility', 'Grown or caught by you or someone you know', 'Fish caught by you or someone you know',
                  'Sport, recreation, or entertainment facility', 'Street vendor, vending truck', 'Fundraiser sales', 'Store - convenience type', 'Store - no additional info',
                  'Other, specify', "Don't know"]


# In[125]:


name_of_occasion = ['Breakfast', 'Lunch', 'Dinner', 'Supper', 'Brunch', 'Snack', 'Drink', 'Infant feeding', 'Extended consumption', 'Desayano', 'Almuerzo',
                    'Comida', 'Merienda', 'Cena', 'Entre comida', 'Botana', 'Bocadillo', 'Tentempie', 'Bebida','Other', "Don't know"]


# In[126]:


merged.columns


# In[127]:


merged.head()


# In[128]:


merged.info()


# In[129]:


user_data = merged.dropna()


# In[130]:


user_data.head()


# In[ ]:




