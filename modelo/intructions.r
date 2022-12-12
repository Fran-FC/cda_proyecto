library(jsonlite)
library("tidyverse")  # data manipulation
library("cluster")    # clustering algorithms
library("factoextra") # clustering algorithms & visualization
library(tidyverse)
library(caret)
library(ggplot2)

dt <- fromJSON("dataset/InfoRecortada.json")
df=dt %>% select(oscilacionTermica, temMed, rachMax, precMaxMen)

df <- as.data.frame(scale(df))
df <- na.omit(df)

# first analysis for clustering
x = c()
y = c()
for(i in 1:11) {
  k2 <- kmeans(df, centers = i, nstart= 1)
  x = append(x, i)
  y = append(y, k2$tot.withinss)
  silhouette(x = k2$cluster, dist = )
}
p = plot(x, y, type="b", pch=16, col="red", 
         main ="Sum of withinss for each number of clusters")


fviz_nbclust(x=df,kmeans,method = c("wss"))
fviz_nbclust(x=df,kmeans,method = c("silhouette"))

# clean the data with no String varibles
#spain have 6 diferents 
k2 <- kmeans(df, centers = 6, nstart = 25)

# uses PCA to plot the data
fviz_cluster(k2, df, 
             ellipse.type = "convex",
             geom=c("point"), 
             palette = "jco", 
             ggtheme = theme_classic()) #you can change the color palette and theme to your preferences



# data_plot = data.frame(x,y)
# # col_names c("clusters", "tot_withinss")
# a = ggplot(data_plot, aes(x,y))
# a+geom_curve(x, y)
#        