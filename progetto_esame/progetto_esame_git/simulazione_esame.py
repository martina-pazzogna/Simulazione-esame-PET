#modulo che simula differenti esami PET, variando i parametri del macchinario o la struttura della sorgente

import numpy as np 
import matplotlib.pyplot as plt 
import sistema_pet
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--e1", "-e1", help = "Ricostruzione di una sorgente puntiforme", action = "store_true")
parser.add_argument("--e2", "-e2", help ="Ricostruzione di una sorgente estesa", action = "store_true")
parser.add_argument("--e3", "-e3", help ="Confronto tra differenti macchinari", action = "store_true")
args= parser.parse_args()

def circonferenza_sup(x , r):

    """

    Restituisce i punti dell'arco superiore di una circonferenza di raggio r centrata nell'origine

    """

    y = np.sqrt(r**2 - x**2)
    return y

def circonferenza_inf(x, r):

    """

    Restituisce i punti dell'arco inferiore di una circonferenza di raggio r centrata nell'origine

    """
    y = - np.sqrt(r**2 - x**2)
    return y

if args.e1:

    #esempio 1: ricostruzione di una sorgente puntiforme

    #costruzione della sorgente puntiforme
    sorgente1_x = 0.2 #m
    sorgente1_y = 0.3 #m

    #definizione dell'esame
    r1 = 0.5 #m
    nr1 = 1000
    dt1 = 10**(-9) #s
    dur1 = 1000 #s
    freq1 = 10 #s^-1

    esame1 = sistema_pet.esame(nr1, r1, dt1, sorgente1_x, sorgente1_y, dur1, freq1)

    fotoni_emessi = esame1.fotoni_emessi_punto()

    x_c = []
    y_c = []
    t_c = []

    for i in range(len(fotoni_emessi)):

        x_coppia, y_coppia = esame1.posizione_riv_coppia(sorgente1_x, sorgente1_y, fotoni_emessi[i])
        t_coppia = esame1.tempi_coppia(x_coppia, y_coppia, sorgente1_x, sorgente1_y)

        x_c.append(x_coppia)
        y_c.append(y_coppia)
        t_c.append(t_coppia)

    x_coppie = np.array(x_c)
    y_coppie = np.array(y_c)
    tempi_coppie = np.array(t_c)

    x_punto, y_punto, xg, yg, griglia = esame1.ricostruzione_punto(x_coppie, y_coppie, tempi_coppie)

    #grafico che mostra la densità di probabilità sulla griglia, dal cui massimo si è stimato il punto ricostruito
    x = np.linspace(-r1, r1, 1000)
    X, Y = np.meshgrid(xg, yg) #definizione delle coordinate di ciascuna cella della griglia
    step_g = 0.01 #m

    plt.figure(figsize=(6,6))
    plt.contourf(X, Y, np.log10(griglia + 1), levels=50, cmap='inferno')
    plt.colorbar(label='Densità di probabilità in scala logaritmica')
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.title('Simulazione esame PET con sorgente puntiforme')


    plt.scatter(sorgente1_x, sorgente1_y, label = 'Posizione della sorgente')
    plt.scatter(x_punto, y_punto, label = 'Ricostruzione della sorgente', alpha = 0.6)
    plt.plot(x, circonferenza_sup(x, r1), color = 'grey', label = 'Sezione del macchinario')
    plt.plot(x, circonferenza_inf(x, r1), color = 'grey')
    plt.legend(loc= 'upper left')
    plt.axis('equal')
    plt.xticks(np.arange(-r1, r1 + step_g, step_g))
    plt.yticks(np.arange(-r1, r1 + step_g, step_g))
    plt.tick_params(axis='x', which='both', labelbottom=False)
    plt.tick_params(axis='y', which='both', labelleft=False)
    plt.grid(True, color = 'grey', alpha = 0.5 )
    plt.show()

    #distanza tra la sorgente reale e la sua ricostruzione
    d = np.sqrt((sorgente1_x - x_punto) **2 + (sorgente1_y - y_punto) **2)
    print("La distanza tra la sorgente puntiforme e la sua ricostruzione è", d, "m")

