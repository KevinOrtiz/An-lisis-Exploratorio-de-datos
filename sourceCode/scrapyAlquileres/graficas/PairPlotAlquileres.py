
import pandas as pd
import matplotlib.pyplot as plt 

df = pd.read_csv('Alquiler_col_influyente copy.csv')
axes = pd.tools.plotting.scatter_matrix(df, alpha=0.5)
plt.tight_layout()
plt.savefig('scatter_matrixAlquileresTop.png')