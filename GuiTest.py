

import sys
import wx
import wx.grid as gridlib

from labyrinth import *
from agent import *


cols = 5
rows = 7


class GridFrame(wx.Frame):
###################
# GUI Constructor #
###################
    def __init__(self, parent):
        wx.Frame.__init__(self, parent,title='Aufgabe-2: Labyrinth')
        self.string_start = 'Start'
        self.string_end = 'End'
        self.string_wall = 'Wall'
        self.rows = rows    #5                                                                          # y-dimension of maze
        self.columns = cols #7                                                                          # x-dimension of maze
        rows_with_borders = self.rows + 2                                                               # y-dimension with borders
        columns_with_borders = self.columns + 2                                                         # x-dimension with borders
        self.edge_length = 40                                                                           # length of edge from square

        self.click_counter = 0

        self.start_pos = [-1, -1]                                                                       # start position[x-coord, y-coord]
        self.dest_pos = [-1, -1]                                                                        # destination position

        self.grid = wx.grid.Grid(self, -1)                                                              # create grid object

        self.grid.CreateGrid(rows_with_borders, columns_with_borders)                                   # create grid layout
        self.grid.SetRowLabelSize(0)                                                                    # without row-heading
        self.grid.SetColLabelSize(0)                                                                    # without column-heading

        self.labyrinth_model = create_labyrinth(self.columns, self.rows)
        print_labyrinth(self.labyrinth_model)

        for i in range(rows_with_borders):                                                              # set pixel size for rows
            self.grid.SetRowSize(i, self.edge_length)

        for j in range(columns_with_borders):                                                           # set pixel size for columns
            self.grid.SetColSize(j, self.edge_length)

        for i_k in range(0,columns_with_borders):                                                       # set borders around the maze
            self.grid.SetCellBackgroundColour(0, i_k, wx.LIGHT_GREY)
            self.grid.SetCellBackgroundColour(rows_with_borders-1, i_k, wx.LIGHT_GREY)

        for i_j in range(0,rows_with_borders):
            self.grid.SetCellBackgroundColour(i_j, 0, wx.LIGHT_GREY)
            self.grid.SetCellBackgroundColour(i_j, columns_with_borders-1, wx.LIGHT_GREY)

        self.grid.SetReadOnly(0, 0)
        self.grid.SetCellValue(0, 0, 'reset')
        self.grid.SetCellTextColour(0, 0, wx.RED)
        self.grid.SetReadOnly(0, 2)
        self.grid.SetCellValue(0, 2, 'solve')
        self.grid.SetCellTextColour(0, 2, wx.RED)

        self.grid.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.single_left_click)
        self.grid.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.single_right_click)

        self.Centre()                                                                                   # centering window on screen
        self.SetSize((columns_with_borders * self.edge_length + 16,rows_with_borders * self.edge_length + 39))    # wow cool shit
        self.Show()                                                                                     # display window

