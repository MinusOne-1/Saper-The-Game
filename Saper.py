import sys
import sqlite3
from Saper_game import SaperGame
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMainWindow, QAction, QSpinBox, QLineEdit, QLabel
from DataBaseSaper import DBSaper


class Saper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect('Saper_Games_and_Players.db')
        self.pole = []
        self.side_number = 0
        self.bombs_number = 0
        self.game = SaperGame()
        self.operation = 'open'
        self.player = 'player1'
        self.resalt = ''
        self.initUI()

    def playerGamesPlusOne(self):
        cur = self.con.cursor()
        player = cur.execute('''Select id from Players WHERE PlayerName like ?''',
                             (self.player,)).fetchall()[0][0]
        cur.execute('''UPDATE Players
        SET Number_of_games = Number_of_games + 1
        WHERE id = ?''', (player,))
        self.con.commit()

    def addPlayer(self):
        cur = self.con.cursor()
        players = [i[0] for i in cur.execute('''Select PlayerName from Players
         WHERE id BETWEEN 0 AND 1001''').fetchall()]
        if self.player not in players:
            cur.execute('INSERT INTO Players(PlayerName, Number_of_games) VALUES(?, ?)', (self.player, 0))
        self.con.commit()

    def addGame(self, side, bombs, result):
        cur = self.con.cursor()
        player = cur.execute('''Select id from Players WHERE PlayerName like ?''',
                             (self.player,)).fetchall()[0][0]
        cur.execute('INSERT INTO Game(side, bombs, player, result) VALUES(?, ?, ?, ?)', (side, bombs, player, result))
        self.con.commit()

    def newGameWindow(self):
        # передаёт полученые ланные и приравнивает self.game
        # вызывает окно, которое спрашивает имя игрока, размерность поля и кол-во бомб
        self.side_number = self.side_sb.value()
        self.bombs_number = self.bombs.value()
        self.player = self.player_line.text()
        self.addPlayer()
        self.game = SaperGame(self.side_sb.value(), self.bombs.value())
        self.close()
        for i in self.pole:
            for j in i:
                j.close()
        self.pole.clear()
        x, y = 10, 70 + self.flag_to_open_b.height() + 10
        for i in range(len(self.game.map_)):
            self.pole.append([])
            for j in range(len(self.game.map_)):
                self.pole[i].append(QPushButton(self))
                self.pole[i][j].move(x, y)
                self.pole[i][j].resize(20, 20)
                self.pole[i][j].clicked.connect(self.checkCell)
                self.pole[i][j].setText('')
                self.pole[i][j].setStyleSheet('background: #76428a;')
                x += 20
            y += 20
            x = 10
        temp = (30 + self.play_b.width() + 10 + self.player_line.width() + 10 + self.side_sb.width() + 10
                + self.bombs.width() + 30)
        self.setGeometry(300, 300, self.width(), len(self.game.map_) * 20 + 70 + self.flag_to_open_b.height() + 10 + 20)
        if len(self.game.map_) * 20 + 20 >= temp:
            self.setGeometry(300, 300, len(self.game.map_) * 20 + 20, self.height())
        elif len(self.game.map_) * 20 + 20 < temp and len(self.game.map_) * 20 + 20 < self.width():
            self.setGeometry(300, 300, temp, self.height())
        self.show()

    def gamerStat(self):
        # открывает окно с таблицей, которая получает данные из ДБ о прошлых играх.
        # данная таблица не изменяема с точки зрени пользователя и берёт информацию исключительно из ДБ
        # если успеешь присобач кнопку которая стирает данные из базы
        db = DBSaper(self, self.player)
        db.show()
        self.hide()

    def initUI(self):

        self.flag_to_open_b = QPushButton(self)
        self.flag_to_open_b.setText('Operation:' + self.operation)
        self.flag_to_open_b.clicked.connect(self.button_that_change_operation_Flag_and_Open)
        self.flag_to_open_b.move(30, 70)
        self.flag_to_open_b.resize(self.flag_to_open_b.sizeHint())

        self.labelresalts = QLabel(self)
        self.labelresalts.setText('')
        self.labelresalts.move(30 + self.flag_to_open_b.width() + 10, 70)

        self.play_b = QPushButton(self)
        self.play_b.setText('Play!')
        self.play_b.clicked.connect(self.newGameWindow)
        self.play_b.move(30, 40)
        self.play_b.resize(self.play_b.sizeHint())

        self.labels = [QLabel(self), QLabel(self), QLabel(self)]

        self.player_line = QLineEdit(self)
        self.player_line.setText('player1')
        self.player_line.move(self.play_b.x() + self.play_b.width() + 10, 40)
        self.labels[0].setText('Enter Player name:')
        self.labels[0].move(self.player_line.x(), 15)

        self.side_sb = QSpinBox(self)
        self.side_sb.setMinimum(10)
        self.side_sb.setMaximum(32)
        self.side_sb.move(self.player_line.x() + self.player_line.width() + 10, 40)
        self.side_sb.resize(self.side_sb.sizeHint())
        self.labels[1].setText('Side:')
        self.labels[1].move(self.side_sb.x(), 15)

        self.bombs = QSpinBox(self)
        self.bombs.setMaximum(99)
        self.bombs.setMinimum(3)
        self.bombs.move(self.side_sb.x() + self.side_sb.width() + 10, 40)
        self.bombs.resize(self.bombs.sizeHint())
        self.labels[2].setText('Num bombs:')
        self.labels[2].move(self.bombs.x(), 15)

        gamerStatAction = QAction('&Show Past Games', self)
        gamerStatAction.setShortcut('Ctrl+S')
        gamerStatAction.setStatusTip('You will see the results of previous games')
        gamerStatAction.triggered.connect(self.gamerStat)

        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Games')
        fileMenu.addAction(gamerStatAction)
        self.setGeometry(300, 300,
                         30 + self.play_b.width() + 10 + self.player_line.width() + 10 + self.side_sb.width() + 10
                         + self.bombs.width() + 30, 300)  # окно
        self.setWindowTitle('Saper')

    def button_that_change_operation_Flag_and_Open(self):
        if self.operation == 'open':
            self.operation = 'flag'
        else:
            self.operation = 'open'
        self.flag_to_open_b.setText('Operation:' + self.operation)

    def checkCell(self):
        x, y = 0, 0
        for i in self.pole:
            if self.sender() in i:
                x, y = i.index(self.sender()), self.pole.index(i)
        temp = self.game.player_check_point(x, y, self.operation)
        if temp == 'You are lose':
            self.breakGame()
        if self.game.check_player_win():
            self.congratulateThePlayer()
        for i in self.pole:
            for j in i:
                if self.game.map_bool[i.index(j)][self.pole.index(i)] == 'c':
                    j.setText('')
                    j.setStyleSheet('background: #76428a;')
                    continue
                j.setText(str(self.game.map_[i.index(j)][self.pole.index(i)]))
                j.setStyleSheet('background: #82a8ff;')
                if self.game.map_bool[i.index(j)][self.pole.index(i)] == 'f':
                    j.setText('⚑')
                    j.setStyleSheet('background: #f00000;')
                if self.game.map_bool[i.index(j)][self.pole.index(i)] == '?':
                    j.setText('?')
                    j.setStyleSheet('background: #82a8ff;')
                if self.game.map_[i.index(j)][self.pole.index(i)] == 0:
                    j.setText('')

    def congratulateThePlayer(self):
        # заносит информацию об игре в ДБ
        # юлокирует все кнопки, выводит поздравление с победой, предлагает новую игру
        for i in self.pole:
            for j in i:
                j.setEnabled(False)
        self.resalt = 'You are the winner! New game?)'
        self.labelresalts.setText(self.resalt)
        self.labelresalts.resize(self.labelresalts.sizeHint())
        self.addGame(self.side_number, self.bombs_number, 'win')
        self.playerGamesPlusOne()

    def breakGame(self):
        for i in self.pole:
            for j in i:
                j.setEnabled(False)
        self.resalt = 'You were wrong ... Try again?'
        self.labelresalts.setText(self.resalt)
        self.labelresalts.resize(self.labelresalts.sizeHint())
        self.addGame(self.side_number, self.bombs_number, 'lose')
        self.playerGamesPlusOne()
        # Зановит информацию об игре в ДБ
        # блокирует все кнопки, выводит сообщение о проигрыше, предлагает новую игру


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Saper()
    ex.show()
    sys.exit(app.exec())
