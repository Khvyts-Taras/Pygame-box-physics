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
	if (rect1.x >= rect2.x and rect1.x <= rect2.x + rect2.w) or (rect2.x >= rect1.x and rect2.x <= rect1.x + rect1.w):
		if (rect1.y >= rect2.y and rect1.y <= rect2.y + rect2.h) or (rect2.y >= rect1.y and rect2.y <= rect1.y + rect1.h):
			return True
	return False

class Rect:
	def __init__(self, x, y, w, h, mass, active=True):
		self.active = active
		self.x, self.y = x, y
		self.w, self.h = w, h
		self.vx, self.vy = 0, 0
		if self.active:
			self.mass = mass
		else:
			self.mass = 1e+10

	def update(self):
		self.vx *= 0.97
		self.vy *= 0.97

		if self.active:
			self.x += self.vx
			self.y += self.vy
		else:
			self.vx = 0
			self.vy = 0

	def update_collision(self):
		for rect in rects[rects.index(self)+1:]:
			if collision(self, rect):
				mass_sum = rect.mass + self.mass

				if rect.x+rect.w/2 >= self.x+self.w/2:
					x_overlap = self.x + self.w - rect.x
				else:
					x_overlap = rect.x + rect.w - self.x

				if rect.y+rect.h/2 >= self.y+self.h/2:
					y_overlap = self.y + self.h - rect.y
				else:
					y_overlap = rect.y + rect.h - self.y


				if x_overlap < y_overlap:
					if rect.x+rect.w/2 >= self.x+self.w/2:
						self.x -= x_overlap * (rect.mass/mass_sum)
						rect.x += x_overlap * (self.mass/mass_sum)
					else:
						self.x += x_overlap * (rect.mass/mass_sum)
						rect.x -= x_overlap * (self.mass/mass_sum)
						
					mean_speed_x = (self.vx*self.mass + rect.vx*rect.mass)/mass_sum
					self.vx = mean_speed_x
					rect.vx = mean_speed_x

				else:
					if rect.y+rect.h/2 >= self.y+self.h/2:
						self.y -= y_overlap * (rect.mass/mass_sum)
						rect.y += y_overlap * (self.mass/mass_sum)
					else:
						self.y += y_overlap * (rect.mass/mass_sum)
						rect.y -= y_overlap * (self.mass/mass_sum)

					mean_speed_y = (self.vy*self.mass + rect.vy*rect.mass)/mass_sum
					self.vy = mean_speed_y
					rect.vy = mean_speed_y


	def render(self):
		render_x = self.x - cam_x
		render_y = self.y - cam_y

		color = (255, 255, 255)
		if not self.active:
			color = (255, 0, 0)
		if rects.index(self) == 0:
			color = (0, 255, 0)

		pygame.draw.rect(screen, color, (render_x, render_y, self.w, self.h), 1)

rects = [Rect(random.randint(0, window_size[0]), random.randint(0, window_size[1]), random.randint(20, 60), random.randint(20, 60), 1, random.randint(0, 1)) for i in range(50)]
rects[0].active = 1


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

	rects[0].vx = (pygame.mouse.get_pos()[0] - rects[0].x + cam_x)/4
	rects[0].vy = (pygame.mouse.get_pos()[1] - rects[0].y + cam_y)/4

	if start_drag_pos != None:
		dx = (start_drag_pos[0] - pygame.mouse.get_pos()[0])
		dy = (start_drag_pos[1] - pygame.mouse.get_pos()[1])

		cam_x = start_cam_pos[0] + dx
		cam_y = start_cam_pos[1] + dy

	for rect in rects:
		rect.update()

	for i in range(steps_per_frame):
		for rect in rects:
			rect.update_collision()

	for rect in rects:
		rect.render()	

	pygame.display.update()
	clock.tick(60)
