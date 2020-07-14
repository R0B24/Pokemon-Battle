import random

WEAKNESSES={'bug':['fire','flying','rock'],\
            'dark':['bug','fairy','fighting'],\
            'dragon':['dragon','fairy','ice'],\
            'electric':['ground'],\
            'fairy':['poison','steel'],\
            'fighting':['fairy','flying','psychic'],\
            'fire':['ground','rock','water'],\
            'flying':['electric','ice','rock'],\
            'ghost':['dark','ghost'],\
            'grass':['bug','fire','flying','ice','poison'],\
            'ground':['grass','ice','water'],\
            'ice':['fighting','fire','rock','steel'],\
            'normal':['fighting'],\
            'poison':['ground','psychic'],\
            'psychic':['ghost','bug','dark'],\
            'rock':['fighting','grass','ground','steel','water'],\
            'steel':['fighting','fire','ground'],\
            'water':['electric','grass']}


#Ran out of time to type these. Fill in if you'd like. 
RESISTANCES={}

class Pokemon:
    def __init__(self, n, l, hp, a, d, sa, sd, s, t, m):
        self.__name=n
        self.__level=l
        self.__max_hp=hp
        self.__hp=hp
        self.__attack=a
        self.__defence=d
        self.__special_attack=sa
        self.__special_defence=sd
        self.__speed=s
        self.__type=t
        self.__moves=m

    def __str__(self):
        return 'Name: ' + self.__name+\
               '\nLevel: ' + str(self.__level)+\
               '\nHP: '+ str(self.__hp)+\
               '\nAttack: '+str(self.__attack)+\
               '\nDefence: '+str(self.__defence)+\
               '\nSpecial Attack: '+str(self.__special_attack)+\
               '\nSpecial Defence: '+str(self.__special_defence)+\
               '\nSpeed: '+str(self.__speed)+\
               '\nType: '+str(self.__type)+\
               '\n'
    
    def get_name(self):
        return self.__name

    def get_hp(self):
        return int(self.__hp)

    def get_max_hp(self):
        return int(self.__max_hp)

    def get_defence(self):
        return self.__defence

    def get_special_defence(self):
        return self.__special_defence

    def get_type(self):
        return self.__type

    def get_speed(self):
        return self.__speed

    def is_dead(self):
        return self.__hp<=0
    
    def display_moves(self):
        move_num=1
        
        for move in self.__moves:
            print(str(move_num)+': '+move)
            move_num+=1
            
    def display_health_bar(self):
        return self.__name + \
              ' HP: '+str(int(self.__hp))+'/'+str(int(self.__max_hp))+\
              ' ['+'#'*int(self.__hp/10)+' '*(int(self.__max_hp/10) - int(self.__hp/10))+']'
        
        
    def damage(self, amount):
        self.__hp-=amount

    def calculate_damage(self, move_name, enemy):
        #Modifier 0.5 for resistant, 2.0 for weak against
        modifier = 1.0
        #Check for weakness
        if self.__moves[move_name].get_type() in WEAKNESSES[enemy.get_type()]:
            modifier = 2.0
        #TBD Didn't get a chance to type out the resistances chart but it could go here
        #elif self.__moves[move_name].get_type() in RESISTANCES[enemy.get_type()]:
        #   modifer=0.5

        #If the move type is physical damage use attack and defence
        if self.__moves[move_name].get_damage_type()=='physical':
            #Equation I used here is taken from https://bulbapedia.bulbagarden.net/wiki/Damage
            damage_amount=(((2*self.__level)/5+2)\
                           *(self.__moves[move_name].get_power()*self.__attack/enemy.get_defence())\
                           /50 + 2) * modifier
        #Otherwise if the move is special damage use special attack and special defence
        else:
            #Equation I used here is taken from https://bulbapedia.bulbagarden.net/wiki/Damage
            damage_amount=(((2*self.__level)/5+2)\
                           *(self.__moves[move_name].get_power()*self.__special_attack/enemy.get_special_defence())\
                           /50 + 2) * modifier

        return damage_amount, modifier

    def attack(self, move_index, enemy):
        #Find name of move in the moveset
        move_name=list(self.__moves.keys())[move_index-1]
        
        #Calculate how much damage should be dealt
        damage_amount,modifier = self.calculate_damage(move_name, enemy)
        
        print(self.__name,'used',move_name,'!\n')
        #Check to see if move hits based on it's accuracy
        if not(random.random()>self.__moves[move_name].get_accuracy()):
            if modifier>1:
                print('Woah!! The move was Super Effective')
            elif modifier<1:
                print('The move was not very Effective')
            enemy.damage(damage_amount)
        else:
            print('But the attack missed!!')

    def ai_attack(self, enemy):
        #The computer has two ways of deciding what attack to use.
        #There is a 60% chance the computer will select the move that does the most damage
        #There is a 40% chance the computer will select a random move
        DECIDING_PERCENTAGE=0.4 #You can change this value to influence the computeres decision making

        #Decide on attack strategy max vs random
        #If this branch is selected the computer will find the move that does the most damage
        if random.random()>DECIDING_PERCENTAGE:
            move_name=''
            damage_amount=0

            #Search for most powerful move available
            for temp_move_name in self.__moves.keys():
                #Calculate damage for this move
                temp_damage_amount, modifier = self.calculate_damage(temp_move_name, enemy)

                #If computer finds a more damaging move set it to move we will use
                if temp_damage_amount > damage_amount:
                    damage_amount = temp_damage_amount
                    move_name = temp_move_name
        #If this branch is selected the computer will use a random move
        else:
            #Select a random move
            move_name=list(self.__moves.keys())[random.randint(0,3)]
            #Calculate damage for this move
            damage_amount,modifier = self.calculate_damage(move_name,enemy)

        print(self.__name,'used',move_name,'!\n')
        #Check to see if move hits based on it's accuracy
        if not(random.random()>self.__moves[move_name].get_accuracy()):
            if modifier>1:
                print('Woah!! The move was Super Effective')
            elif modifier<1:
                print('The move was not very Effective')
            enemy.damage(damage_amount)
        else:
            print('But the attack missed!!')
                
