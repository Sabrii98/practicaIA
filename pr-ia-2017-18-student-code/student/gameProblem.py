#
'''
    Class gameProblem, implements simpleai.search.SearchProblem
'''


from simpleai.search import SearchProblem
import simpleai.search

class GameProblem(SearchProblem):

    # Object attributes, can be accessed in the methods below
    
	MAP=None
	POSITIONS=None
	INITIAL_STATE=None
	GOAL=None
	CONFIG=None
	AGENT_START=None


    # --------------- Common functions to a SearchProblem -----------------
    
    
	def actions(self, state):
		
		actions = []
		posicion_actual = state[0]
		num_filas = self.CONFIG['map_size'][1] 
		num_columnas = self.CONFIG['map_size'][0] 
		
		#Control accion norte
		if posicion_actual[1] != 0:  
			if(posicion_actual[0], posicion_actual[1] - 1) not in (self.POSITIONS['sea']): 
				actions.append('North')  
		#Control accion sur 
		if posicion_actual[1] != (num_filas - 1): 
			if (posicion_actual[0],posicion_actual[1] + 1) not in (self.POSITIONS['sea']): 
				actions.append('South') 
		#Control accion este
		if posicion_actual[0] != (num_columnas - 1):  
			if (posicion_actual[0] + 1, posicion_actual[1]) not in (self.POSITIONS['sea']): 
				actions.append('East') 
		#Control accion oeste
		if posicion_actual[0] != 0: 
			if (posicion_actual[0] - 1, posicion_actual[1]) not in (self.POSITIONS['sea']): 
				actions.append('West') 
											
		return actions
    

	def result(self, state, action):
		
		posicion_actual = state[0]
		fotos = state[1] 
		
		
		#Control accion norte
		if action == 'North': 
			state_final = ((posicion_actual[0], posicion_actual[1] - 1), tuple([cont for cont in fotos if cont != (posicion_actual[0], posicion_actual[1] - 1)]))
		#Control accion sur 
		elif action == 'South':
			state_final = ((posicion_actual[0], posicion_actual[1] + 1), tuple([cont for cont in fotos if cont != (posicion_actual[0], posicion_actual[1] + 1)]))
		#Control accion este
		elif action == 'East':
			state_final = ((posicion_actual[0] + 1, posicion_actual[1]), tuple([cont for cont in fotos if cont != (posicion_actual[0] + 1, posicion_actual[1])]))
		#Control accion oeste
		elif action == 'West':
			state_final = ((posicion_actual[0] - 1, posicion_actual[1]), tuple([cont for cont in fotos if cont != (posicion_actual[0] - 1, posicion_actual[1])]))
			
		return state_final

	def is_goal(self, state):
		if state == self.GOAL:
			return True
		else:
			return False
			

	def cost(self, state, action, state2):
		
		posicion_sgte = state2[0]
		
		return self.MAP[posicion_sgte[0]][posicion_sgte[1]][2]['cost']

	def heuristic(self, state):
		
		posicion_actual = state[0]
		fotos = state[1]
		num_fotos = len(fotos)
		contador =  0
		lista_longitudes = []
		
		if num_fotos == 0:
			return 0
		else:
			while contador < num_fotos:
				lista_longitudes.append((abs(posicion_actual[0] - fotos[contador][0])) + (abs(posicion_actual[1] - fotos[contador][1])))
				contador = contador + 1
			return 	min(lista_longitudes)


	def setup (self):
		
		print '\nMAP: ', self.MAP, '\n'			
		print 'POSITIONS: ', self.POSITIONS, '\n'
		print 'CONFIG: ', self.CONFIG, '\n'
		  
		initial_state = (self.AGENT_START, tuple(self.POSITIONS['goal']))
		final_state= (self.AGENT_START, ())
		algorithm= simpleai.search.astar
				
		return initial_state,final_state,algorithm
		
		



        
    # -------------------------------------------------------------- #
    # --------------- DO NOT EDIT BELOW THIS LINE  ----------------- #
    # -------------------------------------------------------------- #
    
	def getAttribute (self, position, attributeName):
		'''Returns an attribute value for a given position of the map
			position is a tuple (x,y)
			attributeName is a string
           
			Returns:
				None if the attribute does not exist
                Value of the attribute otherwise
        '''
		tileAttributes=self.MAP[position[0]][position[1]][2]
		if attributeName in tileAttributes.keys():
			return tileAttributes[attributeName]
		else:
			return None
        
    # THIS INITIALIZATION FUNCTION HAS TO BE CALLED BEFORE THE SEARCH
	def initializeProblem(self,map,positions,conf,aiBaseName):
        
        # Loads the problem attributes: self.AGENT_START, self.POSITIONS,etc.
		if self.mapInitialization(map,positions,conf,aiBaseName):
			
			initial_state,final_state,algorithm = self.setup()
            
			self.INITIAL_STATE=initial_state
			self.GOAL=final_state
			self.ALGORITHM=algorithm
			super(GameProblem,self).__init__(self.INITIAL_STATE)
            
			return True
		else:
			return False
        
    # END initializeProblem 

	def mapInitialization(self,map,positions,conf,aiBaseName):
        # Creates lists of positions from the configured map
        # The initial position for the agent is obtained from the first and only aiBaseName tile
		self.MAP=map
		self.POSITIONS=positions
		self.CONFIG=conf

		if 'agentInit' in conf.keys():
			self.AGENT_START = tuple(conf['agentInit'])
		else:                    
			if aiBaseName in self.POSITIONS.keys():
				if len(self.POSITIONS[aiBaseName]) == 1:
					self.AGENT_START = self.POSITIONS[aiBaseName][0]
				else:
					print ('-- INITIALIZATION ERROR: There must be exactly one agent location with the label "{0}", found several at {1}'.format(aiAgentName,mapaPosiciones[aiAgentName]))
					return False
			else:
				print ('-- INITIALIZATION ERROR: There must be exactly one agent location with the label "{0}"'.format(aiBaseName))
				return False
        
		return True
    

