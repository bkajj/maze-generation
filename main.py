import random
import threading
import time
import pygame

pygame.init()
pygame.display.set_caption('Maze generation')
class Button:
    font = pygame.font.SysFont('Corbel', 20)
    rendered_text = None
    rect = None
    active = False

    def __init__(self, x, y, width, height, text, active_color, inactive_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = inactive_color
        self.active_color = active_color
        self.inactive_color = inactive_color

    def render_text(self):
        self.rendered_text = self.font.render(self.text, True, pygame.color.THECOLORS['black'])

    def is_clicked(self, mouse, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                return True
            else:
                self.active = False
                return False
        else:
            return False

    def is_hovered(self, mouse):
        if self.x - self.width/2 <= mouse[0] <= self.x + self.width/2 and self.y - self.height/2 <= mouse[1] <= self.y + self.height/2:
            return True
        else:
            return False

    def draw(self):
        self.rect = pygame.draw.rect(screen, self.color, [self.x - self.width/2, self.y - self.height/2, self.width, self.height])
        screen.blit(self.rendered_text, (self.x - self.rendered_text.get_width()/2, self.y - self.rendered_text.get_height()/2))

generate_button = Button(100, 50, 150, 50, 'Generate Maze', pygame.color.THECOLORS['gray'], pygame.color.THECOLORS['white'])
size_field = Button(275, 50, 150, 50, 'Size: 50', pygame.color.THECOLORS['gray'], pygame.color.THECOLORS['white'])

class Field:

    def __init__(self, up, down, left, right):
        self.up = up
        self.down = down
        self.left = left
        self.right = right

def animateMaze():
    global generated, threadRunning
    for f in generated:
        if not threadRunning:
            break
        drawField(f[0], f[1], 8, 25, 100)
        time.sleep(0.01) #JESLI ZA WOLNO SIE GENERUJE TO MOZNA TO ZMNIEJSZYC


size = 50
maze = [[Field(1, 1, 1, 1) for _ in range(size)] for _ in range(size)]
generated = []
text_input_active = False
text_input = '50'
screen = pygame.display.set_mode((1200, 600))
thread = threading.Thread(target=animateMaze)
threadRunning = False
running = True

def rand_dir():
    return random.randint(1, 4)


def get_unvisited_neighbors(x, y, visited):
    neighbors = []
    if 0 <= x+1 <= size-1 and 0 <= y <= size - 1 and not visited[x+1][y]:
        neighbors.append([x+1, y, 1])
    if 0 <= x-1 <= size-1 and 0 <= y <= size - 1 and not visited[x-1][y]:
        neighbors.append([x-1, y, 2])
    if 0 <= x <= size-1 and 0 <= y + 1 <= size - 1 and not visited[x][y+1]:
        neighbors.append([x, y+1, 3])
    if 0 <= x <= size-1 and 0 <= y - 1 <= size - 1 and not visited[x][y-1]:
        neighbors.append([x, y-1, 4])
    return neighbors

def deleteWall(curr, neighbor, field):
    global maze
    if neighbor[2] == 1:
        maze[neighbor[0]][neighbor[1]].left = 0
        maze[curr[0]][curr[1]].right = 0
    elif neighbor[2] == 2:
        maze[neighbor[0]][neighbor[1]].right = 0
        maze[curr[0]][curr[1]].left = 0
    elif neighbor[2] == 3:
        maze[neighbor[0]][neighbor[1]].up = 0
        maze[curr[0]][curr[1]].down = 0
    elif neighbor[2] == 4:
        maze[neighbor[0]][neighbor[1]].down = 0
        maze[curr[0]][curr[1]].up = 0


#1 - path, 0 - wall
def generate_maze():
    global size, maze, generated
    generated = []
    maze = [[Field(1, 1, 1, 1) for _ in range(size)] for _ in range(size)]
    visited = [[False for _ in range(size)] for _ in range(size)]
    stack = []
    start_idx = random.randint(0, size-1)
    stack.append([0, start_idx])
    maze[0][start_idx].left = 0 #set entrance open
    visited[0][start_idx] = True
    found_end = False
    while len(stack) != 0:
        curr = stack.pop()
        generated.append(curr)
        neighbors = get_unvisited_neighbors(curr[0], curr[1], visited)
        if curr[0] == size-1 and not found_end:
            maze[curr[0]][curr[1]].right = 0
            found_end = True
        if len(neighbors) != 0:
            rand_neighbor = random.choice(neighbors)
            stack.append(curr)
            deleteWall(curr, rand_neighbor, maze[rand_neighbor[0]][rand_neighbor[1]])
            visited[rand_neighbor[0]][rand_neighbor[1]] = True
            stack.append([rand_neighbor[0], rand_neighbor[1]])


def drawField(x, y, scale, offsetX, offsetY):
    if maze[x][y].left == 1:
        pygame.draw.line(screen, pygame.color.THECOLORS['white'], (offsetX + x * scale, offsetY + y * scale), (offsetX + x * scale, offsetY + y * scale + scale))
    if maze[x][y].right == 1:
        pygame.draw.line(screen, pygame.color.THECOLORS['white'], (offsetX + x * scale + scale, offsetY + y * scale), (offsetX + x * scale + scale, offsetY + y * scale + scale))
    if maze[x][y].up == 1:
        pygame.draw.line(screen, pygame.color.THECOLORS['white'], (offsetX + x * scale, offsetY + y * scale), (offsetX + x * scale + scale, offsetY + y * scale))
    if maze[x][y].down == 1:
        pygame.draw.line(screen, pygame.color.THECOLORS['white'], (offsetX + x * scale, offsetY + y * scale + scale), (offsetX + x * scale + scale, offsetY + y * scale + scale))

    pygame.display.flip()


def handle_events(event):
    global text_input_active, text_input, size, thread, threadRunning, generated, running
    mouse = pygame.mouse.get_pos()
    size_field.is_clicked(mouse, event)
    generate_button.is_clicked(mouse, event)
    if generate_button.is_clicked(mouse, event):
        if text_input == '' or int(text_input) < 5:
            size = 5
            text_input = '5'
            size_field.text = 'Size: ' + text_input
            size_field.render_text()
        if int(text_input) > 60:
            size = 60
            text_input = '60'
            size_field.text = 'Size: ' + text_input
            size_field.render_text()
        screen.fill(pygame.color.THECOLORS['black'])
        if thread.is_alive():
            generated = []
            threadRunning = False
            thread.join()
        threadRunning = True
        generate_maze()
        thread = threading.Thread(target=animateMaze)
        thread.start()

    if event.type == pygame.MOUSEBUTTONDOWN and size_field.is_hovered(mouse):
        text_input = ''

    if event.type == pygame.KEYDOWN and size_field.active:
        if event.key == pygame.K_BACKSPACE:
            text_input = text_input[:-1]
        elif event.unicode.isdigit() and len(text_input) < 3:
            text_input += event.unicode

    if size_field.active:
        size_field.text = 'Size: ' + text_input
        size_field.render_text()
        if text_input != '':
            size = int(text_input)

    if event.type == pygame.QUIT:
        if thread.is_alive():
            generated = []
            threadRunning = False
            thread.join()
        running = False

    size_field.color = size_field.active_color if size_field.is_hovered(mouse) else size_field.inactive_color
    generate_button.color = generate_button.active_color if generate_button.is_hovered(mouse) else generate_button.inactive_color


def update():
    mouse = pygame.mouse.get_pos()
    generate_button.draw()
    size_field.draw()
    pygame.display.flip()

def start():
    generate_button.render_text()
    size_field.render_text()
def main():
    global running
    start()
    while running:
        update()
        for event in pygame.event.get():
            handle_events(event)

if __name__=="__main__":
    # call the main function
    main()