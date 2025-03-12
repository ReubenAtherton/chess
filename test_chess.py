import pygame as p

WIDTH = 800
HEIGHT = 800

p.init()
screen = p.display.set_mode((WIDTH, HEIGHT))
screen.fill((200, 200, 200))  # Light gray
p.display.flip()
p.event.pump()
p.display.set_caption("Focus Test")
p.mouse.set_pos((WIDTH // 2, HEIGHT // 2))
p.event.pump()
print("Test started. Click to see if it registers.")

running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        elif event.type == p.MOUSEBUTTONDOWN:
            print(f"Clicked at {p.mouse.get_pos()}")
    p.display.flip()

p.quit()