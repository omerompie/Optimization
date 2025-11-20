"""

V 2.0 (2025)

Student's version

@author: Alejandro Murrieta-Mendoza

INSTRUCTIONS: 
    1.- Create your own empty script where you copy and past each question or 
    comment the questions below. Otherwise you will have errors 
    and you will not be able to run the script

    2.- Follow the questions in this document. The parts where you 
    encounter __________ expect you to fill some code on it. 
    
    
    HAVE FUN 
"""


# Run the lines beggining with "conda" the FIRST TIME you run this script 
# as this will install  different libraries that you might not have available. 
# Comment these lines after that. 

# Install Pacakges
# Mac users should run this on the python terminal.
# Windows users should run this on the conda cmd: Type anaconda in the search 
# bar and run the anaconda prompt (anaconda3) as an adminstrator.
# Comment lines Below
# conda install -c anaconda pandas
# conda insatll -c anaconda numpy 
# conda install -c conda-forge matplotlib
# conda install -c anaconda seaborn
# Comment Lines Above 



# 1.- import pandas as pd, numpy as no, matplotlib.pyplot as plt and os
# Pandas is useful for data frames, numpy has interesting mathematical libraries,
# matplotlib.pyplot has tools to plot, seaborn is useful for statistial tools, 
# os will allos you to switch directories (you need to look this up if needed). 


import pandas as pd # Pandas!
import numpy as np # linear algebra
import matplotlib.pyplot as plt #plots!
import os # To move within directories
import seaborn as sns #Fun library to plot
import scipy.stats as stats
from scipy.stats import ttest_ind
from scipy.stats import t   # This is the T-Table Value


# 2.- Save this file under on the directory of your choice
#       NO CODE NEEDED

# 3.- Place the file 'weight-height.csv' available in BS in the same directory 
#     as where you placed this file. 
#       NO CODE NEEDED


# 4.- Use Pandas to load this CSV file as a dataframe called "df".
#     Fill the name under ______.
df = pd.read_csv('weight-height.csv')


# 5.- Examine the data using the object .head(). In other words df.head()
# df.head()

# Run the Script!

# Did see anything in the terminal? If not, go to the terminal and type
# df.head(). To be able to see this output using the script, you need to use 
# the print() function. Uncommnet the line below

print(df.head())  # <--- Uncomment the print statement!

# # Run the script again!

# # 6.- Look for Null (empty) values using df.insnull().sum()
# print(df.isnull().sum())

# #Do you see anything on the terminal? How can you fix this?
# print("")
# print("Checking null values")
# ____________

# # This dataset is clean as i am a nice guy. However it is always a good idea to 
# # check for Null values using df.isnull().sum() or a similar function

# print(df.isnull().sum())

# # 7.- Observe the code below. This code plots an histogram
# #     Plots are displayed on your top right under "plots"
 
# df.Height.plot(kind="hist", title='Height Histogram', color='blue');
# # Where is "Height" in df.Height.plot is coming from? (Hint: Look at df.head())
# plt.hist(x = df.Height, color='blue') # Do you understrand x = df.Height?
# plt.title("Height Histogram (meters)")
# plt.xlabel("Height")
# plt.ylabel("Frequency")
# plt.plot()
# plt.show()


# # 8.- Plot an histogram for Weight now. The color should be black
# plt.figure()
# df.Weight.plot(kind="hist", title='Weight Histogram', color='black');
# plt.hist(x = df.Weight, color='black') # Do you understrand x = df.Height?
# plt.title("Weight Histogram (kg)")
# plt.xlabel("Weight")
# plt.ylabel("Frequency")
# plt.plot()
# plt.show()


# # 9.- Plot an histogram with 2 bins
# plt.figure()    # Have you figured out what this line is for?
# plt.hist(x = df.Height, color='blue', bins = 50)
# plt.title("Height Histogram (inches)")
# plt.xlabel("Height")
# plt.ylabel("Frequency")
# plt.plot();
# plt.show()