if args.e2:

    #esempio 2: ricostruzione di una sorgente estesa 

    #costruzione della sorgente

    n = 100 #numero dei punti dei quali è costituita la sorgente
    r_s = 0.03 #m -- raggio della sorgente
    x0 = 0.1 #m -- coordinata x del centro della sorgente
    y0 = 0.04 #m -- coordinata y del centro della sorgente
    x_s = []
    y_s = []

    for i in range(n):
        r = np.random.uniform(low = 0, high = r_s)
        theta = np.random.uniform(low = 0, high = 2 * np.pi)
        x = x0 + r * np.cos(theta)
        y = y0 + r * np.sin(theta)

        x_s.append(x)
        y_s.append(y)

    x_sorgente = np.array(x_s)
    y_sorgente = np.array(y_s)

    # definizione dell'esame
    r2 = 0.4 #m
    nr2 = 10000
    dt2 =  10**(-9) #s
    dur2 = 100 #s
    freq2 = 100 #s^-1       

    esame2 = sistema_pet.esame(nr2, r2, dt2, x_sorgente, y_sorgente, dur2, freq2)

    step_g = 0.01 #m step della griglia 

    xg = np.arange(-r2, r2 +step_g , step_g)
    yg = np.arange(-r2, r2 + step_g, step_g)

    griglia_tot = np.zeros((len(yg), len(xg))) #griglia totale che sarà data dalla sovrapposizione (somma) delle griglie dei singoli punti


    ric_x = []
    ric_y = []

    for i in range(len(x_sorgente)):

        fotoni_emessi = esame2.fotoni_emessi_punto()

        xpos_riv = []
        ypos_riv = []
        tempi_riv = []

        for k in range(len(fotoni_emessi)):

            xriv, yriv = esame2.posizione_riv_coppia(x_sorgente[i], y_sorgente[i], fotoni_emessi[k])
            tempi = esame2.tempi_coppia(xriv, yriv, x_sorgente[i], y_sorgente[i])

            xpos_riv.append(xriv)
            ypos_riv.append(yriv)
            tempi_riv.append(tempi)

        x_punto, y_punto, xg, yg, griglia_punto = esame2.ricostruzione_punto(np.array(xpos_riv), np.array(ypos_riv), np.array(tempi_riv))

        ric_x.append(x_punto)
        ric_y.append(y_punto)
        griglia_tot += griglia_punto


    x_ricostruite = np.array(ric_x)
    y_ricostruite = np.array(ric_y)

    #grafico che mostra la ricostruzione della sorgente
    x = np.linspace(-r2, r2, 1000)
    X, Y = np.meshgrid(xg, yg) #definizione delle coordinate di ciascuna cella della griglia

    plt.figure(figsize=(6,6))
    plt.contourf(X, Y, np.log10(griglia_tot+1), levels=50, cmap='inferno')
    plt.colorbar(label='Densità di probabilità in scala logaritmica')
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.title('Simulazione esame PET con sorgente estesa')

    plt.scatter(x_sorgente, y_sorgente, label = 'Posizione della sorgente')
    plt.legend(loc = 'upper left')
    plt.axis('equal')
    plt.title('Simulazione esame PET con sorgente estesa')

    plt.scatter(x_ricostruite, y_ricostruite, label = 'Ricostruzione della sorgente', alpha = 0.6)
    plt.plot(x, circonferenza_sup(x, r2), color = 'grey', label = 'Sezione del macchinario')
    plt.plot(x, circonferenza_inf(x, r2), color = 'grey')
    plt.legend(loc = 'upper left')
    plt.axis('equal')
    plt.xticks(np.arange(-r2, r2 + step_g, step_g))
    plt.yticks(np.arange(-r2, r2 + step_g, step_g))
    plt.tick_params(axis='x', which='both', labelbottom=False)
    plt.tick_params(axis='y', which='both', labelleft=False)
    plt.grid(True, color = 'grey', alpha = 0.5 )
    plt.show()

    
