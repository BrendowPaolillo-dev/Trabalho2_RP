"""Example program to show how to read a multi-channel time series from LSL."""

from pylsl import StreamInlet, resolve_stream
import mne
import numpy as np
from time import sleep

#######Seleciona qual bandpower teve o valor mais alto
def selectBand(bandPower):
    return (bandPower.index(max(bandPower)))

#######cálculo de média
def median (buffer):
    total = 0
    data = buffer.get_data()
    for i in range(len(data)):
        for j in range(len(data)):
            total += data[i][j]
    total = total / j
    return (total)

def FindBandPower(buffer, info):
    # epoch = mne.EpochsArray(buffer, info)
    # buffer.filter(l_freq = 8, h_freq = 13)
    # buffer.plot_psd(fmin=0., fmax=60.)


    #######Filtragem das faixas
    deltaBuffer = buffer.filter(l_freq = 0.5, h_freq = 4., verbose = 'ERROR')
    # deltaBuffer = deltaBuffer.filter(l_freq = 0.5, h_freq = 4., verbose = 'ERROR')
    # deltaBuffer = deltaBuffer.filter(l_freq = 0.5, h_freq = 4., verbose = 'ERROR')

    thetaBuffer = buffer.filter(l_freq = 4., h_freq = 8., verbose = 'ERROR')
    # thetaBuffer = thetaBuffer.filter(l_freq = 4., h_freq = 8., verbose = 'ERROR')
    # thetaBuffer = thetaBuffer.filter(l_freq = 4., h_freq = 8., verbose = 'ERROR')

    alphaBuffer = buffer.filter(l_freq = 8., h_freq = 13., verbose = 'ERROR')
    # alphaBuffer = alphaBuffer.filter(l_freq = 8., h_freq = 13., verbose = 'ERROR')
    # alphaBuffer = alphaBuffer.filter(l_freq = 8., h_freq = 13., verbose = 'ERROR')

    betaBuffer = buffer.filter(l_freq = 13., h_freq = 32., verbose = 'ERROR')
    #betaBuffer = betaBuffer.filter(l_freq = 13., h_freq = 32., verbose = 'ERROR')
    # betaBuffer = betaBuffer.filter(l_freq = 13., h_freq = 32., verbose = 'ERROR')

    gammaBuffer = buffer.filter(l_freq = 32., h_freq = 100., verbose = 'ERROR')
    # gammaBuffer = gammaBuffer.filter(l_freq = 32., h_freq = 100., verbose = 'ERROR')
    # gammaBuffer = gammaBuffer.filter(l_freq = 32., h_freq = 100., verbose = 'ERROR')
    
    #print (alphaBuffer.get_data())
    
    #######tentei transformar no dominio do tempo(?) 
    # teste = mne.time_frequency.stft(buffer, 4)
    # print(teste)

    #######chamada da função de cálculo de média para cada buffer filtrado
    deltaMedian = median(deltaBuffer)
    thethaMedian = median(thetaBuffer)
    alphaMedian = median(alphaBuffer)
    betaMedian = median(betaBuffer)
    gammaMedian = median(gammaBuffer)


    ####### lista com a média de todas as bandpower
    bandPower = []
    bandPower.append([deltaMedian, thethaMedian, alphaMedian, betaMedian, gammaMedian])

    returnedIndex = selectBand(bandPower)
    print (returnedIndex)
    if returnedIndex == 0:
        print ("Delta")
    elif returnedIndex == 1:
        print("Theta")
    elif returnedIndex == 2:
        print("Alpha")
    elif returnedIndex == 3:
        print("Beta")
    elif returnedIndex == 4:
        print("Gamma")

        
    # alphaBuffer.plot_psd(fmin=0., fmax=60.)

def func2():
    pass
def func3():
    pass
def func4():
    pass

def main():
    buffer = []

    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')
    info = mne.create_info(8, 1024, "eeg")
    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])
    i = 0
    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample = inlet.pull_sample()
        if len(buffer) < 1024:
            buffer.append(sample[0])
        elif len(buffer) >= 1024:
            # print("---------------------------antes: " , len(buffer))
            npBuffer = np.array(buffer, dtype=np.float64)
            # print(npBuffer.T.shape)
            teste = mne.io.RawArray(npBuffer.T, info)
            FindBandPower(teste, info)
            buffer = buffer[256:1024]
            # print("---------------------------depois: " , len(buffer))
            # print (buffer)

    # print(sampleList)
    # print(npBuffer.dtype)

    # mne.time_frequency.AverageTFR(info, npSample)

if __name__ == '__main__':
    main()