class Move:
    def __init__(self,n,t,dt,a,p):
        self.__name=n
        self.__type=t
        self.__damage_type=dt
        self.__accuracy=a
        self.__power=p

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def get_damage_type(self):
        return self.__damage_type

    def get_accuracy(self):
        return self.__accuracy

    def get_power(self):
        return self.__power
        
def main():
    #Generate a list of playable Pokemon
    pokemon_list=generate_pokemon_list()

    print('Welcome to Pokemon Battler!!')

    #This loop deals with the player choosing their pokemon
    while True:
        try:
            print('\n============================\n')
            print('Choose your pokemon!')
            #Display all possible pokemon choices
            for i in range(len(pokemon_list)):
                print(str(i+1)+': '+pokemon_list[i].get_name())

            choice=int(input('> '))
            print('\n')
            #Show stats of potential pokemon choice
            print(pokemon_list[choice-1])

            #Confirm the users choice
            print('Confirm your choice: y/n\n')
            c_choice=input('> ')

            if c_choice=='y':
                player_pokemon=pokemon_list[choice-1]
                del pokemon_list[choice-1]
                computer_pokemon=pokemon_list[random.randint(0,len(pokemon_list)-1)]
                break
        except:
            print('Error: Bad input please try again.')

    print('Player chose: ',player_pokemon.get_name())
    print('Computer chose: ',computer_pokemon.get_name())
    print('Begin battle!\n')

    #While both pokemon are alive. Break if one Faints
    while True:
        print('\n============================\n')
        #Display Computer Pokemon name, hp and hp bar
        print(computer_pokemon.display_health_bar())

        print('\n\n')

        #Display Human Pokemon name, hp and hp bar
        print(player_pokemon.display_health_bar())

        print('\n\n')

        #Prompt the user to select a move
        player_pokemon.display_moves()
        choice=int(input('> '))


        #Check who's speed is higher that Pokemon gets to attack First.
	#Human wins tie breakers
        if player_pokemon.get_speed() >= computer_pokemon.get_speed():
            #Player Attack action
            player_pokemon.attack(choice, computer_pokemon)

            #Check to see if enemy pokemon fainted
            if computer_pokemon.is_dead():
                print("The enemy's Pokemon has fainted!! You Win!")
                break

            print('\n----------------------------\n')

            #Computer Attack action
            computer_pokemon.ai_attack(player_pokemon)

            #Check to see if player pokemon fainted
            if player_pokemon.is_dead():
                print("Your Pokemon has fainted!! You lose!")
                break

        else:
            #Computer Attack action
            computer_pokemon.ai_attack(player_pokemon)

            #Check to see if player pokemon fainted
            if player_pokemon.is_dead():
                print("Your Pokemon has fainted!! You lose!")
                break
            
            print('\n----------------------------\n')

            #Player Attack action
            player_pokemon.attack(choice, computer_pokemon)

            #Check to see if enemy pokemon fainted
            if computer_pokemon.is_dead():
                print("The enemy's Pokemon has fainted!! You Win!")
                break

#Creates and returns a list of playable Pokemon
def generate_pokemon_list():
    pokemon_list=[]
    #Argument ordering is: Name, Level, HP, Attack, Defence, Sp. Attack, Sp. Defence, Speed, Type, Moveset Dictionary
    #Moveset dictionary contains Name of move as a key and value is a Move object with Name, Type, Damage Type, Accuracy, Power
    
    charmander=Pokemon('Charmander', 100, 282, 223, 203, 240, 218, 251, 'fire', \
                       {'Slash':Move('Slash','normal','physical',1.0,70),\
                        'Flamethrower':Move('Flamethrower','fire','special',1.0,90),\
                        'Fire Blast':Move('Fire Blast','fire','special',0.8,110),\
                        'Fire Fang':Move('Fire Fang','fire','physical',0.95,65)}
                       )
    
    pokemon_list.append(charmander)

    squirtle=Pokemon('Squirtle', 100, 292, 214, 251, 218, 249, 203, 'water', \
                       {'Water Pulse':Move('Water Pulse','water','special',1.0,60),\
                        'Hydro Pump':Move('Hydro Pump','water','special',0.8,110),\
                        'Bite':Move('Bite','dark','physical',1.0,60),\
                        'Skull Bash':Move('Skull Bash','normal','physical',1.0,100)}
                       )
    
    pokemon_list.append(squirtle)

    bulbasaur=Pokemon('Bulbasaur', 100, 294, 216, 216, 251, 251, 207, 'grass', \
                       {'Razor Leaf':Move('Razor Leaf','grass','special',1.0,60),\
                        'Solar Beam':Move('Solar Beam','grass','special',0.85,110),\
                        'Take Down':Move('Take Down','normal','physical',0.85,90),\
                        'Double Edge':Move('Double Edge','normal','physical',1.0,100)}
                       )
    
    pokemon_list.append(bulbasaur)


    #IF YOU WANT TO ADD MORE POKEMON YOU CAN PLACE THEM HERE
    #You can find additional Pokemon here or on other sites: https://pokemondb.net/pokedex/game/heartgold-soulsilver
    #I used their Max IV values which are shown for a Level 100 Pokemon

    return pokemon_list

main()





