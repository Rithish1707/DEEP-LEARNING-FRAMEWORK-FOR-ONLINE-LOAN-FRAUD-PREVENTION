from tkinter import *
import tkinter
from tkinter import filedialog
import numpy as np
from tkinter.filedialog import askopenfilename
import pandas as pd 
from tkinter import simpledialog
import numpy as np
import seaborn as sns
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
import os
import joblib
import matplotlib.pyplot as plt

main = tkinter.Tk()
main.title("Advanced Neural Networks Architetcure for Detecting Fraud in Internet Loan Applications") 
main.geometry("1500x1000")

global filename
global x_train,y_train,x_test,y_test
global X, Y
global le
global dataset
accuracy = []
precision = []
recall = []
fscore = []
global classifier
global cnn_model

def uploadDataset():
    global filename
    global dataset
    text.delete('1.0', END)
    filename = filedialog.askopenfilename(initialdir = "dataset")
    text.insert(END,filename+' Loaded\n')
    dataset = pd.read_csv(filename)
    text.insert(END,str(dataset.head())+"\n\n")

def preprocessDataset():
    global X, y
    global le
    global dataset,le
    global x_train,y_train,x_test,y_test
    le = LabelEncoder()
    dataset['type']=le.fit_transform(dataset['type'])
    dataset['nameOrig']=le.fit_transform(dataset['nameOrig'])
    dataset['nameDest']=le.fit_transform(dataset['nameDest'])
    text.delete('1.0', END)
    dataset.fillna(0, inplace = True)
    text.insert(END,"Dataset after preprocessing"+'\n\n'+str(dataset)+"\n\n")
    
    
    X = dataset.drop('isFraud',axis=1)
    y = dataset.iloc[:,-1]
    # Create a count plot
    sns.set(style="darkgrid")  # Set the style of the plot
    plt.figure(figsize=(8, 6))  # Set the figure size
    # Replace 'dataset' with your actual DataFrame and 'Drug' with the column name
    ax = sns.countplot(x='isFraud', data=dataset, palette="Set3")
    plt.title("Count Plot")  # Add a title to the plot
    plt.xlabel("Categories")  # Add label to x-axis
    plt.ylabel("Count")  # Add label to y-axis
    # Annotate each bar with its count value
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                textcoords='offset points')

    plt.show()  # Display the plot
    
def analysis():
    global X,y
    smote = SMOTE(sampling_strategy='auto', random_state=42)
    X,y= smote.fit_resample(X, y)
    text.insert(END,"Total records found in dataset after applying SMOTE: "+str(X.shape[0])+"\n\n")
    
    # Create a count plot
    sns.set(style="darkgrid")  # Set the style of the plot
    plt.figure(figsize=(8, 6))  # Set the figure size
    # Replace 'dataset' with your actual DataFrame and 'Drug' with the column name
    ax = sns.countplot(x=y, palette="Set3")
    plt.title("Count Plot")  # Add a title to the plot
    plt.xlabel("Categories")  # Add label to x-axis
    plt.ylabel("Count")  # Add label to y-axis
    # Annotate each bar with its count value
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                textcoords='offset points')
    plt.show()
def splitting():
    global x_train, x_test, y_train, y_test
    x_train, x_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=0)
    text.insert(END,"Total records used for training : "+str(x_train.shape[0])+"\n\n")
    text.insert(END,"Total records used for testing: "+str(x_test.shape[0])+"\n\n")

