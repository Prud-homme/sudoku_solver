import numpy as np
import random as rd
import pandas as pd


def available(array_9_x_9, i, j) :
    
    numbers = {'1', '2', '3', '4', '5', '6', '7', '8', '9'} #set([str(int) for int in list(range(1,10))])
    
    #On détermine le(s) chiffre(s) possible de la case vide en fonction
    
    #des chiffres déja présent dans la ligne    
    avail_line = numbers - set(array_9_x_9[i,:])
    
    #des chiffres déjà présent dans la colonne
    avail_col = numbers - set(array_9_x_9[:,j])
    
    #des chiffres déjà présent dans son bloc 3x3
    # i-i%3:i+3-i%3   ---   Permet de ramener à l'un des intervalles [0:3], [3:6] ou [6:9]   ---
    bloc_3x3 = [item for sublist in array_9_x_9[i-i%3:i+3-i%3, j-j%3:j+3-j%3] for item in sublist]
    avail_bloc = numbers - set(bloc_3x3)
    
    #On prend l'intersection des trois variables pour obtenir le(s) chiffre(s) satifsfaisant
    #ces trois critères
    avail_ij = avail_line.intersection(avail_col, avail_bloc)
    
    return(list(avail_ij))
    
    
    
def empty_cell(array_9_x_9) :
    
    table = array_9_x_9.copy()
    
    #On cherche la position des cases vides
    avail_table = np.zeros([9,9],dtype=object)
    coord_empty = [[i, j] for i in range(9) for j,value in enumerate(table[i]) if value == '']
    n_empty = len(coord_empty)
    index = 0
    
    if len(coord_empty) > 0:
        empty_turn = 0
    else :
        empty_turn = 1
        
    while empty_turn < n_empty :
        
        i,j = coord_empty[index]
        avail_nb = available(table, i, j)
        avail_table[i,j] = avail_nb
        
        if len(avail_nb) == 1 : 
            
            table[i,j] = avail_nb[0]
            n_empty -= 1
            empty_turn = 0
            del coord_empty[index]
            avail_table[i,j]=0
            
            if index >= n_empty :
                index = 0
                
            if n_empty == 0 :
                break
        else :
            index+=1
            if index >= n_empty :
                index = 0
            empty_turn += 1
            
    return(table, avail_table, coord_empty)
    
    
def empty_bloc(array_3_x_3, empty_avail) :
    
    table = array_3_x_3.copy()
    available = empty_avail.copy()
    
    #On regarde si le nombre de valeur possible est égale au nobre de cases vides
    avail_sublist = [sublist for elt in available for sublist in elt if type(sublist)==list]
    avail_nb = set([value for sublist in avail_sublist for value in sublist])
    
    #Si ce n'est pas le cas, on ne fait rien
    if len(avail_sublist) != len(avail_nb) :
        return(table)
    
    #Parcours du tableau des possibilités
    #On ne regarde que la ou il y a des possibilités (1)
    #On regarde le nombre d'occurrence d'un nombre parmis l'ensemble des cases vides
    #Si le nombre n'apparait pas cela se traduit par un zero
    #Si le nombre apparait une fois on met ses coordonnées
    #Si le nombre apparait plus d'une fois cela se traduit par 1
    unique_nb = [0]*9
    for i in range(3):       
        for j in range(3):
            
            if type(available[i,j])==list:  #(1)
                
                for item in available[i,j]:
                    
                    item=int(item)
                    
                    if type(unique_nb[item-1]) == list or unique_nb[item-1] == 1:
                        unique_nb[item-1]=1
                    else :
                        unique_nb[item-1]=[i,j]
    
    #index+1 car python commence à 0
    for index in range(9):
        if type(unique_nb[index])==list :
            i = unique_nb[index][0]
            j = unique_nb[index][1]
            table[i,j] = str(index+1)
    
    return(table)
            
            
        
        
