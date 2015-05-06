import sys, pygame, re
from pygame.locals import *


pygame.init()
screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption("CHECKERS: Purple's Turn")

black_square = pygame.image.load("black_square.png").convert()
white_square = pygame.image.load("white_square.png").convert()
selected_square = pygame.image.load("sel_square.png").convert()
red_piece = pygame.image.load("red_piece.png").convert()
purple_piece = pygame.image.load("purple_piece.png").convert()
selected_piece = pygame.image.load("sel_piece.png").convert()
alt_selected_piece = pygame.image.load("sel_piece_alt.png").convert()
king_piece = pygame.image.load("king.png").convert()


class Piece:
	def __init__(self, x_pos, y_pos):
		self.x = x_pos
		self.y = y_pos
		self.is_king = False
				
	def get_pos(self):
		return (self.x, self.y)
	
	def get_real_pos(self):
		return (self.x*64, self.y*64)
	
	def set_pos(self, x_pos, y_pos):
		self.x = x_pos
		self.y = y_pos	
	
	def get_king(self):
		return self.is_king
	
	def set_king(self, k=True):
		self.is_king = k


def identify_square(sx, sy, red_list, purple_list):
	for p in purple_list:
		x, y = p.get_pos()
		if (x, y) == (sx, sy):
			return "purple"
	for r in red_list:
		x, y = r.get_pos()
		if (x, y) == (sx, sy):
			return "red"
	return "empty"

def update_position(old_x, old_y, new_x, new_y, team):
	for piece in team:
		x, y = piece.get_pos() 
		if (x, y) == (old_x, old_y):
			piece.set_pos(new_x, new_y)
		
def capture_piece(ix, iy, team):
	for piece in team:
		x, y = piece.get_pos()
		if (x, y) == (ix, iy):
			team.remove(piece)

def check_king(ix, iy, team):
	for piece in team:
		x, y = piece.get_pos()
		if (x, y) == (ix, iy):
			return piece.get_king()
			
def make_king(ix, iy, team):
	for piece in team:
		x, y = piece.get_pos()
		if (x, y) == (ix, iy):
			piece.set_king()

#draw board
board = pygame.Surface((512, 512))
next_square = -1
for y in range(0, 512, 64):
	for x in range(0, 512, 64):
		if next_square == -1:
			board.blit(black_square, (x, y))
		else:
			board.blit(white_square, (x, y))
		next_square *= -1
	next_square *= -1

#make pieces
red_team = []
purple_team = []

red_team.extend([Piece(0,0), Piece(2,0), Piece(4,0), Piece(6,0),
				Piece(1,1), Piece(3,1), Piece(5,1), Piece(7,1),
				Piece(0,2), Piece(2,2), Piece(4,2), Piece(6,2)])

purple_team.extend([Piece(1,5), Piece(3,5), Piece(5,5), Piece(7,5),
					Piece(0,6), Piece(2,6), Piece(4,6), Piece(6,6),
					Piece(1,7), Piece(3,7), Piece(5,7), Piece(7,7)])
"""
red_team.extend([Piece(1,1)])
purple_team.extend([Piece(2,2)])
"""


def draw(bkgd, red_list, purple_list):
	temp = pygame.Surface((512, 512))
	temp.blit(bkgd, (0,0))
	for r in red_list:
		x, y = r.get_real_pos()
		temp.blit(red_piece, (x,y))
		if r.get_king():
			temp.blit(king_piece, (x,y))

	for p in purple_list:
		x, y = p.get_real_pos()
		temp.blit(purple_piece, (x,y))	
		if p.get_king():
			temp.blit(king_piece, (x,y))
	return temp

screen.blit(draw(board, red_team, purple_team), (0,0))
pygame.display.update()

selected = []
turn = "purple"
valid = False
directions = {"purple":-1,"red":1}
done = False
step = 0
is_kinged = False

print turn + "'s turn:"

