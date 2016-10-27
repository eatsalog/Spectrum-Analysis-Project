# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
cd '.\Documents\College Major Shit\CS456_Wireless-Networks\Homework\Final Project'
import h5py
import math
import pylab
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime as dt

h5 = h5py.File('soxx.dr.z.h5')
#print(h5)
g = h5['sessions/1/spectrum/0']
x = g['powers']
timeTable = g['start_times']
#print(x.shape)

date_format = mdates.DateFormatter('%H:%M')#:%S
dateRange   = ['08/14/2015', '08/15/2015', '08/16/2015', '08/14/2015', '08/15/2015', '08/16/2015']
timeRange1  = ['08142015-0800_1200', '08152015-0800_1200', '08162015-0800_1200']
timeRange2  = ['08142015-1310_1710', '08152015-1610_2010', '08162015-1110_1510']
timeRanges  = timeRange1 + timeRange2
datesNoGame = [[124047, 131206], [167617, 173450], [208893, 216052]]
datesGame   = [[133176, 139977], [180790, 187940], [214602, 221423]]
dates       = datesNoGame + datesGame
frequencies = [[11776, 14848], [11776, 12876], [13076, 13776], [13976, 14848]]
freqRanges  = [[0,3071], [0,1100], [1300,2000], [2200,3071]]
freqMHz     = [[1930, 1990], [1930, 1951.5], [1955.4, 1969.1], [1973, 1990]]
timeStamps1 = [[1439557200, 1439571600], [1439643600, 1439658000], [1439730000, 1439744400]]
timeStamps2 = [[1439575800, 1439590200], [1439673000, 1439687400], [1439741400, 1439755800]]
timeStamps  = timeStamps1 + timeStamps2
freqStart = frequencies[0][0]
freqEnd   = frequencies[0][1]
data = x[:, freqStart:freqEnd]

#--------------------------------------------#
#  1930-1990 MHz                             #
# (1930000000 - 1700000000)/19531.25 = 11776 #
# (1990000000 - 1700000000)/19531.25 = 14848 #
#--------------------------------------------#
# 1930 MHz
# 1930 MHz
# ((11776 + 1300) * 19531.25) + 1700000000 = 1955390625 Hz = 1955.4 MHz
# ((11776 + 2200) * 19531.25) + 1700000000 = 1972968750 Hz = 1973.0 MHz
# 1990 MHz
# ((11776 + 1100) * 19531.25) + 1700000000 = 1951484375 Hz = 1951.5 MHz
# ((11776 + 2000) * 19531.25) + 1700000000 = 1969062500 Hz = 1969.1 MHz
# 1990 MHz

#times = dates[3]
for iterator, times in enumerate(dates, start=0):
#for times in dates:
    timeStart = times[0]
    timeEnd   = times[1]
    rangeNb   = 0
    tStamp    = timeStamps[iterator]
    dateTitle = dateRange[iterator]

    #freq = frequencies[0]
    for freq in frequencies:
        freqStart = freq[0]
        freqEnd = freq[1]
        i = 0
        numsum = []
        numsumx = []
        
        for index in range(timeStart, timeEnd):
            l = x[index, freqStart:freqEnd]
            a = 10 ** (l/10 - 3)
            val = sum(a)
            val = 10 * math.log10(val) + 30
            numsum.insert(i, val)
            numsumx.insert(i, mdates.date2num(dt.datetime.fromtimestamp(timeTable[index])))
            i = i+1
        #end for
        
        time1 = mdates.date2num(dt.datetime.fromtimestamp(tStamp[1]))
        time2 = mdates.date2num(dt.datetime.fromtimestamp(tStamp[0]))
        xLabels = freqMHz[rangeNb]
        
        plt.close('all')
        #Heat Map
        y = data[::250,freqRanges[rangeNb][0]:freqRanges[rangeNb][1]]
        fig = plt.figure()
        #plt.figure(1)
        ax1 = fig.add_subplot(211)#plt.subplot(211)
        ax1.set_title(dateTitle)
        ax1.set_xlabel('Frequency (MHz)')
        ax1.set_ylabel('Time (UTC-6:00)')
        ax1.yaxis.set_major_formatter(date_format)
        ax1.imshow(y, aspect='auto', extent=[xLabels[0], xLabels[1], time1, time2])
        
        #Heat Map - Interpolation Applied
        ax2 = fig.add_subplot(212)
        ax2.set_title(dateTitle)
        ax2.set_xlabel('Frequency (MHz)')
        ax2.set_ylabel('Time (UTC-6:00)')
        ax2.yaxis.set_major_formatter(date_format)
        ax2.imshow(y, aspect='auto', extent=[xLabels[0], xLabels[1], time1, time2], interpolation = 'nearest')
        #plt.show()
        fig.tight_layout()
        plt.savefig('./Images-PCS/HM-'+timeRanges[iterator]+'-'+str(xLabels[0])+'_'+str(xLabels[1])+'.png', format="png")
        
        plt.close('all')
        #Time Series
        fig = plt.figure(1)
        c = np.linspace(numsumx[0],numsumx[len(numsumx)-1], len(numsumx))
        ax1 = fig.add_subplot(211)
        ax1.set_title(dateTitle)
        ax1.set_xlabel('Time (UTC-6:00)')
        ax1.set_ylabel('Power (dBm)')
        ax1.xaxis.set_major_formatter(date_format)
        ax1.plot(c, numsum)
        
        #Time Series - Moving Average Applied
        factor = 150
        ma = np.ones(factor)/factor
        filtered = np.correlate(numsum, ma)
        b = np.linspace(numsumx[0],numsumx[len(numsumx)-1], len(filtered))
        ax2 = fig.add_subplot(212)
        ax2.set_title(dateTitle)
        ax2.set_xlabel('Time (UTC-6:00)')
        ax2.set_ylabel('Power (dBm)')
        ax2.xaxis.set_major_formatter(date_format)
        ax2.plot(b, filtered)
        #plt.show()
        fig.tight_layout()
        plt.savefig('./Images-PCS/TS-'+timeRanges[iterator]+'-'+str(xLabels[0])+'_'+str(xLabels[1])+'.png', format="png")
        
        rangeNb = rangeNb + 1
    #end for
#end for