if args.e3:

    #esempio 3: confronto degli esiti di 3 esami PET variando la risoluzione temporale del macchinario

    #configurazione della sorgente
    n = 100 #numero dei punti dei quali è costituita la sorgente
    r_s = 0.03#m -- raggio della sorgente
    x0 = 0.1#m -- coordinata x del centro della sorgente
    y0 = 0.04 # -- coordinata y del centro della sorgente
    x_s = []
    y_s = []

    for i in range(n):
        r = np.random.uniform(low = 0, high = r_s)
        theta = np.random.uniform(low = 0, high = 2 * np.pi)
        x = x0 + r * np.cos(theta)
        y = y0 + r * np.sin(theta)

        x_s.append(x)
        y_s.append(y)

    x_sorgente = np.array(x_s)
    y_sorgente = np.array(y_s)

    #configurazione dei tre macchinari
    r = 0.4 #m
    nr = 10000 
    dur = 100 #s
    freq= 100 #s^-1

    dt1 = 100 * 10**(-9 ) #s
    dt2 = 10 *10**(-9 ) #s
    dt3 = 1 * 10 **(-9 ) #s

    dt_array = np.array([dt1, dt2, dt3])
    es = []

    for dt_val in dt_array:
        exam = sistema_pet.esame(nr, r, dt_val, x_sorgente, y_sorgente, dur, freq)
        es.append(exam)

    esami = np.array(es)


    step_g = 0.01  #m step della griglia 
    xg = np.arange(-r, r +step_g , step_g)
    yg = np.arange(-r, r + step_g, step_g)


    x_es = []
    y_es = []
    griglia_es = []

    for esame in esami:

        ric_x = []
        ric_y = []
        griglia_tot = np.zeros((len(yg), len(xg)))

        for i in range(len(x_sorgente)):

            fotoni_emessi = esame.fotoni_emessi_punto()

            xpos_riv = []
            ypos_riv = []
            tempi_riv = []

            for k in range(len(fotoni_emessi)):

                xriv, yriv = esame.posizione_riv_coppia(x_sorgente[i], y_sorgente[i], fotoni_emessi[k])
                tempi = esame.tempi_coppia(xriv, yriv, x_sorgente[i], y_sorgente[i])

                xpos_riv.append(xriv)
                ypos_riv.append(yriv)
                tempi_riv.append(tempi)

            x_punto, y_punto, xg, yg, griglia_punto = esame.ricostruzione_punto(np.array(xpos_riv), np.array(ypos_riv), np.array(tempi_riv))
            ric_x.append(x_punto)
            ric_y.append(y_punto)
            griglia_tot += griglia_punto

        x_ricostruite = np.array(ric_x)
        y_ricostruite = np.array(ric_y)
        
    
        x_es.append(x_ricostruite)
        y_es.append(y_ricostruite)
        griglia_es.append(griglia_tot)

    x_esami = np.array(x_es)
    y_esami = np.array(y_es)
    griglia_esami = np.array(griglia_es)

    #grafici dei tre esami e di confronto
    x = np.linspace(-r, r, 1000)
    X, Y = np.meshgrid(xg, yg)


    fig, ax = plt.subplots(1, 3, figsize=(18, 6))

    for i in range(3):
        cf = ax[i].contourf(X, Y, np.log10(griglia_esami[i] + 1), levels=50, cmap='inferno')
        fig.colorbar(cf, ax=ax[i], label='Densità di probabilità in scala logaritmica')
        ax[i].set_xlabel('x [m]')
        ax[i].set_ylabel('y [m]')
        ax[i].scatter(x_sorgente, y_sorgente, label = 'Posizione della sorgente')
        ax[i].set_aspect('equal')
        ax[i].scatter(x_esami[i], y_esami[i], label = 'Ricostruzione della sorgente', alpha= 0.6)
        ax[i].plot(x, circonferenza_sup(x, r), color = 'grey', label = 'Sezione del macchinario')
        ax[i].plot(x, circonferenza_inf(x, r), color = 'grey')
        ax[i].set_xticks(np.arange(-r, r + step_g, step_g))
        ax[i].set_yticks(np.arange(-r, r + step_g, step_g))
        ax[i].tick_params(axis='x', which='both', labelbottom=False)
        ax[i].tick_params(axis='y', which='both', labelleft=False)
        ax[i].grid(True, color='grey', alpha=0.5)
        ax[i].legend(loc = 'upper left')
        ax[i].set_title('Ricostruzione con dt=' + str(10 ** (2 - i))+" ns")

    plt.show()

    #grafico di confronto
    plt.scatter(x_sorgente, y_sorgente, label = 'Posizione della sorgente')
    for i in range(3):
        plt.scatter(x_esami[2-i], y_esami[2-i] , label = 'Ricostruzione della sorgente estesa con dt= '+ str(10 ** (i)) +" ns", alpha = 0.3)
         
    plt.legend(loc = 'upper left')
    plt.plot(x, circonferenza_sup(x, r), color = 'grey', label = 'Sezione del macchinario')
    plt.plot(x, circonferenza_inf(x, r), color = 'grey')
    plt.axis('equal')
    plt.xticks(np.arange(-r, r + step_g, step_g))
    plt.yticks(np.arange(-r, r + step_g, step_g))
    plt.tick_params(axis='x', which='both', labelbottom=False)
    plt.tick_params(axis='y', which='both', labelleft=False)
    plt.grid(True, color = 'grey', alpha = 0.5 )
    plt.title('Confronto tra le ricostruzioni dei differenti macchinari')
    plt.show()







    
    