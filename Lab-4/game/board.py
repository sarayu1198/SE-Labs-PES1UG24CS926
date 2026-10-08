import random
import pygame

GRID_SIZE = 8
TILE_SIZE = 60

GEM_COLORS = [
    (220, 50, 50),   # Red
    (50, 200, 50),   # Green
    (50, 100, 240),  # Blue
    (240, 200, 40),  # Yellow
    (180, 50, 220),  # Purple
    (240, 130, 40),  # Orange
]

# -----------------------------
# GAMEPLAY PARAMETERS
# -----------------------------

TARGET_SCORE = 500
MAX_MOVES = 20

# Task 2
CASCADE_MULTIPLIER = 1.5

# Task 4
HINT_DELAY = 5000  # milliseconds


class Gem:

    def __init__(self, color, target_row, col, special=None):
        self.color = color
        self.target_row = target_row
        self.col = col

        # special can be:
        # None
        # "row"
        # "column"
        self.special = special

        self.current_y = (target_row - 2) * TILE_SIZE
        self.target_y = target_row * TILE_SIZE
        self.fall_speed = 12.0

    def update(self):
        if self.current_y < self.target_y:
            self.current_y += self.fall_speed

            if self.current_y > self.target_y:
                self.current_y = self.target_y

    def is_animating(self):
        return self.current_y < self.target_y


