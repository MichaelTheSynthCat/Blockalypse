# Blockalypse.py
# Author: Michal Krulich
#
# This game uses tkinter GUI but it would be better if it used some other GUI framework,
# because the tkinter's Canvas does not properly destroys old frames, so the longer you
# play the game, the more lags you can encounter (due to all nonexistient objects which
# canvas tries to render). 
#
# This game I programmed when I was for the first time learning to code, therefore it's quite a messy code.

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from string import *
from copy import *
from random import *
import time

class App(Frame):
    def __init__(self, master):  # main frame
        Frame.__init__(self, master)
        self.grid()
        self.cheats_on = StringVar(value=0)
        tk.bind('<KeyPress>', self.keybindings)
        
    def create_menus(self):  # menu
        self.menubar = Menu(tk)
        tk['menu'] = self.menubar
        self.menus = [Menu(self.menubar), Menu(self.menubar), Menu(self.menubar), Menu(self.menubar)]
        self.menubar.add_cascade(menu=self.menus[0], label='Main')
        self.menus[0].add_command(label='Pause', command=self.pause_handler)
        self.menus[0].add_command(label='About', command=AboutWindow)
        self.menus[0].add_command(label='Version: '+version, state='disabled')
        self.menus[0].add_command(label='Exit', command=tk.destroy)
        self.menubar.add_cascade(menu=self.menus[1], label='Classic')
        self.menus[1].add_command(label='Singleplayer', command=self.singleplayer_game)
        self.menus[1].add_command(label='Adventure', command=self.adventure_game)
        self.menus[1].add_separator()
        self.menus[1].add_command(label='Co-op', command=self.coop_game)
        self.menus[1].add_separator()
        self.menus[1].add_command(label='Triple the Trouble', command=self.triple_game)
        self.menubar.add_cascade(menu=self.menus[2], label='Arcade')
        self.menus[2].add_command(label='Quick', command=self.quick_game)
        self.menus[2].add_command(label='Destruction', command=self.destruction_game)
        self.menus[2].add_separator()
        self.menus[2].add_command(label='Not enough space', command=self.notenoughspace_game)
        self.menubar.add_cascade(menu=self.menus[3], label='Options')
        self.menus[3].add_command(label='Keybindings', command=keybindings.open_window)
        self.menus[3].add_checkbutton(label='Cheats', variable=self.cheats_on, onvalue=1, offvalue=0)
            
    def keybindings(self, event):  # keybindings
        key = event.keysym_num
        if chr(key) in ascii_lowercase:
            key = ord(chr(key).capitalize())

        if game.game_go and game.players_playable >= 1:
            # player 1
            p1 = keys['player1']
            if p1['left'] == key:
                game.move_block(direction='left')
            elif p1['right'] == key:
                game.move_block(direction='right')
            elif p1['put_down'] == key:
                game.put_down()
            elif p1['rotate_counterclockwise'] == key:
                game.rotate_block(rotate=-90)
            elif p1['rotate_clockwise'] == key:
                game.rotate_block(rotate=90)
            elif p1['one_down'] == key:
                game.one_down()
            elif p1['orbital_strike'] == key:
                game.special_abilities(ability='Orbital strike')
            elif p1['atom_bomb'] == key:
                game.special_abilities(ability='Atom bomb')
            elif p1['skyshift'] == key:
                game.special_abilities(ability='Skyshift')

        if game.game_go and game.players_playable >= 2:
            # player 2
            p2 = keys['player2']
            if p2['left'] == key:
                game.move_block(direction='left', player=2)
            elif p2['right'] == key:
                game.move_block(direction='right', player=2)
            elif p2['put_down'] == key:
                game.put_down(player=2)
            elif p2['rotate_counterclockwise'] == key:
                game.rotate_block(rotate=-90, player=2)
            elif p2['rotate_clockwise'] == key:
                game.rotate_block(rotate=90, player=2)
            elif p2['one_down'] == key:
                game.one_down(player=2)
                
        if game.game_go and game.players_playable >= 3:
            # player 3
            p3 = keys['player3']
            if p3['left'] == key:
                game.move_block(direction='left', player=3)
            elif p3['right'] == key:
                game.move_block(direction='right', player=3)
            elif p3['put_down'] == key:
                game.put_down(player=3)
            elif p3['rotate_counterclockwise'] == key:
                game.rotate_block(rotate=-90, player=3)
            elif p3['rotate_clockwise'] == key:
                game.rotate_block(rotate=90, player=3)
            elif p3['one_down'] == key:
                game.one_down(player=3)

        # special keys
        sp = keys['special']
        if sp['pause'] == key:
            game.pause()
        elif sp['faster'] == key and int(self.cheats_on.get()) == 1:
            game.faster()
        elif sp['slower'] == key and int(self.cheats_on.get()) == 1:
            game.slower()
        elif sp['singleplayer'] == key:
            self.singleplayer_game()
        elif sp['adventure'] == key:
            self.adventure_game()
        elif sp['quick'] == key:
            self.quick_game()
        elif sp['destruction'] == key:
            self.destruction_game()
        elif sp['coop'] == key:
            self.coop_game()
        elif sp['triple_the_trouble'] == key:
            self.triple_game()
        elif sp['not_enough_space'] == key:
            self.notenoughspace_game()

    def start(self, game_object):
        global game
        game.grid_forget()
        game.__del__()
        game = game_object

    def start_confirm(self):
        if not game.demo and not game.game_lost:
            game.game_go = False
            value = messagebox.askyesno(message='Would you like to start a new game?', detail='You will lose all your progress in actual game.')
            game.game_go = True
            if not game.demo:
                game.engine_process = game.after(0, game.engine)
            return value
        else:
            return True
            
    def singleplayer_game(self):
        if self.start_confirm():
            self.start(Game())

    def coop_game(self):
        if self.start_confirm():
            self.start(Game(name='Co-op', start=[20, 18], sq_size=30,
                            speed=700, lvl={'goal':2000, 'new_goal':'x1.5', 'faster':30, 'maximal':180}, players=2))
            
    def triple_game(self):
        if self.start_confirm():
            self.start(Game(name='Triple', start=[30, 20], sq_size=30,
                            speed=700, lvl={'goal':3000, 'new_goal':'x1.5', 'faster':30, 'maximal':180}, players=3))

    def adventure_game(self):
        if self.start_confirm():
            self.start(Game(name='Adventure', start=[16, 18], sq_size=30,
                            speed=500, spawn_chance={'normal':0.6, 'adventure':0.27, 'big':0.1, 'boss':0.03}, lvl={'goal':1000, 'new_goal':'+1000', 'faster':20, 'maximal':220}, spab=True))

    def quick_game(self):
        if self.start_confirm():
            self.start(Game(name='Quick', start=[6, 16],
                            speed=200, spawn_chance={'tiny':1}, lvl={'goal':900, 'new_goal':'x1.4', 'faster':20, 'maximal':40}))

    def destruction_game(self):
        if self.start_confirm():
            self.start(Game(name='Destruction', start=[20, 16], sq_size=30,
                            speed=1000, spawn_chance={'adventure':1}, lvl={'goal':700, 'new_goal':'+700', 'faster':20, 'maximal':400},
                            spab=True, randomfall={'spawn_chance':{'normal':0.5, 'big':0.47, 'boss':0.03}, 'count':3}))

    def notenoughspace_game(self):
        if self.start_confirm():
            self.start(Game(name='Not enough space', start=[10, 16], sq_size=40,
                            speed=300, spawn_chance={'tiny':1}, lvl={'goal':2000, 'new_goal':'x1.4', 'faster':20, 'maximal':100},
                            players=3))

    def pause_handler(self):
        game.pause()


