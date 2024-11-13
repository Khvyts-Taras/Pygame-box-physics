import pygame


def rect_in_rect(x1, y1, w1, h1, x2, y2, w2, h2):
	return (x1+w1 > x2 and x1 < x2+w2) and (y1+h1 > y2 and y1 < y2+h2)


class Object:
	def __init__(self, x, y, w, h):
		self.x, self.y = x, y
		self.w, self.h = w, h
		self.vx, self.vy = 0, 0

	@property
	def rect(self):
		return [self.x, self.y, self.w, self.h]

	def update(self, dt):
		self.vx *= 0.5**dt
		self.vy *= 0.5**dt

		
		if self.vx > 0:
			collisions = []
			for wall in walls:
				if rect_in_rect(*[self.x, self.y, self.w+self.vx*dt, self.h], *wall):
					collisions.append(wall)
			if len(collisions) > 0:
				wall = min(collisions, key=lambda a: a[0])
				self.x = wall[0]-self.w
				self.vx = 0
			else:
				self.x += self.vx*dt
		else:
			collisions = []
			for wall in walls:
				if rect_in_rect(*[self.x+self.vx*dt, self.y, self.w-self.vx*dt, self.h], *wall):
					collisions.append(wall)
			if len(collisions) > 0:
				wall = max(collisions, key=lambda a: a[0])
				self.x = wall[0]+wall[2]
				self.vx = 0
			else:
				self.x += self.vx*dt

		
		if self.vy > 0:
			collisions = []
			for wall in walls:
				if rect_in_rect(*[self.x, self.y, self.w, self.h+self.vy*dt], *wall):
					collisions.append(wall)
			if len(collisions) > 0:
				wall = min(collisions, key=lambda a: a[1])
				self.y = wall[1]-self.h
				self.vy = 0
			else:
				self.y += self.vy*dt

		else:
			collisions = []
			for wall in walls:
				if rect_in_rect(*[self.x, self.y+self.vy*dt, self.w, self.h-self.vy*dt], *wall):
					collisions.append(wall)
			if len(collisions) > 0:
				wall = max(collisions, key=lambda a: a[1])
				self.y = wall[1]+wall[3]
				self.vy = 0
			else:
				self.y += self.vy*dt

	def render(self, screen):
		color = (255, 255, 255)
		pygame.draw.rect(screen, color, self.rect, 1)



pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()


obj1 = Object(50, 50, 30, 30)
walls = [[200, 200, 150, 150],
		 [150, 20, 65, 44]]

while True:
	dt = clock.tick(60)/1000
	screen.fill((0, 0, 0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()

	mouse_x, mouse_y = pygame.mouse.get_pos()
	if pygame.mouse.get_pressed()[0]:
		obj1.vx += (mouse_x - obj1.x)*0.1
		obj1.vy += (mouse_y - obj1.y)*0.1

	obj1.update(dt)

	obj1.render(screen)
	for wall in walls:
		pygame.draw.rect(screen, (255, 0, 0), wall, 1)

	pygame.display.update()