# # How useful is this number of bins for your plot?
# # What would you expect if you change it?

# # 10.- Do a for loop to crate different plots containing bins from  10 to 60
# #      in steps of 5. Be aware, this will create many plots
# print("")
# num_bins = [5,10,15,20,25,30,35,40,45,50,55,60]
#
# for i in range(len(num_bins)):
#     plt.figure()
#     plt.hist(x = df.Height, color='blue', bins = num_bins[i])
#     plt.title("Height Histogram (inches) - " + str(num_bins[i]) + " bins")
#     plt.xlabel("Height")
#     plt.ylabel("Frequency")
#     plt.plot();
#     plt.show()


    
# # 11,- Create a Plot showing the population density. 
# #   Hint: This plot kind is called "kde"
# plt.figure()
# df.Height.plot(kind="kde", title='Univariate: Height KDE', color='b');
# plt.xlabel("Height (inches)")
# plt.ylabel("Frequency")
# plt.show()
# # Does it look like a bell?

# # 12.- Plot the weight distribution for men and women in the same plot. 
# # 12a.- Create a new Data Frame for Data with MEN only and explore it.
df_men = df.loc[df["Gender"] == 'Male']
print(df_men)

# # 12b.- Create a new Data Frame for Data with WOMEN only.

df_women = df.loc[df["Gender"] == 'Female']
print(df_women)



# # 12c.- Plot both histograms next to each other. Women in Yellow and Men in Red
# # Hint: Some ____ are to be repalced for the dataframes created before. 

# plt.hist(_______['Height'], bins = ___, alpha=0.4, color = '_______', label='Men')
# plt.hist(_____['Height'], bins = ___, alpha=0.4, color = '_____', label='Women')
# plt.show()

# # What does alpha mean? Play with it... (it values go from 0 to 1)


# # 13.- Compute the mean value for male and women for height and weight. 
# #     Print these values on the terminal

# mean_men = np.mean(df['Height'])  # Example
# print("Mean Weight")
# print (mean_men)

# # 14.- Compute the standar deviation for male and women for height and weight. 
# #      Print these values on the terminal
# std_men = np.std(df_men['Height'])  # Example


# 15.- Can you reproduce the same plot on 12c for Weight?




# # 16.- Look at the code below. 

# import scipy.stats as stats
# import math

# #bins = np.linspace(54, 79, 60)
# bins = 70
# plt.hist(YOUR MEN DATAFRAME['Height'], bins, alpha=0.5, label='males', density=True)
# plt.hist(YOUR SOMEN DATAFRAME['Height'], bins, alpha=0.5, label='females', density=True)
# x = np.linspace(54, 79, 100)  # Range of data, creat 100 values for x
# plt.plot(x, stats.norm.pdf(x, mean_men, std_men))
# plt.plot(x, stats.norm.pdf(x, mean_women, std_women))
# plt.xlabel("Height (inches)")
# plt.show()

# # 17.- Reproduce this code for Weight.







# 18.- Central Theorem Value.
#      Take different samples of n values and compute the mean and 
#      the standard deviation for the whole population

# sample_1 = df['Weight'].sample(n = 15, replace=True)
# print(sample_1.mean())

# # How different are the values?




# 19.- import pandas as pd, numpy as np, matplotlib.pyplot as plt and os
# Pandas is useful for data frames, numpy has interesting mathematical libraries,
# matplotlib.pyplot has tools to plot, seaborn is useful for statistical tools, 
# os will allow you to switch directories (you need to look this up if needed). 


