#install.packages("ggplot2", repos="http://cran.us.r-project.org")
#install.packages("tidyverse", repos="http://cran.us.r-project.org")
library(ggplot2)
library(tidyverse)


df = read_csv("ml_importances_with_categories.csv")
print(df)

df$feature = as.factor(df$feature)
df %>% group_by(feature, cateogry, time_period) %>% 
	summarise(mean_importance = mean(importancel), count = n()) %>% 
	group_by(cateogry, time_period) %>%
	summarise(sum_importance = sum(mean_importance)) %>%

ggplot(aes(x=time_period,y=sum_importance, fill=cateogry)) +
	geom_bar(position="fill", stat="identity", colour="black") +
	theme_bw() +
	scale_x_continuous(breaks = pretty(df$time_period, n = 6)) +
	theme(axis.text.x = element_text(size = 17), axis.text.y = element_text(size=17), axis.title.y = element_text(size=15), axis.title.x = element_text(size=15), plot.title = element_text(hjust = 0.5, size=15)) + 
	ylab("importance (proportion)") +
	ggtitle("ML Feature Importances for Predicting\nSpectral Power from Catchment Characteristics") +
	xlab("time period") #+

        #scale_color_gradient(high="red", space ="Lab" )

ggsave("humanPercent2_withoutDTR.png")


