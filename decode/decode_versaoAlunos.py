
#Importe todas as bibliotecas
from suaBibSignal import *
import peakutils
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time

#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    #*****************************instruções********************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = signalMeu() 
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    fs = 44100
    sd.default.samplerate = fs #taxa de amostragem
    sd.default.channels =  1 #numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas.
    #Muitas vezes a gravação retorna uma lista de listas. Você poderá ter que tratar o sinal gravado para ter apenas uma lista.
    duration =  5 # #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic   
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisições) durante a gravação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
    numAmostras = fs*duration
    #faca um print na tela dizendo que a captação comecará em n segundos. e então 
    #use um time.sleep para a espera.
   
    #A seguir, faca um print informando que a gravacao foi inicializada
    print(f'A gravação vai começar em 3 segundos')
    time.sleep(2)
    print("Gravação iniciada")
    #para gravar, utilize
    audio = sd.rec(int(numAmostras), samplerate=fs, channels=1)
    sd.wait()
    print("...     FIM")


    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, ou uma lista, ou ainda uma lista de listas (isso dependerá do seu sistema, drivers etc...).
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    dados = audio[:,0]
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    t = np.linspace(0, duration, num=numAmostras)
    # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) . 
    plt.figure(figsize=(10, 4))
    plt.plot(t, dados)
    plt.title("Recorded Audio")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.grid(True)
    ## Calcule e plote o Fourier do sinal audio. como saída tem-se a amplitude e as frequências.
    xf, yf = signal.calcFFT(dados, fs)
    plt.figure(figsize=(10, 4))
    plt.plot(xf, np.abs(yf))
    plt.title("FFT of Recorded Audio")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.show()
    #Agora você terá que analisar os valores xf e yf e encontrar em quais frequências estão os maiores valores (picos de yf) de da transformada.
    #Encontrando essas frequências de maior presença (encontre pelo menos as 5 mais presentes, ou seja, as 5 frequências que apresentam os maiores picos de yf). 
    #Cuidado, algumas frequências podem gerar mais de um pico devido a interferências na tranmissão. Quando isso ocorre, esses picos estão próximos. Voce pode desprezar um dos picos se houver outro muito próximo (5 Hz). 
    #Alguns dos picos  (na verdade 2 deles) devem ser bem próximos às frequências do DTMF enviadas!
    #Para descobrir a tecla pressionada, você deve encontrar na tabela DTMF frquências que coincidem com as 2 das 5 que você selecionou.
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

    
    #printe os picos encontrados! 
    index_peaks = peakutils.indexes(np.abs(yf), thres=0.5, min_dist=20)
    # Ordenar os picos pela magnitude e pegar os 5 maiores
    peak_freqs = [(xf[i], np.abs(yf[i])) for i in index_peaks]
    peak_freqs.sort(key=lambda x: x[1], reverse=True)
    top_five_peaks = peak_freqs[:5]
    print("Picos detectados:", top_five_peaks)
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print o valor tecla!!!
    #Se acertou, parabens! Voce construiu um sistema DTMF

    #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 

      
    ## Exiba gráficos do fourier do som gravados 


if __name__ == "__main__":
    main()
