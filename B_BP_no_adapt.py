# -*- coding: utf-8 -*-
"""
Created on Thu May  9 17:06:18 2019

@author: Jesus, based on @javiergaleano
"""

# bibliotecas
import imageio
import matplotlib.style as mpls
import matplotlib.pyplot as pp
import copy as cp
from random import random, uniform, shuffle, gauss, randint
import time
from time import sleep
import win32api

mpls.use('bmh')

## Parameters, initial and boundary conditions

num_agents = 1000    # num_agentes = 50, 100, 500, 1000, 2000, 5000, 10 000
recinto=round(100*((num_agents/5000)**(0.5)))/100         # recinto     = 0.1, 0.14, 0.31, 0.44, 0.63, 1, 1.41


### Predators

#Bdellovibrio (foxes)
f_init = int(0.1*num_agents) #initial Bdellovibrio population

mf = 0.05 # magnitude of movement of Bdellovibrio
df = 0.05 # death rate of Bdellovibrio
hunting_f = 1  # probabilidad de caza fortuita
offspring_f=1 #fagos adicionales que nacen de la caza

#Vampirovibrio (wolves)
w_init = int(0.0*num_agents) # initial Vampirovibrio population

mw = 0.07 # magnitude of movement of Vampirovibrio
dw = 0.02 # death rate of Vampirovibrio
hunting_w = 0.5 # probabilidad de caza fortuita
offspring_w=3 #fagos adicionales que nacen de la caza


### Preys

mr = 0.03 # magnitude of movement of preys


#Pseudomonas (rats)
r_init = int(0.9*num_agents) # 0.7 initial Pseudomonas population

rr = 0.2 # old reproduction rate of Pseudomonas (1/tiempo medio de reproducción)
cdr=0.75*(1/rr) # minimum time for Pseudomonas to complete cell division cycle. choose 0 for rr

if rr**(-1)-cdr > 0:
    nrr= 1/(rr**(-1)-cdr) # new reproduction rate of Pseudomas
else:
    print('te has colado con los numeros')
    exit()

dr=0.00 # probabilidad de muerte por unidad de tiempo


#Staphylococcus (rabbits)
ra_init = int(0.0*num_agents) # initial Staphylococcus population

rra = 0.5 # reproduction rate of Staphylococcus
cdra=0.75*(1/rra) # minimum time for Pseudomonas to complete cell division cycle.

if rra**(-1)-cdra > 0:
    nrra= 1/(rra**(-1)-cdra) # new reproduction rate of Staphylococcus
else:
    print('te has colado con los numeros')
    exit()

dra=0.03 # probabilidad de muerte por unidad de tiempo

#Haemophilus (hares)
h_init =int(0.0*num_agents) # initial Haemophilus population
 
rh = 0.2 # reproduction rate of Haemophilus
cdh=0.75*(1/rh) # minimum time for Pseudomonas to complete cell division cycle.

if rh**(-1)-cdh > 0:
    nrh= 1/(rh**(-1)-cdh) # new reproduction rate of Haemophilus
else:
    print('te has colado con los numeros')
    exit()

dh=0.01 # probabilidad de muerte por unidad de tiempo

#spatial interaction (radius of a bacteria + radius of a phage)
cd = 0.01 # radius for collision detection 
cdsq = cd ** 2


# Initialize agent class

class agent:    # "agent" es una clase. No hay funciones dentro.
                # Se añadirá especie, posiciones y tiempo para asignarle una estructura a cada agente.
    pass

def initialize():       # función sin entradas que sirve para hacer el reparto de tipos de especies
                        # y repartirlas espacialmente.
    global agents, rdata, radata, hdata, wdata, fdata   # indica como globales esas variables para
                                                        # para alterarlas dentro de los bucles.
                                                        
    agents = []     # crea listas vacias para luego añadir
    rdata = []      # aquí introduce los datos de poblaciones
    radata = []
    hdata = []
    fdata = []
    wdata = []
    
    for i in range(num_agents):     # en este bucle asigna un tipo a cada agente basandose en sus
                                    # distribuciones iniciales (designadas al principio)
        
        ag = agent()                # crea un agente en cada iteración
        
        if i < r_init:                          # a una primera porción le asigna un tipo de presa
            ag.type = 'r'
            ag.time = randint(0,round(cdr))
        elif r_init <= i < r_init + ra_init:    # a otra porción, otro tipo de presa, etc.
            ag.type = 'ra'  
            ag.time = randint(0,round(cdra))
        elif r_init + ra_init <= i < r_init + ra_init + h_init:
            ag.type = 'h'
            ag.time = randint(0,round(cdh))
        elif r_init + ra_init + h_init <= i < r_init + ra_init + h_init+w_init:
            ag.type = 'w'
        else:
            ag.type = 'f'
        
        ag.x = uniform(-recinto,recinto)     # a cada agente, una vez asignado un tipo, se le asigna una posición.
        ag.y = uniform(-recinto,recinto)
        agents.append(ag)   # introduce, uno a uno, a todos los agentes en una lista