def empty_cell2(array_9_x_9, empty_avail):
    table = array_9_x_9.copy()
    avail_table = empty_avail.copy()
    
    #On utilise la fonction empty_bloc sur les 9 blocs
    for i in range(3):
        for j in range(3):        
            table[3*i:3*i+3,3*j:3*j+3] = empty_bloc(table[3*i:3*i+3,3*j:3*j+3],
                                                    avail_table[3*i:3*i+3,3*j:3*j+3])
    return(table)
    
    
def constraints(array_9_x_9,i,j,value) :
    not_in_line = value not in set(array_9_x_9[i,:])
    not_in_column = value not in set(array_9_x_9[:,j])
    bloc_3x3 = [item for sublist in array_9_x_9[i-i%3:i+3-i%3, j-j%3:j+3-j%3] for item in sublist] 
    not_in_bloc = value not in set(bloc_3x3)
    if not_in_line and not_in_column and not_in_bloc :
        return(True)
    else:
        return(False)
    
    


def empty_cell3(array_9_x_9,
                  possibilities_array,
                  coord_empty,
                  coord_pos=0,
                  value_pos=0,
                  root_coord_pos=[],
                  root_value_pos=[]
                 ) :
    i = coord_empty[coord_pos][0]
    j = coord_empty[coord_pos][1]
    if value_pos < len(possibilities_array[i,j]) :
        value = possibilities_array[i,j][value_pos]

        if constraints(array_9_x_9,i,j,value) : 
            array_9_x_9[i,j] = value
            root_coord_pos.append(coord_pos)
            root_value_pos.append(value_pos)
            #print('valide ---   c ',coord_pos,'       v ',value_pos)
            #print(root_coord_pos[-1],'    ',root_value_pos[-1],'\n')
            if coord_pos == len(coord_empty)-1 :
                return(print('Clear'))#array_9_x_9)
            empty_cell3(array_9_x_9,
                          possibilities_array,
                          coord_empty,
                          coord_pos+1,
                          0,
                          root_coord_pos,
                          root_value_pos
                         )


        else : 

            #print('Non valide --- c',coord_pos,'       v else else ',value_pos)
            #print(root_coord_pos[-1],'    ',root_value_pos[-1],'\n')
            empty_cell3(array_9_x_9,
                          possibilities_array,
                          coord_empty,
                          coord_pos,
                          value_pos+1,
                          root_coord_pos,
                          root_value_pos
                         )
            

    else : 
        #print('Non valide (fin) --- c  ',coord_pos,'       v else if ',value_pos,'\n')
        #print(root_coord_pos[-1],'    ',root_value_pos[-1])
        last_coord = root_coord_pos[-1]
        i = coord_empty[last_coord][0]
        j = coord_empty[last_coord][1]
        last_value = root_value_pos[-1]
        #print('del ',root_coord_pos[-1],'    ',root_value_pos[-1])
          
        root_coord_pos = root_coord_pos[:-1].copy()
        root_value_pos = root_value_pos[:-1].copy()
        #print('after del ',root_coord_pos[-3:],'    ',root_value_pos[-3:],'\n')
        array_9_x_9[i,j] = ''
        empty_cell3(array_9_x_9,                        
                      possibilities_array,
                      coord_empty,
                      last_coord,
                      last_value+1,
                      root_coord_pos,
                      root_value_pos
                         )

def correct_table(array_9_x_9):
    for i in range(9):
        for j in range(9):
            nb = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
            in_line = [item for item in array_9_x_9[i,:] if item in nb]
            in_col = [item for item in array_9_x_9[:,j] if item in nb]
            bloc_3x3 = [item for sublist in array_9_x_9[i-i%3:i+3-i%3, j-j%3:j+3-j%3] for item in sublist]
            in_bloc = [item for item in bloc_3x3 if item in nb]
            if len(in_line) != len(set(in_line)) or len(in_col) != len(set(in_col)) or len(in_bloc) != len(set(in_bloc)):return(False)
                
    return(True)
        
    