class Game(Canvas):  # game engine
    fall = ['x', 'X', 'y', 'Y', 'z', 'Z', 'a', 'A', 'b', 'B', 'c', 'C']
    PLAYERS = [['x', 'X'], ['y', 'Y'], ['z', 'Z'], ['a', 'A'], ['b', 'B'], ['c', 'C']]
    CENTERS = ['X', 'Y', 'Z', 'A', 'B', 'C']
    none = [0]
    def __init__(self, name='Singleplayer', demo=False, start=[10, 16], sq_size=40,
                 speed=600, spawn_chance={'normal':1}, lvl={'goal':1000, 'new_goal':'x1.5', 'faster':30, 'maximal':180}, spab=False, randomfall={'spawn_chance':{}, 'count':0},
                 players=1):  # singleplayer preset
        sq = sq_size
        w = start[0]*sq
        h = start[1]*sq
        Canvas.__init__(self, main, width=w, height=h, bg='black')
        self.grid(column=10, row=10, padx=50, pady=10, rowspan=100)

        # canvas parameters
        self.width = w  # width of canvas in pixels
        self.height = h  # height of canvas in pixels
        self.square = sq  # width of a block in pixels; use only: 20, 30, 40, 50
        self.Gscale = self.square/40  # scaling parameter

        # main game parameters
        self.NAME = name
        self.demo = demo
        self.game_go = not demo
        self.game_lost = False
        self.game_wait = False
        self.speed = speed
        self.lvl = 1
        self.lvl_preset = lvl
        self.spawn_chance = spawn_chance
        self.spab_use = spab
        self.randomfall = randomfall

        # player info
        self.players_playable = players
        self.players = players+randomfall['count']
        self.block = []
        self.block_color = []
        self.block_rotateable = []
        self.block_orient = []
        self.rotations = []
        self.block_next = []
        player_lists = [self.block, self.block_color, self.block_rotateable, self.block_orient, self.rotations, self.block_next]
        for x in range(self.players):
            for y in player_lists:
                y.append(None)

        # start
        self.scoreboard = Scoreboard(main, demo=demo, speed=self.speed, players=self.players_playable)
        if not demo:
            self.start_game()
            
    def start_game(self):  # load needed data and start engine
        global gamenum
        gamenum += 1
        self.game_num = gamenum
        self.blockslist = {}
        self.load_blocks()
        self.load_graphics()
        self.create_game()
        self.block_overview = BlockOverview(self.players_playable)
        if self.spab_use:
            self.spab = SpecialAbilities()
            self.animate = Animations()
        self.engine()

    def create_game(self):  # create data list
        data = []
        for rows in range((self.height)//self.square):  # list[rows][columns]
            row = []
            for columns in range(self.width//self.square):
                row.append(0)
            data.append(row)
        self.data = data
        # 0 is None

    def load_blocks(self):  # load block templates
        with open('assets/blocks.txt', 'r') as file:
            count = file.read().count('#')
            file.seek(0)
            start = file.readline().split()
            options = start[1:]
            for z in range(count):
                file.readline()
                for y in range(len(options)):
                    line = file.readline()[:-1]
                    if y == 0:
                        type_ = line
                        if type_ not in self.blockslist:
                            self.blockslist.setdefault(type_, {})
                    elif y == 1:
                        name = line
                        self.blockslist[type_].setdefault(name, {})
                    elif y == 2:
                        size = int(line)
                        block = []
                        for i in range(size):
                            line = file.readline()[:-1]
                            line_list = []
                            for x in line:
                                if x == '0':
                                    x = int(x)
                                line_list.append(x)
                            block.append(deepcopy(line_list))
                        self.blockslist[type_][name].setdefault('config', deepcopy(block))
                    else:
                        self.blockslist[type_][name].setdefault(options[y], line)
        print('Loaded blocks\n', self.blockslist, '\n')

    def load_graphics(self):  # load images
        images = ('bomb', 'shard', 'laser_row')
        self.images = {}
        for image in images:
            self.images.setdefault(image, PhotoImage(file='assets/w'+str(self.square)+'/'+image+'.png'))
        print('Loaded images\n', self.images, '\n')

    def graphics(self):  # graphics engine
        try:
            utilities.show_status()
        except NameError:
            pass
        self.delete('static', 'falling', 'player_show', 'trailing')

        # show trailings
        for player in range(1, self.players_playable+1):
            exists = False
            left_border = len(self.data[0])
            right_border = 0
            for row in range(len(self.data)-1, -1, -1):
                for column in range(len(self.data[0])):
                    if self.data[row][column] in self.PLAYERS[player-1]:
                        exists = True
                        if column <= left_border:
                            left_border = column
                            left_bottom = row
                        if column >= right_border:
                            right_border = column
                            right_bottom = row
                        bottom = row
            if exists:
                self.create_line(left_border*self.square+1, (len(self.data)-left_bottom)*self.square, left_border*self.square+1, self.height, fill='white', width=2, tags='trailing')
                self.create_line((right_border+1)*self.square-1, (len(self.data)-right_bottom)*self.square, (right_border+1)*self.square-1, self.height, fill='white', width=2, tags='trailing')

        # show blocks
        for row in range(len(self.data)):
            y = self.height-(1+row)*self.square
            for column in range(len(self.data[0])):
                x = column*self.square
                if self.data[row][column] not in [0, '#']+self.fall:
                    if self.data[row][column][0] != '@':
                        self.create_rectangle(x, y, x+self.square, y+self.square, fill=self.data[row][column], tag='static')
                    else:
                        self.create_image(x, y, anchor=NW, image=self.images[self.data[row][column][1:]], tags='static')
                if self.data[row][column] in self.fall:
                    for i in range(self.players):
                        if self.data[row][column] in self.PLAYERS[i]:
                            if self.block_color[i][0] != '@':
                                self.create_rectangle(x, y, x+self.square, y+self.square, fill=self.block_color[i], stipple='gray50', tag='falling')
                                if self.data[row][column] == self.PLAYERS[i][1] and i < self.players_playable:
                                    self.create_text(x, y, anchor=NW, text=str(i+1), fill='white', font=('Arial', str(self.square*2//3)), tags='player_show')
                            if self.block_color[i][0] == '@' and self.data[row][column] == self.PLAYERS[i][1]:
                                self.create_image(x, y, anchor=NW, image=self.images[self.block_color[i][1:]], tags='falling')
                                if i < self.players_playable:
                                    self.create_text(x, y, anchor=NW, text=str(i+1), fill='cyan', font=('Arial', str(self.square*2//3)), tags='player_show')
        self.tag_raise('lvlup')

    def del_popup(self, popup='lvlup'):
        self.delete(popup)

    def engine(self):  # time engine, organises fall physics, block spawning
        if gamenum != self.game_num:
            print('Destroying running engine')
            return 0
        if self.game_lost:
            self.scoreboard.after_cancel(self.scoreboard.time_process)
            self.game_go = False
            messagebox.showinfo(message='You lost!')
        if self.game_go and not self.game_lost and not self.game_wait:
            self.lvl_check()
            self.special_mechanics()
            self.delete('pause')
            for player in range(1, self.players+1):
                spawn_block = True
                for row in self.data:
                    for column in row:
                        if column in self.PLAYERS[player-1]:
                            spawn_block = False
                            break
                    if not spawn_block:
                        break
                if spawn_block:
                    self.new_block(player=player)
            for t in range(self.players):
                for player in range(1, self.players+1):
                    self.make_static(player=player)
            self.block_fall()
            self.delete_row()
            self.graphics()
            self.engine_process = self.after(self.speed, self.engine)  # loop engine

    def pause(self):  # pause function
        if not self.demo and not self.game_lost:
            self.game_go = not self.game_go
            if self.game_go:
                self.scoreboard.time_counter()
            else:
                self.scoreboard.after_cancel(self.scoreboard.time_process)
            self.create_text(self.width//2, self.height//2, text='Paused', font=('Arial', 30), fill='white', tags='pause')
            self.engine()

    def lvl_check(self):
        if self.lvl_preset['goal'] <= float(self.scoreboard.score.get()):
            self.lvl += 1
            if self.spab_use:
                ability = choice(self.spab.LIST)
                self.spab.storage[ability].set(str(int(self.spab.storage[ability].get())+1))
            if self.speed > self.lvl_preset['maximal']:
                self.speed -= self.lvl_preset['faster']
                self.scoreboard.speedvar.set(str(self.speed)+' ms')
            self.scoreboard.lvl.set(str(self.lvl))
            if self.lvl_preset['new_goal'][0] == 'x':
                self.lvl_preset['goal'] = self.lvl_preset['goal']*float(self.lvl_preset['new_goal'][1:])
            elif self.lvl_preset['new_goal'][0] == '+':
                self.lvl_preset['goal'] = self.lvl_preset['goal']+float(self.lvl_preset['new_goal'][1:])
            self.create_text(self.width//2, self.height//2, text='LEVEL UP!', font=('Arial', 50), fill='yellow', tags='lvlup')
            self.after(1400, self.del_popup)

    def make_static(self, player=1, force=False):  # check if block should be made static
        if not force:
            makestatic = False
            for r in range(len(self.data)):
                for c in range(len(self.data[0])):
                    x = self.data[r][c]
                    if x in self.PLAYERS[player-1]:
                        if r == 0 or self.data[r-1][c] not in self.fall+[0]:
                            makestatic = True
                            break
                if makestatic:
                    break
        else:
            makestatic = force
        if makestatic:
            for r in range(len(self.data)):
                for c in range(len(self.data[r])):
                    x = self.data[r][c]
                    if x in self.PLAYERS[player-1]:
                        if self.block_color[player-1][0] == '@':
                            if x == self.PLAYERS[player-1][1]:
                                self.data[r][c] = self.block_color[player-1]
                            else:
                                self.data[r][c] = '#'
                        else:
                            self.data[r][c] = self.block_color[player-1]
            if player <= self.players_playable:
                self.scoreboard.add_to(option='Blocks placed', value=1, player=player)
                self.last_placed_block = player
        return makestatic

    def block_fall(self, player='everyone'):  # move remaining blocks down
        if player == 'everyone':
            target = self.fall
        else:
            target = self.PLAYERS[player-1]
        for r in range(len(self.data)):
            for c in range(len(self.data[r])):
                x = self.data[r][c]
                if x in target:
                    self.data[r-1][c] = self.data[r][c]
                    self.data[r][c] = 0
        self.graphics()

    def delete_row(self):  # delete filled rows
        for row in range(len(self.data)):
            full = True
            for column in self.data[row]:
                if column in [0]+self.fall:
                    full = False
            if full:
                del self.data[row]
                new_row = []
                for x in range(self.width//self.square):
                    new_row.append(0)
                self.data.append(new_row)
                self.scoreboard.add_to(option='Score', value=10*(self.width//self.square), player=self.last_placed_block)
                self.scoreboard.add_to(option='Destroyed rows', value=1, player=self.last_placed_block)

    def special_mechanics(self):  # special game mechanics
        for row in range(len(self.data)):
            for column in range(len(self.data[row])):
                if self.data[row][column] == '@bomb':  # bomb, delete all blocks in radius 1
                    game.animate.explosion(x=column, y=row, maxradius=4)
                    self.SA_do(ability='Explode', pos=[column, row], radius=1)
                elif self.data[row][column] == '@shard':  # shard, delete all blocks under the shard
                    game.animate.laser(x=column, y=row, orient=180, color='blue')
                    for r in range(row+1):
                        if self.data[r][column] not in [0]+self.fall:
                            self.data[r][column] = 0
                            self.scoreboard.add_to(option='Score', value=15, player=self.last_placed_block)
                elif self.data[row][column] == '@laser_row':
                    game.animate.laser(x=0, y=row, orient=90)
                    for c in range(len(self.data[0])):
                        if self.data[row][c] not in [0]+self.fall:
                            self.data[row][c] = 0
                            self.scoreboard.add_to(option='Score', value=15, player=self.last_placed_block)
        self.graphics()

    def special_abilities(self, ability):
        if int(self.spab.storage[ability].get()) > 0:
            self.spab.storage[ability].set(int(self.spab.storage[ability].get())-1)
            if ability == 'Orbital strike':
                self.animate.orbital_strike(pos=0)
            elif ability == 'Atom bomb':
                x = randint(0, len(game.data[0])-1)
                y = 0
                for b in range(len(self.data)-1, -1, -1):
                    if self.data[b][x] not in self.fall+[0]:
                        y = b
                        break
                self.animate.atom_bomb(x, y)
            elif ability == 'Skyshift':
                found = False
                for r in range(len(self.data)-1, -1, -1):
                    for c in range(len(self.data[0])):
                        if self.data[r][c] not in self.fall+[0]:
                            self.animate.skyshift(pos=r)
                            found = True
                            break
                    if found:
                        break

    def SA_do(self, ability=None, pos=None, radius=None):
        if ability == 'Orbital strike':
            deleting = []
            for b in range(len(self.data)-1, -1, -1):
                if len(deleting) == 2:
                    break
                if self.data[b][pos] not in self.fall+[0]:
                    deleting.append(b)
            for x in deleting:
                self.data[x][pos] = 0
                self.scoreboard.add_to(option='Score', value=10*(self.width//self.square))
                game.animate.explosion(x=pos, y=x, maxradius=3)
                self.graphics()
        if ability == 'Explode':
            row = pos[1]
            column = pos[0]
            for r in range(-radius, radius+1):
                if row+r>=0 and row+r<len(self.data):
                    for c in range(-radius, radius+1):
                        if column+c>=0 and column+c<len(self.data[0]):
                            if self.data[row+r][column+c] not in [0]+self.fall:
                                self.data[row+r][column+c] = 0
                                self.scoreboard.add_to(option='Score', value=15, player=self.last_placed_block)
            self.graphics()
        if ability == 'Del Row':
            for c in range(len(self.data[0])):
                if self.data[pos][c] not in self.fall+[0]:
                    self.data[pos][c] = 0
                    self.scoreboard.add_to(option='Score', value=10*(self.width//self.square))
            self.graphics()

    def move_block(self, direction, player=1):  # move falling block left or right
        if direction == 'left':
            d = -1
            iterator = range(0, len(self.data[0]), -d)
        else:
            d = 1
            iterator = range(len(self.data[0])-1, -1, -d)
        
        # check if can be moved left or right
        move = True
        for r in range(len(self.data)):
            for c in range(len(self.data[r])):
                x = self.data[r][c]
                if x in self.PLAYERS[player-1]:
                    if (c == 0 and d == -1 or c == len(self.data[r])-1 and d == 1) or (self.data[r][c+d] != 0 and self.data[r][c+d] not in self.PLAYERS[player-1]):
                        move = False
                        break
            if not move:
                break
        # move block in data list
        if move:
            for r in range(len(self.data)):
                for c in iterator:
                    x = self.data[r][c]
                    if x in self.PLAYERS[player-1]:
                        self.data[r][c+d] = self.data[r][c]
                        self.data[r][c] = 0
        self.graphics()

    def rotate_block(self, rotate, player=1):  # rotate function
        if not eval(self.block_rotateable[player-1]):
            return 0
        # check if block can be rotated
        orient = self.block_orient[player-1]+rotate
        if orient == 360:
            orient = 0
        if orient == -90:
            orient = 270
        rotation = True

        if eval(self.block_rotateable[player-1]):
            # find scanning point
            stop = False
            for row in range(len(self.data)):
                for column in range(len(self.data[0])):
                    if self.data[row][column] == self.PLAYERS[player-1][1]:
                        scan_start = (row-len(self.block[player-1])//2, column-len(self.block[player-1])//2)
                        stop = True
                        break
                if stop:
                    break

            # check rotation posibility
            try:
                for row in range(len(self.block[player-1])):
                    for column in range(len(self.block[player-1])):
                        if self.rotations[player-1][orient][len(self.block[player-1])-1-row][column] != 0:
                            if scan_start[0]+row < 0 or scan_start[0]+row >= len(self.data) or scan_start[1]+column < 0 or scan_start[1]+column >= len(self.data[0]):
                                rotation = False
                                break
                            if self.data[scan_start[0]+row][scan_start[1]+column] not in [0]+self.PLAYERS[player-1]:
                                rotation = False
                                break
                    if not rotation:
                        break

                # rotate block
                if rotation:
                    self.block_orient[player-1] = orient
                    for row in range(len(self.block[player-1])):
                        for column in range(len(self.block[player-1])):
                            part = self.rotations[player-1][orient][len(self.block[player-1])-1-row][column]
                            if part == 'x':
                                part = self.PLAYERS[player-1][0]
                            elif part == 'X':
                                part = self.PLAYERS[player-1][1]
                            try:
                                if self.data[scan_start[0]+row][scan_start[1]+column] in [0]+self.PLAYERS[player-1]:
                                        self.data[scan_start[0]+row][scan_start[1]+column] = part
                            except IndexError:
                                pass
            except UnboundLocalError:
                pass
        self.graphics()

    def one_down(self, player=1):  # move block one rown down
        for r in range(len(self.data)):
            for c in range(len(self.data[0])):
                x = self.data[r][c]
                if x in self.PLAYERS[player-1] and r != 0:
                    for part in self.PLAYERS:
                        if self.data[r-1][c] in part and x not in part:
                            return 0
        if not self.make_static(player=player):
            self.block_fall(player=player)
            self.scoreboard.add_to(option='Score', value=2, player=player)

    def put_down(self, player=1):  # let the block fall down immediately
        free = True

        # check if there are not two falling blocks above themselves
        left_border = len(self.data[0])
        right_border = 0
        try:
            for row in range(len(self.data)-1, -1, -1):
                for column in range(len(self.data[0])):
                    if self.data[row][column] in self.PLAYERS[player-1]:
                        if column < left_border:
                            left_border = column
                        if column > right_border:
                            right_border = column
                        bottom = row
            for row in range(bottom+1):
                for column in range(left_border, right_border+1):
                    if self.data[row][column] in self.fall and self.data[row][column] not in self.PLAYERS[player-1]:
                        free = False
                        break
                if not free:
                    break

            # fall
            while free:
                # check if block can fall one row down
                fall = True
                for r in range(len(self.data)):
                    for c in range(len(self.data[r])):
                        x = self.data[r][c]
                        if x in self.PLAYERS[player-1]:
                            if r == 0 or self.data[r-1][c] not in self.fall+[0]:
                                fall = False
                                break
                    if not fall:
                        break
                if fall:  # move block one row down
                    self.scoreboard.add_to(option='Score', value=5, player=player)  # add score
                    for r in range(len(self.data)):
                        for c in range(len(self.data[r])):
                            x = self.data[r][c]
                            if x in self.PLAYERS[player-1]:
                                self.data[r-1][c] = self.data[r][c]
                                self.data[r][c] = 0
                else:  # make block static
                    free = False
                    self.make_static(player=player, force=True)
                    self.scoreboard.add_to(option='Quick put-down', value=1, player=player)
        except UnboundLocalError:
            pass
        self.graphics()

    def new_block(self, player=1):  # spawn new block
        if self.block_next[player-1] == None:
            type_ = self.random_type(player=player)
            self.block_next[player-1] = [type_, self.random_select_from_type(type_=type_)]
        self.block[player-1] = self.blockslist[self.block_next[player-1][0]][self.block_next[player-1][1]]['config']
        self.block_color[player-1] = self.blockslist[self.block_next[player-1][0]][self.block_next[player-1][1]]['color']
        self.block_rotateable[player-1] = self.blockslist[self.block_next[player-1][0]][self.block_next[player-1][1]]['rotateable']
        self.block_orient[player-1] = 0
        self.block_next[player-1] = None
        type_ = self.random_type(player=player)
        self.block_next[player-1] = [type_, self.random_select_from_type(type_=type_)]
        self.block_overview.change(player=player, block=self.blockslist[self.block_next[player-1][0]][self.block_next[player-1][1]])
        self.create_block_rotations(player=player)
        self.insert_block(player=player)

    def random_type(self, player=1):  # select randomly from types (use self.spawn_chance to customize)
        num = random()
        if player <= self.players_playable:
            for t in iter(self.spawn_chance):
                if num < self.spawn_chance[t]:
                    return t
                else:
                    num -= self.spawn_chance[t]
        else:
            for t in iter(self.randomfall['spawn_chance']):
                if num < self.randomfall['spawn_chance'][t]:
                    return t
                else:
                    num -= self.randomfall['spawn_chance'][t]

    def random_select_from_type(self, type_='normal'):  # select randomly from blocks of a given type
        blocks_select = []
        for x in iter(self.blockslist[type_]):
            blocks_select.append(x)
        return choice(blocks_select)

    def insert_block(self, player=1):  # insert block
        global list_width, skip_rows, spoint_rows

        # find out from which row in block template start with
        list_width = len(self.block[player-1])
        skip_rows = 0
        spoint_rows = len(self.data)-1
        for row in self.block[player-1]:
            empty = True
            for column in row:
                if column != 0:
                    empty = False
                    break
            if empty:
                skip_rows += 1
                spoint_rows -= 1
            else:
                break
                
        # set spawnpoint
        columns = []
        for x in range(self.width//self.square):
            columns.append(x)
        regions = [] # divide all positions in number of players regions
        for x in range(self.players):
            reg = []
            for t in range(self.width//self.square//self.players):
                reg.append(columns.pop(0))
            regions.append(reg)
        try:
            for x in columns:
                regions[-1].append(x)
        except:
            pass
        for r in range(len(self.data)):
            for c in range(len(self.data[0])):
                if self.data[r][c] in self.CENTERS[:self.players_playable]:
                    for reg in range(len(regions)):
                        if c in regions[reg]:
                            regions.append(regions.pop(reg))
                            break
        positions = []
        for reg in regions:
            shuffle(reg)
            for x in reg:
                positions.append(x)
        found_pos = False
        for pos in positions:
            if self.insert_possibility(pos, player=player):
                found_pos = True
                spoint_column = pos
                break
        
        # insert block
        if found_pos:
            for row in range(skip_rows, list_width):
                for column in range(list_width):
                    part = self.block[player-1][row][column]
                    if part != 0:
                        if part == 'X':
                            part = self.PLAYERS[player-1][1]
                        if part == 'x':
                            part = self.PLAYERS[player-1][0]
                        if self.data[spoint_rows+skip_rows-row][spoint_column+column] != 0:
                            pass
                        self.data[spoint_rows+skip_rows-row][spoint_column+column] = part
        else:
            self.game_lost = True
        self.graphics()

    def insert_possibility(self, position, player=1):  # check if block can be inserted in given position
        global list_width, skip_rows, spoint_rows
        possible = True
        for row in range(list_width-1, skip_rows-1, -1):
            for column in range(list_width):
                part = self.block[player-1][row][column]
                if part != 0:
                    try:
                        if self.data[spoint_rows-row][position+column] != 0:
                            possible = False
                            break
                    except IndexError:
                        possible = False
                        break
            if not possible:
                break
        return possible

    def create_block_rotations(self, player=1):  # create data objects of a block in all 4 orientations
        self.rotations[player-1] = {0:deepcopy(self.block[player-1])}
        last = deepcopy(self.rotations[player-1][0])
        for rotation in range(90, 360, 90):
            new = deepcopy(last)
            for row in range(len(self.block[player-1])):
                for column in range(len(self.block[player-1])):
                    new[row][column] = last[len(self.block[player-1])-1-column][row]
            self.rotations[player-1].setdefault(rotation, deepcopy(new))
            last = deepcopy(new)

    def faster(self):
        if self.speed > 100:
            self.speed -= 100
        self.scoreboard.speedvar.set(str(self.speed)+' ms')

    def slower(self):
        if self.speed < 3000:
            self.speed += 100
        self.scoreboard.speedvar.set(str(self.speed)+' ms')
        
    def __del__(self):  # important procedures when ending game
        try:
            print('Ending engine #', self.engine_process)
            self.after_cancel(self.engine_process)
            self.scoreboard.__del__()
            self.block_overview.__del__()
            if self.spab_use:
                self.spab.__del__()
        except AttributeError:
            pass


class Scoreboard(Frame):  # scoreboard frame, shows score and time
    def __init__(self, master, demo=False, speed='N/A', players=1):
        self.bg = 'green'
        self.fg = 'white'
        self.font = ('Arial Black', '15')
        Frame.__init__(self, master, bg=self.bg)
        self.grid(column=50, row=10, rowspan=40, columnspan=10, padx=4, sticky=N)
        Label(self, text='Scoreboard', font=('Arial Black', '24'), fg=self.fg, bg=self.bg).grid(column=50, row=15, columnspan=2)  # scoreboard title

        # level label
        Label(self, text='Level:', font=self.font, fg=self.fg, bg=self.bg).grid(column=50, row=20, sticky=W)
        self.lvl = StringVar(value=1)
        if demo:
            self.lvl.set('Demo')
        Label(self, textvariable=self.lvl, font=self.font, fg=self.fg, bg=self.bg).grid(column=51, row=20, sticky=E)

        # score label
        Label(self, text='Score:', font=self.font, fg=self.fg, bg=self.bg).grid(column=50, row=22, sticky=W)
        self.score = StringVar(value=0)
        Label(self, textvariable=self.score, font=self.font, fg=self.fg, bg=self.bg).grid(column=51, row=22, sticky=E)

        # time label
        Label(self, text='Time:', font=self.font, fg=self.fg, bg=self.bg).grid(column=50, row=24, sticky=W)
        self.timevar = StringVar(value='00:00')
        Label(self, textvariable=self.timevar, font=self.font, fg=self.fg, bg=self.bg).grid(column=51, row=24, sticky=E)
        self.time = [0, 0]  # secs, mins
        if not demo:
            self.time_counter()

        # speed label
        Label(self, text='Speed:', font=self.font, fg=self.fg, bg=self.bg).grid(column=50, row=26, sticky=W)
        self.speedvar = StringVar(value=str(speed)+' ms')
        if demo:
            self.speedvar.set('0 ms')
        Label(self, textvariable=self.speedvar, font=self.font, fg=self.fg, bg=self.bg).grid(column=51, row=26, sticky=E)

        # chart for more players
        self.chart = Frame(self, bg='purple')
        self.chart.grid(column=50, row=30, columnspan=2, sticky=(W, E))
        self.chartfont=('Arial', 12)
        self.stats = {'Score':[], 'Blocks placed':[], 'Destroyed rows':[], 'Quick put-down':[]}
        for x in range(players):
            Label(self.chart, text='Player '+str(x+1), font=self.chartfont, fg=self.fg, bg='purple').grid(column=51+x, row=30)
        i = 1
        for stat in iter(self.stats):
            Label(self.chart, text=stat, font=self.chartfont, fg=self.fg, bg='purple').grid(column=50, row=30+i, sticky=W)
            for p in range(players):
                self.stats[stat].append(StringVar(value=0))
                Label(self.chart, textvariable=self.stats[stat][p], font=self.chartfont, fg=self.fg, bg='purple').grid(column=51+p, row=30+i, sticky=E)
            i += 1

    def add_score(self, value=0):  # add and show score
        # score rules:
        # - when quickly putting down a block, 5 points for every row
        # - 2 points for pushing block one row down
        # - when a row is filled, 10 points for every block in the row
        self.score.set(str(int(self.score.get())+value))

    def add_to(self, option, value=0, player=1):  # add value to option
        self.stats[option][player-1].set(int(self.stats[option][player-1].get())+value)
        if option == 'Score':
            self.add_score(value=value)

    def time_counter(self):  # count time
        self.time[0] += 1
        if self.time[0] == 60:
            self.time[0] = 0
            self.time[1] += 1
        t = ''
        for x in self.time[::-1]:
            x = str(x)
            if len(x) < 2:
                t += '0'+x
            else:
                t += x
            t += ':'
        self.timevar.set(t[:-1])
        self.time_process = self.after(1000, self.time_counter)

    def __del__(self):
        try:
            self.after_cancel(self.time_process)
            for x in self.winfo_children():
                x.grid_forget()
        except TclError:
            pass
        except AttributeError:
            pass


class BlockOverview(Frame):  # show blocks that will players get next
    def __init__(self, players):
        Frame.__init__(self, main)
        self.grid(column=50, row=50)
        self.views = []
        for view in range(players):
            self.views.append(Canvas(self, width=100, height=100, bg='black'))
            self.views[view].grid(column=10+view, row=50)
            Label(self, text='Player '+str(view+1)).grid(column=10+view, row=51)

    def change(self, block, player=1):  # show next block
        if player > game.players_playable:
            return 0
        self.views[player-1].delete('next')
        dimension = 100//len(block['config'])
        if block['color'][0] != '@':
            for row in range(len(block['config'])):
                for column in range(len(block['config'])):
                    if block['config'][row][column] != 0:
                        self.views[player-1].create_rectangle(column*dimension, row*dimension, (column+1)*dimension, (row+1)*dimension, fill=block['color'], tags='next')
        else:
            try:
                self.views[player-1].create_image(50, 50, image=game.images[block['color'][1:]], tags='next')
            except:
                print('Startup Error')
                print(self.views)
                print('block', block)
                try:
                    print('Starting again')
                    print(game.images)
                except:
                    game.load_graphics()

    def __del__(self):
        try:
            for view in self.winfo_children():
                view.grid_forget()
            self.grid_forget()
        except TclError:
            pass


class SpecialAbilities(Frame):  # frame showing remaining charges of the abilities
    def __init__(self):
        Frame.__init__(self, main)
        self.grid(column=50, row=60)
        Label(self, text='Special Abilities', font=('Arial', 20)).grid(column=50, row=60, columnspan=2)
        self.LIST = ['Orbital strike', 'Atom bomb', 'Skyshift']
        self.storage = {}
        for ability in self.LIST:
            self.storage.setdefault(ability, StringVar(value=0))
        i = 0
        for ability in iter(self.storage):
            Label(self, text=ability).grid(column=50, row=64+i)
            Label(self, textvariable=self.storage[ability]).grid(column=51, row=64+i)
            i += 1
        
    def __del__(self):
        try:
            for part in self.winfo_children():
                part.grid_forget()
            self.grid_forget()
        except TclError:
            pass


class Animations(Frame):  # code processing animations
    def __init__(self):
        Frame.__init__(self, main)

    def explosion(self, x, y, maxradius, r=0):
        if r < maxradius:
            game.create_oval((x-r)*game.square, game.height-(y+1+r)*game.square, (x+1+r)*game.square, game.height-(y-r)*game.square, outline='red', width=6, fill='orange', stipple='gray25',
                             tags='explosion')
            self.after(70, lambda: self.explosion(x=x, y=y, maxradius=maxradius, r=r+1))
            self.after(50, lambda: game.delete('explosion'))

    def laser(self, x, y, orient, phase=4, color='red'):
        if phase >= 0:
            if orient == 0:
                pass
            if orient == 90:
                game.create_rectangle(x*game.square, game.height-(y+1)*game.square+phase*(game.square//10), game.width, game.height-y*game.square-phase*(game.square//10), fill=color,
                                      stipple='gray75', tags='laser')
            if orient == 180:
                game.create_rectangle(x*game.square+phase*(game.square//10), game.height-(y+1)*game.square, (x+1)*game.square-phase*(game.square//10), game.height, fill=color,
                                      stipple='gray75', tags='laser')
            if orient == 270:
                pass
            self.after(40, lambda: self.laser(x=x, y=y, orient=orient, phase=phase-1, color=color))
            self.after(30, lambda: game.delete('laser'))
        
    def orbital_strike(self, pos):
        if pos < len(game.data[0]):
            game.create_rectangle(pos*game.square, 0, (pos+1)*game.square, game.height, fill='white', tags='orbital_strike')
            game.create_rectangle(pos*game.square+game.square//4, 0, (pos+1)*game.square-game.square//4, game.height, fill='cyan', stipple='gray50', tags='orbital_strike')
            game.SA_do(ability='Orbital strike', pos=pos)
            self.after(100, lambda: self.orbital_strike(pos=pos+1))
        self.after(80, lambda: game.delete('orbital_strike'))

    def atom_bomb(self, x, y):
        self.laser(x, len(game.data)-1, orient=180)
        self.after(50, lambda: self.laser(x-1, len(game.data)-1, orient=180))
        self.after(50, lambda: self.laser(x+1, len(game.data)-1, orient=180))
        self.after(100, lambda: self.laser(x, len(game.data)-1, orient=180))
        self.after(300, lambda: self.explosion(x=x, y=y, maxradius=9))
        self.after(300, lambda: game.SA_do(ability='Explode', pos=[x, y], radius=3))

    def skyshift(self, pos):
        start = 0
        for i in range(pos, pos-4, -1):
            self.after(start*50+1, lambda p=i: self.laser(0, p, orient=90, color='green'))
            self.after(start*50+21, lambda p=i: game.SA_do(ability='Del Row', pos=p))
            start += 1


class Keybindings():  # class for organizing keybindings
    def __init__(self):
        self.active = None
        self.data = {}
        self.default = {'player1': {'left': 65, 'right': 68, 'rotate_clockwise': 69, 'rotate_counterclockwise': 81, 'put_down': 83, 'one_down': 87,
                                    'orbital_strike': 82, 'atom_bomb': 84, 'skyshift': 70},
                        'player2': {'left': 52, 'right': 54, 'rotate_clockwise': 57, 'rotate_counterclockwise': 55, 'put_down': 53, 'one_down': 56},
                        'player3': {'left': 65361, 'right': 65363, 'rotate_clockwise': 65506, 'rotate_counterclockwise': 65508, 'put_down': 65364, 'one_down': 65362},
                        'special': {'pause': 32, 'faster': 43, 'slower': 45, 'singleplayer': 65470, 'adventure': 65471, 'quick': 65472, 'destruction': 65473, 'coop': 65474, 'triple_the_trouble': 65475, 'not_enough_space': 65476}}
        with open('keybindings.txt', mode='r') as file:  # read file
            try:
                while True:
                    line = file.readline()
                    if line == '':
                        break
                    elif line[0] == '@':
                        self.data.setdefault(line[1:-1], {})
                        loading = self.data[line[1:-1]]
                    else:
                        parts = line.split('=')
                        opt = parts[0]
                        key = parts[1]
                        loading.setdefault(opt, int(key))
            except:
                print('Error has occured.\nLoading default.')
                self.data = self.default
        with open('assets/key_identifier.txt', 'r') as file:  # load dictionary with keysym_num:Key_symbol
            self.identifier = eval(file.read())

    def open_window(self):  # open window for customizing
        self.window = Toplevel(tk, bg='green')
        self.window.title('Keybindings')
        self.create_tabs()
        Button(self.window, text='Close', command=self.window.destroy).grid(column=0, row=500, sticky=W)
        Button(self.window, text='Reset to defaults', command=self.reset).grid(column=1, row=500, sticky=E)
        self.window.bind('<KeyPress>', self.change_keybind)
        self.window.bind('<Destroy>', self.window_destroy)

    def create_tabs(self):  # create individual tabs
        self.mainframe = ttk.Notebook(self.window)
        self.mainframe.grid(column=0, row=1, columnspan=2)
        self.tabs = []
        self.tabkeys = {}
        try:
            for tab in iter(self.data):
                self.tabs.append(Frame(self.mainframe))
                self.tabkeys.setdefault(tab, {})
                building = self.tabs[-1]
                r = 1
                for x in iter(self.data[tab]):
                    self.tabkeys[tab].setdefault(x, KeySet(building, tab, x, r))
                    r += 1
                self.mainframe.add(self.tabs[-1], text=tab)
        except KeyError:
            pass

    def change_keybind(self, event):  # change keybind if some button is active
        if self.active == None:
            return 0
        key = event.keysym_num
        if chr(key) in ascii_lowercase:
            key = ord(chr(key).capitalize())
        self.tabkeys[self.active[0]][self.active[1]].set_confirmed(key=key)
        if key != 65307:
            self.data[self.active[0]][self.active[1]] = key
        self.rewrite()
        self.active = None

    def rewrite(self):  # write changes to the data file
        with open('keybindings.txt', 'r+') as file:
            for group in iter(self.data):
                file.write('@'+group+'\n')
                for key in iter(self.data[group]):
                    file.write(key+'='+str(self.data[group][key])+'\n')
            file.truncate()
        

    def reset(self):  # reset everything to default
        self.data = self.default
        self.rewrite()
        for tab in iter(self.tabkeys):
            for k in iter(self.tabkeys[tab]):
                self.tabkeys[tab][k].show(key=self.data[tab][k])

    def window_destroy(self, event):
        self.active = None
        

class KeySet():  # functional button for customizing keybindings
    def __init__(self, master, overkey, key, row, column=1):
        self.path = [overkey, key]
        self.label = Label(master, text=key.capitalize().replace('_', ' '))
        self.label.grid(column=column, row=row, sticky=W)
        self.keyvar = StringVar()
        self.button = Button(master, textvariable=self.keyvar, command=self.set, width=7)
        self.button.grid(column=column+1, row=row, sticky=E)
        self.show()

    def show(self, key='yourself'):  # show key symbol on the button
        if key == 'yourself':
            key = int(keys[self.path[0]][self.path[1]])
        if key in keybindings.identifier:
            key = keybindings.identifier[key]
        elif chr(key) in ascii_letters+digits:
            key = chr(key)
        self.keyvar.set(key)
        
    def set(self):  # set this button active and wait for key input
        if keybindings.active != None:
            keybindings.tabkeys[keybindings.active[0]][keybindings.active[1]].show(keybindings.data[keybindings.active[0]][keybindings.active[1]])
        keybindings.active = deepcopy(self.path)
        self.keyvar.set('?')

    def set_confirmed(self, key):  # execute when a key was pressed
        if key == 65307:  # if key is Esc/65307 don't change
            self.show(key=keys[self.path[0]][self.path[1]])
        else:  # change key
            self.show(key=key)


class AboutWindow(Toplevel):
    def __init__(self):
        Toplevel.__init__(self, master=tk)
        self.text = Text(self, width=80, height=18, wrap='word')
        self.text.insert(1.0, """Blockalypse Alpha
Tetris-like game which comes with new innovative mechanics and gamemodes:
  - co-op modes (2 or 3 players play together on a single computer)
  - super quick gamemode which tests your reflexes
  - adventure and destruction mode introduce new action blocks and special abilities
  
Check keybindings in Options and customize them to your preferences.

Author: Michal Krulich
License: GNU GPL v3.0
Github repository: https://github.com/MichaelTheSynthCat/Blockalypse""")
        self.text.grid()
        self.text['state'] = DISABLED


class Utilities(Toplevel):  # utilities
    def __init__(self, master):
        Toplevel.__init__(self, master, bg='yellow')
        self.geometry('+1000+200')
        Label(self, text='Developer Console', font=('25')).grid(column=50, row=10, pady=5)
        
        # show data list in text
        Button(self, text='Show', command=self.show_status).grid(column=50, row=15)
        self.show_text = Text(self, width=20, height=20)
        self.show_text.grid(column=50, row=20)
        
        # spawn or delete selected block
        f = Frame(self, bg='yellow')
        f.grid(column=50, row=25)
        Button(f, text='Spawn', command=self.spawn_square).grid(column=50, row=25)
        Button(f, text='Delete', command=self.delete_square).grid(column=51, row=25)
        f = Frame(self, bg='yellow')
        f.grid(column=50, row=26, columnspan=4)
        Label(f, text='R:').grid(column=50, row=26)
        self.row_select = StringVar(value='1')
        Spinbox(f, textvariable=self.row_select, from_=1, to=len(game.data), width=3).grid(column=51, row=26)
        Label(f, text='C:').grid(column=52, row=26)
        self.column_select = StringVar(value='1')
        Spinbox(f, textvariable=self.column_select, from_=1, to=len(game.data[0]), width=3).grid(column=53, row=26)

        tk.focus()

    def show_status(self):
        data = game.data.copy()
        self.show_text.delete(0.0, 'end')
        for row in data[::-1]:
            for column in row:
                if column in game.fall+[0]:
                    self.show_text.insert('end', str(column)+' ')
                else:
                    self.show_text.insert('end', str(1)+' ')
            self.show_text.insert('end', '\n')

    def spawn_square(self):
        game.data[int(self.row_select.get())-1][int(self.column_select.get())-1] = 1
        game.graphics()

    def delete_square(self):
        game.data[int(self.row_select.get())-1][int(self.column_select.get())-1] = 0
        game.graphics()


if __name__ == '__main__':
    version = 'alpha'
    gamenum = 0
    tk = Tk()  # create main window
    tk.title('Blockalypse')
    tk.option_add('*tearOff', FALSE)
    keybindings = Keybindings()  # load keybindings
    keys = keybindings.data  #shortcut
    main = App(tk)  # create main frame
    game = Game(demo=True)  # show demo
    main.create_menus()
    tk.mainloop()
