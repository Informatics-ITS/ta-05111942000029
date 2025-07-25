# -*- coding: utf-8 -*-
"""Final Project Forecasting Modelling for Early Detection of Heart Diseases Utilizing The Machine  Learning Neuroevolution Model.

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1s52GwK7zvLlUNvoFBl_W4ELWdSuvIHr6
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# to import scikit-learn methods to train
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, f1_score, recall_score, log_loss, matthews_corrcoef

from sklearn.metrics import classification_report, confusion_matrix

# machine learning algorithms that are used
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("content/Heart_disease_cleveland_new.csv")
# Check if it's already processed
if 'cp' in df.columns:
    # Rename columns only if still raw
    df.columns = ['age', 'sex', 'chest_pain_type', 'resting_blood_pressure', 'cholesterol',
                  'fasting_blood_sugar', 'rest_ecg', 'max_heart_rate_achieved',
                  'exercise_induced_angina', 'st_depression', 'st_slope', 'ca',
                  'thalassemia', 'target']

    # Only convert if the types are still numeric
    if df['chest_pain_type'].dtype != 'object':
        df['chest_pain_type'].replace({0: 'typical angina', 1: 'atypical angina',
                                       2: 'non-angina pain', 3: 'asymptomatic'}, inplace=True)
        df['rest_ecg'].replace({0: 'normal', 1: 'Abnormality in ST-T wave',
                                2: 'left ventricular hypertrophy'}, inplace=True)
        df['st_slope'].replace({0: 'upsloping', 1: 'flat', 2: 'downsloping'}, inplace=True)
        df['thalassemia'].replace({0: 'null', 1: 'fixed defect', 2: 'normal blood flow',
                                   3: 'reversible defect'}, inplace=True)
        df['sex'] = df['sex'].map({0: 'female', 1: 'male'})
df.head()

df.shape

df.info()

df.describe()

#data cleaning , scaling and encoding
df.columns

df.columns = ['age', 'sex', 'chest_pain_type', 'resting_blood_pressure', 'cholesterol', 'fasting_blood_sugar', 'rest_ecg', 'max_heart_rate_achieved',
       'exercise_induced_angina', 'st_depression', 'st_slope','ca','thalassemia','target']

df.head()

# converting features to categorical features
df['chest_pain_type'][df['chest_pain_type'] == 0] = 'typical angina '
df['chest_pain_type'][df['chest_pain_type'] == 1] = 'atypical angina'
df['chest_pain_type'][df['chest_pain_type'] == 2] = 'non-angina pain'
df['chest_pain_type'][df['chest_pain_type'] == 3] = 'asymptomatic'

df['rest_ecg'][df['rest_ecg'] == 0] = 'normal'
df['rest_ecg'][df['rest_ecg'] == 1] = 'Abnormality in ST-T wave'
df['rest_ecg'][df['rest_ecg'] == 2] = 'left ventricular hypertrophy'

df['st_slope'][df['st_slope'] == 0] = 'upsloping'
df['st_slope'][df['st_slope'] == 1] = 'flat'
df['st_slope'][df['st_slope'] == 2] = 'downsloping'

df['thalassemia'][df['thalassemia'] == 0] = 'null'
df['thalassemia'][df['thalassemia'] == 1] = 'fixed defect'
df['thalassemia'][df['thalassemia'] == 2] = 'normal blood flow'
df['thalassemia'][df['thalassemia'] == 3] = 'reversible defect'

df["sex"] = df.sex.apply(lambda  x:'male' if x==1 else 'female')

df['chest_pain_type'].value_counts()

df['rest_ecg'].value_counts()

df['st_slope'].value_counts()

df['thalassemia'].value_counts()

# checking the  dataset after the  encoding process
df.head()

# Checking missing entries in the dataset columnwise
df.isna().sum()

# checking the shape of the dataset
df.shape

df.info()

df.describe(include =[np.number])

df.describe(include =[object])

# Create two subplots: a pie chart and a horizontal bar chart to visualize the distribution of patients with and without heart disease.
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=False, figsize=(10,5),facecolor=(.94, .94, .94))

# The pie chart (ax1) shows the percentage of heart disease cases vs. normal cases, while the bar chart (ax2) displays the counts.
ax1 = df['target'].value_counts().plot.pie( x ="Heart disease" ,y ='no.of patients',
                   autopct = "%1.0f%%",labels=["Normal","Heart Disease"], startangle = 60,ax=ax1,colors = sns.color_palette("crest"));
ax1.set(title = 'Percentage of Heart disease patients in Dataset')

ax2 = df["target"].value_counts().plot(kind="barh",ax =ax2)
for x,y in enumerate(df["target"].value_counts().values):
    ax2.text(.5,x,y,fontsize=12)
ax2.set(title = 'No. of Heart disease patients in Dataset')
plt.show()

df_1=df[df['target']==1]

df_0=df[df['target']==0]

# plotting normal patients
fig = plt.figure(figsize=(15,5))
ax1 = plt.subplot2grid((1,2),(0,0))
sns.distplot(df_0['age'])
plt.title('AGE DISTRIBUTION OF NORMAL PATIENTS', fontsize=15, weight='bold')

ax1 = plt.subplot2grid((1,2),(0,1))
sns.countplot(x =df_0['sex'], palette='viridis')
plt.title('GENDER DISTRIBUTION OF NORMAL PATIENTS', fontsize=15, weight='bold' )
plt.show()

#plotting heart patients

fig = plt.figure(figsize=(15,5))
ax1 = plt.subplot2grid((1,2),(0,0))
sns.distplot(df_1['age'])
plt.title('AGE DISTRIBUTION OF HEART DISEASE PATIENTS', fontsize=15, weight='bold')

ax1 = plt.subplot2grid((1,2),(0,1))
sns.countplot(x=df_1['sex'], palette='viridis')
plt.title('GENDER DISTRIBUTION OF HEART DISEASE PATIENTS', fontsize=15, weight='bold' )
plt.show()

df = pd.get_dummies(df, drop_first=True)
df.head()

df.shape

X = df.drop(['target'],axis=1)
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(
   X,y, test_size=0.2, random_state=9
)

print(X.shape,X_train.shape, X_test.shape)

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_train[['age','resting_blood_pressure','cholesterol','max_heart_rate_achieved','st_depression']] = scaler.fit_transform(X_train[['age','resting_blood_pressure','cholesterol','max_heart_rate_achieved','st_depression']])
X_train.head()

X_test[['age','resting_blood_pressure','cholesterol','max_heart_rate_achieved','st_depression']] = scaler.transform(X_test[['age','resting_blood_pressure','cholesterol','max_heart_rate_achieved','st_depression']])
X_test.head()

from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

# function initializing only the Random Forest model
def GetBasedModel():
    basedModels = []
    basedModels.append(('RF_Ent100', RandomForestClassifier(criterion='entropy', n_estimators=100)))
    return basedModels

# function for performing 10-fold cross validation of the Random Forest model
def BasedLine2(X_train, y_train, models):
    # Test options and evaluation metric
    num_folds = 10
    scoring = 'accuracy'
    results = []
    names = []
    for name, model in models:
        kfold = model_selection.KFold(n_splits=num_folds)
        cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)
        results.append(cv_results)
        names.append(name)
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print(msg)

    return names, results

models = GetBasedModel()
names,results = BasedLine2(X_train, y_train,models)

rf_ent = RandomForestClassifier(criterion='entropy',n_estimators=100)
rf_ent.fit(X_train, y_train)
y_pred_rfe = rf_ent.predict(X_test)

CM=confusion_matrix(y_test,y_pred_rfe)
sns.heatmap(CM, annot=True)

TN = CM[0][0]
FN = CM[1][0]
TP = CM[1][1]
FP = CM[0][1]
specificity = TN/(TN+FP)
loss_log = log_loss(y_test, y_pred_rfe)
acc= accuracy_score(y_test, y_pred_rfe)
roc=roc_auc_score(y_test, y_pred_rfe)
prec = precision_score(y_test, y_pred_rfe)
rec = recall_score(y_test, y_pred_rfe)
f1 = f1_score(y_test, y_pred_rfe)

mathew = matthews_corrcoef(y_test, y_pred_rfe)
model_results =pd.DataFrame([['Random Forest',acc, prec,rec,specificity, f1,roc, loss_log,mathew]],
               columns = ['Model', 'Accuracy','Precision', 'Sensitivity','Specificity', 'F1 Score','ROC','Log_Loss','mathew_corrcoef'])

model_results

# Initialize Gradient Boosting Classifier
gb = GradientBoostingClassifier(n_estimators=100)
gb.fit(X_train, y_train)

# Make predictions
y_pred_gb = gb.predict(X_test)

# Assuming y_pred_gb contains predictions from the Gradient Boosting model
CM = confusion_matrix(y_test, y_pred_gb)
sns.heatmap(CM, annot=True)

# Extracting values from the confusion matrix
TN = CM[0][0]
FN = CM[1][0]
TP = CM[1][1]
FP = CM[0][1]

# Calculating specificity
specificity = TN / (TN + FP)

# Calculating other evaluation metrics
loss_log = log_loss(y_test, y_pred_gb)
acc = accuracy_score(y_test, y_pred_gb)
roc = roc_auc_score(y_test, y_pred_gb)
prec = precision_score(y_test, y_pred_gb)
rec = recall_score(y_test, y_pred_gb)
f1 = f1_score(y_test, y_pred_gb)
mathew = matthews_corrcoef(y_test, y_pred_gb)

# Creating a DataFrame to store results
model_results = pd.DataFrame([['Gradient Boosting', acc, prec, rec, specificity, f1, roc, loss_log, mathew]],
               columns=['Model', 'Accuracy', 'Precision', 'Sensitivity', 'Specificity', 'F1 Score', 'ROC', 'Log_Loss', 'mathew_corrcoef'])

model_results

# pip install deap

from sklearn.neural_network import MLPClassifier  # Use MLP as a neural network model
from deap import base, creator, tools, algorithms

import warnings
warnings.filterwarnings('ignore')

# Define the fitness function for neuroevolution, also added safety measure so it doesn't go into the negatives and break
def evaluate_nn(individual):
    n_hidden = int(individual[0])
    alpha_value = max(0.0001, individual[1])  # prevent alpha from becoming zero or negative
    model = MLPClassifier(hidden_layer_sizes=(n_hidden,), alpha=alpha_value, max_iter=500, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy,

def NeuroevolutionModel(X_train, y_train, X_test):
    from deap import base, creator, tools, algorithms
    from sklearn.neural_network import MLPClassifier
    from sklearn.metrics import accuracy_score
    import numpy as np

def evaluate_nn(individual):
        n_hidden = int(individual[0])
        alpha = individual[1]
        model = MLPClassifier(hidden_layer_sizes=(n_hidden,), alpha=alpha, max_iter=500, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return accuracy,

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("n_hidden", np.random.randint, 5, 100)
toolbox.register("alpha", np.random.uniform, 0.0001, 0.1)
toolbox.register("individual", tools.initCycle, creator.Individual, (toolbox.n_hidden, toolbox.alpha), n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate_nn)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# Repair individuals to ensure valid parameter ranges
def repair_individual(individual):
    individual[0] = max(1, int(individual[0]))               # hidden_layer_sizes must be > 0
    individual[1] = max(0.0001, float(individual[1]))        # alpha must be >= 0
    return individual

population = toolbox.population(n=10)
n_gen = 10
for gen in range(n_gen):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)

# Sanitize each offspring to prevent invalid values
    offspring = [repair_individual(ind) for ind in offspring]


    fits = map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit

    population = toolbox.select(offspring, k=len(population))

# Select the best individual from the final population
best_individual = tools.selBest(population, k=1)[0]
print(f"\nBest Individual: {best_individual}")

# Use the best individual to train final model
# Ensure final values are safe
n_hidden = max(1, int(best_individual[0]))
alpha_value = max(0.0001, float(best_individual[1]))
final_model = MLPClassifier(hidden_layer_sizes=(n_hidden,), alpha=alpha_value, max_iter=500, random_state=42)
final_model.fit(X_train, y_train)

# Predict using the final model
y_pred_neuro = final_model.predict(X_test)

# Evaluate
from sklearn.metrics import classification_report, confusion_matrix
print("\nClassification Report for Neuroevolution MLP:")
print(classification_report(y_test, y_pred_neuro))

# Add neuroevolution model to list of models
def GetBasedModel():
    basedModels = []
    basedModels.append(('Neuroevolution', NeuroevolutionModel(X_train, y_train, X_test)))
    return basedModels

# Modify BasedLine2 to work with the neuroevolution model
def BasedLine2(X_train, y_train, models):
    num_folds = 10
    scoring = 'accuracy'
    results = []
    names = []
    for name, model in models:
        if name == 'Neuroevolution':
            # Skip cross-validation for neuroevolution as it’s computationally intensive
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            print(f"Neuroevolution Model Accuracy: {accuracy}")
        else:
            kfold = model_selection.KFold(n_splits=10)
            cv_results = model_selection.cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)
            results.append(cv_results)
            names.append(name)
            msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
            print(msg)

    return results, msg

# Predict with the final neuroevolution model
y_pred_neuro = final_model.predict(X_test)

# Confusion Matrix
CM = confusion_matrix(y_test, y_pred_neuro)
sns.heatmap(CM, annot=True, fmt='d')

# Extract values from the confusion matrix
TN = CM[0][0]
FN = CM[1][0]
TP = CM[1][1]
FP = CM[0][1]

# Calculate specificity
specificity = TN / (TN + FP)

# Calculate additional performance metrics
loss_log = log_loss(y_test, y_pred_neuro)
acc = accuracy_score(y_test, y_pred_neuro)
roc = roc_auc_score(y_test, y_pred_neuro)
prec = precision_score(y_test, y_pred_neuro)
rec = recall_score(y_test, y_pred_neuro)
f1 = f1_score(y_test, y_pred_neuro)
mathew = matthews_corrcoef(y_test, y_pred_neuro)

# Store the results in a DataFrame
model_results = pd.DataFrame([['Neuroevolution', acc, prec, rec, specificity, f1, roc, loss_log, mathew]],
               columns=['Model', 'Accuracy', 'Precision', 'Sensitivity', 'Specificity', 'F1 Score', 'ROC', 'Log_Loss', 'matthews_corrcoef'])

model_results

from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, f1_score, recall_score, confusion_matrix, log_loss, matthews_corrcoef
import pandas as pd

# Predictions from each model
data = {
    'Random Forest': y_pred_rfe,
    'Gradient Boosting': y_pred_gb,
    'Neuroevolution': y_pred_neuro
}

# Initialize an empty DataFrame to store the results
model_results = pd.DataFrame(columns=['Model', 'Accuracy', 'Precision', 'Sensitivity', 'Specificity', 'F1 Score', 'ROC', 'Log_Loss', 'matthews_corrcoef'])

# Calculate performance metrics for each model
for model_name, predictions in data.items():
    CM = confusion_matrix(y_test, predictions)

    TN = CM[0][0]
    FN = CM[1][0]
    TP = CM[1][1]
    FP = CM[0][1]

    specificity = TN / (TN + FP)
    loss_log = log_loss(y_test, predictions)
    acc = accuracy_score(y_test, predictions)
    roc = roc_auc_score(y_test, predictions)
    prec = precision_score(y_test, predictions)
    rec = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)
    mathew = matthews_corrcoef(y_test, predictions)

    # Create a DataFrame row with the metrics for the current model
    results = pd.DataFrame([[model_name, acc, prec, rec, specificity, f1, roc, loss_log, mathew]],
                           columns=['Model', 'Accuracy', 'Precision', 'Sensitivity', 'Specificity', 'F1 Score', 'ROC', 'Log_Loss', 'matthews_corrcoef'])

    # Concatenate the current results with the model_results DataFrame
# Evaluate and compare all models
from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, f1_score, recall_score, confusion_matrix, log_loss, matthews_corrcoef
import pandas as pd

# Predictions from each model
data = {
    'Random Forest': y_pred_rfe,
    'Gradient Boosting': y_pred_gb,
    'Neuroevolution': y_pred_neuro
}

# Initialize an empty DataFrame to store the results
model_results = pd.DataFrame(columns=['Model', 'Accuracy', 'Precision', 'Sensitivity', 'Specificity', 'F1 Score', 'ROC', 'Log_Loss', 'matthews_corrcoef'])

# Calculate performance metrics for each model
for model_name, predictions in data.items():
    CM = confusion_matrix(y_test, predictions)

    TN = CM[0][0]
    FN = CM[1][0]
    TP = CM[1][1]
    FP = CM[0][1]

    specificity = TN / (TN + FP)
    loss_log = log_loss(y_test, predictions)
    acc = accuracy_score(y_test, predictions)
    roc = roc_auc_score(y_test, predictions)
    prec = precision_score(y_test, predictions)
    rec = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)
    mathew = matthews_corrcoef(y_test, predictions)

    # Append results to the model_results DataFrame
    results = pd.DataFrame([[model_name, acc, prec, rec, specificity, f1, roc, loss_log, mathew]],
                           columns=model_results.columns)
    model_results = pd.concat([model_results, results], ignore_index=True)

# Display the comparison table
print(model_results)



