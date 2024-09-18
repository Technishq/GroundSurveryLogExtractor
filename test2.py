
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
# Read the Excel file into a DataFrame
df = pd.read_excel('csv_finals/mpmb.xlsx')

# Print the first few lines of the cDataFrame
print(df.head())



# Sort the DataFrame by PRN column
df_sorted = df.sort_values(by="PRN")

# Print the sorted DataFrame
print(df_sorted)

df['Seconds of Week'] = df['Seconds of Week'].apply(lambda x: round(x, 1))


# Create a new column for dB values
df['Amplitude_dB'] = 20 * df['AMPLITUDE'].apply(lambda x: np.log10(x))

# Print the DataFrame with the new column
print(df)

#for prn in df['PRN'].unique():
 #   df_prn = df[df['PRN'] == prn]
  #  plt.plot(df_prn['Seconds of Week'], df_prn['Amplitude_dB'], label=prn)

#plt.xlabel('Seconds of Week')
#plt.ylabel('Amplitude (dB)')
#plt.title('Amplitude in dB vs. Seconds of Week for Each PRN')
plt.legend()
plt.show()

prn_list = df['PRN'].unique()

for prn in prn_list:
  df_prn = df[df['PRN'] == prn]
  plt.plot(df_prn['Seconds of Week'], df_prn['Amplitude_dB'])
  plt.xlabel('Seconds of Week')
  plt.ylabel('Amplitude (dB)')
  plt.title(f'Amplitude vs. Time for PRN {prn}')
  plt.show()