# # 20.- Load this Data Base and separate it in Men and Women
# df = pd.read_csv('_________.csv')
# df_men = df.loc[df['_____'] == '_____']
# df_women = df.loc[df['______'] == '_____']
# print("Data Frame Men")
# print(df_men)
# print ("Data Frame Women")
# print(df_women)
#
# # 21.- Take a 30 elements samples from each population
# sample_m = ______.sample(n = __, replace=True)
# sample_w = ______.sample(n = __, replace=True)
#
# # 22.- Compute the average for both samples
# print("Mean Men: ")
# mean_men = np.mean(____[___])
# print(mean_men)
# print("Mean Women: ")
# mean_women = np.mean(____[___])
# print(mean_women)
#
# # 23.- Compute the standard deviation for both samples
# std_men = np.std(____[___])
# print("SD Men")
# print(std_men)
# std_women = np.std(____[___])
# print("SD Women")
# print(std_women)
#
# # 24.- Plot both histograms next to each other. Women in Yellow and Men in Red
# bins = 100
# plt.hist(____[___], bins, alpha=0.5, label='males', color = 'red', density=True)
# plt.hist(____[___], bins, alpha=0.5, label='females', color = 'yellow', density=True)
# x = np.linspace(54, 79, 100)  # Range of data, create 100 values for x
# plt.plot(x, stats.norm.pdf(x, mean_men, std_men))
# plt.plot(x, stats.norm.pdf(x, mean_women, std_women))
#
#
# plt.xlabel("Height (inches)")
# plt.show()   # <----- Remove/comment this line for exercise 9
#
# # 25.- Plot the average lines (for men and women samples) using the function
# #      plt.axvline() [Google it!]. Remove the plt.show() above and add it at the
# #      end of this part
# # LINE MEAN FOR MEN HERE
# # LINE MEAN FOR WOMEN HERE
# plt.show()
#
#
# # 26.- Compute your t_value
# #     hints:
# #           absolute value = abs()
# #           vector length = len()
# #           square root = np.sqrt()
# #           cube of 2 = 2**3
#
#
# print("T-Value")
# print(t_value)
#
# # 27.- Compute your degrees of freedom
# df = __ + __ - 2 # -2 as we have two set of samples .
# print("Degrees of Freedom: ")
# print(df)
#
# # 28.- Compute the T-Test
# statistic = stats.ttest_rel(a= YOUR SAMPLE A['Height'], b= YOUR OTHER SAMPLE['Height'])  # Put your samples here
# alpha = 0.05 # We want the 95% confidence interval.
# alpha = alpha/2 # Two Tails so we have to divide alpha/2
# # This is the table:
# cv = t.ppf(1.0 - alpha, df)  # This function gives you the CRITICAL VALUE
#
#
# print("*************************")
# print("*       RESULTS         *")
# print("*************************")
# if t_value <= cv:
#     print("ACCEPT Null Hypothesis: No Statistical Difference between the samples")
#     print("CV value is is equal to: " + str(cv))
#     print("T-Value is equal to: " + str(t_value))
# else:
#     print("REJECT Null Hypothesis; There is a statistical difference between the samples")
#     print("CV value is is equal to: " + str(cv))
#     print("T-Value is equal to: " + str(t_value))
#
#
# # 29.- Run the code many times. Is the Hypothesis ever rejected?
#         # Play with Question 5 and reduce the samples... What happens?
#
#
# # 30.- Plot, as in Workshop 2, the distribution for both populations
#     # Is the Null hypothesis rejection correct? Are men normally taller than women?
#
# # 31.- Perform the T-Test for a two tailed 97% confidence.
#
# # 32.- You know that men tend to be taller than women. You are confident
# #      due to experience that this is true. This means that you know the
# #      direction of change.
# #      Make a one tailed test with 95% confidence interval
#
#
#
# # """
# # NOTES:
# # 1.- There are no notes today. Well, this song played waaaaaay too many times
# #     while developing this workshop
# #     https://www.youtube.com/watch?v=ZSSfcjAfC9w&list=PL0586609652B2033E
# #     They released a new album last year after waiting 7 years!. Check it out!
#
# #     1.- List of colors
# #         https://matplotlib.org/3.1.0/gallery/color/named_colors.html
# #         I found this by typing "Plot python colors" on google.
# #     2.- Plot Options: Google ".dataframe.plot:
# #     2.- If you have any comments how to improve this workshop please let me know
# # """