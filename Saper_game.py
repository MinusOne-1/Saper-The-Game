import random as ran


class SaperGame:
    def __init__(self, len_pole=10, num_of_bomb=3):
        self.bomb = 'b'  # обозначение бомбы
        self.map_ = []  # список с клетками поля
        self.map_bool = []  # список состояний клеток поля
        self.playr_die = False  # на случай если плейер подорвётся
        self.player_win = False  # на случай если плейер выиграл
        self.num_bomb_gl = 0  # кол-во бомб на карте
        self.map_generate(len_pole, num_of_bomb)

    # подсчёт бомб вокруг одной клетки,
    # нужно для выставления циферок
    def check_bomb_around(self, ind_i, ind_j):
        num_bomb = 0
        if self.map_[ind_i][ind_j] != self.bomb:
            for i in range(ind_i - 1, ind_i + 2):
                for j in range(ind_j - 1, ind_j + 2):
                    if not (0 <= i < len(self.map_[0]) and 0 <= j < len(self.map_)):
                        continue
                    else:
                        if self.map_[i][j] == self.bomb:
                            num_bomb += 1
            return num_bomb
        else:
            return self.bomb

    def check_player_win(self):  # проверка выиграл ли игрок
        global num_bomb_gl
        num_of_flag_point = 0  # кол-во зафлагованых точек
        player_win_temp = True
        for i in range(len(self.map_[0])):
            for j in range(len(self.map_)):
                # если есть хотя бы одна закрытая точка плейер ещё не выиграл
                if self.map_bool[i][j] == 'c':
                    player_win_temp = False
                    break
                # подсчёт зафлагованых точек и точек отмеченых вопросом
                if self.map_bool[i][j] == 'f' or self.map_bool[i][j] == '?':
                    num_of_flag_point += 1
            if not player_win_temp:
                break
        # если количество точек, к которых предположительно есть бомбы больше,
        # чем бомб на самом деле естьб плейер не выиграл
        if num_of_flag_point != self.num_bomb_gl or not player_win_temp:
            player_win_temp = False
        return player_win_temp

    # функция проверки клетки игроком

    def player_check_point(self, x, y, operation, after_the_num=False):
        if not (0 <= x < len(self.map_[0]) and 0 <= y < len(self.map_)):
            return 'ERROR: wrong coords'
        if self.map_bool[x][y] != 'o':  # если клетка не открыта, то выполняем операцию
            if operation == 'open':
                if self.map_bool[x][y] == 'f':
                    self.map_bool[x][y] = '?'
                    return 'make "?"'
                elif self.map_bool[x][y] == '?':
                    self.map_bool[x][y] = 'c'
                    return 'make close'
                else:
                    self.map_bool[x][y] = 'o'
                    if self.map_[x][y] == self.bomb:
                        self.playr_die = True
                        return 'You are lose'
                    # раскрываем все пустые клетки вокруг.
                    # не должно войти в рекурсивный ад
                    # т.к. это всё делается только если
                    # клетка закрыта, а
                    # преддущая клетка уже открыта
                    if self.map_[x][y] != self.bomb and not after_the_num:
                        if x + 1 < len(self.map_[0]):
                            if y + 1 < len(self.map_):
                                if self.map_[x + 1][y + 1] == 0:
                                    self.player_check_point(x + 1, y + 1, operation, bool(self.map_[x][y]))
                                if self.map_[x][y + 1] == 0:
                                    self.player_check_point(x, y + 1, operation, bool(self.map_[x][y]))
                            if self.map_[x + 1][y] == 0:
                                self.player_check_point(x + 1, y, operation, bool(self.map_[x][y]))
                            if y - 1 >= 0:
                                if self.map_[x + 1][y - 1] == 0:
                                    self.player_check_point(x + 1, y - 1, operation, bool(self.map_[x][y]))
                                if self.map_[x][y - 1] == 0:
                                    self.player_check_point(x, y - 1, operation, bool(self.map_[x][y]))
                        if x - 1 >= 0:
                            if y - 1 >= 0:
                                if self.map_[x - 1][y - 1] == 0:
                                    self.player_check_point(x - 1, y - 1, operation, bool(self.map_[x][y]))
                            if self.map_[x - 1][y] == 0:
                                self.player_check_point(x - 1, y, operation, bool(self.map_[x][y]))
                            if y + 1 < len(self.map_):
                                if self.map_[x - 1][y + 1] != self.bomb:
                                    self.player_check_point(x - 1, y + 1, operation, bool(self.map_[x][y]))
                    return 'make open'
            if operation == 'flag':
                self.map_bool[x][y] = 'f'
                return 'make flag'
        else:
            return 'Opened point'

    # генерация карты расположения бомб
    def map_generate(self, x, num_bomb):
        self.num_bomb_gl = num_bomb
        self.map_ = [[0 for j in range(x)] for i in range(x)]
        self.map_bool = [['c' for j in range(x)] for i in range(x)]
        temp_x = []
        for i in range(x):
            for j in range(x):
                temp_x.append((i, j))
        for i in range(num_bomb):
            x_bomb_coord = ran.choice(temp_x)
            self.map_[x_bomb_coord[0]][x_bomb_coord[1]] = self.bomb
            del temp_x[temp_x.index(x_bomb_coord)]
        for i in range(x):
            for j in range(x):
                self.map_[i][j] = self.check_bomb_around(i, j)
