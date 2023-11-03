import time
import cellList

class Game:

  def __init__(self , rows , cols):
    self.rows = rows
    self.cols = cols
    assert self.rows >0 and cols > 0      
    #grid initalization
    self.grid = [['.' for i in range(self.cols)] for i in range(self.rows)]

    #displaying current game status
    self.display_current_game()
    print(self.display_message("Welcome"))

    #--------------cell cordinates for each row and corner----------------------#
    self.cell_neighbour_coordinates = {
     0: (-1, -1),
     1: (-1, 0),
     2: (-1, 1),
     3: (0, -1),
     4: (0, 1),
     5: (1, -1),
     6: (1, 0),
     7: (1, 1)
     }
    self.current_neigbours_cordinates = self.cell_neighbour_coordinates.copy()
    self.upper_left_pop = [0,1,2,3,5]
    self.upper_right_pop = [0,1,2,4,7]
    self.upper_normal_pop = [0,1,2]
    self.mid_left_pop = [0,3,5]
    self.mid_right_pop = [2,4,7]
    self.mid_normal_pop = []
    self.lower_left_pop = [0,3,5,6,7]
    self.lower_right_pop = [2,4,5,6,7]
    self.lower_normal_pop = [5,6,7]

    
    #--------------cell cordinates for each row and corner----------------------#

  #------------------cell planting ---------------------------#
  def plant_cells(self , cells_list):
      if self._check_list_(cells_list):
        for item in cells_list:
          self.grid[item[0]][item[1]] = 1
        self.display_current_game()
        print(self.display_message("Cells-planted"))
      else:
        print("cell cordinates are invalid")
  #----------------cell planting ------------------------------#
  
  #------------------------------Cell generation start----------------#
  #starting the cell generations
  def _start_generation_(self , gen):
    self.generations = gen
    assert self.generations > 0
    input("Simulation Ready : Press any key to continue")  
    for currentGen in range(gen):
     for i in range(self.rows):
      for j in range(self.cols):
        cell_status = self.check_cell_status(self.grid[i][j])
        current_cell_row = self.determine_cell_row(i)
        if cell_status == True:
          if current_cell_row == "top":#checks if the cell is the uppermost row
            self.handle_upper_live_row(i,j)
          elif current_cell_row == "bottom" :#runs if the cell is in the lowermost row
            self.handle_lower_live_row(i,j)
          elif current_cell_row == "mid": 
            self.handle_mid_live_row(i,j)
        else:
         if current_cell_row == "top":
          self.handle_upper_dead_row(i,j)
         elif current_cell_row == "bottom":
          self.handle_lower_dead_row(i,j)
         elif current_cell_row == "mid":
          self.handle_mid_dead_row(i,j)
     self.display_current_game()
     print(f"CURRENT GENERATION : {currentGen+1}")
     time.sleep(1)
  #--------------------celll generation start ------------------------------#

  #--------------------------for dead cells ------------------------#
  #upper left corner : 1 , upper Right corner : 2 , lower Left corner : 3 , Lower Right corner : 4
  def handle_upper_dead_row(self , i, j):
    cornerCell = self.check_cell_corner(i,j)
    if cornerCell == 1 :
      self.handle_dead_cell(i ,j, self.upper_left_pop) 
    elif cornerCell == 2:
      self.handle_dead_cell(i ,j , self.upper_right_pop)
    elif cornerCell == False:
      self.handle_dead_cell(i,j , self.upper_normal_pop)
  
  def handle_lower_dead_row(self ,i ,j):
    cornerCell = self.check_cell_corner(i,j)
    if cornerCell == 3:
      self.handle_dead_cell(i , j , self.lower_left_pop)
    elif cornerCell == 4 :
      self.handle_dead_cell(i , j , self.lower_right_pop)
    elif cornerCell == False:
      self.handle_dead_cell(i , j , self.lower_normal_pop)
  
  def handle_mid_dead_row(self , i , j):
    if j == 0:
      self.handle_dead_cell(i , j , self.lower_left_pop)
    elif j == self.cols-1:
      self.handle_dead_cell(i , j , self.lower_right_pop)
    else:
      self.handle_dead_cell(i , j , self.lower_normal_pop)

  def handle_dead_cell(self , i , j , cordinates_list):
    self.reset_cell_cordinates()
    self.modified_pop(cordinates_list)
    cell_result = 0
    for value in self.current_neigbours_cordinates.values():
      if self.grid[i+value[0]][j+value[1]] == 1:
        cell_result += 1 
    self.modify_dead_cell(i , j , cell_result)
  
  def modify_dead_cell(self ,i , j , value):
    if value == 3:
      print(f"cell reviving {i}{j}")
      self.grid[i][j] = 1
  
  #-----------------------dead cells-----------------------------------#
  
 #------------------------cell status - cordinate -------------------------#

  def determine_cell_row(self, i):
    if i == 0 :
      return "top"
    elif i == self.rows - 1:
      return "bottom"
    else:
      return "mid"

  
  #checks if cell is alive or dead
  def check_cell_status(self, cell):
    if cell == 1 : 
      return True
    else: 
      return False
  
  #upper left corner : 1 , upper Right corner : 2 , lower Left corner : 3 , Lower Right corner : 4
  def check_cell_corner(self , row , col):
    if row == 0 and col == 0:
      return 1
    elif row == 0 and col == self.cols - 1:
      return 2
    elif row == self.rows-1 and col == 0:
      return 3
    elif row == self.rows-1 and col == self.cols - 1:
      return 4 
    else:
      return False
  
  #--------------------------------cell status - cordinate---------------------------------------------#
  
 #---------------------------------live cell handling ---------------------------------3

  def handle_upper_live_row(self , i, j):
    cornerCell = self.check_cell_corner(i,j)
    if cornerCell == 1 :
      self.handle_live_cell(i ,j, self.upper_left_pop) 
    elif cornerCell == 2:
      self.handle_live_cell(i ,j , self.upper_right_pop)
    else:
      self.handle_live_cell(i,j , self.upper_normal_pop)
  
  def handle_mid_live_row(self , i , j):
    if j == 0 :
      self.handle_live_cell(i , j , self.mid_left_pop)
    elif j == self.cols-1:
      self.handle_live_cell(i,j, self.mid_right_pop)
    else:
      self.handle_live_cell(i,j,self.mid_normal_pop)

  def handle_lower_live_row(self , i , j):
    cornerCell = self.check_cell_corner(i,j)
    if cornerCell == 3:
      self.handle_live_cell(i,j,self.lower_left_pop)
    elif cornerCell == 4:
      self.handle_live_cell(i.j.self.lower_right_pop)
    else:
      self.handle_live_cell(i,j,self.lower_normal_pop)
  

  def handle_live_cell(self , i , j , cordinates_list):
    self.reset_cell_cordinates()
    self.modified_pop(cordinates_list)
    cell_result = 0
    for value in self.current_neigbours_cordinates.values():
      if self.grid[i+value[0]][j+value[1]] == 1:
        cell_result += 1 
    self.modify_live_Cell(i,j,cell_result)
  
  def modify_live_Cell(self, i ,j , value):
    if value <= 1 or value >= 4:
      self.grid[i][j] = '.'
    
  # ------------------------------ live cell handling ------------------------------#

  # ---------------------------cell cordinates intialization and pop list ----------------------#

  def reset_cell_cordinates(self):
    self.current_neigbours_cordinates = self.cell_neighbour_coordinates.copy()
  

  def modified_pop(self, cordinates_index):
    for item in cordinates_index:
      self.current_neigbours_cordinates.pop(item)
  # ---------------------------cell cordinates intialization and pop list ----------------------#

  #----------------------------grid intalization and current status ----------------------------#
  
    #checks the cordinates func:
  def _check_list_(self, cells_list):
      for item in cells_list:
        if item[0] < 0 or item[0] > self.rows-1:
          return False
        if item[1] < 0 or item[1] > self.cols-1:
          return False
      return True 
  
  def display_current_game(self):
     for item in self.grid:
       for coloum in item:
        print (coloum , end="")
       print("")
  
  def display_message(self, msg):
     if msg == 'Welcome':
      return "Game has been intialized! Plant the cells using a list and let the game begin!"
     elif msg == 'Cells-planted':
      return "Cells have been planted! Start the Game by setting the number of generation"
  

  #------------------------grid intalization and current status ----------------------------------#

game1 = Game(30,30)
game1.plant_cells(cellList.initial_cells2)
game1._start_generation_(20)
#curent update : checks if the cell is in the uppermost or lowermost and checks if the cell is in the corner