def afficheZoneSaisie():
    global entries, zoneSaisie, main_gui
    #zoneSaisie = e1.get()
    
    entries=[
        e1, 
        e2, 
        e3, 
        e4,
        e5, 
        e6,
        e7, 
        e8, 
        e9,
        e10, 
        e11,
        e12, 
        e13, 
        e14, 
        e15, 
        e16, 
        e17, 
        e18, 
        e19, 
        e20, 
        e21, 
        e22, 
        e23, 
        e24,
        e25, 
        e26,
        e27, 
        e28, 
        e29,
        e30,
        e31, 
        e32, 
        e33, 
        e34, 
        e35, 
        e36, 
        e37, 
        e38, 
        e39, 
        e40, 
        e41, 
        e42, 
        e43, 
        e44, 
        e45, 
        e46, 
        e47, 
        e48, 
        e49, 
        e50,
        e51, 
        e52,
        e53, 
        e54, 
        e55, 
        e56, 
        e57,
        e58,
        e59,
        e60,
        e61,
        e62,
        e63, 
        e64,
        e65,
        e66, 
        e67, 
        e68, 
        e69, 
        e70, 
        e71, 
        e72,
        e73,
        e74, 
        e75, 
        e76,
        e77,
        e78,
        e79, 
        e80,
        e81]
    
    zoneSaisie = [e.get() for e in entries]
    main_gui.destroy()

