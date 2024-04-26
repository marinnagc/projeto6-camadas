
#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import peakutils
import time


#funções caso queriram usar para sair...
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        #sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

freq = {1:(1209,679), 2:(1336,679), 3:(1477,679), 4:(1209,770), 5:(1336,770), 6:(1477,770), 7:(1209,852), 8:(1336,852), 9:(1477,852), 0:(1336,941)}

def getFreq(num):
    return freq[num]

def main():
    NUM = int(input("Digite um número: "))
    freq = getFreq(NUM)
    tone = []
    duration = 3
    time.sleep(5)
    tempo = np.linspace(0, duration, duration*44100,endpoint=False)
    tone1 = np.sin(2*np.pi*freq[0]*tempo)
    tone2 = np.sin(2*np.pi*freq[1]*tempo)
    tone = tone1 + tone2
    
    #********************************************instruções*********************************************** 
    # Seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada, conforme tabela DTMF.
    # Então, inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF.
    # De posse das duas frequeências, agora voce tem que gerar, por alguns segundos suficientes para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada.
    # Essas senoides têm que ter taxa de amostragem de 44100 amostras por segundo, sendo assim, voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # Lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t).
    # O tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Construa com amplitude 1.
    # Some as duas senoides. A soma será o sinal a ser emitido.
    # Utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # Você pode gravar o som com seu celular ou qualquer outro microfone para o lado receptor decodificar depois. Ou reproduzir enquanto o receptor já capta e decodifica.
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado, como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    fs = 44100
    print("Inicializando encoder")
    print("Aguardando usuário")
    print("Gerando Tons base")
    print("Executando as senoides (emitindo o som)")
    print("Gerando Tom referente ao símbolo : {}".format(NUM))
    sd.play(tone, fs)
    # aguarda fim do audio
    sd.wait()
    sinal = signalMeu()
    sinal.plotFFT(tone, fs)
    # Exibe gráficos
    plt.show()


    plt.plot(tempo, tone)
    plt.xlim([0, 0.02])
    plt.title("Sinal total emitido")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()
    

if __name__ == "__main__":
    main()