##############
# GUI Logic  #
##############
    def single_left_click(self, event):
        self.click_counter += 1
        print('click single')
        if event.GetCol() == 2 and event.GetRow() == 0:
            print('solve')
            solve(self.labyrinth_model)
            return
        if self.click_counter % 2 == 1:
            if event.GetCol() == 0 and event.GetRow() == 0:
                print('call_clear_labyrinth')
                self.clear_labyrinth()
                return
            start_old = self.start_pos
            if self.start_pos[0] == -1 and self.start_pos[1] == -1:
                print("current-x: %s, current-y: %s" % (event.GetCol(),event.GetRow()))
                self.start_pos[0] = event.GetCol()
                self.start_pos[1] = event.GetRow()
                if self.start_pos[1] > 0 and self.start_pos[0] > 0 \
                        and self.start_pos[1] < self.rows + 1 and self.start_pos[0] < self.columns + 1:
                    self.grid.SetCellBackgroundColour(self.start_pos[1],self.start_pos[0],wx.GREEN)                     # set start for first click
                    self.grid.SetCellValue(self.start_pos[1], self.start_pos[0], self.string_start)
                    set_start(self.start_pos[0], self.start_pos[1])                                                     # 1st x_coord, 2nd y_coord because of agent
                    self.grid.ForceRefresh()
                else:
                    print('go 1. else')
                    self.clear_labyrinth()
                    return
            else:
                if start_old[1] != 0 and start_old[0] != 0:
                    self.grid.SetCellBackgroundColour(start_old[1], start_old[0], wx.WHITE)
                    self.grid.SetCellValue(start_old[1], start_old[0], '')
                if event.GetCol() > 0 and event.GetRow() > 0 and \
                        event.GetCol() < self.columns+1 and event.GetRow() < self.rows+1:
                    self.start_pos[0] = event.GetCol()
                    self.start_pos[1] = event.GetRow()
                if self.start_pos[1] > 0 and self.start_pos[0] > 0 \
                        and self.start_pos[1] < self.rows+1 and self.start_pos[0] < self.columns+2:
                    self.grid.SetCellBackgroundColour(self.start_pos[1], self.start_pos[0], wx.GREEN)                   # set from 2nd click and so on
                    self.grid.SetCellValue(self.start_pos[1], self.start_pos[0], self.string_start)
                    set_start(self.start_pos[0], self.start_pos[1])
                    self.grid.ForceRefresh()
                else:
                    print('go 2. else')
                    print("current-x: %s, current-y: %s" % (event.GetCol(), event.GetRow()))
                    print("else-old-x: %s, old-y: %s" % (start_old[0], start_old[1]))
                    self.grid.SetCellBackgroundColour(start_old[1], start_old[0], wx.LIGHT_GREY)
                    self.grid.SetCellBackgroundColour(self.start_pos[1], self.start_pos[0], wx.LIGHT_GREY)
                    self.clear_labyrinth()
                    self.grid.ForceRefresh()
                    return
            event.Skip()
        else:
            if event.GetCol() == 0 and event.GetRow() == 0:
                print('call_clear_labyrinth')
                self.clear_labyrinth()
                return
            dest_old = self.dest_pos
            if self.dest_pos[0] == -1 and self.dest_pos[1] == -1:
                print("current-x: %s, current-y: %s" % (event.GetCol(), event.GetRow()))
                self.dest_pos[0] = event.GetCol()
                self.dest_pos[1] = event.GetRow()
                if self.dest_pos[1] > 0 and self.dest_pos[0] > 0 \
                        and self.dest_pos[1] < self.rows + 1 and self.dest_pos[0] < self.columns + 2:
                    self.grid.SetCellBackgroundColour(self.dest_pos[1], self.dest_pos[0], wx.BLUE)                      # set end for 1st click
                    self.grid.SetCellValue(self.dest_pos[1], self.dest_pos[0], self.string_end)
                    set_end(self.dest_pos[0], self.dest_pos[1])
                    self.grid.ForceRefresh()
                else:
                    print('go 3. else')
                    self.clear_labyrinth()
                    return
            else:
                self.grid.SetCellBackgroundColour(dest_old[1], dest_old[0], wx.WHITE)
                self.grid.SetCellValue(self.dest_pos[1], self.dest_pos[0], '')
                if event.GetCol() > 0 and event.GetRow() > 0 and \
                        event.GetCol() < self.columns + 1 and event.GetRow() < self.rows + 1:
                    self.dest_pos[0] = event.GetCol()
                    self.dest_pos[1] = event.GetRow()
                if self.dest_pos[1] > 0 and self.dest_pos[0] > 0 \
                        and self.dest_pos[1] < self.rows + 1 and self.dest_pos[0] < self.columns + 2:
                    self.grid.SetCellBackgroundColour(self.dest_pos[1], self.dest_pos[0], wx.BLUE)                      # set end from 2nd click and so on
                    self.grid.SetCellValue(self.dest_pos[1], self.dest_pos[0], self.string_end)
                    set_end(self.dest_pos[0], self.dest_pos[1])
                    self.grid.ForceRefresh()
                else:
                    print('go 2. else')
                    self.grid.SetCellBackgroundColour(self.dest_pos[1], self.dest_pos[0], wx.LIGHT_GREY)
                    self.grid.SetCellValue(self.dest_pos[1], self.dest_pos[0], '')
                    self.grid.ForceRefresh()
            event.Skip()


    def single_right_click(self, event):
        current_pos = [-1,-1]
        print("current-x: %s, current-y: %s" % (event.GetCol(), event.GetRow()))
        current_pos[0] = event.GetCol()
        current_pos[1] = event.GetRow()
        print(current_pos)
        if current_pos[1] > 0 and current_pos[0] > 0 \
            and current_pos[1] < self.rows + 1 and current_pos[0] < self.columns + 2:
            if self.grid.GetCellValue(current_pos[1], current_pos[0]) == '':
                self.grid.SetCellBackgroundColour(current_pos[1], current_pos[0], wx.LIGHT_GREY)
                self.grid.SetCellValue(current_pos[1], current_pos[0], self.string_wall)
                toggle_wall(self.labyrinth_model, current_pos[0], current_pos[1])
                print_labyrinth(self.labyrinth_model)
            else:
                self.grid.SetCellBackgroundColour(current_pos[1], current_pos[0], wx.WHITE)
                self.grid.SetCellValue(current_pos[1], current_pos[0], '')
                toggle_wall(self.labyrinth_model, current_pos[0], current_pos[1])
                print_labyrinth(self.labyrinth_model)
        event.Skip()


    def clear_labyrinth(self):
        for i in range(1, self.columns+1):
            for j in range(1, self.rows+1):
                self.grid.SetCellValue(j, i, '')
                self.grid.SetCellBackgroundColour(j, i, wx.WHITE)
        self.grid.SetCellValue(0, 0, 'reset')
        self.grid.SetCellTextColour(0, 0, wx.RED)
        clear_labyrinth(self.labyrinth_model)
        print_labyrinth(self.labyrinth_model)


#################
# main function #
#################
if __name__ == '__main__':

    cols = int(sys.argv[1])
    rows = int(sys.argv[2])

    if cols >= 2 and rows >= 2 and cols <= 20 and rows <= 20:
        app = wx.App(0)
        frame = GridFrame(None)
        app.MainLoop()
    else:
        if cols < 2 or rows < 2:
            print('2 cols x 2 rows minumum')
        else:
            print('20 cols and 20 rows are maximum')