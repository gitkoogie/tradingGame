import pygame, sys
import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt 
import matplotlib.backends.backend_agg as agg

fig = plt.figure(figsize=(6, 4))
fig.tight_layout()
ax = fig.add_subplot(111)
canvas = agg.FigureCanvasAgg(fig)

# distribution
# 10% losing 5x risk
# 30% losing 1x risk
# 55% winning 2x risk
# 5% winning 10x risk

# compute R for trade
l = [-5, -5, -1, -1, -1, -1, -1, -1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 10]
def compute_R(risk):
        # pick return uniformly from distribution
        p = int(np.random.uniform(1, 20))
        res = l[p] * risk
        return res 

# draw rectangles and labels where user input
def draw_rectangles_and_labels():
    # draw rect for inputing into
    pygame.draw.rect(screen, color, risk_per_trade_box, 2)
    pygame.draw.rect(screen, color, num_shares_box, 2)
    pygame.draw.rect(screen, color, done_box, 2)

    # text surfaces for labels
    text_surface_risk_text = base_font.render(text_risk, True, (255, 255, 255))
    text_surface_shares_text = base_font.render(text_num_shares, True, (255, 255, 255))
    text_done_text = base_font.render(text_done, True, (255, 255, 255))

    # draw texts for labels
    screen.blit(text_surface_risk_text, (width * 0, height * 0.65 - text_height))
    screen.blit(text_surface_shares_text, (width * 0.2, height * 0.65 - text_height))
    screen.blit(text_done_text, (width * 0.1, height * 0.75 - text_height))

# winning animation
def winning_animation(balance):
    text_won = "YOU WON!"
    text_end_balance = "Your Final Balance: " + str(balance) + " SEK"
    user_text = ""
    
    text_surface_won = base_font.render(text_won, True, (255, 255, 255))
    text_surface_balance = base_font.render(text_end_balance, True, (255, 255, 255))

    while True:
        # events 
        for event in pygame.event.get():
            # if user press quit    
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    i += 1
                    user_text = ""
                    if i > len(states) - 1:
                        i = 0
                    state = states[i]    
                else:
                    user_text += event.unicode
        # clear screen            
        screen.fill((0, 0, 0)) 

        # won
        screen.blit(text_surface_won, (width/2,height/2))
        screen.blit(text_surface_balance, (width/2, height/2 + text_height))
        
        # Question
        text_Q = "Retry? (y / n)"
        text_surface_Q = base_font.render(text_Q, True, (255, 255, 255))
        screen.blit(text_surface_Q, (width/2, height/2 + 2 * text_height))

        if user_text == "y":
            return 1
        elif user_text == "n":
            return 0

        # flip display
        pygame.display.flip()
        clock.tick(60)


# losing animation
def losing_animation(balance):
    text_lost = "YOU LOST!"
    text_end_balance = "Your Final Balance: " + str(balance) + " SEK"
    user_text = ""

    text_surface_lost = base_font.render(text_lost, True, (255, 255, 255))
    text_surface_balance = base_font.render(text_end_balance, True, (255, 255, 255))
    while True:
        # events 
        for event in pygame.event.get():
            # if user press quit    
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    i += 1
                    user_text = ""
                    if i > len(states) - 1:
                        i = 0
                        state = states[i]    
                else:
                    user_text += event.unicode
        # clear screen            
        screen.fill((0, 0, 0)) 

        # lost 
        screen.blit(text_surface_lost, (width/2,height/2))
        screen.blit(text_surface_balance, (width/2, height/2 + 22))

        # Question
        text_Q = "Retry? (y / n)"
        text_surface_Q = base_font.render(text_Q, True, (255, 255, 255))
        screen.blit(text_surface_Q, (width/2, height/2 + 2 * text_height))

        if user_text == "y":
            return 1
        elif user_text == "n":
            return 0

        # flip display
        pygame.display.flip()
        clock.tick(60)


# plot account 
def plot_balance(data, goal):
    ax.cla()
    ax.plot(data, label = "Current Balance")
    ax.set_title("Account Balance")
    ax.set_xlabel("Trades")
    ax.set_ylabel("SEK")
    ax.set_xlim(0, 20)
    ax.set_ylim(0, goal*1.5)
    ax.plot([goal]*21, '--', label = "Goal")
    ax.legend()
    canvas.draw()
    renderer = canvas.get_renderer()

    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()

    return pygame.image.fromstring(raw_data, size, "RGB")

# initialize 
pygame.init()
pygame.display.set_caption("Position Sizing")
programIcon = pygame.image.load("kellyicon.PNG")
pygame.display.set_icon(programIcon)
width = 1200                                         # window dim
height = 800                                        # window dim
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()                         # clock
text_height = 22
base_font = pygame.font.Font(None, text_height)     # font

# text boxes for inputing into
risk_per_trade_box = pygame.Rect(width * 0, height * 0.65, 140, 22)
num_shares_box = pygame.Rect(width * 0.2, height * 0.65, 140, 22)
done_box = pygame.Rect(width * 0.1, height * 0.75, 140, 22)

# box color
color = pygame.Color('lightskyblue3')

# static texts
text_risk = "Risk per trade (SEK)"
text_num_shares = "Number of shares"
text_done = "Done? (y / n)"

