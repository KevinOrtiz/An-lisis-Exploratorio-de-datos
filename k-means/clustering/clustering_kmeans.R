require(ggplot2)
require(ggmap)
require(rworldmap)

NUM_CLUSTERS = 20

geo_data <- data.frame(x=coordenadas_lugares_com$Lon, y=coordenadas_lugares_com$Lat)
geo_data_no_na <- na.omit(geo_data)
valid_rows <- strtoi(rownames(geo_data_no_na))

model <- kmeans(geo_data_no_na, NUM_CLUSTERS)

data_with_clusters <- data.frame(geo_data_no_na, cluster = factor(model$cluster))
centers <- as.data.frame(model$centers)
smaller_sample <- data_with_clusters[sample(nrow(data_with_clusters), 700, replace=F),]

map = get_map(location = c(lon = -78.4558138,lat =  -0.2324668), zoom = 11, maptype = 'satellite')

ggmap(map) + geom_point(data=smaller_sample, aes(x=x, y=y, color=cluster )) + geom_point()

require(sqldf)

info = sqldf("SELECT DISTINCT * FROM smaller_sample, coordenadas_lugares_com WHERE smaller_sample.x = coordenadas_lugares_com.Lon AND smaller_sample.y = coordenadas_lugares_com.Lat")

result = sqldf("SELECT cluster, SUM(NoComments) FROM info GROUP BY cluster ORDER BY SUM(NoComments) DESC")

write.csv(file = "info_com.csv", x = info)
write.csv(file = "clusters_com.csv", x = result)
write.csv(file = "centers_com.csv", x = centers)
