# -*- coding: utf-8 -*-
# Clases para el juego
import sys

class place(object):
# LUGAR: Isla en la que pueden haber pasajeros
    
    def __init__(self, name, human_flag):
        # Crea una isla sin habitantes
        self.habitantes =[]
        self.name = name 
        self.human_flag = human_flag
        
    def __str__(self):        
        return 'LUGAR: ' + self.name + ". HABITANTES: " + ", ".join([str(e) for e in self.habitantes])
    
    def getName(self):
        return self.name
            
    def addHab(self, habitante):
        #Agrega un habitante
        self.habitantes.append(habitante)
    
    def removeHab(self, habitante):
        #Resta un habitante
        self.habitantes.remove(habitante)
    
    def lunchTime(self, juego):
        #Los habitantes comen lo que corresponde a su especie
        if self.human_flag == 0:
            #print "No hay humano, especies se comeran en " + str(self)            
            #print "ordeno por eat level"
            hab_new = sorted(self.habitantes, key=lambda especie: especie.eat_level)
            #obtener el num de elementos para iterar
            #print str(hab_new)
            #raw_input("presione una tecla..")
            it = len(hab_new)
            index = 0
            eatens = 0
            while it > 1:
                if hab_new[index].getEatLevel() + 1 == hab_new[index + 1].getEatLevel():
                    print str(hab_new[index + 1]) + " se come a: " + str(hab_new[index])
                    hab_new.remove(hab_new[index])
                    eatens = eatens + 1
                    it = len(hab_new)
                else:
                    #print "sin comidas"
                    #raw_input("control2")
                    index = index + 1
                    it = it - 1
            self.habitantes = hab_new
            if eatens >= 1:
                print "Perdidas en " + str(self.name)
                juego.gameOver()
            else:
                #especies no se comen
                print "Ok, sin muertes en " + str(self.name)
                #raw_input("control 5")                      
              
        else:
            print "Ok, humano presente en " + str(self.name)
        
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
        return "Bote disponible en " + str(self.origen.name) + " con destino " + str(self.destino.name)
   
    def runBoat(self, pasajero, juego):
        #Verifica origen de pasajeros
        print self
        if pasajero != "empty":               
            #print "Verificando pasajero " + str(pasajero)
            #raw_input("presione una tecla...")
            if self.origen.isHab(pasajero) == False:
                print str(pasajero) + " no esta en el origen, intenta de nuevo"
                #raw_input("presione una tecla...")            
                return 1
            else:
                #se lleva a pasajeros de isla1 a isla2
                #raw_input("presione una tecla...")
                self.destino.addHab(pasajero)
                self.origen.removeHab(pasajero)
                #print "pasajero transportado"
                #raw_input("presione una tecla...")
            
        #cambia al humano
        self.origen.human_flag = 0
        self.destino.human_flag = 1
        print "Has llegado a la isla " + str(self.destino.name)
        #raw_input("presione una tecla...")
            
        #habitantes comen
        self.origen.lunchTime(juego)
        self.destino.lunchTime(juego)
        #print "hora comida lista"
        #raw_input("presione una tecla...")
            
        #cambia de ruta
        nuevoOrigen = self.destino
        nuevoDestino = self.origen
        self.origen = nuevoOrigen
        self.destino = nuevoDestino
        print "Viaje terminado \n"
        return 0           
            

# BOTERO: Humano encargado de transportar pasajeros y cuidar que no se coman mutuamente
class humano(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "humano"

# PASAJERO: Un animal o vegetal que come a otro es de un nivel inmediatamente inferior
class passenger(object):
    def __init__(self, kind, eat_level):
        self.kind = kind
        self.eat_level = eat_level
    def __str__(self):
        return str(self.kind)
    def getEatLevel(self):
        return self.eat_level

# JUGADA: Movimiento de un turno

# JUEGO: Juego completo compuesto de varias jugadas y un resultado
class game(object):
    def __init__(self, islas, inicio, destino, bote):
        self.turn = 0
        self.state = 1
        self.islas = islas
        self.isla_actual = inicio #isla de partida
        #self.otra_isla = destino
        self.isla_meta = destino
        
    def __str__(self):
        return "Estas en " + str(self.isla_actual.name) + ". Jugada numero " + str(self.turn) + "\n"
        
    def startGame(self):
        #da la bienvenida al juego e inicia primera jugada
        print "BIENVENIDO AL JUEGO DEL BOTERO \n"
        print "Debes llevar a un lobo, una cabra y una lechuga a la otra isla. \n. En tu bote cabes tu con una carga a la vez. \n Si dejas al lobo sin vigilancia, se come a la cabra. Lo mismo la cabra con la verdura.\n"
        #raw_input("press a key to continue")
        self.playTurn()
    
    def playTurn(self):
        #Juega un turno
        
        #Muestra el escenario y estado
        for e in self.islas:
            print (e)
        print self
                    
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
        pasDic = {"C": cabra1, "V": verdura1, "L": lobo1, "S": "empty", "exit": 0 }
        pas = raw_input("Ingresa que quieres llevar: C = Cabra, V = Verdura, L = Lobo, S = Viajas solo, exit = salir del juego. >>> ")
        if pasDic.has_key(str(pas)) :
            return pasDic[str(pas)]            
        else:
            print "Eleccion invalida, intenta nuevamente"
            self.askInput()                   
       
    def evalGame(self):
        if self.state == 0:
            print "Game Over"
            return 0
        else:
            #Cumple el objetivo del juego
            if len(self.isla_meta.habitantes) == 3:
                print "MUY BIEN GANASTE con " + str(self.turno) + " jugadas." 
                return 2
            else:
                self.playTurn() 
                return 1
        
    def gameOver(self):
        self.state = 0       
    
       
         
#ESCENARIO
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
