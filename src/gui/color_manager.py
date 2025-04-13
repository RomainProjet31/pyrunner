from pygame import Surface

from src.sprite_constants import DAY, NIGHT, BLACK


class ColorManager:

    def __init__(self):
        # Timers
        self.day_tick = 0
        self.stay_timer = 500
        self.game_changing_timer = 150
        self.game_over_changing_timer = 0
        self.timer_day_changer = 0
        self.current_color = [NIGHT[0], NIGHT[1], NIGHT[2]]
        self.ratio = NIGHT[0] + NIGHT[1] + NIGHT[2] / DAY[0] + DAY[1] + DAY[2]
        self.to_day = False
        self.fade_to_black = False

    def update(self, dt: int, game_over: bool) -> bool:
        """
        :param dt:
        :param game_over:
        :return: True if the color is day, False otherwise
        """
        if game_over:
            comparator = BLACK
            self.timer_day_changer = self.game_over_changing_timer
        else:
            comparator = DAY if self.to_day else NIGHT

        self.__handle_day_n_night_cycle(dt, comparator)
        current_ratio = self.current_color[0] + self.current_color[1] + self.current_color[2] / DAY[0] + DAY[1] + DAY[2]
        return current_ratio - self.ratio >= 50 and not game_over

    def draw(self, screen: Surface, forced_color: tuple[int, int, int] = None):
        current_color = (self.current_color[0], self.current_color[1], self.current_color[2]) \
            if not forced_color else forced_color
        screen.fill(current_color)

    def __handle_day_n_night_cycle(self, dt: int, comparator: list[int]) -> None:
        self.day_tick += dt
        if self.day_tick >= self.timer_day_changer:
            self.day_tick = 0

            if self.timer_day_changer == self.stay_timer:
                self.timer_day_changer = self.game_changing_timer

            goal = True
            for i in range(len(self.current_color)):
                if self.current_color[i] < comparator[i]:
                    self.current_color[i] += 1
                    goal = False
                elif self.current_color[i] > comparator[i]:
                    self.current_color[i] -= 1
                    goal = False

            if goal and comparator is not BLACK:
                self.to_day = not self.to_day
                self.timer_day_changer = self.stay_timer
