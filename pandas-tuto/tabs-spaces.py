#!/usr/bin/env python2
# Prerequisites:
# - knowing Python basics,
# - using Python 2.7 (>=.14)
# - pandas (>= 0.22), numpy (>= 1.14), seaborn (>=0.8.1) installed, maybe using Anaconda distribution
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

pd.__version__
np.__version__
sns.__version__

# environment trick: depending on where you launched the console, you may need to change directory
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

df = pd.read_csv('tabs-spaces-resources/survey_results_public.csv')

# Learning how dataframes looks like
df

df['Salary']
df.Salary

# Leanrning how the information if the coder uses tabs or spaces is stored
df.TabsSpaces.unique()

df['Country'].unique();

df[['Respondent', 'Salary', 'Country', 'TabsSpaces']]

df[df.Salary > 20000].count()

df[df.Salary > 20000].Respondent.count()

max(df.Salary)

df.Salary.notna()

max(df[df.Salary.notna()].Salary)

df = df[df.Salary.notna()]
df = df[df.TabsSpaces.notna()]

df.pivot_table(index='TabsSpaces', values='Salary')

df.pivot_table(index='TabsSpaces', values='Respondent', aggfunc=pd.Series.count)
df.pivot_table(index='TabsSpaces', values='Respondent', aggfunc="count")

df.pivot_table(index='TabsSpaces', values='Salary').\
    merge(
        df.pivot_table(index='TabsSpaces', values='Respondent', aggfunc=pd.Series.count),
        left_index=True,
        right_index=True)

# Learning how number of years of coding as a job data is stored
df.YearsCodedJob.unique()

df.YearsProgram.apply(lambda s: (np.NaN if type(s) != str else 0 if s == "Less than a year" else int(s.split(" ")[0]))).unique()

df['YearsCodedJobI'] = df.YearsCodedJob.apply(lambda s: (0 if s == "Less than a year" else np.NaN if type(s) != str else int(s.split(" ")[0])))

df['YearsCodedJobG'] = df.YearsCodedJobI.apply(lambda i: (np.NaN if type(i) != float
                                                         else "a) 0-4" if i <5
                                                         else "b) 5-9" if i<10
                                                         else "c) 10-14" if i<15
                                                         else "d) 15-19" if i <20
                                                         else "e) >20"))

df['YearsCodedJobG']

df.pivot_table(index='YearsCodedJobI',  columns='TabsSpaces', values='Salary')[['Spaces', 'Tabs', 'Both']].plot(kind='line')
plt.show()

df.pivot_table(index='YearsCodedJobG',  columns='TabsSpaces', values='Salary')[['Spaces', 'Tabs', 'Both']].plot(kind='bar')
plt.show()

# -- learning distribution
sns.distplot(df.Salary)
plt.show()

sns.distplot(df.Salary, hist=False)
plt.show()

sns.distplot(df[df.TabsSpaces == 'Spaces'].Salary,  label='Spaces', hist=False)
plt.show()

for strategy in df.TabsSpaces.unique():
    sns.distplot(df[df.TabsSpaces == strategy].Salary, label=strategy, hist=False)
plt.show()

topCountries = df.pivot_table(index='Country', values='Respondent', aggfunc="count").sort_values('Respondent', ascending=False)\
    .head(10).index

len(df)
len(df[df.Country.isin(topCountries)])

for country in topCountries:
    sns.distplot(df[df.Country == country].Salary, label=country, hist=False)
plt.show()

for country in ['Poland', 'Germany', 'France']:
    sns.distplot(df[df.Country == country].Salary, label=country, hist=False)
plt.show()

# -- learning groupby()
df.groupby(['Country']).size()

df.groupby(['Country']).Salary.mean()['France']

salaryM = df.groupby(['Country']).Salary.mean()
df['SalaryM'] = df.Country.apply(lambda c: salaryM[c])
df[['SalaryM', 'Country']]

