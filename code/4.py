import pygame
import random

pygame.init()

window_size = [800, 600]
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

cam_x = 0
cam_y = 0

steps_per_frame = 4

def collision(rect1, rect2):
	x1, y1, w1, h1 = rect1.x, rect1.y, rect1.w, rect1.h
	x2, y2, w2, h2 = rect2.x, rect2.y, rect2.w, rect2.h

	return (x1+w1 > x2 and x1 < x2+w2) and (y1+h1 > y2 and y1 < y2+h2)

class Wall:
	def __init__(self, x, y, w, h):
		self.x, self.y = x, y
		self.w, self.h = w, h

	def render(self):
		pygame.draw.rect(screen, (255, 0, 0), [self.x - cam_x, self.y - cam_y, self.w, self.h], 1)

def rect_in_rect(x1, y1, w1, h1, x2, y2, w2, h2):
	return (x1+w1 > x2 and x1 < x2+w2) and (y1+h1 > y2 and y1 < y2+h2)

class Rect:
	def __init__(self, x, y, w, h, mass=1):
		self.x, self.y = x, y
		self.w, self.h = w, h
		self.vx, self.vy = 0, 0
		self.mass = mass

	def update(self, dt=1):
		self.vy += 0.5*dt

		self.vx *= 0.97**dt
		self.vy *= 0.97**dt

		
		if self.vx > 0:
			collisions = []
			for wall in walls:
				if rect_in_rect(*[self.x, self.y, self.w+self.vx*dt, self.h], *[wall.x, wall.y, wall.w, wall.h]):
					collisions.append(wall)
			if len(collisions) > 0:
				wall = min(collisions, key=lambda a: a.x)
				self.x = wall.x - self.w
				self.vx = 0
			else:
				self.x += self.vx*dt
		
		else:
			collisions = []
			for wall in walls:
				if rect_in_rect(*[self.x+self.vx*dt, self.y, self.w-self.vx*dt, self.h], *[wall.x, wall.y, wall.w, wall.h]):
					collisions.append(wall)
			if len(collisions) > 0:
				wall = max(collisions, key=lambda a: a.x)
				self.x = wall.x + wall.w
				self.vx = 0
			else:
				self.x += self.vx*dt



		
		if self.vy > 0:
			collisions = []
			for wall in walls:
				if rect_in_rect(*[self.x, self.y, self.w, self.h+self.vy*dt], *[wall.x, wall.y, wall.w, wall.h]):
					collisions.append(wall)
			if len(collisions) > 0:
				wall = min(collisions, key=lambda a: a.y)
				self.y = wall.y - self.h
				self.vy = 0
			else:
				self.y += self.vy*dt

		else:
			collisions = []
			for wall in walls:
				if rect_in_rect(*[self.x, self.y+self.vy*dt, self.w, self.h-self.vy*dt], *[wall.x, wall.y, wall.w, wall.h]):
					collisions.append(wall)
			if len(collisions) > 0:
				wall = max(collisions, key=lambda a: a.y)
				self.y = wall.y + wall.h
				self.vy = 0
			else:
				self.y += self.vy*dt
		

	def render(self):
		render_x = self.x - cam_x
		render_y = self.y - cam_y

		color = (255, 255, 255)
		if rects.index(self) == 0:
			color = (0, 255, 0)

		pygame.draw.rect(screen, color, (render_x, render_y, self.w, self.h), 1)


def update_collisions(rect1, rect2):
	if collision(rect1, rect2):
		mass_sum = rect2.mass + rect1.mass

		if rect2.x+rect2.w/2 >= rect1.x+rect1.w/2:
			x_overlap = rect1.x + rect1.w - rect2.x
		else:
			x_overlap = rect2.x + rect2.w - rect1.x

		if rect2.y+rect2.h/2 >= rect1.y+rect1.h/2:
			y_overlap = rect1.y + rect1.h - rect2.y
		else:
			y_overlap = rect2.y + rect2.h - rect1.y


		if x_overlap < y_overlap:
			if rect2.x+rect2.w/2 >= rect1.x+rect1.w/2:
				rect1.x -= x_overlap * (rect2.mass/mass_sum)
				rect2.x += x_overlap * (rect1.mass/mass_sum)
			else:
				rect1.x += x_overlap * (rect2.mass/mass_sum)
				rect2.x -= x_overlap * (rect1.mass/mass_sum)
				
			mean_speed_x = (rect1.vx*rect1.mass + rect2.vx*rect2.mass)/mass_sum
			rect1.vx = mean_speed_x
			rect2.vx = mean_speed_x

		else:
			if rect2.y+rect2.h/2 >= rect1.y+rect1.h/2:
				rect1.y -= y_overlap * (rect2.mass/mass_sum)
				rect2.y += y_overlap * (rect1.mass/mass_sum)
			else:
				rect1.y += y_overlap * (rect2.mass/mass_sum)
				rect2.y -= y_overlap * (rect1.mass/mass_sum)

			mean_speed_y = (rect1.vy*rect1.mass + rect2.vy*rect2.mass)/mass_sum
			rect1.vy = mean_speed_y
			rect2.vy = mean_speed_y









rects = [Rect(random.randint(0, window_size[0]), random.randint(0, window_size[1]), random.randint(20, 60), random.randint(20, 60)) for i in range(50)]
walls = [Wall(0, 600, 800, 50), Wall(150, 400, 150, 44)]


start_drag_pos = None
while 1:
	screen.fill((0, 0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()

		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
			start_drag_pos = pygame.mouse.get_pos()
			start_cam_pos = [cam_x, cam_y]
		if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
			start_drag_pos = None

	rects[0].vx = (pygame.mouse.get_pos()[0] - rects[0].x - rects[0].w/2 + cam_x)/4
	rects[0].vy = (pygame.mouse.get_pos()[1] - rects[0].y - rects[0].h/2 + cam_y)/4

	if start_drag_pos != None:
		dx = (start_drag_pos[0] - pygame.mouse.get_pos()[0])
		dy = (start_drag_pos[1] - pygame.mouse.get_pos()[1])

		cam_x = start_cam_pos[0] + dx
		cam_y = start_cam_pos[1] + dy

	for rect in rects:
		rect.update()

	for i in range(steps_per_frame):
		for rect1 in rects:
			for rect2 in rects[rects.index(rect1)+1:]:
				update_collisions(rect1, rect2)

			for wall in walls:
				if collision(wall, rect1):

					if rect1.x+rect1.w/2 >= wall.x+wall.w/2:
						x_overlap = wall.x + wall.w - rect1.x
					else:
						x_overlap = rect1.x + rect1.w - wall.x

					if rect1.y+rect1.h/2 >= wall.y+wall.h/2:
						y_overlap = wall.y + wall.h - rect1.y
					else:
						y_overlap = rect1.y + rect1.h - wall.y


					if x_overlap < y_overlap:
						if rect1.x+rect1.w/2 >= wall.x+wall.w/2:
							rect1.x += x_overlap
						else:
							rect1.x -= x_overlap
							
						rect1.vx = 0

					else:
						if rect1.y+rect1.h/2 >= wall.y+wall.h/2:
							rect1.y += y_overlap
						else:
							rect1.y -= y_overlap

						rect1.vy = 0




	for wall in walls:
		wall.render()

	for rect in rects:
		rect.render()	

	pygame.display.update()
	clock.tick(60)