# Plotting functions
# Drawing spatially distributed the predators and preys

def draw_space():       # dibuja a todos los agentes en el plano. No hay sorpresa.
    global agents, rdata, radata, hdata, wdata, fdata
    
    
    rabbits = [ag for ag in agents if ag.type == 'r']   # así selecciona los agentes según su tipo
                                                        # y los introduce en una lista.
    if len(rabbits) > 0:    # si no está vacío, asigna x e y en un plot.
        x = [ag.x for ag in rabbits]
        y = [ag.y for ag in rabbits]
        
        pp.plot(x, y, 'bo',label='rabbits')
        
        
    rats = [ag for ag in agents if ag.type == 'ra']
    
    if len(rats) > 0:
        x = [ag.x for ag in rats]
        y = [ag.y for ag in rats]
        pp.plot(x, y, 'go',label='rats')
        
        
    haemo = [ag for ag in agents if ag.type == 'h']
    
    if len(haemo) > 0:
        x = [ag.x for ag in haemo]
        y = [ag.y for ag in haemo]
        pp.plot(x, y, 'co',label='hares')

        
    foxes = [ag for ag in agents if ag.type == 'f']
    
    if len(foxes) > 0:
        x = [ag.x for ag in foxes]
        y = [ag.y for ag in foxes]
        pp.plot(x, y, 'r.',label='foxes')
        
        
    wolves = [ag for ag in agents if ag.type == 'w']
    
    if len(wolves) > 0:
        x = [ag.x for ag in wolves]
        y = [ag.y for ag in wolves]
        pp.plot(x, y, 'y.',label='wolves')
        
    pp.axis([-recinto-0.05, recinto+0.05, -recinto-0.05, recinto+0.05])
    pp.legend(loc='center left', bbox_to_anchor=(1, 0.5))
   
    
# Drawing the time evolution of predators and preys

def draw_evol2():
    global agents, rdata, radata, hdata, wdata, fdata

    pp.plot(rdata,'b',label = '$\it{Presas}$') # en los _data están guardadas las poblaciones
    
    if radata[0]!=0:
        pp.plot(radata,'g',label = '$\it{S. aureus}$')      # cada vez que se ejecutó evolt()
    
    if hdata[0]!=0:
        pp.plot(hdata,'c',label = '$\it{H. influenzae}$')
    
    pp.plot(fdata,'r',label = '$\it{Depredadores}$')
    
    if wdata[0]!=0:
        pp.plot(wdata,'y',label = '$\it{Vampirovibrio}$')
    
    pp.xlabel('Evolution time (a.u.)')
    pp.ylabel('Population size')
    pp.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    pp.ylim(bottom=0)
    
#   Updating the life and interaction of the agents

# - Dinámicas de mortalidad de los depredadores y/o movimiento de agentes.
# - Interacción (depredación) de los depredadores que sobreviven con las presas.
# - Reproducción de los depredadores que han interaccionado.
# - Reproducción de las presas que han sobrevivido.

def update():
    
    global agents, rdata, radata, hdata, wdata, fdata
    
    newborn=[]
    
    if len(agents) == 0 : # si no hay agentes, se sale.
        return
    
       
    else:
        
        shuffle(agents)     # mezclamos los agentes aleatoriamente para determinar en qué orden se
                            # evaluamos sus acciones.

        for ag in agents:

            # mortalidad depredadores y asignación de parámetro de movimiento
        
            if ag.type == 'w':   
                m=mw
                if random() < dw:
                    agents.remove(ag)
                    
        
            elif ag.type == 'f':
                m=mf
                if random() < df:
                   agents.remove(ag)
                   
            
            # mortalidad presas y asignación de parámetro de movimiento
        
            elif ag.type == 'r':   
                m=mr
                if random() < dr:
                    agents.remove(ag)
                    
                    
        
            elif ag.type == 'ra':
                m=mr
                if random() < dra:
                   agents.remove(ag)
                   
               
            else:
                m=mr
                if random() < dh:
                   agents.remove(ag)
            
            # simulating random movement
            
        for ag in agents:
            
            if flight=='si':  # Asignamos una distribución normal donde x=4m entra en 2 sigmas
                ag.x+=gauss(0,2*m)   # da la posibilidad de que bastantes bacterias den saltos grandes.
                ag.y+=gauss(0,2*m)
                
                if ag.x>recinto:
                    ag.x=recinto
                elif ag.x<-recinto:
                    ag.x=-recinto
                    
                if ag.y>recinto:
                    ag.y=recinto
                elif ag.y<-recinto:
                    ag.y=-recinto
                
            elif flight=='no':
                
                ag.x+=uniform(-m,m)
                ag.y+=uniform(-m,m)
                
                if ag.x>recinto:
                    ag.x=recinto
                elif ag.x<-recinto:
                    ag.x=-recinto
                    
                if ag.y>recinto:
                    ag.y=recinto
                elif ag.y<-recinto:
                    ag.y=-recinto
            
            
    # Depredación y reproducción
    
        for ag in agents:
            
            if ag.type=='f':
            
                neighbours = [nb for nb in agents if (nb.type == 'r' or nb.type =='ra'or nb.type =='h') and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]
                
                if len(neighbours)>0:
        
                    elegido=neighbours[0]    # sólo afecta a uno de las bacterias
                    
                    if random() < hunting_f:     # aplicamos probabilidad de caza fortuita
                        agents.remove(elegido)
                        
                        for i in range(offspring_f): # creamos los nuevos agentes
                            agents.append(cp.copy(ag))

            elif ag.type=='w':
            
                neighbours = [nb for nb in agents if (nb.type == 'r' or nb.type =='ra'or nb.type =='h') and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]
                
                if len(neighbours)>0:
                    
                    elegido=neighbours[0]    # sólo afecta a uno de las bacterias
                    
                    if random() < hunting_w:     # aplicamos probabilidad de caza fortuita
                        agents.remove(elegido)
                        
                        for i in range(offspring_w): # creamos los nuevos agentes
                            agents.append(cp.copy(ag))
                            
    
            elif ag.type=='r': 
                ag.time+=1
                if ag.time > cdr and random()<nrr:
                    ag.time=0
                    newborn.append(cp.copy(ag))
    
            elif ag.type=='ra':
                ag.time+=1
                if ag.time > cdra and random()<nrra:
                    ag.time=0
                    newborn.append(cp.copy(ag))
            else:
                ag.time+=1
                if ag.time > cdh and random()<nrh:
                    ag.time=0
                    newborn.append(cp.copy(ag))
        
        agents = agents + newborn
                    