# -- learning a simpler way (from https://stackoverflow.com/questions/30757272/pivot-each-group-in-pandas)
df = df.set_index(['Country'])
df['SalaryM2'] = df.groupby(['Country']).Salary.mean()
df = df.reset_index()
(df['SalaryM2'] - df['SalaryM']).unique()

dfs = df[df.Salary >= df.SalaryM / 6]

df.pivot_table(index='TabsSpaces', values='Salary')
dfs.pivot_table(index='TabsSpaces', values='Salary')

df.pivot_table(index='TabsSpaces', values='Salary').merge(
    dfs.pivot_table(index='TabsSpaces', values='Salary'),
    left_index=True, right_index=True).plot(kind='bar')
plt.show()

for strategy in df.TabsSpaces.unique():
    sns.distplot(df[df.TabsSpaces == strategy].Salary, label="raw "+strategy, hist=False, kde_kws={'shade': True})
plt.show()

for strategy in dfs.TabsSpaces.unique():
    sns.distplot(dfs[dfs.TabsSpaces == strategy].Salary, label=strategy, hist=False, kde_kws={"lw": 3})
plt.show()

for country in topCountries:
    sns.distplot(dfs[dfs.Country == country].Salary, label=country, hist=False)
plt.show()

df.pivot_table(index='YearsCodedJobG',  columns='TabsSpaces', values='Salary')[['Spaces', 'Tabs', 'Both']].plot(kind='bar')
plt.show()

dfs.pivot_table(index='YearsCodedJobG',  columns='TabsSpaces', values='Salary')[['Spaces', 'Tabs', 'Both']].plot(kind='bar')
plt.show()

top_countries_dfs = df[df.Country.isin(topCountries)]

dfgg = top_countries_dfs.groupby(['Country', 'TabsSpaces'])
dfgg.Salary.mean().plot(kind='bar')
plt.show()

top_countries_dfs.pivot_table(index='Country', columns='TabsSpaces', values='Salary').plot(kind='bar')
plt.show()

top_countries_dfs.pivot_table(index='Country', columns='TabsSpaces', values='Respondent', aggfunc="count").plot(kind='bar')

for strategy in dfs.TabsSpaces.unique():
    sns.distplot(df[(df.TabsSpaces == strategy) & (df.Country == 'India')].Salary, label="India "+strategy, hist=False, kde_kws={'shade': True})
plt.show()

for strategy in dfs.TabsSpaces.unique():
    sns.distplot(df[(df.TabsSpaces == strategy) & (df.Country == 'United States')].Salary, label="US "+strategy, hist=False)
plt.show()

dfs.pivot_table(index='JobSatisfaction',  columns='TabsSpaces',values='Respondent', aggfunc="count")[['Spaces', 'Tabs', 'Both']].plot(kind='bar')
plt.show()

dfs.pivot_table(index='PronounceGIF',  columns='TabsSpaces', values='Respondent', aggfunc="count")[['Spaces', 'Tabs', 'Both']].plot(kind='bar')
plt.show()

dfs.pivot_table(index='VersionControl',  columns='TabsSpaces', values='Respondent', aggfunc="count")[['Spaces', 'Tabs', 'Both']].plot(kind='bar')
plt.show()

dfs.ProgramHobby.unique()
dfs['OpenSourceContributor'] = (dfs.ProgramHobby.apply(lambda s: s == "Yes, I contribute to open source projects" or s == "Yes, both"))
dfs.pivot_table(index='OpenSourceContributor', columns='TabsSpaces', values='Respondent', aggfunc="count")[['Spaces', 'Tabs', 'Both']].plot(kind='bar')
plt.show()

dfs.pivot_table(index='OpenSourceContributor', columns='TabsSpaces', values='Salary')[['Spaces', 'Tabs', 'Both']].plot(kind='bar')
plt.show()

dfs.pivot_table(index='YearsCodedJobG', columns=['TabsSpaces', 'OpenSourceContributor'], values='Salary')[['Spaces', 'Tabs', 'Both']].plot(kind='line')
plt.show()



