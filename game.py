import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Set up some constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
RADIUS_THRESHOLD = 50  # The minimum distance from the center
STD_DEV_THRESHOLD = 100  # The maximum allowed standard deviation
CLOSENESS_THRESHOLD = 50  # The maximum distance between start and end points for a circle
MIN_POINTS = 100

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a list to store points
points = []

# Create a variable to track whether the mouse button is down
mouse_down = False

# Create a font object for rendering text
font = pygame.font.Font(None, 36)

# Initialize perfection_score
perfection_score = 0.0

def is_close(p1, p2, threshold):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) < threshold


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Start drawing
            mouse_down = True
            points.clear()  # Clear the points list for a new circle
            points.append(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONUP:
            # Stop drawing
            mouse_down = False
        elif event.type == pygame.MOUSEMOTION and mouse_down:
            # Continue drawing
            current_point = pygame.mouse.get_pos()
            points.append(current_point)

            # Check if the circle is complete
            if len(points) > MIN_POINTS and is_close(points[0], current_point, CLOSENESS_THRESHOLD):
                running = False

    # Get the current mouse position after processing all events
    current_point = pygame.mouse.get_pos()

    # Check if the circle is complete outside the event processing
    if len(points) > MIN_POINTS and is_close(points[0], current_point, CLOSENESS_THRESHOLD):
        running = False



    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the center point
    pygame.draw.circle(screen, (255, 255, 255), CENTER, 8)

    # Draw the line and calculate the perfection score
    if len(points) >= 2:
        # Calculate the distances from the center to each point
        distances = [np.sqrt((p[0] - CENTER[0]) ** 2 + (p[1] - CENTER[1]) ** 2) for p in points]

        # Calculate the standard deviation of the distances
        std_dev = np.std(distances)

        # Calculate the perfection score
        perfection_score = max(0, 1 - std_dev / STD_DEV_THRESHOLD)

        # Interpolate between green and red based on the perfection score
        color = (255 * (1 - perfection_score), 255 * perfection_score, 0)

        # Draw the line
        pygame.draw.lines(screen, color, False, points, 2)

        # If the standard deviation is too high, end the game
        if std_dev > STD_DEV_THRESHOLD:
            running = False

    # Render the perfection score as text
    score_text = font.render("Perfection: {:.2%}".format(perfection_score), True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    # Update the display
    pygame.display.flip()

    # # Wait for a short time to avoid using too much CPU
    # pygame.time.wait(10)

    # End of game: Show final score and reset variables
    if not running and len(points) >= 2:
        final_text = font.render("Final Perfection: {:.2%}".format(perfection_score), True, (255, 255, 255))
        screen.blit(final_text, (20, 50))
        pygame.display.flip()

        # Wait for the user to start drawing again
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = True
                    points.clear()
                    break
            if running:
                break

# Quit the game
pygame.quit()
