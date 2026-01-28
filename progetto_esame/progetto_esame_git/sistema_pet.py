#Modulo che definisce la classe "macchinario", che permette di descrivere e rappresentare caratteristiche e funzionamento del macchinario per la PET

import numpy as np

class esame:

    def __init__(self, nr, r_m, dt, x_s, y_s, dur, freq):

        """
        
        costruttore che permette di impostare le seguenti caratteristiche:
            - numero di rivelatori da distribuire lungo la circonferenza 
            - raggio interno della corona circolare nella quale può essere schematizzato il rivelatore
            - risoluzione temporale dei rivelatori
            - posizione rispetto al centro della sorgente di fotoni che schematizza l'organo o il tessuto in esame
            - durata della misura diagnostica
            - frequenza di decadimento tipica del materiale iniettato al paziente

            Per identificare la posizione si considera un sistema di coordinate cartesiane centrato nel centro della sezione circolare del rivelatore.

        """

        self.nr = nr #numero di rivelatori sulla circonferenza
        self.r_m = r_m #raggio interno del macchinario [m]
        self.dt = dt #risoluzione temporale [s]
        self.x_sorgente = x_s #coordinate x dei punti che costituiscono la sorgente [m]
        self.y_sorgente = y_s #coordinate y dei punti che costituiscono la sorgente [m]
        self.dur = dur #durata dell'esame [s]
        self.freq = freq #frequenza di decadimento [Hz]
        

    def emissione_coppia_punto(self):

        """

        Con questo metodo si implementa la simulazione dell'emissione di una coppia di fotoni in direzioni diametralmente opposte
        in un punto costituente la sorgente.
        Per farlo, si genera una direzione casuale e la si assegna ad uno dei due fotoni della coppia. 
        La direzione dell'altro può essere ottenuta di conseguenza e non è di fondamentale importanza.


        """

        
        angolo = np.random.uniform(low= 0, high = 2 * np.pi)
        

        return angolo

    def fotoni_emessi_punto(self):

        """

        Con questo metodo si determina l'insieme delle coppie di fotoni emesse durante tutto l'esame in un punto costituente la sorgente.
        Il numero di coppie di fotoni emesse dipende dalla frequenza di decadimento e dalla durata dell'esame. 
        Il numero di coppie medie è dato proprio dal prodotto di questi due fattori. Pertanto, il numero di coppie per ciascun evento
        può essere simulato estraendo un valore distribuito poissonianamente con media appena definita.

        """


        #numero di coppie emesse in un punto
        mu = self.freq * self.dur #numero medio di coppie emesse durante l'esame
        n_coppie = np.random.poisson(mu)

        #coppie di fotoni emesse durante l'esame in punto
        direzioni = []

        for i in range(n_coppie):
            direzione = self.emissione_coppia_punto()
            direzioni.append(direzione)

        coppie_emesse_punto = np.array(direzioni)

        return coppie_emesse_punto

    def determinazione_q_retta(self, x_punto, y_punto, direzione_fotone):

        """

        In questo metodo si implementa la determinazione del termine noto della retta passante per il punto P della sorgente in esame con coefficiente angolare
        determinato dalla direzione con la quale viene emessa una coppia di fotoni back to back nel punto considerato.

        """

        q = y_punto - np.tan(direzione_fotone) * x_punto

        return q

    def posizione_riv_coppia(self, x_punto, y_punto, direzione_fotone):

        """ 

        In questo metodo si determinano le intersezioni della retta precedentemente costruita con la circonferenza che schematizza la sezione del rivelatore:
        i due punti trovati corrispondono alle posizioni dei due rivelatori colpiti. Di tali posizioni vengono poi fatte delle opportune fluttuazioni statistiche.

        """

        def retta(x, m, q):

            """

            funzione interna di lavoro che permette semplicemente di calcolare y = m*x +q

            """

            y = m * x + q

            return y

        
        #parametri della retta
        q = self.determinazione_q_retta(x_punto, y_punto, direzione_fotone)
        m = np.tan(direzione_fotone)


        #soluzioni dell'intersezione della retta con la circonferenza
        x1 = (-(m * q) + np.sqrt(self.r_m **2 * (m**2 + 1) - q**2)) / (m**2 + 1)
        y1 = retta(x1, m, q)

        x2 = (-(m * q) - np.sqrt(self.r_m **2 * (m**2 + 1) - q**2)) / (m**2 + 1)
        y2 = retta(x2, m, q)

        #fluttuazioni delle due posizioni
        delta_theta = 2 * np.pi / self.nr  #precisione angolare del rivelatore 

        angolo1 = np.arctan2(y1, x1)
        angolo2 = np.arctan2(y2, x2)
        angoli = np.array([angolo1, angolo2])


        x_riv = []
        y_riv = []

        for i in range(len(angoli)):

            angolo = np.random.uniform(low = angoli[i] - delta_theta/2, high = angoli[i] + delta_theta/2)
            x = self.r_m * np.cos(angolo)
            y = self.r_m * np.sin(angolo)

            x_riv.append(x)
            y_riv.append(y)

        x_fluttuate = np.array(x_riv)
        y_fluttuate = np.array(y_riv)

        return x_fluttuate, y_fluttuate

    def tempi_coppia(self, x_riv, y_riv, x_punto, y_punto):

        """

        In questo metodo si implementa il calcolo dei tempi di rivelazione dei due fotoni di una stessa coppia. 
        Anche questi vengono opportunamente fluttuati.

        """
        c = 3 * 10**8 #m/s
        dist = []

        for i in range(len(x_riv)):

            d = np.sqrt((x_punto - x_riv[i]) **2 + (y_punto - y_riv[i])**2)

            dist.append(d)

        distanze = np.array(dist)
        tempi = distanze / c

        #fluttuazione statistica dei tempi
        flut = []

        for i in range(len(tempi)):
            tempo = np.random.uniform(low = tempi[i] - self.dt /2, high = tempi[i] + self.dt / 2)

            flut.append(tempo)

        tempi_fluttuati = np.array(flut)


        return tempi_fluttuati

    def ricostruzione_punto(self, x_pos_riv, y_pos_riv, tempi):

        """

        In questo metodo si implementa la ricostruzione della posizione del punto della sorgente in esame a partire dalla conoscenza dei due rivelatori
        colpiti e della differenza dei tempi di arrivo dei due fotoni.

        """

        c = 3 * 10**8 #m/s
        dist = []

        for i in range(len(x_pos_riv)):

            d = np.sqrt((x_pos_riv[i][0] - x_pos_riv[i][1]) ** 2 + (y_pos_riv[i][0] - y_pos_riv[i][1]) ** 2)

            dist.append(d)

        distanze = np.array(dist) #array che contiene le distanze tra i rivelatori colpiti da ciascuna coppia

        xc = []
        yc = []

        for i in range(len(distanze)):

            x_pm = (x_pos_riv[i][0] + x_pos_riv[i][1]) / 2 #coordinata x del punto medio del segmento che unisce i due rivelatori
            y_pm = (y_pos_riv[i][0] + y_pos_riv[i][1]) / 2 #coordinata y del punto medio del segmento che unisce i due rivelatori

            dx = x_pos_riv[i][1] - x_pos_riv[i][0] 
            dy = y_pos_riv[i][1] - y_pos_riv[i][0] 

            delta_t = tempi[i][0] - tempi[i][1]
            delta_d = c * delta_t / 2 #spostamento dalla posizione centrale

            x_p = x_pm + delta_d * dx/distanze[i]
            y_p = y_pm + delta_d * dy/distanze[i]

            xc.append(x_p)
            yc.append(y_p)

        x_centri = np.array(xc) #array con le coordinate x dei centri di ciascuna distribuzione
        y_centri = np.array(yc) #array con le coordinate y dei centri di ciascuna distribuzione
        
        #definizione di una griglia per individuare il punto

        step = 0.01 #m step della griglia compatibile con la risoluzione del rivelatore

        xg = np.arange(-self.r_m, self.r_m +step , step)
        yg = np.arange(-self.r_m, self.r_m + step, step)
        X, Y = np.meshgrid(xg, yg)
        griglia = np.zeros((len(yg), len(xg)))

        sigma_d = c * self.dt/2 #supponendo la distribuzione isotropa


        def probabilita(x ,y, x0, y0, sigma):

            """

            Questa funzione interna di lavoro permette di calcolare la probabilità associata a ciascun punto della griglia, adottando la distribuzione
            gaussiana lungo la retta che unisce ogni coppia di rivelatori colpiti, centrata nel punto sopra definito e con ampiezza data dalle sigma sopra 
            definite.

            ---

            restituisce: p= exp(-(s-s0)^2 / (2 * sigma^2)) -- s0 centro della distribuzione

            """

            dist2 = (x-x0) **2 + (y-y0)**2

            prob = np.exp((- dist2) / (2 * sigma ** 2))

            return prob

        for i in range(len(distanze)):

            mask = np.sqrt((X - x_centri[i])**2 + (Y - y_centri[i])**2) < 3*sigma_d #si considerano significativi solo i punti della griglia che distano meno di 3 sigma
            griglia[mask] += probabilita(X[mask], Y[mask], x_centri[i], y_centri[i], sigma_d)                     
                   

        indice_max = np.unravel_index(np.argmax(griglia), griglia.shape) #restituzione dell'indice corrispondente al punto di massima probabilità

        x_fin = xg[indice_max[1]]
        y_fin = yg[indice_max[0]]
              
                
        return x_fin, y_fin, xg, yg, griglia



            
        



       