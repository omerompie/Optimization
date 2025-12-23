import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Fixed seed that produces the contrast
rng = np.random.default_rng(1)

# T-TEST and WELSH'S T-TEST

# 1.- Simulate two groups
# Read documentation
# https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.normal.html

# Group A: large sample, tight variance
group_A = rng.normal(loc=50, scale=5, size=400)

# Group B: small sample, huge variance, slightly higher mean
group_B = rng.normal(loc=52, scale=40, size=15)

# A.- What are the mean and SD for these two? What is this function doing?


# 2.- Plot both groups to observe their distribution.

# 3.- Perform the typical T-Test. Use stats.ttest_ind.
# Read Documentation: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html
# Remember the variance condition for T-Test


# 4.- Using tats.ttest_ind, perform the Welch's t-test.
# Hint: Variance.


# 5.- Define your confidence to be 95%

# 6. Given the hypothesis:
# Null hypothesis H0: The two group means are equal
# Alternative hypothesis H1: The two group means are different
# Provide your conclusions from the hypothesis testing.
print("Student's t-test (equal variances):")

print("  Decision:", decision)

if p_value_student < alpha:
    decision = "Reject H₀ at 95% confidence (means differ)"
else:
    decision = "Fail to reject H₀ at 95% confidence (no evidence of difference)"

# 7.- Plot The distributions. Plot their averages, and make a box plot.

# B.- Why are the conclusions different?
# C.- Which one is the correct test to use?


# LEVENS TEST

# 8.- Let's Test if the varances are the same... we know the result. So, Read the
# documentation.

# https://docs.scipy.org/doc//scipy-1.16.2/reference/generated/scipy.stats.levene.html
# Assume center = "mean"

# 9.- Conclude based on:
# H0: The population variances of Group A and Group B are equal.
# Ha: The population variances of Group A and Group B are not equal


# Wilcox Test

np.random.seed(2025)

# Simulated paired flight delays (same flights measured before and after)
# Before procedure: longer delays
delays_before = np.random.exponential(scale=30, size=100)

# After procedure: shorter delays for the same flights
delays_after = delays_before - np.random.normal(loc=5, scale=3, size=100)

# D.- By inference, What is the distribution?


# 9.- Make a Wilcoxon Signed-Rank Test (paired samples, assume alternative to be 'two sided')
# read documentation :
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html

# 10.-  Based on the results, conclude given the following hypotheses with 95% of confidence rate:
# H0: The median difference between paired delays (before – after) is zero. Procedure had no effect.
# Ha: The median difference is not zero. Procedure changed delays.


# 11.- PLOT the abolute differences.

# 12.- PLOT both distributons ("raw data")

# 13.- PLOT Box plots to visaulize the data
#


#



