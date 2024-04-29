import tkinter as tk
import random
from tkinter import messagebox

class Cell: 
    def __init__(self, row, col):
        self.open_status = 0
        self.probability_array = [] 
        self.neighbour_blocks = []
        self.max_per_mine = 0
        self.row = row
        self.col = col
        self.inner_run_prob = []
        self.reduced_prob = None

class Minesweeper:
    def __init__(self, master):
        self.master = master
        self.master.title('Minesweeper: S.P.A.R.K ')
        self.num_rows = 10
        self.num_columns = 15
        self.num_mines = 25
        self.cells = [[Cell(row, col) for col in range(self.num_columns)] for row in range(self.num_rows)]
        self.buttons = {}
        self.mines = []
        self.covered = set((i, j) for i in range(self.num_rows) for j in range(self.num_columns))
        self.create_game_board()

    def create_game_board(self):
        heading_label = tk.Label(self.master, text="Strategic Probabilistic Analysis of Real-time Minesweeper Kinetics", font=("Helvetica", 10, "bold"))
        heading_label.pack(pady=10)
        game_frame = tk.Frame(self.master)
        game_frame.pack()
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                button = tk.Button(game_frame, text=' ', width=6, height=3, bg ='grey', fg='white', font=("Helvetica",12,"bold"))
                button.grid(row=row, column=column)
                button.bind('<Button-1>', lambda e, x=row, y=column: self.reveal_cell(x, y))
                self.buttons[(row, column)] = button

    def initialize_game(self, first_selected_cell): 
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                self.cells[row][col].neighbour_blocks = [(row + dx, col + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if 0 <= row + dx < self.num_rows and 0 <= col + dy < self.num_columns]
        self.place_mines(first_selected_cell[0], first_selected_cell[1])

    def place_mines(self, x, y):   
        count = 0
        while count < self.num_mines:
            rand_row = random.randint(0, self.num_rows - 1)
            rand_column = random.randint(0, self.num_columns - 1)
            if abs(rand_row - x) <= 1 and abs(rand_column - y) <= 1:
                continue
            if (rand_row, rand_column) not in self.mines:
                self.mines.append((rand_row, rand_column))
                count += 1

    def reveal_cell(self, x, y):
        if not self.mines:  
            self.initialize_game((x, y))
        if (x, y) in self.mines:
            self.buttons[(x, y)].config(text='*', bg='red', fg='black')
            messagebox.showinfo("Game Over", "You clicked on a mine!")
            self.reveal_all_mines()
            self.master.destroy()
        else:
            num_mines = self.count_mines(x, y)    
            self.buttons[(x, y)].config(text=str(num_mines), bg='SystemButtonFace', fg='black')
            self.covered.remove((x, y))  
            self.cells[x][y].open_status = 1
            if num_mines == 0:
                self.auto_clear(x, y)
            self.update_probabilities() 

    def count_mines(self, x, y):      
        return sum((i, j) in self.mines for i in range(max(0, x-1), min(self.num_rows, x+2)) for j in range(max(0, y-1), min(self.num_columns, y+2)))

    def reveal_all_mines(self): 
        for mine in self.mines:
            self.buttons[mine].config(text='*', bg='red')

    def auto_clear(self, x, y):    
        for i in range(max(0, x-1), min(self.num_rows, x+2)):
            for j in range(max(0, y-1), min(self.num_columns, y+2)):
                if (i, j) in self.covered and self.buttons[(i, j)]['text'] == ' ':
                    num_mines = self.count_mines(i, j)
                    self.buttons[(i, j)].config(text=str(num_mines), bg='SystemButtonFace',fg='black')
                    self.cells[i][j].inner_run_prob.append(0.0)
                    self.cells[i][j].max_per_mine = 0
                    self.covered.remove((i, j))
                    self.cells[i][j].open_status = 1
                    if num_mines == 0:
                        self.auto_clear(i, j)

    def update_probabilities(self):
        list_of_edges = []
        for (x, y) in self.covered:
            adjacent_open_cells=[]
            X=[-1,0,1]
            for io in X:
                for jo in X:
                    newx = x+io
                    newy= y+jo
                    if( newx>=0 and newx<self.num_rows and newy>=0 and newy<self.num_columns and self.cells[newx][newy].open_status==1):
                       adjacent_open_cells.append((newx,newy))  
            if(len(adjacent_open_cells)>0):
                list_of_edges.append(((x,y),adjacent_open_cells))
        for i in list_of_edges:
            for j in i[1]:
                numrator = self.count_mines(j[0],j[1])
                denominator=0
                X=[-1,0,1]
                for io in X:
                    for jo in X:
                        newx = j[0]+io
                        newy= j[1]+jo
                        if( newx>=0 and newx<self.num_rows and newy>=0 and newy<self.num_columns and self.cells[newx][newy].open_status==0):
                            denominator+=1   
                self.cells[i[0][0]][i[0][1]].probability_array.append(numrator/denominator)
            self.cells[i[0][0]][i[0][1]].max_per_mine = max(self.cells[i[0][0]][i[0][1]].probability_array)
            self.buttons[(i[0][0], i[0][1])].config(text=f'{self.cells[i[0][0]][i[0][1]].max_per_mine * 100:.1f}%', bg ='grey')
        list_of_confirmed = [x for x in list_of_edges if (self.cells[x[0][0]][x[0][1]].max_per_mine == 1)]
        uniq_confirmed_touching_inner_edges = list(set([y for x in list_of_confirmed for y in x[1]]))
        super_non_mine_cells=[]
        for i in uniq_confirmed_touching_inner_edges:
            adjacent_closed_cells = []
            adjacent_confirmed_mines = []
            X=[-1,0,1]
            for io in X:
                for jo in X:
                    newx = i[0]+io
                    newy= i[1]+jo
                    if( newx>=0 and newx<self.num_rows and newy>=0 and newy<self.num_columns and self.cells[newx][newy].open_status==0):
                       adjacent_closed_cells.append((newx,newy))
                       if(self.cells[newx][newy].max_per_mine == 1):
                            adjacent_confirmed_mines.append((newx,newy))
            nume = self.count_mines(i[0],i[1]) - len(adjacent_confirmed_mines)
            deno = (len(adjacent_closed_cells) - len(adjacent_confirmed_mines)) if (len(adjacent_closed_cells) - len(adjacent_confirmed_mines)) > 0 else 1
            non_mine_cells = [k for k in adjacent_closed_cells if k not in adjacent_confirmed_mines]
            for i in non_mine_cells:
                super_non_mine_cells.append(i)
            for p in non_mine_cells:
                self.cells[p[0]][p[1]].inner_run_prob.append(nume/deno)
        for i in list(set(super_non_mine_cells)):
            self.cells[i[0]][i[1]].reduced_prob = min(self.cells[i[0]][i[1]].inner_run_prob)
            self.buttons[(i[0], i[1])].config(text=f'{self.cells[i[0]][i[1]].reduced_prob * 100:.1f}%',bg ='grey')
        self.remove_zero_mines()
        if(len(self.covered)==self.num_mines):
            messagebox.showinfo("Game Won", "Congratulations! You won!!")
            self.reveal_all_mines()
            self.master.destroy()

    def remove_zero_mines(self):
        list_of_edges = []
        for (x, y) in self.covered:
            adjacent_open_cells=[]
            X=[-1,0,1]
            for io in X:
                for jo in X:
                    newx = x+io
                    newy= y+jo
                    if( newx>=0 and newx<self.num_rows and newy>=0 and newy<self.num_columns and self.cells[newx][newy].open_status==1):
                        adjacent_open_cells.append((newx,newy))  
            if(len(adjacent_open_cells)>0):
                list_of_edges.append(((x,y),adjacent_open_cells))
        list_of_inner_edges = list(set([y for x in list_of_edges for y in x[1]]))
        for i in list_of_inner_edges:
            if self.count_mines(i[0],i[1])==0:
                X=[-1,0,1]
                for io in X:
                    for jo in X:
                        newx = i[0]+io
                        newy= i[1]+jo
                        if( newx>=0 and newx<self.num_rows and newy>=0 and newy<self.num_columns and self.cells[newx][newy].open_status==0): # yahaan needs changess
                            self.buttons[(newx, newy)].config(text=f'{0 * 100:.1f}%', bg ='grey')

    def count_unopened_adjacent(self, x, y):      
        return sum((i, j) in self.covered for i in range(max(0, x-1), min(self.num_rows, x+2)) for j in range(max(0, y-1), min(self.num_columns, y+2)))

if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()