def grille_9_x_9():
    
    global main_gui, e1,e2,e3,e4,e5,e6,e7,e8,e9,e10, e11,e12, e13, e14, e15, e16, e17, e18, e19, e20, e21, e22, e23, e24,e25, e26,e27, e28, e29,e30,e31, e32, e33, e34, e35, e36, e37, e38, e39, e40, e41, e42, e43, e44, e45, e46, e47, e48, e49, e50,e51, e52,e53, e54, e55, e56, e57,e58,e59,e60,e61,e62,e63, e64,e65,e66, e67, e68, e69, e70, e71, e72,e73,e74, e75, e76,e77,e78,e79, e80,e81
    
    main_gui = tk.Tk()
    main_gui.title("Sudoku")
    fontStyle1 = tkFont.Font(size=18)
    fontStyle2 = tkFont.Font(size=16)
    fontStyle3 = tkFont.Font(size=14)

    df_gui = tk.Frame(main_gui)
    df_gui.grid(row=0,column=0,pady=(10,10),padx=(10,10))

    e1 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e2 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e3 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e4 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e5 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e6 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e7 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e8 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e9 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e10 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e11 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e12 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e13 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e14 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e15 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e16 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e17 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e18 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e19 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e20 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e21 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e22 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e23 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e24 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e25 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e26 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e27 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e28 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e29 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e30 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e31 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e32 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e33 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e34 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e35 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e36 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e37 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e38 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e39 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e40 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e41 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e42 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e43 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e44 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e45 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e46 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e47 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e48 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e49 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e50 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e51 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e52 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e53 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e54 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e55 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e56 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e57 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e58 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e59 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e60 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e61 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e62 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e63 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e64 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e65 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e66 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e67 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e68 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e69 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e70 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e71 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e72 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e73 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e74 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e75 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e76 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e77 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e78 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e79 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e80 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)
    e81 = tk.Entry(df_gui,bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1)

    num_ligne=0
    e1.grid(row=num_ligne, column=0,padx=(0,0), pady=(0,0))
    e2.grid(row=num_ligne, column=1,padx=(0,0), pady=(0,0))
    e3.grid(row=num_ligne, column=2,padx=(0,0), pady=(0,0))
    e4.grid(row=num_ligne, column=3,padx=(3,0), pady=(0,0))
    e5.grid(row=num_ligne, column=4,padx=(0,0), pady=(0,0))
    e6.grid(row=num_ligne, column=5,padx=(0,0), pady=(0,0))
    e7.grid(row=num_ligne, column=6,padx=(3,0), pady=(0,0))
    e8.grid(row=num_ligne, column=7,padx=(0,0), pady=(0,0))
    e9.grid(row=num_ligne, column=8,padx=(0,0), pady=(0,0))

    num_ligne=1
    e10.grid(row=num_ligne, column=0,padx=(0,0), pady=(0,0))
    e11.grid(row=num_ligne, column=1,padx=(0,0), pady=(0,0))
    e12.grid(row=num_ligne, column=2,padx=(0,0), pady=(0,0))
    e13.grid(row=num_ligne, column=3,padx=(3,0), pady=(0,0))
    e14.grid(row=num_ligne, column=4,padx=(0,0), pady=(0,0))
    e15.grid(row=num_ligne, column=5,padx=(0,0), pady=(0,0))
    e16.grid(row=num_ligne, column=6,padx=(3,0), pady=(0,0))
    e17.grid(row=num_ligne, column=7,padx=(0,0), pady=(0,0))
    e18.grid(row=num_ligne, column=8,padx=(0,0), pady=(0,0))

    num_ligne=2
    e19.grid(row=num_ligne, column=0,padx=(0,0), pady=(0,0))
    e20.grid(row=num_ligne, column=1,padx=(0,0), pady=(0,0))
    e21.grid(row=num_ligne, column=2,padx=(0,0), pady=(0,0))
    e22.grid(row=num_ligne, column=3,padx=(3,0), pady=(0,0))
    e23.grid(row=num_ligne, column=4,padx=(0,0), pady=(0,0))
    e24.grid(row=num_ligne, column=5,padx=(0,0), pady=(0,0))
    e25.grid(row=num_ligne, column=6,padx=(3,0), pady=(0,0))
    e26.grid(row=num_ligne, column=7,padx=(0,0), pady=(0,0))
    e27.grid(row=num_ligne, column=8,padx=(0,0), pady=(0,0))

    num_ligne=3
    e28.grid(row=num_ligne, column=0,padx=(0,0), pady=(3,0))
    e29.grid(row=num_ligne, column=1,padx=(0,0), pady=(3,0))
    e30.grid(row=num_ligne, column=2,padx=(0,0), pady=(3,0))
    e31.grid(row=num_ligne, column=3,padx=(3,0), pady=(3,0))
    e32.grid(row=num_ligne, column=4,padx=(0,0), pady=(3,0))
    e33.grid(row=num_ligne, column=5,padx=(0,0), pady=(3,0))
    e34.grid(row=num_ligne, column=6,padx=(3,0), pady=(3,0))
    e35.grid(row=num_ligne, column=7,padx=(0,0), pady=(3,0))
    e36.grid(row=num_ligne, column=8,padx=(0,0), pady=(3,0))

    num_ligne=4
    e37.grid(row=num_ligne, column=0,padx=(0,0), pady=(0,0))
    e38.grid(row=num_ligne, column=1,padx=(0,0), pady=(0,0))
    e39.grid(row=num_ligne, column=2,padx=(0,0), pady=(0,0))
    e40.grid(row=num_ligne, column=3,padx=(3,0), pady=(0,0))
    e41.grid(row=num_ligne, column=4,padx=(0,0), pady=(0,0))
    e42.grid(row=num_ligne, column=5,padx=(0,0), pady=(0,0))
    e43.grid(row=num_ligne, column=6,padx=(3,0), pady=(0,0))
    e44.grid(row=num_ligne, column=7,padx=(0,0), pady=(0,0))
    e45.grid(row=num_ligne, column=8,padx=(0,0), pady=(0,0))

    num_ligne=5
    e46.grid(row=num_ligne, column=0,padx=(0,0), pady=(0,0))
    e47.grid(row=num_ligne, column=1,padx=(0,0), pady=(0,0))
    e48.grid(row=num_ligne, column=2,padx=(0,0), pady=(0,0))
    e49.grid(row=num_ligne, column=3,padx=(3,0), pady=(0,0))
    e50.grid(row=num_ligne, column=4,padx=(0,0), pady=(0,0))
    e51.grid(row=num_ligne, column=5,padx=(0,0), pady=(0,0))
    e52.grid(row=num_ligne, column=6,padx=(3,0), pady=(0,0))
    e53.grid(row=num_ligne, column=7,padx=(0,0), pady=(0,0))
    e54.grid(row=num_ligne, column=8,padx=(0,0), pady=(0,0))

    num_ligne=6
    e55.grid(row=num_ligne, column=0,padx=(0,0), pady=(3,0))
    e56.grid(row=num_ligne, column=1,padx=(0,0), pady=(3,0))
    e57.grid(row=num_ligne, column=2,padx=(0,0), pady=(3,0))
    e58.grid(row=num_ligne, column=3,padx=(3,0), pady=(3,0))
    e59.grid(row=num_ligne, column=4,padx=(0,0), pady=(3,0))
    e60.grid(row=num_ligne, column=5,padx=(0,0), pady=(3,0))
    e61.grid(row=num_ligne, column=6,padx=(3,0), pady=(3,0))
    e62.grid(row=num_ligne, column=7,padx=(0,0), pady=(3,0))
    e63.grid(row=num_ligne, column=8,padx=(0,0), pady=(3,0))

    num_ligne=7
    e64.grid(row=num_ligne, column=0,padx=(0,0), pady=(0,0))
    e65.grid(row=num_ligne, column=1,padx=(0,0), pady=(0,0))
    e66.grid(row=num_ligne, column=2,padx=(0,0), pady=(0,0))
    e67.grid(row=num_ligne, column=3,padx=(3,0), pady=(0,0))
    e68.grid(row=num_ligne, column=4,padx=(0,0), pady=(0,0))
    e69.grid(row=num_ligne, column=5,padx=(0,0), pady=(0,0))
    e70.grid(row=num_ligne, column=6,padx=(3,0), pady=(0,0))
    e71.grid(row=num_ligne, column=7,padx=(0,0), pady=(0,0))
    e72.grid(row=num_ligne, column=8,padx=(0,0), pady=(0,0))

    num_ligne=8
    e73.grid(row=num_ligne, column=0,padx=(0,0), pady=(0,0))
    e74.grid(row=num_ligne, column=1,padx=(0,0), pady=(0,0))
    e75.grid(row=num_ligne, column=2,padx=(0,0), pady=(0,0))
    e76.grid(row=num_ligne, column=3,padx=(3,0), pady=(0,0))
    e77.grid(row=num_ligne, column=4,padx=(0,0), pady=(0,0))
    e78.grid(row=num_ligne, column=5,padx=(0,0), pady=(0,0))
    e79.grid(row=num_ligne, column=6,padx=(3,0), pady=(0,0))
    e80.grid(row=num_ligne, column=7,padx=(0,0), pady=(0,0))
    e81.grid(row=num_ligne, column=8,padx=(0,0), pady=(0,0))



    tk.Button(main_gui,text='Valider', command=afficheZoneSaisie, font=fontStyle2).grid(row=1,pady=(0,10))
    tk.Button(main_gui,text='Quitter', command=main_gui.destroy, font=fontStyle2).grid(row=2,pady=(10,10))
    main_gui.mainloop() 
        

