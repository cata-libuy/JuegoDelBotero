# -*- coding: utf-8 -*-
# Clases para el juego

class place(object):
# LUGAR: Isla en la que pueden haber pasajeros
    
    def __init__(self, name):
        # Crea una isla sin habitantes
        self.habitantes =[]
        self.name = name 
        
    def __str__(self):        
        return '* ISLA ' + self.name + ". > Habitantes: " + ", ".join([str(e) for e in self.habitantes]) +". *"
    
    def addHab(self, habitante):
        #Agrega un habitante
        self.habitantes.append(habitante)
    
    def removeHab(self, habitante):
        #Resta un habitante
        self.habitantes.remove(habitante)
    
    def lunchTime(self):
        #Los habitantes comen lo que corresponde a su especie
        return "lunch time no implementado"
        
    def isHab(self, habitante):        
        if self.habitantes.count(habitante) != 0:
            return True
        else:
            return False        
            
        
# BOTE: Transporta un límite de pasajeros de un lugar a otro, necesita un humano para funcionar
class boat(object):
    def __init__(self, origen):
        self.origen = origen
        self.pasajeros = []
    
    def __str__(self):
        return "bote disponible en " + str(self.origen)
    
    def runBoat(self, destino, pasajeros):
        #Verifica origen de pasajeros                
        for e in pasajeros:
            if self.origen.isHab(e) == False:
                return str(e) + " no esta en el origen, intenta de nuevo"
        #Verifica capacidad        
        if len(pasajeros) > 2:
            return "Lo siento, maximo dos pasajeros"
        #Verifica humano            
        elif pasajeros.count("humano") == 0:
            return "Necesitas un humano dentro del bote"
        else:
            #se lleva a pasajeros de isla1 a isla2
            for e in pasajeros:
                destino.addHab(e)
                self.origen.removeHab(e)
            #habitantes comen
            self.origen.lunchTime()
            destino.lunchTime()
            self.origen = destino
            return "viaje ok"           
            

# BOTERO: Humano encargado de transportar pasajeros y cuidar que no se coman mutuamente

# PASAJERO: Un animal o vegetal que come a otro pasajero si es de un nivel inmediatamente inferior

# JUGADA: Movimiento de un turno

# JUEGO: Juego completo compuesto de varias jugadas y un resultado

#TEST

isla1 = place("isla bonita")
isla2 = place("isla feita")
bote = boat(isla1)
isla1.addHab("tori")
isla1.addHab("humano") 
    