class Board:

    def __init__(
        self,
        offset_x,
        offset_y,
        target_score=TARGET_SCORE,
        max_moves=MAX_MOVES,
    ):
        self.offset_x = offset_x
        self.offset_y = offset_y

        self.target_score = target_score
        self.max_moves = max_moves

        self.grid = [
            [None for _ in range(GRID_SIZE)]
            for _ in range(GRID_SIZE)
        ]

        self.selected = None
        self.score = 0
        self.moves_remaining = max_moves

        # Task 2
        self.current_combo = 0
        self.last_cascade_score = 0

        # Task 4
        self.last_input_time = pygame.time.get_ticks()
        self.hint_pair = None
        self.hint_pulse = 0

        self.reset()

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):
        self.score = 0
        self.moves_remaining = self.max_moves
        self.selected = None

        self.current_combo = 0
        self.last_cascade_score = 0

        self.last_input_time = pygame.time.get_ticks()
        self.hint_pair = None
        self.hint_pulse = 0

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):

                color = random.choice(GEM_COLORS)

                gem = Gem(color, r, c)

                # Initial board should not animate
                gem.current_y = gem.target_y

                self.grid[r][c] = gem

        # Remove accidental starting matches
        self.resolve_matches()

        self.last_input_time = pygame.time.get_ticks()

    # =========================================================
    # ANIMATION
    # =========================================================

    def is_animating(self):

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):

                if self.grid[r][c] and self.grid[r][c].is_animating():
                    return True

        return False

    # =========================================================
    # SWAPPING
    # =========================================================

    def swap_gems(self, pos1, pos2):

        r1, c1 = pos1
        r2, c2 = pos2

        g1 = self.grid[r1][c1]
        g2 = self.grid[r2][c2]

        self.grid[r1][c1], self.grid[r2][c2] = g2, g1

        if self.grid[r1][c1]:

            self.grid[r1][c1].target_row = r1
            self.grid[r1][c1].target_y = r1 * TILE_SIZE
            self.grid[r1][c1].current_y = r1 * TILE_SIZE
            self.grid[r1][c1].col = c1

        if self.grid[r2][c2]:

            self.grid[r2][c2].target_row = r2
            self.grid[r2][c2].target_y = r2 * TILE_SIZE
            self.grid[r2][c2].current_y = r2 * TILE_SIZE
            self.grid[r2][c2].col = c2

    def is_adjacent(self, pos1, pos2):

        r1, c1 = pos1
        r2, c2 = pos2

        return abs(r1 - r2) + abs(c1 - c2) == 1

    # =========================================================
    # MATCH DETECTION
    # =========================================================

    def find_matches(self):

        matched = set()

        # Horizontal matches
        for r in range(GRID_SIZE):

            for c in range(GRID_SIZE - 2):

                if (
                    self.grid[r][c]
                    and self.grid[r][c + 1]
                    and self.grid[r][c + 2]
                    and self.grid[r][c].color
                    == self.grid[r][c + 1].color
                    == self.grid[r][c + 2].color
                ):

                    matched.update([
                        (r, c),
                        (r, c + 1),
                        (r, c + 2),
                    ])

        # Vertical matches
        for r in range(GRID_SIZE - 2):

            for c in range(GRID_SIZE):

                if (
                    self.grid[r][c]
                    and self.grid[r + 1][c]
                    and self.grid[r + 2][c]
                    and self.grid[r][c].color
                    == self.grid[r + 1][c].color
                    == self.grid[r + 2][c].color
                ):

                    matched.update([
                        (r, c),
                        (r + 1, c),
                        (r + 2, c),
                    ])

        return matched

    # =========================================================
    # FIND 4-IN-A-ROW
    # =========================================================

    def find_four_matches(self):

        specials = []

        # Horizontal 4+
        for r in range(GRID_SIZE):

            c = 0

            while c < GRID_SIZE - 3:

                if (
                    self.grid[r][c]
                    and self.grid[r][c + 1]
                    and self.grid[r][c + 2]
                    and self.grid[r][c + 3]
                    and self.grid[r][c].color
                    == self.grid[r][c + 1].color
                    == self.grid[r][c + 2].color
                    == self.grid[r][c + 3].color
                ):

                    specials.append(
                        ((r, c + 1), "row")
                    )

                    c += 4

                else:
                    c += 1

        # Vertical 4+
        for c in range(GRID_SIZE):

            r = 0

            while r < GRID_SIZE - 3:

                if (
                    self.grid[r][c]
                    and self.grid[r + 1][c]
                    and self.grid[r + 2][c]
                    and self.grid[r + 3][c]
                    and self.grid[r][c].color
                    == self.grid[r + 1][c].color
                    == self.grid[r + 2][c].color
                    == self.grid[r + 3][c].color
                ):

                    specials.append(
                        ((r + 1, c), "column")
                    )

                    r += 4

                else:
                    r += 1

        return specials

    # =========================================================
    # SPECIAL GEM ACTIVATION
    # =========================================================

    def activate_special(self, pos):

        r, c = pos

        gem = self.grid[r][c]

        if gem is None or gem.special is None:
            return set()

        affected = set()

        if gem.special == "row":

            for col in range(GRID_SIZE):
                affected.add((r, col))

        elif gem.special == "column":

            for row in range(GRID_SIZE):
                affected.add((row, c))

        return affected

    # =========================================================
    # DROP + REFILL
    # =========================================================

    def drop_and_refill(self):

        for c in range(GRID_SIZE):

            empty_slots = 0

            # Move existing gems downward
            for r in range(GRID_SIZE - 1, -1, -1):

                if self.grid[r][c] is None:

                    empty_slots += 1

                elif empty_slots > 0:

                    gem = self.grid[r][c]

                    gem.target_row = r + empty_slots
                    gem.target_y = (r + empty_slots) * TILE_SIZE
                    gem.col = c

                    self.grid[r + empty_slots][c] = gem
                    self.grid[r][c] = None

            # Create new gems
            for r in range(empty_slots):

                color = random.choice(GEM_COLORS)

                gem = Gem(color, r, c)

                gem.current_y = -(
                    (empty_slots - r) * TILE_SIZE
                )

                self.grid[r][c] = gem

    # =========================================================
    # RESOLVE MATCHES
    # =========================================================

    def resolve_matches(self, count_score=True):

        total_cleared = 0
        cascade_number = 0

        while True:

            matches = self.find_matches()

            if not matches:
                break

            cascade_number += 1

            # -----------------------------------------
            # Create special gems from 4-in-a-row
            # -----------------------------------------

            four_matches = self.find_four_matches()

            special_positions = set()

            for pos, direction in four_matches:

                if pos in matches and self.grid[pos[0]][pos[1]]:

                    self.grid[pos[0]][pos[1]].special = direction

                    special_positions.add(pos)

            # -----------------------------------------
            # Expand matches for existing special gems
            # -----------------------------------------

            expanded_matches = set(matches)

            for r, c in list(matches):

                gem = self.grid[r][c]

                if gem and gem.special:

                    expanded_matches.update(
                        self.activate_special((r, c))
                    )

            # -----------------------------------------
            # Don't destroy newly created special gems
            # -----------------------------------------

            for pos in special_positions:

                if pos in expanded_matches:

                    expanded_matches.remove(pos)

            cleared_this_cascade = len(expanded_matches)

            total_cleared += cleared_this_cascade

            # -----------------------------------------
            # Remove gems
            # -----------------------------------------

            for r, c in expanded_matches:

                self.grid[r][c] = None

            # -----------------------------------------
            # Task 2: Cascade scoring
            # -----------------------------------------

            if count_score:

                multiplier = CASCADE_MULTIPLIER ** (
                    cascade_number - 1
                )

                cascade_score = int(
                    cleared_this_cascade * 10 * multiplier
                )

                self.score += cascade_score
                self.last_cascade_score = cascade_score

            # -----------------------------------------
            # Gravity + refill
            # -----------------------------------------

            self.drop_and_refill()

        self.current_combo = cascade_number

        return total_cleared

    # =========================================================
    # PROCESS PLAYER SWAP
    # =========================================================

    def process_swap(self, pos1, pos2):

        if (
            not self.is_adjacent(pos1, pos2)
            or self.is_game_over()
            or self.is_animating()
        ):
            return False

        # Swap
        self.swap_gems(pos1, pos2)

        # Check whether swap produced a match
        matches = self.find_matches()

        # =====================================================
        # TASK 1 FIX:
        # Invalid swaps DO NOT consume a move
        # =====================================================

        if not matches:

            self.swap_gems(pos1, pos2)

            return False

        # Valid move
        self.moves_remaining -= 1

        # Reset combo counter
        self.current_combo = 0

        # Resolve all matches and cascades
        self.resolve_matches(count_score=True)

        return True

    # =========================================================
    # TASK 4: INPUT / HINT SYSTEM
    # =========================================================

    def register_input(self):

        self.last_input_time = pygame.time.get_ticks()
        self.hint_pair = None
        self.hint_pulse = 0

    def find_available_swap(self):

        # Try every adjacent pair
        for r in range(GRID_SIZE):

            for c in range(GRID_SIZE):

                # Right
                if c < GRID_SIZE - 1:

                    pos1 = (r, c)
                    pos2 = (r, c + 1)

                    self.swap_gems(pos1, pos2)

                    matches = self.find_matches()

                    self.swap_gems(pos1, pos2)

                    if matches:
                        return (pos1, pos2)

                # Down
                if r < GRID_SIZE - 1:

                    pos1 = (r, c)
                    pos2 = (r + 1, c)

                    self.swap_gems(pos1, pos2)

                    matches = self.find_matches()

                    self.swap_gems(pos1, pos2)

                    if matches:
                        return (pos1, pos2)

        return None

    def update_hint(self):

        current_time = pygame.time.get_ticks()

        idle_time = current_time - self.last_input_time

        if idle_time >= HINT_DELAY:

            if self.hint_pair is None:

                self.hint_pair = self.find_available_swap()

            # Pulsing animation
            self.hint_pulse += 0.12

        else:

            self.hint_pair = None

    # =========================================================
    # GAME STATE
    # =========================================================

    def is_game_over(self):

        return (
            self.score >= self.target_score
            or self.moves_remaining <= 0
        )

    def check_result(self):

        if self.score >= self.target_score:
            return "WIN"

        if self.moves_remaining <= 0:
            return "LOSS"

        return None

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self):

        for r in range(GRID_SIZE):

            for c in range(GRID_SIZE):

                if self.grid[r][c]:

                    self.grid[r][c].update()

        self.update_hint()

    # =========================================================
    # RENDER
    # =========================================================

    def render(self, surface):

        board_rect = pygame.Rect(
            self.offset_x,
            self.offset_y,
            GRID_SIZE * TILE_SIZE,
            GRID_SIZE * TILE_SIZE,
        )

        pygame.draw.rect(
            surface,
            (20, 22, 28),
            board_rect,
            border_radius=8,
        )

        pygame.draw.rect(
            surface,
            (60, 65, 75),
            board_rect,
            width=3,
            border_radius=8,
        )

        # -----------------------------------------
        # Draw gems
        # -----------------------------------------

        for r in range(GRID_SIZE):

            for c in range(GRID_SIZE):

                gem = self.grid[r][c]

                if gem:

                    x = self.offset_x + c * TILE_SIZE
                    y = self.offset_y + gem.current_y

                    tile_rect = pygame.Rect(
                        x + 2,
                        y + 2,
                        TILE_SIZE - 4,
                        TILE_SIZE - 4,
                    )

                    pygame.draw.rect(
                        surface,
                        gem.color,
                        tile_rect,
                        border_radius=10,
                    )

                    pygame.draw.rect(
                        surface,
                        (255, 255, 255),
                        tile_rect,
                        width=1,
                        border_radius=10,
                    )

                    # ---------------------------------
                    # Task 3: Special gem appearance
                    # ---------------------------------

                    if gem.special:

                        pygame.draw.rect(
                            surface,
                            (255, 255, 255),
                            tile_rect.inflate(-12, -12),
                            width=4,
                            border_radius=8,
                        )

                        # Cross/line indicator
                        if gem.special == "row":

                            pygame.draw.line(
                                surface,
                                (255, 255, 255),
                                (x + 10, y + TILE_SIZE // 2),
                                (x + TILE_SIZE - 10, y + TILE_SIZE // 2),
                                4,
                            )

                        elif gem.special == "column":

                            pygame.draw.line(
                                surface,
                                (255, 255, 255),
                                (x + TILE_SIZE // 2, y + 10),
                                (x + TILE_SIZE // 2, y + TILE_SIZE - 10),
                                4,
                            )

        # -----------------------------------------
        # Selected gem
        # -----------------------------------------

        if self.selected:

            r, c = self.selected

            sel_x = self.offset_x + c * TILE_SIZE
            sel_y = self.offset_y + r * TILE_SIZE

            sel_rect = pygame.Rect(
                sel_x + 2,
                sel_y + 2,
                TILE_SIZE - 4,
                TILE_SIZE - 4,
            )

            pygame.draw.rect(
                surface,
                (255, 255, 255),
                sel_rect,
                width=4,
                border_radius=10,
            )

        # -----------------------------------------
        # Task 4: Hint indicator
        # -----------------------------------------

        if self.hint_pair and not self.is_animating():

            pulse = (
                abs(pygame.math.Vector2(
                    1 + pygame.math.Vector2(
                        0, 0
                    ).length()
                ).x)
            )

            # Smooth pulse between 0 and 1
            import math

            pulse = (
                math.sin(self.hint_pulse) + 1
            ) / 2

            alpha = int(80 + 120 * pulse)

            hint_surface = pygame.Surface(
                surface.get_size(),
                pygame.SRCALPHA,
            )

            for r, c in self.hint_pair:

                x = self.offset_x + c * TILE_SIZE
                y = self.offset_y + r * TILE_SIZE

                hint_rect = pygame.Rect(
                    x + 4,
                    y + 4,
                    TILE_SIZE - 8,
                    TILE_SIZE - 8,
                )

                pygame.draw.rect(
                    hint_surface,
                    (255, 255, 255, alpha),
                    hint_rect,
                    width=4,
                    border_radius=10,
                )

            surface.blit(hint_surface, (0, 0))