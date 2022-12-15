library(jsonlite)
library("tidyverse")  # data manipulation
library("cluster")    # clustering algorithms
library("factoextra") # clustering algorithms & visualization
library(tidyverse)
library(caret)
library(ggplot2)

dt <- fromJSON("info2011.json")
dt$oscilacion=dt$tmax-dt$tmin
df=dt %>% select(precTot,tmed,tmax,tmin)

df <- as.data.frame(scale(df))
df = replace(df,is.na(df),0)
# df <- na.omit(df)
# df <- na.predict(x=df, )

# first analysis for clustering
x = c()
y = c()
for(i in 1:11) {
  k2 <- kmeans(df, centers = i, nstart= 1)
  x = append(x, i)
  y = append(y, k2$tot.withinss)
  # silhouette(x = k2$cluster, dist = )
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

df$climate_type = k2$cluster
dt$climate_type = k2$cluster
library(jsonlite)
x <- toJSON(dt)
write(x,"ClasificacionFinal2011.json")