#updating asynchronous agents

def update_macro(microtime):
    global agents, rdata, radata, hdata, wdata, fdata
    
    if len(agents)>0:                     # le he añadido el > 0
        t = 0.
        while t < microtime:               # crea un bucle que va a ejecutar update(), 
            t += 1                         # que es la evolución de  de los agentes, 
            # print(t)                       # varias veces.
            update()                
    else:                                          
        return
    
        
# gathering the evolution of the predator-prey's size
        
def evolt():
    global agents, rdata, radata, hdata, wdata, fdata

    
    rabbits = [ag for ag in agents if ag.type == 'r']
    rdata.append(len(rabbits))
    
    rats = [ag for ag in agents if ag.type == 'ra']
    radata.append(len(rats))
    
    haemo = [ag for ag in agents if ag.type == 'h']
    hdata.append(len(haemo))
    
    foxes = [ag for ag in agents if ag.type == 'f']
    fdata.append(len(foxes))
    
    wolves = [ag for ag in agents if ag.type == 'w']
    wdata.append(len(wolves))
    
def draw_cycle():
    global agents, rdata, radata, hdata, wdata, fdata

    pp.plot(rdata[0],fdata[0],'ro')
    pp.plot(rdata,fdata,'g')
    pp.plot(rdata[len(rdata)-1],fdata[len(rdata)-1],'bo')
    
    pp.xlabel('$\it{P. aeruginosa}$ (presa)')
    pp.ylabel('$\it{Bdellovibrio}$ (dep.)')
    
# main program 

flight='no'
opcion='pop'
cycle='no'

Tstep = 20000
p=0

initialize()
evolt()

draw_space()
pp.show()
# pp.savefig('2pred(0p04+0p01)_vs_3pray(70_20)_init_5000.png')


if opcion=='space':
    for p in range(Tstep):
        print(p)
    
        evolt()
    
        draw_space()
    
        pp.show()
    
        update()

        sleep(1)
        
        print(fdata[len(fdata)-1])
        print(rdata[len(rdata)-1])


if opcion=='pop':
    
    if cycle=='no':
    
        while rdata[len(rdata)-1]>0 and fdata[len(fdata)-1]>0 and p<=Tstep:
        
                p+=1
                print(Tstep-p)
                evolt()
                draw_evol2()
                pp.show()
                update_macro(1)
    
        draw_evol2()
        pp.show()
    
    else:
        
        start_time_bucle = time.time()
        
        while rdata[len(rdata)-1]>0 and fdata[len(fdata)-1]>0 and p<=Tstep:
        
                p+=1
                #print(Tstep-p)
                evolt()
                draw_cycle()
                pp.show()
                update_macro(1)
                
                if round((time.time() - start_time_bucle)/60,2)>=1000:
                    break
    
        draw_evol2()
        pp.show()


draw_space()
pp.show()
print(fdata[len(fdata)-1])
print(rdata[len(rdata)-1])

draw_cycle()
pp.savefig('700agentes_Ciclo_con hunting_=_{0:.3f},_df_=_{1:.3f},_rr_=_{2:.3f}_dr_={3:.3f}.png'.format(hunting_f,df,rr,dr))
pp.show()

win32api.MessageBox(0, '¡Ya acabé!', 'Main', 0x00001000) 
