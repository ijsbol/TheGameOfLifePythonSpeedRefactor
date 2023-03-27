from typing import List, Final, Tuple
from random import choice, seed
import cProfile

import pygame
from pygame import Surface
from pygame.time import Clock

seed(10000)

WINDOW_WIDTH_IN_CELLS: Final[int] = 200
WINDOW_HEIGHT_IN_CELLS: Final[int] = 200
CELL_WIDTH_IN_PIXELS: Final[int] = 2
RANDOM_INITAL_BOARD: Final[bool] = True
ALIVE_CELL_COLOUR: Final[str] = "white"
DEAD_CELL_COLOUR: Final[str] = "black"

GENERATION_PERMUTATIONS_ENABLED: bool = True
GAME_BOARD: List[List[bool]] = []

delta_offsets = [-1, 0, 1]
DELTA_SURROUNDING_OFFSETS_PACKED: List[Tuple[int]] = [
    (dx, dy) for dx in delta_offsets for dy in delta_offsets
    if not (dx == 0 and dy == 0)
]

# Game logic functions.

def generate_temp_board(random_board: bool = False) -> List[List[bool]]:
    # Generate a game board, empty unless random requested.
    cell_alive_states = [True, False]
    temp_board: List[List[bool]] = []
    for y in range(WINDOW_HEIGHT_IN_CELLS):
        temp_board.append([])
        for x in range(WINDOW_WIDTH_IN_CELLS):
            if random_board:
                temp_board[y].append(choice(cell_alive_states))
            else:
                temp_board[y].append(False)
    
    return temp_board

def get_surrounding_cells(x: int, y: int) -> int:
    dx = 1
    dy = 1
    if (x+dx) >= WINDOW_WIDTH_IN_CELLS:
        dx -= x
    if (y+dy) >= WINDOW_HEIGHT_IN_CELLS:
        dy -= y
    return sum([
        GAME_BOARD[y +dy][x - 1], GAME_BOARD[y +dy][x    ], GAME_BOARD[y +dy][x +dx],
        GAME_BOARD[y    ][x - 1],                           GAME_BOARD[y    ][x +dx],
        GAME_BOARD[y - 1][x - 1], GAME_BOARD[y - 1][x    ], GAME_BOARD[y - 1][x +dx],
    ])

def update_game_board(updated_cells: List[int]) -> None:
    for x, y in zip(*[iter(updated_cells)]*2):
        # Update the cells that have been listed for an update.
        # Invert the cell type on the game board.
        if GAME_BOARD[y][x]:
            GAME_BOARD[y][x] = False
        else:
            GAME_BOARD[y][x] = True

def permutate_cells() -> List[int]:
    # Permute cells one generation.
    # Returns a list of updated cell locations.
    updated_cells: List[int] = []
    for y, _ in enumerate(GAME_BOARD):
        for x, cell in enumerate(GAME_BOARD[y]):
            # Permutate game board logic
            surrounding_cell_count: int = get_surrounding_cells(x, y)
            if cell:
                # Current cell is live.
                if surrounding_cell_count < 2:
                    # A live cell dies if it has fewer than two live neighbors.
                    updated_cells.extend([x, y])

                # A live cell with two or three live neighbors lives on to the next generation.
                # Cell does not need to be updated as it is already alive on the board.
                
                elif surrounding_cell_count > 3:
                    # A live cell with more than three live neighbors dies.
                    updated_cells.extend([x, y])
            else:
                # Current cell is dead
                if surrounding_cell_count == 3:
                    # A dead cell will be brought back to live if it has exactly three live neighbors.
                    updated_cells.extend([x, y])

    update_game_board(updated_cells)

    return updated_cells


# Graphic logic functions.

