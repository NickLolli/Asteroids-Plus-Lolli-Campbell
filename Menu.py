import pygame
from AsteroidsRound import *
from shipSelectScreen import *
from button import *
from leaderboard import *
from instructions import *
from CoOp import *
import pygame.font
import os
import threading
import traceback
import praw
from dotenv import load_dotenv

load_dotenv()

class Menu:
    def __init__(self):
        pygame.init()
        self.title = "Asteroids   Plus"
        self.title_font = pygame.font.Font('Galaxus-z8Mow.ttf', 100)
        self.title_text = self.title_font.render(self.title, True, WHITE)
        self.title_y = 150
        self.title_y_velocity = 0.20
        # load screen and images for background
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.background = pygame.image.load('Images/backgrounds/space-backgound.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIN_WIDTH, WIN_HEIGHT))
        stars_image = pygame.image.load('Images/backgrounds/space-stars.png')
        self.bg_stars = pygame.transform.scale(stars_image, (WIN_WIDTH, WIN_HEIGHT))
        self.shipicon = pygame.image.load('Images/ships/ship-a/ship-a-damaged.png')
        
        # init vars for background movement
        self.bg_stars_x1 = 0
        self.bg_stars_x2 = WIN_WIDTH
        # init clock for FPS
        self.clock = pygame.time.Clock()

        self.running = True

        self.startup_shown = False

        # news fetched from subreddit (background thread fills this)
        self.news = ["Welcome to Asteroids Plus!"]
        # subreddit to pull news from; override with env var if desired
        self.subreddit = os.getenv("ASTEROIDS_STARTUP_SUBREDDIT")
        # start background fetch so menu doesn't block on network
        threading.Thread(target=self._fetch_news_thread, daemon=True).start()
        
        self.playButton = Button((WIN_WIDTH/2 - 130, WIN_HEIGHT/2 - 150), (100, 100), CYAN, "PLAY")
        self.shipSelect = Button((WIN_WIDTH/2 -50, WIN_HEIGHT/2), (100, 100), CYAN, "SHIP", 'Images/ships/ship-a/ship-a-damaged.png')
        self.exitButton = Button((WIN_WIDTH/2 -50, WIN_HEIGHT/2 + 150), (100, 100), CYAN, "EXIT")
        self.statButton = Button((WIN_WIDTH/2 -50, WIN_HEIGHT/2 + 300), (100, 100), CYAN, "STATS")
        self.instructionsButton = Button((WIN_WIDTH - 120, WIN_HEIGHT - 70), (100, 50), CYAN, "Help")
        self.coOpButton = Button((WIN_WIDTH/2 + 20, WIN_HEIGHT/2 - 150), (100, 100), CYAN, "CO-OP")

        
    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.bg_stars, (self.bg_stars_x1 ,0))
        self.screen.blit(self.bg_stars, (self.bg_stars_x2 ,0))
        
        self.title_y += self.title_y_velocity
        if self.title_y >= WIN_HEIGHT - 635:
            self.title_y = WIN_HEIGHT - 635  # Limit the title's position to the bottom of the screen
            self.title_y_velocity = -0.20  # Reverse direction when reaching bottom
        elif self.title_y <= 150:
            self.title_y = 150  # Limit the title's position to the top of the screen
            self.title_y_velocity = 0.20 

        # Add the following lines
        title_rect = self.title_text.get_rect(center=(WIN_WIDTH/2, self.title_y)) 
        self.screen.blit(self.title_text, title_rect)

        self.clock.tick(FPS) #update the screen based on FPS
        pygame.mouse.set_visible(True)
        
        self.playButton.draw(self.screen, BLACK)
        self.shipSelect.draw(self.screen, BLACK)
        self.exitButton.draw(self.screen, BLACK)
        self.statButton.draw(self.screen,BLACK)
        self.instructionsButton.draw(self.screen,BLACK)
        self.coOpButton.draw(self.screen,BLACK)
    
        pygame.display.update()

    def update_background(self):
        self.bg_stars_x1 -= 0.5
        self.bg_stars_x2 -= 0.5
        
        if self.bg_stars_x1 <= -WIN_WIDTH:
            self.bg_stars_x1 = WIN_WIDTH
        if self.bg_stars_x2 <= -WIN_WIDTH:
            self.bg_stars_x2 = WIN_WIDTH

    def _fetch_news_thread(self):
        try:
            reddit = praw.Reddit(
                client_id=os.getenv("REDDIT_CLIENT_ID"),
                client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                user_agent=os.getenv("REDDIT_USER_AGENT")
            )
            print("Connected to Reddit API")  # Debug print
            
            sub = reddit.subreddit(self.subreddit)
            titles = []
            desired_count = 3
            
            for post in sub.hot(limit=12):
                if getattr(post, "stickied", False):
                    continue
                titles.append(post.title)
                if len(titles) >= desired_count:
                    break
                    
            if titles:
                self.news = ["News from r " + self.subreddit + ":"] + titles
                print("Updated news successfully")  # Debug print
            
        except Exception as e:
            print(f"Reddit API Error: {str(e)}")
            self.news = ["Welcome to Asteroids Plus!", "Unable to load news feed."]

    def show_startup_popup(self):
        def wrap_text(text, font, max_width):
            words = text.split(' ')
            lines = []
            cur = ""
            for w in words:
                test = cur + (" " if cur else "") + w
                if font.size(test)[0] <= max_width:
                    cur = test
                else:
                    if cur:
                        lines.append(cur)
                    cur = w
            if cur:
                lines.append(cur)
            return lines

        base_w = 700
        padding_x = 24
        padding_y = 20
        msg_font = pygame.font.Font('Galaxus-z8Mow.ttf', 20)
        line_h = msg_font.get_linesize()

        showing = True
        while showing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    showing = False

            # Prepare wrapped lines each frame so updates from fetch thread appear
            max_text_w = base_w - padding_x * 2
            raw_lines = []
            for item in self.news:
                wrapped = wrap_text(item, msg_font, max_text_w)
                raw_lines.extend(wrapped)
                raw_lines.append("")  # small gap between posts

            raw_lines.append("")  # extra gap
            raw_lines.append("Press any key or click to continue...")

            # Limit number of lines so popup stays on screen
            max_available_h = WIN_HEIGHT - 120
            max_lines = max(3, (max_available_h - padding_y * 2) // line_h)
            if len(raw_lines) > max_lines:
                raw_lines = raw_lines[: max_lines - 1] + ["...more on r " + self.subreddit]

            popup_h = min(padding_y * 2 + line_h * len(raw_lines), max_available_h)
            popup_w = base_w
            popup = pygame.Surface((popup_w, popup_h))
            popup.set_alpha(230)
            popup.fill((20, 20, 30))
            popup_rect = popup.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))

            # draw background so popup appears over the menu
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.bg_stars, (self.bg_stars_x1, 0))
            self.screen.blit(self.bg_stars, (self.bg_stars_x2, 0))

            # render lines
            popup.fill((20, 20, 30))
            for i, line in enumerate(raw_lines):
                txt = msg_font.render(line, True, WHITE)
                txt_rect = txt.get_rect(topleft=(padding_x, padding_y + i * line_h))
                popup.blit(txt, txt_rect)

            self.screen.blit(popup, popup_rect)
            pygame.display.update()
            self.clock.tick(FPS)



    def play(self):
        selected_ship = 0

        # show startup popup only once when play() first runs
        if not self.startup_shown:
            self.show_startup_popup()
            self.startup_shown = True

        while True:
            m.draw()
            m.update_background()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()

                if self.playButton.is_clicked(event):
                        g = Game(selected_ship) #init Game class
                        g.new() #create a new game everytime we run
                        while g.running:
                            g.main()

                if self.shipSelect.is_clicked(event):
                    select = ShipSelection()
                    selected_ship = select.main()
                    while select.running:
                        select.main()

                if self.instructionsButton.is_clicked(event):
                    self.show_instructions()

                if self.statButton.is_clicked(event):
                    # exit
                    leaderboard = LeaderBoard()
                    while leaderboard.running:
                        leaderboard.view()
                        
                if self.coOpButton.is_clicked(event):
                        c = CoOp(selected_ship) #init Game class
                        c.new() #create a new game everytime we run
                        while c.running:
                            c.main()

                if self.exitButton.is_clicked(event):
                    # exit
                    pygame.quit()
                    exit()
        
        
m = Menu()
while m.running:
    m.play()
