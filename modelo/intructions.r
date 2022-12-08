##https://uc-r.github.io/kmeans_clustering
install.packages("rjson")
install.packages("tidyverse")
install.packages("cluster")
install.packages("factoextra")
install.packages("jsonlite")
library(jsonlite)
library("tidyverse")  # data manipulation
library("cluster")    # clustering algorithms
library("factoextra") # clustering algorithms & visualization
library(tidyverse)

dt <- fromJSON("dataset/temperaturaProcesado.json")
df=dt %>% select(4:7)
##data_new2$x1 <- as.numeric(as.factor(data_new2$x1))##
df$temMin = as.numeric(as.factor(df$temMin))
df$temMax = as.numeric(as.factor(df$temMax))
df$temMedBaja = as.numeric(as.factor(df$temMedBaja))
df$temMedAlta = as.numeric(as.factor(df$temMedAlta))

#Kendall correlation distance
df <- na.omit(df)
df <- scale(df) #Error in colMeans(x, na.rm = TRUE) : 'x' must be numeric
distance <- get_dist(df)
fviz_dist(distance, gradient = list(low = "#00AFBB", mid = "white", high = "#FC4E07"))


# k-means clustering
# clean the data with no String varibles
#spain have 6 diferents 
k2 <- kmeans(df, centers = 6, nstart = 25)
fviz_cluster(k2, df)