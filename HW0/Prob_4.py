import MySQLdb, pprint, time
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import lfilter

# Connect
db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="*******",
                     db="taipower")

cursor = db.cursor()

date_sql = "SELECT timestamp FROM Power"
Q_sql = "SELECT northSupply FROM Power"
C_sql = "SELECT northUsage FROM Power"

cursor.execute(date_sql)
date = [element[0] for element in cursor.fetchall()]
cursor.execute(Q_sql)
Q_data = [element[0] for element in cursor.fetchall()]
cursor.execute(C_sql)
C_data = [element[0] for element in cursor.fetchall()]

Q_data = np.asarray(Q_data)
C_data = np.asarray(C_data)

Q_data_offset = Q_data - np.mean(Q_data)
C_data_offset = C_data - np.mean(C_data)

Q_data_Amplitude = Q_data_offset/np.std(Q_data)
C_data_Amplitude = C_data_offset/np.std(C_data)

Q_data_linear = signal.detrend(Q_data)
C_data_linear = signal.detrend(C_data)

Q_data_denoise = lfilter([1.0 / 240] * 240, 1, Q_data)
C_data_denoise = lfilter([1.0 / 240] * 240, 1, C_data)


original_D = np.sqrt(np.sum((Q_data-C_data)**2))
print "Original D(Q,C):", original_D
OT_D = np.sqrt(np.sum((Q_data_offset-C_data_offset)**2))
print "Offset Translation D(Q,C):", OT_D
AS_D = np.sqrt(np.sum((Q_data_Amplitude-C_data_Amplitude)**2))
print "Amplitude Scaling D(Q,C):", AS_D
LTR_D = np.sqrt(np.sum((Q_data_linear-C_data_linear)**2))
print "Linear Trend Removal D(Q,C):", LTR_D
DN_D = np.sqrt(np.sum((Q_data_denoise-C_data_denoise)**2))
print "Noise Reduction D(Q,C):", DN_D

plt.figure("Original")
plt.xlabel('Date')
plt.ylabel('Power')
plt.plot(date,Q_data, color = 'red', linewidth = 1.0, label='northSupply_ori')
plt.plot(date,C_data, color = 'blue', linewidth = 1.0, label='northUsage_ori')
plt.legend()

plt.figure("Offset Translation")
plt.xlabel('Date')
plt.ylabel('Power')
plt.plot(date,Q_data_offset, color = 'red', linewidth = 1.0, label='northSupply_off')
plt.plot(date,C_data_offset, color = 'blue', linewidth = 1.0, label='northUsage_off')
plt.legend()

plt.figure("Amplitude Scaling")
plt.xlabel('Date')
plt.ylabel('Power')
plt.plot(date,Q_data_Amplitude, color = 'red', linewidth = 1.0, label='northSupply_amp')
plt.plot(date,C_data_Amplitude, color = 'blue', linewidth = 1.0, label='northUsage_amp')
plt.legend()

plt.figure("Linear Trend Removal")
plt.xlabel('Date')
plt.ylabel('Power')
plt.plot(date,Q_data_linear, color = 'red', linewidth = 1.0, label='northSupply_lin')
plt.plot(date,C_data_linear, color = 'blue', linewidth = 1.0, label='northUsage_lin')
plt.legend()

plt.figure("Noise Reduction")
plt.xlabel('Date')
plt.ylabel('Power')
plt.plot(date,Q_data_denoise, color = 'red', linewidth = 1.0, label='northSupply_dn')
plt.plot(date,C_data_denoise, color = 'blue', linewidth = 1.0, label='northUsage_dn')
plt.legend()

plt.show()