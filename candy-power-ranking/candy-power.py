#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Created on Sat May 20 15:13:35 2023

@author: Petar
"""



import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
import seaborn as sns
import statistics


df = pd.read_csv("candy-data.csv") #Read the data.
print("Info of the data:",df.info()) #Give ourselves a basic overview of it.
print(df.keys()) #What datatypes do we have?

#We have the data types "object", "int64", and "float64".
#Columns 1-9 are clearly categorical data.
#Given the digits, the last three seem continuous to me.
#Therefore, I'll write a function describing its mean and std:

print("Describing the percentiles: ",df.describe(include='float64'))

#The sugar and price percentiles seem very similar to me.
#They have roughly the same minimum, maximum, standard deviation, and mean.
#Not many outliers, probably. I'd say we can plot the two of them against the win percentiles.

#I derived the p-values in R, since I considered it too difficult in Python.

#We have two independent and one dependent variable.
#I'd say we make two linear regressions to see how strongly they correlate with popularity.

#I calculated the correlation coefficients and p-vales in R. The code will be provided as well.

#Also, I divided the winpercent numbers by 100 so that they are between 1 and 0, like everything else. This will be important later.

df['winpercent'] = df['winpercent']/100

fig, axes = plt.subplots(1, 2, figsize=(15, 7), sharey=True)
fig.suptitle('Einfluss von Zucker und Preis auf die Beliebtheit',fontsize=30)

sns.regplot(ax=axes[0],x='sugarpercent', y='winpercent', color='red',data=df, ci=95)
axes[0].set_title("Zucker und Beliebtheit (korr. = 0.229, p = 3.49%)", fontdict={'fontsize': 17})
sns.regplot(ax=axes[1],x='pricepercent', y='winpercent', color='blue',data=df, ci=95)
axes[1].set_title("Preis und Beliebtheit (korr. = 0.345, p = 0.12%)", fontdict={'fontsize': 17})

#The p-value and the correlation coefficient were all calculated in an R-script.
#They are primarily here to give the figure a quantitative touch.
#I will discuss them in the R-script.

#From visual inspection, we can tell that the slope is very flat for both.
#Also, most data points are far from the regression, although it looks a little bit better in the price.

#It seems like neither of these two can really explain a lot of the variation in the dataset.
#Can we prove this or is it just a hunch?

#Well, we can.
#A multiple linear regression tells us how much of the variance in winpercent is explained by these two variables.

X_con = df[['sugarpercent', 'pricepercent']]
y = df['winpercent']

regr = linear_model.LinearRegression()
regr.fit(X_con, y)

print(regr.score(X_con,y))

#The score is 0.134.
#So, roughly 13% of variation can be explained by the sugar and price percentage.
#That's almost nothing. From a marketing perspective, neither of these two are interesting.


#Here, we can also calculate the slope that was used in the figure:

print(regr.coef_)

#0.067 and 0.156 for the sugar and price, respectively.
#Again, two very flat slopes, especially the sugar.


#We need something else.
#How do the categorical variables measure up?

X_cat = df[['chocolate', 'fruity', 'caramel', 'peanutyalmondy',
       'nougat', 'crispedricewafer', 'hard', 'bar', 'pluribus']]
y = df['winpercent']

regr.fit(X_cat, y)

regr.score(X_cat,y)

#Together, these explain 51.48% of the variation which is still not great, but a start.
#We, unfortunately, can't do linear regression with these dummy variables, so we might try something else.

import statsmodels.formula.api as smf


candymodel = smf.logit(formula = 'winpercent ~ chocolate + fruity + caramel + peanutyalmondy + nougat + crispedricewafer + hard + bar + pluribus', data = df).fit() 

#It seems like chocolate is the clear winner. Logit coef. = 0.8155
#It's p-value isn't great (p=0.27), but it's far better than in the rest.
#Fruity (coef = 0.4347, p=0.549), Peanutalmondy(coef = 0.4343, p=0.530),

#For the rest, we have nothing, but statistical noise where the results are more likely by chance than not.
#So, we need a different approach.

#We could try clustering them.

#According to the df.describe we did above, the mean of "winpercent" column is 50.3
#It's median is 47.83:
    
print(statistics.median(df['winpercent']))

#Also, 39 of 85 (or, in other words, 46%) of all scores are greater than 50%:

sum(i > 0.5 for i in df['winpercent'])

#I'd say it's safe to say that roughly half of all sweets are liked by above or below half.

#Let's create two clusters. One of winners above 50% and the other losers below 50%.

winners = df[df['winpercent'] > 0.5]

losers = df[df['winpercent'] < 0.5]

#Let's isolate categorical data here, too:

X_cat_w = winners[['chocolate', 'fruity', 'caramel', 'peanutyalmondy',
       'nougat', 'crispedricewafer', 'hard', 'bar', 'pluribus']]

X_cat_l = losers[['chocolate', 'fruity', 'caramel', 'peanutyalmondy',
       'nougat', 'crispedricewafer', 'hard', 'bar', 'pluribus']]

for i in X_cat.columns:
    winner_share = X_cat_w[i].value_counts()[1]/0.39
    loser_share = X_cat_l[i].value_counts()[1]/0.46
    win_bonus = round(winner_share,3)/round(loser_share,3)
    print(i," is present among ",round(winner_share,3),"% of winners and ",round(loser_share,3),"% of losers.")
    
    
#chocolate  is present among  71.795 % of winners and  19.565 % of losers (p<0.0001).
#fruity  is present among  28.205 % of winners and  58.696 % of losers (p=0.004).
#caramel  is present among  25.641 % of winners and  8.696 % of losers (p=0.044).
#peanutyalmondy  is present among  30.769 % of winners and  4.348 % of losers (p=0.002).
#nougat  is present among  12.821 % of winners and  4.348 % of losers (p=0.178).
#crispedricewafer  is present among  15.385 % of winners and  2.174 % of losers (p=0.04).
#hard  is present among  2.564 % of winners and  30.435 % of losers (p=0.0003).
#bar  is present among  43.59 % of winners and  8.696 % of losers (p=0.0003).
#pluribus  is present among  43.59 % of winners and  58.696 % of losers (p=0.169).

#For the p-values, I will again refer you to the R-script.