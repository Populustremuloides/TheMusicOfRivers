library(tidyverse)
library(ggplot2)
library(scales)


df = read.csv("long_matrix_temp_order_seas_prec.csv")

print(df)


ggplot(df, aes(x=period, y=power)) + 
	geom_smooth() + 
	#coord_trans(x="log2")
	scale_x_log10(breaks = trans_breaks("log10", function(x) 10^x),
	              labels = trans_format("log10", math_format(10^.x))) +
	ggtitle("global distribution of frequency decompositions") + 
	theme_bw() +
	theme(plot.title = element_text(hjust = 0.5)) +
	ylab("mean spectral power") +
	xlab("period (days)")


ggsave("global_distribution_of_frequency_decompositions.png")



ggplot(df, aes(x=period, y=power, color=temp, linetype=precip)) + 
	geom_smooth() + 
	#coord_trans(x="log2")
	scale_x_log10(breaks = trans_breaks("log10", function(x) 10^x),
	              labels = trans_format("log10", math_format(10^.x))) +
	ggtitle("global frequency decompositions - by order") + 
	theme_bw() +
	theme(plot.title = element_text(hjust = 0.5)) +
	ylab("mean spectral power")
	xlab("period")


ggsave("global_freq_decomp_stream_order.png")




ggplot(df, aes(x=period, y=power, color=seasonality)) + 
	geom_smooth() + 
	#coord_trans(x="log2")
	scale_x_log10(breaks = trans_breaks("log10", function(x) 10^x),
	              labels = trans_format("log10", math_format(10^.x))) +
	ggtitle("global frequency decompositions - by precipitation seasonality") + 
	theme_bw() +
	theme(plot.title = element_text(hjust = 0.5)) +
	ylab("mean spectral power")
	xlab("period")


ggsave("global_freq_decomp_seasonality.png")



ggplot(df, aes(x=period, y=power, color=temp)) + 
	geom_smooth() + 
	#coord_trans(x="log2")
	scale_x_log10(breaks = trans_breaks("log10", function(x) 10^x),
	              labels = trans_format("log10", math_format(10^.x))) +
	ggtitle("global frequency decompositions - by temperature") + 
	theme_bw() +
	theme(plot.title = element_text(hjust = 0.5)) +
	ylab("mean spectral power")
	xlab("period")


ggsave("global_freq_decomp_temp.png")

ggplot(df, aes(x=period, y=power, color=precip)) + 
	geom_smooth() + 
	#coord_trans(x="log2")
	scale_x_log10(breaks = trans_breaks("log10", function(x) 10^x),
	              labels = trans_format("log10", math_format(10^.x))) +
	ggtitle("global frequency decompositions - by precipitation") + 
	theme_bw() +
	theme(plot.title = element_text(hjust = 0.5)) +
	ylab("mean spectral power")
	xlab("period")


ggsave("global_freq_decomp_precip.png")




ggplot(df, aes(x=period, y=power, color=temp, linetype=precip)) + 
	geom_smooth() + 
	#coord_trans(x="log2")
	scale_x_log10(breaks = trans_breaks("log10", function(x) 10^x),
	              labels = trans_format("log10", math_format(10^.x))) +
	ggtitle("global frequency decompositions - by precipitation and temperature") + 
	theme_bw() +
	theme(plot.title = element_text(hjust = 0.5)) +
	ylab("mean spectral power")
	xlab("period")


ggsave("global_freq_decomp_temp_and_precip.png")



ggplot(df, aes(x=period, y=power, color=temp, linetype=order)) + 
	geom_smooth() + 
	#coord_trans(x="log2")
	scale_x_log10(breaks = trans_breaks("log10", function(x) 10^x),
	              labels = trans_format("log10", math_format(10^.x))) +
	ggtitle("global frequency decompositions - by stream order and temperature") + 
	theme_bw() +
	theme(plot.title = element_text(hjust = 0.5)) +
	ylab("mean spectral power")
	xlab("period")


ggsave("global_freq_decomp_temp_and_size.png")



ggplot(df, aes(x=period, y=power, color=temp, linetype=seasonality)) + 
	geom_smooth() + 
	#coord_trans(x="log2")
	scale_x_log10(breaks = trans_breaks("log10", function(x) 10^x),
	              labels = trans_format("log10", math_format(10^.x))) +
	ggtitle("global frequency decompositions - by precipitation seasonality and temperature") + 
	theme_bw() +
	theme(plot.title = element_text(hjust = 0.5)) +
	ylab("mean spectral power")
	xlab("period")


ggsave("global_freq_decomp_temp_and_seasonality.png")
