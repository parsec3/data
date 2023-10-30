#This here serves as an addendum to the Python script.
#Here, I will do some tasks that I find easier in R than in Python, such as significance testing and determining correlations.

#We import all we need (and possibly a little more):


library(PerformanceAnalytics)

#We load the data again.

candy<-read.csv("C:/Users/mapap/Documents/Informatik/Lidl/candy-data.csv",header=T)

#As in Python

candy$winpercent = candy$winpercent/100

#Let's take a look at the data (again).

head(candy)
chart.Correlation(candy[,11:13], histogram=TRUE, pch=19)

#Seems fairly normally distributed, so we can do some linear regression here.
#First, we translate the variables into something handier

x1 = candy$sugarpercent
x2 = candy$pricepercent
y = candy$winpercent

#This is the source of the p-values we've had in Python:

sugar_model = lm(formula = y ~ x1, data = candy)
price_model = lm(formula = y ~ x2, data = candy)
summary(sugar_model)
summary(price_model)

#There's also a non-negligible chance that the correlation between sugar and popularity is by chance.
#Here's some correlation coefficients for the Python plot:

cor(x1, y)
cor(x2, y)

#A correlation coefficient of 0.2 is generally considered neglible[1]. 0.3 is also very weak, though notable.

#[1] Mukaka MM. Statistics corner: A guide to appropriate use of correlation coefficient in medical research.
#    Malawi Med J. 2012 Sep;24(3):69-71. PMID: 23638278; PMCID: PMC3576830.

#The correlation between price and popularity is notable, but only tangentially relevant to our question.
#We can probably ignore the sugar entirely.


#Finally, here's a multiple linear regression:
candy_model = lm(formula = y ~ x1 + x2, data = candy)

summary(candy_model)
#As in Python, we see that these variables only a explain a tiny fraction of the variance.


#Here is a glm for candy:

candymodel <-glm(winpercent ~ chocolate + fruity + caramel + peanutyalmondy + nougat + crispedricewafer + hard + bar + pluribus, family=binomial, data = candy)
summary(candymodel)

#As in Python, the logit coefficient is highest in chocolate.

#Here are correlation coefficients for some of the high-logit ingredients.

cor(candy$chocolate,y)
#[1] 0.6365167
cor(candy$fruity,y)
#[1] -0.3809381
cor(candy$peanutyalmondy,y)
#[1] 0.4061922
cor(candy$crispedricewafer,y)
#[1] 0.3246797


#We want to divide the dataset into "winners" and "losers" and analyze it.
#Remember: "Winners" are liked by more than 50% of respondents, "losers" by less than 50%.

losers = candy[which(candy$winpercent < .5),]
winners = candy[which(candy$winpercent >= .5),]

#Now, we can do t-tests to find out if certain candies are more popular among winners or losers.
#We want to know if the difference in distributions is statistically significant.

#First, chocolate:
t.test(losers$chocolate, winners$chocolate)
# p-value <.0001, very significant.

#Next, fruity candies:
t.test(losers$fruity, winners$fruity)
# p-value .004. Also significant (on the loser's side, that is)

#This, caramel:
t.test(losers$caramel, winners$caramel)
# p-value .044. A little bit significant, but not that much.


#Peanut butter/almond candies:
t.test(losers$peanutyalmondy, winners$peanutyalmondy)
# p-value .002. Significant.

#Nougat:
t.test(losers$nougat, winners$nougat)
# p-value .178. Insignificant.

#Crisped rice wafer:
t.test(losers$crispedricewafer, winners$crispedricewafer)
#p-value .04. In other words, not super significant

#hard:
t.test(losers$hard, winners$hard)
#p-value .0003 (significant on the loser's side).

#bar:
t.test(losers$bar, winners$bar)
#p-value .0003 (significant on the loser's side).


#Finally, pluribus candies.
t.test(losers$pluribus, winners$pluribus)
#p-value .17. Insignificant.
