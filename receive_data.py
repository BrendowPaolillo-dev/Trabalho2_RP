"""Example program to show how to read a multi-channel time series from LSL."""

from pylsl import StreamInlet, resolve_stream
import mne
import numpy as np
from time import sleep
from scipy.signal import stft

#######Seleciona qual bandpower teve o valor mais alto
def selectBand(bandPower):
    sortedBand = sorted(bandPower[0])
    maxElement = sortedBand[-1]
    bIndex = bandPower[0].index(maxElement)
    return (bIndex) 

#######cálculo de média
def median (buffer):
    total = np.average(buffer)
    return (total)

def FindBandPower(buffer):

    #######Filtragem das faixas
    data = buffer.filter(l_freq=1, h_freq=50, verbose = 'ERROR')
    data = data.filter(l_freq=1, h_freq=50, verbose = 'ERROR')
    data = data.filter(l_freq=1, h_freq=50, verbose = 'ERROR')
    
    deltaBuffer, _ = mne.time_frequency.psd_welch(
        data, n_per_seg=250, fmin=0.5, fmax=4)
    thetaBuffer, _ = mne.time_frequency.psd_welch(
        data, n_per_seg=250, fmin=4, fmax=8)
    alphaBuffer, _ = mne.time_frequency.psd_welch(
        data, n_per_seg=250, fmin=8, fmax=13)
    betaBuffer, _ = mne.time_frequency.psd_welch(
        data, n_per_seg=250, fmin=13, fmax=32)
    gammaBuffer, _ = mne.time_frequency.psd_welch(
        data, n_per_seg=250, fmin=32, fmax=100)

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

    # print (returnedIndex)
    if returnedIndex == 0:
        print ("A emissão mais alta é da banda: Delta")
    elif returnedIndex == 1:
        print("A emissão mais alta é da banda: Theta")
        print("O indivíduo está passando por emoções profundas")
    elif returnedIndex == 2:
        print("A emissão mais alta é da banda: Alpha")
        print("O indivíduo está meditando")
    elif returnedIndex == 3:
        print("A emissão mais alta é da banda: Beta")
        print("O indivíduo está concentrado")
    elif returnedIndex == 4:
        print("A emissão mais alta é da banda: Gamma")


def main():
    buffer = []
    bigBuffer = []

    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')
    sample_rate = 250
    info = mne.create_info( 8, sfreq=sample_rate, ch_types='eeg')
    
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
            raw = mne.io.RawArray(npBuffer.T, info)
            values = raw.get_data()
            print(values)
            FindBandPower(raw)
            # values = mne.time_frequency.stftfreq(values, 4)
            print(np.array(values).shape)
            # values = values.reshape(1, values.shape[-1])
            # print(values.shape)
            evoked = mne.EvokedArray(values, raw.info)
            print(evoked.ch_names)
            print(evoked.data)
            evoked.pick_channels(['0', '1'])
            evoked.plot(spatial_colors=True, time_unit='s')
            buffer = buffer[256:1024]
            # print("---------------------------depois: " , len(buffer))
            # print (buffer)

    # print(sampleList)
    # print(npBuffer.dtype)

    # mne.time_frequency.AverageTFR(info, npSample)

if __name__ == '__main__':
    main()