# text input and settings
risk = ""
shares = ""
done = ""
user_text = ""
balance = [1000]
goal = 1500
surf = plot_balance(balance, goal)

iterations = 20
iterations_left = 20
price = round(np.random.uniform(1, 500), 2)
price_set = True

# program states
display_position = False
states = ["risk", "numShares", "enter"]
i = 0
state = states[i]

# error flags
error_funds = False

# game loop 
while True: 
    # events 
    for event in pygame.event.get():
        # if user press quit    
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            elif event.key == pygame.K_RETURN:
                i += 1
                user_text = ""
                if i > len(states) - 1:
                    i = 0
                state = states[i]    
            else:
                user_text += event.unicode

    # clear previous drawing 
    screen.fill((0, 0, 0))     
    # draw rectangles and labels for input       
    draw_rectangles_and_labels()
    

    # draw balance and goal
    text_surface_balance = base_font.render("Your Account Balance: " + str(balance[-1]) + " SEK", True, (255, 255, 255))
    screen.blit(text_surface_balance, (width * 0, 0))
    text_surface_goal = base_font.render("Your Goal: " + str(goal) + " SEK", True ,(255, 255, 255))
    screen.blit(text_surface_goal, (width * 0, 22))

    # draw price of stock
    if state == "risk" and price_set == False and done != "y":
        price =  round(np.random.uniform(1, 500), 2)
        price_set = True

    text_surface_stockprice = base_font.render("Price of Stock: " + str(price) + " SEK", True, (255, 255, 255))
    screen.blit(text_surface_stockprice, (width * 0, height * 0.5))

    # SET USER INPUT AT CORRECT FIELD 
    if state == "risk":
        risk = user_text
        display_position = False
        computed_R = False
    elif state == "numShares":
        shares = user_text
    else:
        display_position = True
        price_set = False
        last_risk = int(risk)*int(shares)
        done = user_text

    # if user enters "y" into done field and press enter (i.e moves to next step)
    if done == "y" and state == "risk" and error_funds == False:
        res = compute_R(int(last_risk))
        new_balance = balance[iterations - iterations_left] + res 
        balance.append(new_balance)
        done = ""
        iterations_left -= 1
        surf = plot_balance(balance, goal)

    # plot balance
    screen.blit(surf, (width*0.4, 80))

    # input text from user
    if state == "risk":
        text_surface_risk_in = base_font.render(risk+"<", True, (255, 255, 255))
        text_surface_shares_in = base_font.render(shares, True, (255, 255, 255))
        text_surface_done_in = base_font.render(done, True, (255, 255, 255))
    elif state == "numShares":
        text_surface_risk_in = base_font.render(risk, True, (255, 255, 255))
        text_surface_shares_in = base_font.render(shares+"<", True, (255, 255, 255))
        text_surface_done_in = base_font.render(done, True, (255, 255, 255))
    else:
        text_surface_risk_in = base_font.render(risk, True, (255, 255, 255))
        text_surface_shares_in = base_font.render(shares, True, (255, 255, 255))
        text_surface_done_in = base_font.render(done+"<", True, (255, 255, 255))
    # draw texts from user
    screen.blit(text_surface_risk_in, risk_per_trade_box)
    screen.blit(text_surface_shares_in, num_shares_box)
    screen.blit(text_surface_done_in, done_box)

    # display position
    if display_position:
        tot_shares = "Number of Shares: " + shares + ", Risk Per Share: " + risk
        tot_risk = "Your Total Risk: " + str(int(risk) * int(shares)) + " SEK"
        tot_position = "Your Position: " + str(int(price)*int(shares)) + " SEK"

        # if position > account balance
        if int(price)*int(shares) > balance[iterations - iterations_left]:

            screen.blit(base_font.render("Not Sufficient Funds!, Position: " + str(int(price)*int(shares)), True, (255, 255, 255)), (0,330))
            error_funds = True
        else:
            text_surface_tot_risk = base_font.render(tot_risk, True, (255, 255, 255))
            text_surface_shares = base_font.render(tot_shares, True, (255, 255, 255))
            text_surface_position = base_font.render(tot_position, True, (255, 255, 255))
            screen.blit(text_surface_shares, (width * 0.5, height * 0.75))
            screen.blit(text_surface_tot_risk, (width * 0.5, height * 0.75 + text_height))
            screen.blit(text_surface_position, (width * 0.5, height * 0.75 + text_height * 2))
            error_funds = False
    
    # display iterations 
    iter_str = "Iterations Left / Total Iterations: " + str(iterations_left) + " / " + str(iterations)
    text_surface_iterations = base_font.render(iter_str, True, (255, 255, 255))
    screen.blit(text_surface_iterations, (0,44))

    # if goal is reached
    if balance[iterations - iterations_left] >= goal:
        ret = winning_animation(balance[-1])
        if ret == 0:    
            pygame.quit()
            sys.exit()
        else:
            balance = 1000
            iterations_left = iterations

    # if there are no iterations left
    if iterations_left == 0 or balance[iterations - iterations_left] < goal / 10:
        ret = losing_animation(balance[-1])
        if ret == 0:
            pygame.quit()
            sys.exit()
        else:
            balance = 1000
            iterations_left = iterations

    # flip display
    pygame.display.flip()
    # delay
    clock.tick(60)