import numpy as np
import pandas as pd
import tkinter as tk
from tkinter.filedialog import askopenfilename
import tkinter.font as tkFont
import time
def main_prgm(dataframe,etat) :
    main_gui = tk.Tk()
    main_gui.title("Sudoku")
    fontStyle1 = tkFont.Font(size=18)
    fontStyle2 = tkFont.Font(size=16)
    fontStyle3 = tkFont.Font(size=14)
    
    if etat==1 : 
        tk.Button(main_gui,text='Update', command=main_gui.destroy, font=fontStyle2).grid(row=1,pady=(0,10))
    elif etat==2 : 
        tk.Button(main_gui,text='Quitter', command=main_gui.destroy, font=fontStyle2).grid(row=1,pady=(0,10))
    elif etat==3 :
        tk.Label(main_gui, text='Impossible de continuer', font=fontStyle3).grid(row=1)
        tk.Button(main_gui,text='Quitter', command=main_gui.destroy, font=fontStyle2).grid(row=2,pady=(10,10))
    elif etat==4 :
        tk.Label(main_gui, text='Erreur dans la saisie', font=fontStyle3).grid(row=1)
        tk.Button(main_gui,text='Quitter', command=main_gui.destroy, font=fontStyle2).grid(row=2,pady=(10,10))
    
    
    df_gui = tk.Frame(main_gui)
    df_gui.grid(row=0,column=0,pady=(10,10),padx=(10,10))
    df = dataframe
    #df_gui
    ri, cj = np.shape(df)
    for i in range(ri):
        for j in range(cj):
            margex=0
            margey=0
            if i%3 ==0 and i>0 :
                margey=3
            if j%3 == 0 and j>0 :
                margex=3
            try:
                if int(df.iloc[i,j])>0:
                    tk.Label(df_gui, text=int(df.iloc[i,j]),bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1).grid(row=i, column=j,padx=(margex,0), pady=(margey,0))
            except:
                tk.Label(df_gui, text='',bg='white',borderwidth=2,width=2,relief="groove", font=fontStyle1).grid(row=i, column=j,padx=(margex,0), pady=(margey,0))
    
    
    main_gui.mainloop()
    
    
    