def draw_grid(updated_cells: List[int] = None) -> None:
    # Draw the game board to the screen in a grid formation.

    if updated_cells is None:
        # This is the first drawing of the board.
        for cell_pos_y in range(WINDOW_HEIGHT_IN_CELLS):
            for cell_pos_x in range(WINDOW_WIDTH_IN_CELLS):
                rect = pygame.Rect(
                    cell_pos_x * CELL_WIDTH_IN_PIXELS,
                    cell_pos_y * CELL_WIDTH_IN_PIXELS,
                    CELL_WIDTH_IN_PIXELS,
                    CELL_WIDTH_IN_PIXELS,
                )

                cell = GAME_BOARD[cell_pos_x][cell_pos_y]
                cell_colour = ALIVE_CELL_COLOUR if cell else DEAD_CELL_COLOUR

                pygame.draw.rect(SCREEN, cell_colour, rect)
        return

    # This is a subsequent drawing of the board and should
    # only update the updated cells provided.
    for updated_cell_x, updated_cell_y in zip(*[iter(updated_cells)]*2):
        # Iterate over the updated cells list.
        cell_alive_state: bool = GAME_BOARD[updated_cell_y][updated_cell_x]
        window_pos_x: int = updated_cell_x * CELL_WIDTH_IN_PIXELS
        window_pos_y: int = updated_cell_y * CELL_WIDTH_IN_PIXELS
        
        rect = pygame.Rect(
            window_pos_x,
            window_pos_y,
            CELL_WIDTH_IN_PIXELS,
            CELL_WIDTH_IN_PIXELS,
        )

        cell_colour = ALIVE_CELL_COLOUR if cell_alive_state else DEAD_CELL_COLOUR

        pygame.draw.rect(SCREEN, cell_colour, rect)

def figure_out_clicked_cell(mouse_pos_x: int, mouse_pos_y: int) -> Tuple[int]:
    # Figure out what cell what clicked.
    cell_pos_x: int = mouse_pos_x // CELL_WIDTH_IN_PIXELS
    cell_pos_y: int = mouse_pos_y // CELL_WIDTH_IN_PIXELS

    return cell_pos_x, cell_pos_y

def test():
    test = 0

    draw_grid()

    mouse_first_clicked_cell_alive_state = False
    first_clicked_state_has_been_set = False
    mouse_is_currently_clicked = False


    while True:
        # The game loop
        
        events_this_frame = pygame.event.get()
        for event in events_this_frame:
            if event.type == pygame.QUIT:
                # Check if the player has closed the game.
                pygame.quit()

            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     mouse_is_currently_clicked = True
            #     first_clicked_state_has_been_set, mouse_first_clicked_cell_alive_state = (
            #         carry_out_user_interaction(
            #             first_clicked_state_has_been_set,
            #             mouse_first_clicked_cell_alive_state
            #         )
            #     )
                
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     first_clicked_state_has_been_set = False
            #     mouse_is_currently_clicked = False
            
            # elif event.type == pygame.MOUSEMOTION and mouse_is_currently_clicked:
            #     first_clicked_state_has_been_set, mouse_first_clicked_cell_alive_state = (
            #         carry_out_user_interaction(
            #             first_clicked_state_has_been_set,
            #             mouse_first_clicked_cell_alive_state
            #         )
            #     )

                    
        # keys_pressed_this_frame = pygame.key.get_pressed()
        # if keys_pressed_this_frame[pygame.K_SPACE]:
        #     # If space key is pressed, resume the simulation.
        #     GENERATION_PERMUTATIONS_ENABLED = True
        # elif keys_pressed_this_frame[pygame.K_TAB]:
        #     # If tab key is pressed, pause the simulation.
        #     GENERATION_PERMUTATIONS_ENABLED = False

        if GENERATION_PERMUTATIONS_ENABLED:
            updated_cells = permutate_cells()
            draw_grid(updated_cells)
            # Update the display
            pygame.display.update()
            test += 1
            if test == 600:
                return

pygame.init()

SCREEN: Surface = pygame.display.set_mode((
    WINDOW_WIDTH_IN_CELLS * CELL_WIDTH_IN_PIXELS,
    WINDOW_HEIGHT_IN_CELLS * CELL_WIDTH_IN_PIXELS,
))
CLOCK: Clock = pygame.time.Clock()

GAME_BOARD = generate_temp_board(RANDOM_INITAL_BOARD)

cProfile.run('test()')