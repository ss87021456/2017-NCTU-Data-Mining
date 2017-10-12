import pandas as pd
import numpy as np
import pprint
from pandas.tseries.offsets import *
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style


style.use('ggplot')

df = pd.read_csv('./Data/Weather/Weather_hour.csv')
df_2 = pd.read_csv('./Data/Taipower/September.csv')

X = df.loc[df.Location == 'TAIPEI',['Timestamp','Temp']]
X = X.loc[X.Timestamp >= '2016-01-01 00:00:00', :]
X = X.loc[X.Timestamp <= '2017-12-31 23:59:59', :]
X['Datetime'] = pd.to_datetime(X['Timestamp'])
X = X.drop_duplicates(subset='Timestamp', keep='last').set_index('Datetime')
X = X.drop(['Timestamp'],axis=1)
print "X Unique:",X.index.is_unique	#check w/o duplicate index
#print X.head()
#print X.shape

Y = df_2.loc[df_2.Timestamp >= '2016-01-01 00:00:00', ['Timestamp','NorthSupply']]
Y = Y.loc[Y.Timestamp <= '2017-12-31 23:59:59', :]
Y['Datetime'] = pd.to_datetime(Y['Timestamp'])
Y = Y.drop_duplicates(subset='Timestamp', keep='last').set_index('Datetime')
Y = Y.drop(['Timestamp'],axis=1)
Y.index = Y.index - Minute(10)	# e.g. align 00:10:00 to 00:00:00

Y_2 = df_2.loc[df_2.Timestamp >= '2016-01-01 00:00:00', ['Timestamp','NorthUsage']]
Y_2 = Y_2.loc[Y_2.Timestamp <= '2017-12-31 23:59:59', :]
Y_2['Datetime'] = pd.to_datetime(Y_2['Timestamp'])
Y_2 = Y_2.drop_duplicates(subset='Timestamp', keep='last').set_index('Datetime')
Y_2 = Y_2.drop(['Timestamp'],axis=1)
Y_2.index = Y_2.index - Minute(10)
print "Y_2 Unique:",Y_2.index.is_unique #check w/o duplicate index
#print Y.head()
#print Y.shape


result = pd.concat([X, Y], axis=1)
result_2 = pd.concat([X, Y_2], axis=1)
temp = result
temp_2 = result_2
#print "original data size:",result.shape
result = result[~result.NorthSupply.isnull()]
result = result[~result.Temp.isnull()]
result_2 = result_2[~result_2.NorthUsage.isnull()]
result_2 = result_2[~result_2.Temp.isnull()]
#print "modified data size:",result.shape
print result.head()

x = np.array(result['Temp'])
y = np.array(result['NorthSupply'])
y_2 = np.array(result_2['NorthUsage'])
# training for a Linear Regression
clf = LinearRegression()
clf.fit(x.reshape(-1,1), y.reshape(-1,1))
#accuracy = clf.score(x_test.reshape(-1,1),y_test.reshape(-1,1))
#print "accuracy:",accuracy
clf_2 = LinearRegression()
clf_2.fit(x.reshape(-1,1), y_2.reshape(-1,1))


# missing data from 2017-01-25 02:10:00 to 2017-04-19 18:10:00
missing_df = temp['2017-01-25 02:00:00':'2017-04-19 18:10:00']
missing_attr = np.array(missing_df['Temp'])
missing_data = clf.predict(missing_attr.reshape(-1,1))
missing_df['NorthSupply_missing'] = missing_data
missing_df = missing_df.drop(['NorthSupply'],axis=1)
print missing_df.head()

missing_df_2 = temp_2['2017-01-25 02:00:00':'2017-04-19 18:10:00']
missing_attr_2 = np.array(missing_df_2['Temp'])
missing_data_2 = clf_2.predict(missing_attr_2.reshape(-1,1))
missing_df_2['NorthUsage_missing'] = missing_data_2
missing_df_2 = missing_df_2.drop(['NorthUsage'],axis=1)

#missing_data = result.loc[result.Timestamp >= '2017-01-25 02:00:00', ['Timestamp','NorthSupply']]
#missing_data = missing_data[missing_data.Timestamp <= '2017-04-19 18:10:00', :]
result = pd.concat([result, missing_df], axis=1)
result_2 = pd.concat([result_2, missing_df_2], axis=1)
print result.head(30)
print result.tail()
plt.figure()
plt.xlabel('Date')
plt.ylabel('Power')
result['NorthSupply'].plot()
missing_df['NorthSupply_missing'].plot()
plt.legend(loc=4)

plt.figure()
plt.xlabel('Date')
plt.ylabel('Power')
result_2['NorthUsage'].plot()
missing_df_2['NorthUsage_missing'].plot()
plt.legend(loc=4)
#missing_df['NorthSupply'].plot()

plt.show()

