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
	ylab("importance (proportion)") +
	ggtitle("ML model importances by category and frequency") +
	xlab("time period") #+
        #scale_color_gradient(high="red", space ="Lab" )

ggsave("humanPercent2_withoutDTR.png")