def custom_knn_classifier():
    global x_train, y_train
    global KNN
    text.delete('1.0', END)
    # Check if kNN model file exists
    if os.path.exists('model/knn_classifier.joblib'):
        # Load saved kNN model
        KNN = joblib.load('model/knn_classifier.joblib')
        print("kNN model loaded successfully.")
        predict = KNN.predict(x_test)
        p = precision_score(y_test, predict, average='macro') * 100
        r = recall_score(y_test, predict, average='macro') * 100
        f = f1_score(y_test, predict, average='macro') * 100
        a = accuracy_score(y_test, predict) * 100
        accuracy.append(a)
        precision.append(p)
        recall.append(r)
        fscore.append(f)
        text.insert(END, "KNN Precision : " + str(p) + "\n")
        text.insert(END, "KNN Recall    : " + str(r) + "\n")
        text.insert(END, "KNN FMeasure  : " + str(f) + "\n")
        text.insert(END, "KNN Accuracy  : " + str(a) + "\n\n")
        # Compute confusion matrix
        cm = confusion_matrix(y_test,predict)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('KNN Classifier Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.show()
        # Compute classification report
        report = classification_report(y_test,predict)
        # Display confusion matrix in the Text widget
        text.insert(END, "Confusion Matrix:\n")
        text.insert(END, str(cm) + "\n\n")
        # Display classification report in the Text widget
        text.insert(END, "Classification Report:\n")
        text.insert(END, report)
    else:
        
        KNN = KNeighborsClassifier(n_neighbors=10,leaf_size=30,metric='minkowski',)  # Create an instance of KNeighborsClassifier
        #x_train_reshaped = np.array(x_train).reshape(-1, 1)
        #x_test_reshaped = np.array(x_test).reshape(-1, 1)
        KNN.fit(x_train, y_train)
        # Save kNN classifier to file
        joblib.dump(KNN, 'model/knn_classifier.joblib')
        predict = KNN.predict(x_test)
        p = precision_score(y_test, predict, average='macro') * 100
        r = recall_score(y_test, predict, average='macro') * 100
        f = f1_score(y_test, predict, average='macro') * 100
        a = accuracy_score(y_test, predict) * 100
        accuracy.append(a)
        precision.append(p)
        recall.append(r)
        fscore.append(f)
        text.insert(END, "KNN Precision : " + str(p) + "\n")
        text.insert(END, "KNN Recall    : " + str(r) + "\n")
        text.insert(END, "KNN FMeasure  : " + str(f) + "\n")
        text.insert(END, "KNN Accuracy  : " + str(a) + "\n\n")
        # Compute confusion matrix
        cm = confusion_matrix(y_test,predict)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('KNN Classifier Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.show()
        # Compute classification report
        report = classification_report(y_test,predict)
        # Display confusion matrix in the Text  widget
        text.insert(END, "Confusion Matrix:\n")
        text.insert(END, str(cm) + "\n\n")
        # Display classification report in the Text widget
        text.insert(END, "Classification Report:\n")
        text.insert(END, report)
   

def MLPclassifier():
    global x_train, y_train, x_test, y_test
    global MLP
    text.delete('1.0', END)
    # Check if MLP model file exists
    if os.path.exists('model/mlp_classifier.joblib'):
        # Load saved MLP model
        MLP= joblib.load('model/mlp_classifier.joblib')
        print("MLP model loaded successfully.")
        predict = MLP.predict(x_test)
        
        p = precision_score(y_test, predict, average='macro', zero_division=0) * 100
        r = recall_score(y_test, predict, average='macro', zero_division=0) * 100
        f = f1_score(y_test, predict, average='macro', zero_division=0) * 100
        a = accuracy_score(y_test, predict) * 100
        accuracy.append(a)
        precision.append(p)
        recall.append(r)
        fscore.append(f)
        # Display precision, recall, F1-score, and accuracy in the Text widget
        text.insert(END, "MLP Precision: " + str(p) + "\n")
        text.insert(END, "MLP Recall: " + str(r) + "\n")
        text.insert(END, "MLP FMeasure: " + str(f) + "\n")
        text.insert(END, "MLP Accuracy: " + str(a) + "\n\n")
        
        # Compute confusion matrix
        cm = confusion_matrix(y_test, predict)
        
        # Compute classification report
        report = classification_report(y_test, predict)
        
        # Display confusion matrix in the Text widget
        text.insert(END, "Confusion Matrix:\n")
        text.insert(END, str(cm) + "\n\n")
        
        # Display classification report in the Text widget
        text.insert(END, "Classification Report:\n")
        text.insert(END, report)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('MLPclassifier Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.show()
        report= classification_report(y_test, predict)
        print(report)
    else:
        # After training with Cross validation, this was derived as the best model.
        MLP = MLPClassifier()
    
        # commence training -
        MLP.fit(x_train, y_train)
        # Save MLP classifier to file
        joblib.dump(MLP, 'model/mlp_classifier.joblib')
        predict = MLP.predict(x_test)
        
        p = precision_score(y_test, predict, average='macro', zero_division=0) * 100
        r = recall_score(y_test, predict, average='macro', zero_division=0) * 100
        f = f1_score(y_test, predict, average='macro', zero_division=0) * 100
        a = accuracy_score(y_test, predict) * 100
        accuracy.append(a)
        precision.append(p)
        recall.append(r)
        fscore.append(f)
        # Display precision, recall, F1-score, and accuracy in the Text widget
        text.insert(END, "MLP Precision: " + str(p) + "\n")
        text.insert(END, "MLP Recall: " + str(r) + "\n")
        text.insert(END, "MLP FMeasure: " + str(f) + "\n")
        text.insert(END, "MLP Accuracy: " + str(a) + "\n\n")
        
        # Compute confusion matrix
        cm = confusion_matrix(y_test, predict)
        
        # Compute classification report
        report = classification_report(y_test, predict)
        
        # Display confusion matrix in the Text widget
        text.insert(END, "Confusion Matrix:\n")
        text.insert(END, str(cm) + "\n\n")
        
        # Display classification report in the Text widget
        text.insert(END, "Classification Report:\n")
        text.insert(END, report)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('MLP Classifier Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.show()
        report= classification_report(y_test, predict)
        print(report)

def Prediction():
    filename = filedialog.askopenfilename(initialdir="Dataset")
    text.delete('1.0', END)
    text.insert(END, f'{filename} Loaded\n')
    dataset = pd.read_csv(filename)
    dataset['type']=le.fit_transform(dataset['type'])
    dataset['nameOrig']=le.fit_transform(dataset['nameOrig'])
    dataset['nameDest']=le.fit_transform(dataset['nameDest'])
    for i in range(len(dataset)):
        input_data = dataset.iloc[i, :].values.reshape(1, -1)
        predict = KNN.predict(input_data)  # Assuming MLP.predict expects a 2D array
        
        text.insert(END, f'Input data for row {i}: {input_data}\n')
        if predict == 0:
            predicted_data = "No Fruad"  
        elif predict == 1:
            predicted_data = "fruad"
                
        text.insert(END, f'Predicted output for row {i}: {predicted_data}\n')
def graph():
    # Create a DataFrame
    df = pd.DataFrame([
    ['KNN', 'Precision', precision[0]],
    ['KNN', 'Recall', recall[0]],
    ['KNN', 'F1 Score', fscore[0]],
    ['KNN', 'Accuracy', accuracy[0]],
    ['MLP', 'Precision', precision[-1]],
    ['MLP', 'Recall', recall[-1]],
    ['MLP', 'F1 Score', fscore[-1]],
    ['MLP', 'Accuracy', accuracy[-1]],
    ], columns=['Parameters', 'Algorithms', 'Value'])

    # Pivot the DataFrame and plot the graph
    pivot_df = df.pivot_table(index='Parameters', columns='Algorithms', values='Value', aggfunc='first')
    pivot_df.plot(kind='bar')
    # Set graph properties
    plt.title('Classifier Performance Comparison')
    plt.ylabel('Score')
    plt.xticks(rotation=0)
    plt.tight_layout()
    # Display the graph
    plt.show()
def close():
    main.destroy()

font = ('times', 16, 'bold')
title = Label(main, text='Advanced Neural Networks Architetcure for Detecting Fraud in Internet Loan Applications', justify=LEFT)
title.config(bg='misty rose', fg='blue')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=100,y=5)
title.pack()

font1 = ('times', 13, 'bold')
uploadButton = Button(main, text="Upload Dataset", command=uploadDataset)
uploadButton.place(x=50,y=100)
uploadButton.config(font=font1)

preprocessButton = Button(main, text="Preprocess Dataset", command=preprocessDataset)
preprocessButton.place(x=220,y=100)
preprocessButton.config(font=font1)

analysisButton = Button(main, text="Applying smote", command=analysis)
analysisButton.place(x=450,y=100)
analysisButton.config(font=font1)

analysisButton = Button(main, text="Data splitting",command=splitting)
analysisButton.place(x=50,y=150)
analysisButton.config(font=font1) 

knnButton = Button(main, text="KNN Classifier", command=custom_knn_classifier)
knnButton.place(x=220,y=150)
knnButton.config(font=font1)

LRButton = Button(main, text="Deep Learning Model", command=MLPclassifier)
LRButton.place(x=420,y=150)
LRButton.config(font=font1)

predictButton = Button(main, text="Prediction", command=Prediction)
predictButton.place(x=50,y=200)
predictButton.config(font=font1)

graphButton = Button(main, text="Comparison Graph", command=graph)
graphButton.place(x=200,y=200)
graphButton.config(font=font1)

exitButton = Button(main, text="Exit", command=close)
exitButton.place(x=400,y=200)
exitButton.config(font=font1)
                        

font1 = ('times', 12, 'bold')
text=Text(main,height=23,width=183)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=300)
text.config(font=font1) 

main.config(bg='LightSteelBlue1')
main.mainloop()