import sys
sys.setrecursionlimit(100000) # 10000 is an example, try with different values


moyen=np.array([
[3,'','', '','','', '',9,4],
['',5,'', 4,'',3, '',6,''],
['',2,'', '','',9, '',3,''],
['',9,2, 6,'','', 5,'',''],
['','','', '','','', '','',''],
['','',3, '','',8, 1,2,''],
['',8,'', 9,'','', '',5,''],
['',3,9, 2,'',5, '',1,''],
[6,7,'', '',3,'', '','',2]
],dtype=str)


d=np.array([
[1,2,'', 7,'',9, '','',6],
['','','', 1,2,3, 7,'',9],
[7,'',9, 4,5,6, 1,2,''],
[2,'',1, '','',7, 5,6,4],
[5,'',4, 2,3,1, 8,'',7],
[8,'',7, 5,6,'', 2,'',1],
[3,'',2, '','','', '','',5],
[6,'',5, 3,1,2, '','',8],
[9,'',8, 6,'',5, '','','']
],dtype=str)


#table=save.copy()
#main_prgm(pd.DataFrame(table,dtype=str),1)
#correct_table(table)
#main_prgm(pd.DataFrame(table,dtype=str),4)

grille_9_x_9()
try :
    if len([item for item in zoneSaisie if item in {'1', '2', '3', '4', '5', '6', '7', '8', '9'}])==0:
        main_prgm(pd.DataFrame(table,dtype=str),3)
    table = np.array(zoneSaisie,dtype=str).reshape(9,9)
    
    if correct_table(table):
    #if len([item for item in zoneSaisie if item in {'1', '2', '3', '4', '5', '6', '7', '8', '9'}])==0:
    #    main_prgm(pd.DataFrame(table,dtype=str),3)

    #table = pd.DataFrame(np.array(zoneSaisie,dtype=str).reshape(9,9))
    #print(table)
        not_same_table = True
        empty_cell3_function = True
        while not_same_table :
            table_temp, avail_temp,coord_temp = empty_cell(table)
            table_temp = empty_cell2(table_temp, avail_temp)
            not_same_table = table.tolist() == table_temp.tolist()
            table = table_temp.copy()
            if len([sublist for elt in avail_temp for sublist in elt if sublist==0]) == 81 : 
                #main_prgm(pd.DataFrame(table,dtype=str),2)
                empty_cell3_function = False
                break
            #else :
               #main_prgm(pd.DataFrame(table_temp,dtype=str),1)
        print('Phase de déduction terminée.')
        
        if empty_cell3_function:
            try:
            	print('Début des essais...')
            	empty_cell3(table,avail_temp,coord_temp)
            	main_prgm(pd.DataFrame(table,dtype=str),2)
            except:
            	main_prgm(pd.DataFrame(table,dtype=str),3)
        else : 
            main_prgm(pd.DataFrame(table,dtype=str),3)

    else:
        main_prgm(pd.DataFrame(table,dtype=str),4)
    
except :
    table = np.zeros((9,9),dtype=str)
    main_prgm(pd.DataFrame(table,dtype=str),4)

