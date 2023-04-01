import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("correlations_between_fourier_and_cat_chars_mini.csv")

#scales = list(df[df.columns[0]])
#scales.reverse()
#df[df.columns[0]] = scales

print(df)

for col in df.columns:
    plt.plot(df[df.columns[0]], df[col])
    plt.title(col)
    plt.xscale("log")
    plt.show()
