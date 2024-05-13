import random, pygame 

pygame.init()

WIDTH, HEIGHT = 700, 600 
ROWS, COLUMNS = 4, 4
len_grid_X = WIDTH // COLUMNS
len_grid_Y = HEIGHT // ROWS

def initBoardGame(initBlock):
    numbers = [i % ((ROWS * COLUMNS) // 2) + 1 for i in range(ROWS * COLUMNS)]
    random.shuffle(numbers)
    blocks = []
    for i in range(ROWS):
        in_line = []
        for j in range(COLUMNS):
            x = random.randint(j * len_grid_X, (j + 1) * len_grid_X - initBlock.width - 10)
            y = random.randint(i * len_grid_Y, (i + 1) * len_grid_Y - initBlock.height - 10)
            number = numbers.pop(0)        
            block = Block(x, y, number)
            in_line.append(block)

        blocks.append(in_line)

    return blocks

class Block:
    def __init__(self, x, y, number):
        self.width = 50
        self.height = 70
        self.x = x 
        self.y = y 
        self.number = number
        self.clicked = False 

        # image 
        self.image_back = pygame.transform.scale(pygame.image.load("C:\\Users\\PC\\Documents\\backpage.png"), (50, 70))         
        self.frontPage = pygame.transform.scale(pygame.image.load("C:\\Users\\PC\\Documents\\frontpage.png"), (50, 70))
    

    def draw_block(self, win):
        pygame.draw.rect(win, "white", (self.x, self.y, self.width, self.height))

        if self.clicked:
            font = pygame.font.SysFont("comicsans",30)
            text = font.render(str(self.number), True, "white")

            win.blit(self.frontPage, (self.x, self.y))

            win.blit(text, (self.x + self.width / 2 - text.get_width()/2, 
                                    self.y + self.height / 2 - text.get_height()/ 2))

        else:
            win.blit(self.image_back, (self.x, self.y))

    def check_clicked(self, mouse_pos):
        x, y = mouse_pos
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            return True

        else:
            return False  

class Game:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.initBlock = Block(0, 0, 0)
        self.blocks = initBoardGame(self.initBlock)
        self.checking_block = []
        self.won = False 
        self.moves = 0

    def resetGame(self):
        self.blocks = initBoardGame(self.initBlock)
        self.checking_block = []
        self.won = False 
        self.moves = 0


    def check_win(self):
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.blocks[row][col]:
                    return False

        return True 

    def draw_won_window(self):
        self.win.fill("black")
        font = pygame.font.SysFont("comicsans", 50)
        text = font.render(f"You won in {self.moves} moves", True, "white")
        text2 = font.render(f"Click anywhere to play again", True, "white")
        distance = 50
        self.win.blit(text, (WIDTH/2 - text.get_width() / 2, HEIGHT/2 - (text.get_height() + text2.get_height() + distance)/2))
        self.win.blit(text2, (WIDTH/2 - text2.get_width() / 2, HEIGHT/2 - (text.get_height() + text2.get_height() + distance)/2 + distance + text.get_height()))
        
        pygame.display.update()

    def draw_window(self):
        self.win.fill("black")

        for rows in self.blocks:
            for block in rows:
                if block:
                    block.draw_block(self.win)

        pygame.display.update()
        if len(self.checking_block) == 4:
            pygame.time.wait(200)

    def run(self):
        run = True 

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.won == True:
                        self.won = False 
                        self.resetGame()

                    m_x, m_y = pygame.mouse.get_pos()
                    x = m_x // len_grid_X
                    y = m_y // len_grid_Y

                    block = self.blocks[y][x]
                    if block and block.check_clicked((m_x, m_y)) and len(self.checking_block) <= 3:
                        block.clicked = True 
                        self.checking_block.append(y)
                        self.checking_block.append(x)
                        # self.checking_block = [y1, x1, y2, x2]

            
            if not self.won:
                self.draw_window()

            if len(self.checking_block) == 4:
                if self.blocks[self.checking_block[0]][self.checking_block[1]].number == self.blocks[self.checking_block[2]][self.checking_block[3]].number:
                    self.blocks[self.checking_block[0]][self.checking_block[1]] = None                    
                    self.blocks[self.checking_block[2]][self.checking_block[3]] = None                    
                else:
                    self.blocks[self.checking_block[0]][self.checking_block[1]].clicked = False
                    self.blocks[self.checking_block[2]][self.checking_block[3]].clicked = False

                self.checking_block.clear()
                self.moves += 1


            self.won = self.check_win()
            if self.won: 
                self.draw_won_window()



game = Game()
game.run()