while 1:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEBUTTONDOWN:
			if event.button == 1:
				real_x, real_y = event.pos
				
				sel_x, sel_y = real_x/64, real_y/64 
				
				square_type = identify_square(sel_x, sel_y, red_team, purple_team)
				
				if valid and sel_x == selected[-1][0] and sel_y == selected[-1][1]:
					
					
						
					if turn == "purple":
						for i in selected:
							if i[2] == "red":
								capture_piece(i[0],i[1], red_team)
						if is_kinged:
							make_king(selected[0][0], selected[0][1], purple_team)
							print "KINGED"
						update_position(selected[0][0], selected[0][1], selected[-1][0], selected[-1][1], purple_team)
						turn = "red"
					else:
						for i in selected:
							if i[2] == "purple":
								capture_piece(i[0],i[1], purple_team)
						if is_kinged:
							make_king(selected[0][0], selected[0][1], red_team)
							print "KINGED!"
						turn = "purple"
						update_position(selected[0][0], selected[0][1], selected[-1][0], selected[-1][1], red_team)
					print turn + "'s turn:"
					pygame.display.set_caption("CHECKERS: %s's Turn" %turn.capitalize()) 
					valid = False
					done = False
					is_kinged = False
					step = 0
					selected = []
					screen.blit(draw(board, red_team, purple_team), (0,0))
					pygame.display.update()
					
					if len(red_team) == 0:
						print "PURPLE WINS!"
						break
					elif len(purple_team) == 0:
						print "RED WINS!"
						break
				
				
				if done:
					print "You've already selected a move."
					continue
				
				if not selected:
					if square_type != turn:
						print "Select one of your own pieces to move"
					else:
						print "Selected " + str(sel_x) + "," + str(sel_y)
						if (turn == "red" and check_king(sel_x, sel_y, red_team)) or (turn == "purple" and check_king(sel_x, sel_y, purple_team)):
							print "Selected a king!"
							is_kinged = True
							
						selected.append((sel_x, sel_y, square_type))
						screen.blit(selected_piece, (sel_x*64, sel_y*64))
						pygame.display.update(pygame.Rect(sel_x*64, sel_y*64, 64, 64))
				else:
					if square_type == turn:
						print "You already have a piece there."
					if square_type == "empty":
						print "Trying to move Piece at %d,%d to square %d,%d" %(selected[0][0], selected[0][1], sel_x, sel_y)
						
						
						if abs(sel_x - selected[0][0]) == 1:
							if (sel_y - selected[0][1] == directions[turn]) or (is_kinged and (sel_y - selected[0][1] == -directions[turn])):
								selected.append((sel_x, sel_y, square_type))
								screen.blit(selected_square, (sel_x*64, sel_y*64))
								pygame.display.update(pygame.Rect(sel_x*64, sel_y*64, 64, 64))
								print "Valid Move"
								valid = True
								done = True
								if (turn == "red" and sel_y == 7) or (turn == "purple" and sel_y == 0):
										is_kinged = True
								
						elif (sel_y - selected[step][1] == 2 * directions[turn]) or (is_kinged and (sel_y - selected[step][1] == -2 * directions[turn])):
							if abs(sel_x - selected[step][0]) == 2:
								jx = (sel_x + selected[step][0])/2
								jy = (sel_y + selected[step][1])/2
								jumped_type = identify_square(jx, jy, red_team, purple_team) 
								if jumped_type != "empty" and jumped_type != turn:
									selected.append((jx, jy, jumped_type))
									selected.append((sel_x, sel_y, square_type))
									screen.blit(alt_selected_piece, (jx*64, jy*64))
									pygame.display.update(pygame.Rect(jx*64, jy*64, 64, 64))
									screen.blit(selected_square, (sel_x*64, sel_y*64))
									pygame.display.update(pygame.Rect(sel_x*64, sel_y*64, 64, 64))
									step += 2
									print "Valid Capture"
									valid = True
									if (turn == "red" and sel_y == 7) or (turn == "purple" and sel_y == 0):
										is_kinged = True
						if valid == False:
							print "Illegal move."	
					
					
					
				
				
			elif event.button == 3:
				selected = []
				screen.blit(draw(board, red_team, purple_team), (0,0))
				pygame.display.update()
				done = False
				step = 0
				valid = False
				is_kinged = False
	
	
	
		
		
				
				
					
			

	
	
