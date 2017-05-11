# Naive Bayes KDE visualization
# Nurvirta Monarizqa
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
import seaborn as sns
sns.set_style("white")
%pylab inline

def generatekde(file, param):
    prob = pd.read_csv(file)
    prob.columns = ["id","seword","piyungan"]
    prob["date"] = prob["id"].apply(lambda x: datetime.datetime.strptime(x[:10], "%Y-%m-%d"))
    prob["sel"] = prob["seword"] - prob["piyungan"]
    prob["daydelta"] = ((prob["date"] - datetime.datetime(2016, 10,5))/7)
    prob["week"]=(prob["daydelta"] / np.timedelta64(1, 'D')).astype(int)

    fig = plt.figure(figsize=(8,4))
    ax = fig.add_subplot(111)
    sns.kdeplot(prob[prob.week==-10]['sel'], ax=ax, label="Ten weeks before", color="purple")
    sns.kdeplot(prob[prob.week==0]['sel'], ax=ax,label="The incident week", color="gray", linestyle="--")
    sns.kdeplot(prob[prob.week==10]['sel'], ax=ax, label="Ten weeks after", color="orange")
    ax.set_xlabel("More Similar to Piyungan    Neutral     More Similar to Seword")
    ax.set_title("KDE of Posteriors: " +param, fontweight="bold", fontsize=16)
    return prob

prob2 = generatekde("theprobs_2.csv","Tolerance Issues")

# statistical test
d1= prob2[prob2.week==10]['sel']
d2= prob2[prob2.week==0]['sel']
d3= prob2[prob2.week==-0]['sel']
stats.ks_2samp(d1, d2)
stats.ks_2samp(d1, d3)
stats.ks_2samp(d3, d2)
