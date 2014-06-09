# -*- coding: utf-8 -*-
# Juego del botero, instrucciones en readme
import sys
import time

class place(object):
# LUGAR: Isla en la que pueden haber habitantes
    
    def __init__(self, name, human_flag):
        # Crea una isla sin habitantes
        self.habitantes =[]
        self.name = name 
        self.human_flag = human_flag
        
    def __str__(self):
        human = ""
        if self.human_flag == 1:
            human = ". ==> Estas aqui"        
        return self.name + ". HABITANTES: " + ", ".join([str(e) for e in self.habitantes]) + str(human)
    
    def getName(self):
        return self.name
            
    def addHab(self, habitante):
        #Agrega un habitante
        self.habitantes.append(habitante)
    
    def removeHab(self, habitante):
        #Resta un habitante
        self.habitantes.remove(habitante)
    
    def lunchTime(self, juego):
        #Si no hay humanos, los habitantes comen lo que corresponde a su especie
        if self.human_flag == 0:
            #ordeno por nivel alimenticio
            hab_new = sorted(self.habitantes, key=lambda especie: especie.eat_level)
            it = len(hab_new)
            index = 0
            eatens = 0
            while it > 1:
                #verifico si hay especies que se coman
                if hab_new[index].getEatLevel() + 1 == hab_new[index + 1].getEatLevel():
                    print "Oops... " + str(hab_new[index + 1]) + " se come a " + str(hab_new[index])
                    hab_new.remove(hab_new[index])
                    eatens = eatens + 1
                    it = len(hab_new)
                else:
                    index = index + 1
                    it = it - 1
            self.habitantes = hab_new
            if eatens >= 1:
                print str(self.name) + "     CON PERDIDAS!!!" 
                juego.gameOver()
            else:
                #especies no se comen
                print str(self.name) + " sin perdidas."                 
              
        else:
            #Hay humano, asi es que especies no se comen
            print str(self.name) + " con humano presente."
        
    def isHab(self, habitante):        
        if self.habitantes.count(habitante) != 0:
            return True
        else:
            return False        
            
        
# BOTE: Transporta un límite de pasajeros de un lugar a otro, necesita un humano para funcionar
class boat(object):
    def __init__(self, origen, destino):
        self.origen = origen
        self.destino = destino
            
    def __str__(self):
        return "\nBote saliendo de " + str(self.origen.name) + " con destino " + str(self.destino.name) + " ..."

    def runBoat(self, pasajero, juego):
        #Verifica que pasajero este en origen
        print self        
        if pasajero != "solo":               
            if self.origen.isHab(pasajero) == False:
                print str(pasajero) + " no esta en esta isla (" + str(self.origen.name) + "), intenta de nuevo."        
                return 1
            else:
                #se lleva a pasajeros de isla1 a isla2
                self.destino.addHab(pasajero)
                self.origen.removeHab(pasajero)
            
        #cambia al humano
        self.origen.human_flag = 0
        self.destino.human_flag = 1
            
        #habitantes comen en sus islas respectivas
        self.origen.lunchTime(juego)
        self.destino.lunchTime(juego)
            
        #actualiza ruta
        nuevoOrigen = self.destino
        nuevoDestino = self.origen
        self.origen = nuevoOrigen
        self.destino = nuevoDestino
        return 0           
            

# BOTERO: Humano encargado de transportar pasajeros y cuidar que no se coman mutuamente
class humano(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "humano"

# PASAJERO: Un animal o vegetal que come a otro si es de un nivel inmediatamente inferior en la piramide alimenticia
class passenger(object):
    def __init__(self, kind, eat_level):
        self.kind = kind
        self.eat_level = eat_level
    def __str__(self):
        return str(self.kind)
    def getEatLevel(self):
        return self.eat_level


# JUEGO: Juego completo con jugadas y un resultado
class game(object):
    def __init__(self, islas, inicio, destino, bote):
        self.turn = 1
        self.state = 1
        self.islas = islas
        self.isla_actual = inicio
        self.isla_meta = destino
        
    def showState(self):
        #Muestra el escenario y estado
        print "\n-----------------------------------------------------"
        print "Jugada numero " + str(self.turn)
        print "-----------------------------------------------------"        
        for e in self.islas:
            print (e)
        print "-----------------------------------------------------"       
        
    def startGame(self):
        #da la bienvenida al juego e inicia primera jugada
        print "\n"
        print "***BIENVENIDO AL JUEGO DEL BOTERO*** \n"
        print "Instrucciones: Debes llevar a un lobo, una cabra y una verdura a la otra isla. \nPuedes viajar en tu bote con una carga a la vez. \nSi dejas al lobo sin vigilancia, se come a la cabra. Lo mismo la cabra con la verdura.\n"
        #raw_input("press a key to continue")
        self.playTurn()
    
    def playTurn(self):
        self.showState()                    
        #Pregunta que quiere mover                     
        viajero = self.askInput()
        if viajero == 0:
            sys.exit()
            return 0
        else:
            #Pide el bote                
            bote.runBoat(viajero, self)
        #Termina el turno
        self.isla_actual = bote.origen
        self.turn = self.turn + 1
        self.evalGame()        

    def askInput(self):
        #Pedir opcion
        pas =""
        pasDic = {"C": cabra1, "V": verdura1, "L": lobo1, "S": "solo", "exit": 0 }
        pas = raw_input("QUE LLEVARAS A LA OTRA ISLA? \nC = Cabra, V = Verdura, L = Lobo, S = Viajas solo, exit = salir del juego. >>> ")
        if pasDic.has_key(str(pas)) :
            return pasDic[str(pas)]            
        else:
            print "Eleccion invalida, intenta nuevamente"
            return self.askInput()                   
       
    def evalGame(self):
        if self.state == 0:
            #Pierde el juego
            print "*** GAME OVER :( ***"
            return 0
        else:
            #Sigue el juego
            if len(self.isla_meta.habitantes) == 3:
                self.showState() 
                print "MUY BIEN GANASTE EN " + str(self.turn) + " JUGADAS!!!" 
                return 2
            else:
                self.playTurn() 
                return 1
        
    def gameOver(self):
        self.state = 0       
    
       
         
#ESCENARIO, en proximas versiones pueden haber alternativas mas complejas conmas jugadores
isla1 = place("ISLA 1", 1)
isla2 = place("ISLA 2", 0)
bote = boat(isla1, isla2)
cabra1 = passenger("Cabra", 1)
lobo1 = passenger("Lobo", 2)
verdura1 = passenger("Verdura", 0)
humano1 = humano("Humano")
isla1.addHab(cabra1)
isla1.addHab(lobo1)
isla1.addHab(verdura1)
islas = [isla1, isla2]

#comenzar
juego = game(islas, isla1, isla2, bote)
juego.startGame()