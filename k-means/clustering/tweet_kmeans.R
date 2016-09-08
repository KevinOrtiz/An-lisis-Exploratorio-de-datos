require(ggplot2)
require(ggmap)
require(rworldmap)

NUM_CLUSTERS = 20


geo_data <- data.frame(x=tweets_depurated_noText$id_str, y=tweets_depurated_noText$longitude)
geo_data_no_na <- na.omit(geo_data)
valid_rows <- strtoi(rownames(geo_data_no_na))

model <- kmeans(geo_data_no_na, NUM_CLUSTERS)

data_with_clusters <- data.frame(geo_data_no_na, cluster = factor(model$cluster))
centers <- as.data.frame(model$centers)
smaller_sample <- data_with_clusters[sample(nrow(data_with_clusters), 1000, replace=F),]

map = get_map(location = c(lon = -78.4558138,lat =  -0.2324668), zoom = 11, maptype = 'satellite')

ggmap(map) + geom_point(data=smaller_sample, aes(x=x, y=y, color=cluster )) + geom_point()

require(sqldf)

info = sqldf("SELECT DISTINCT * FROM smaller_sample, tweets_depurated_noText WHERE smaller_sample.x = tweets_depurated_noText.id_str AND smaller_sample.y = tweets_depurated_noText.longitude")

result = sqldf("SELECT cluster, COUNT(cluster) FROM info GROUP BY cluster ORDER BY COUNT(cluster) DESC")

write.csv(file = "info_tweet.csv", x = info)
write.csv(file = "clusters_tweet.csv", x = result)
write.csv(file = "centers_tweet.csv", x = centers)