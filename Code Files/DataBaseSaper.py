import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class DBSaper(QMainWindow):
    def __init__(self, main=None, player='player1'):
        self.main = main
        super().__init__(main)
        uic.loadUi('gamerStat.ui', self)
        self.player = player
        self.con = sqlite3.connect('Saper_Games_and_Players.db')
        self.show_b.clicked.connect(self.showGames)
        self.back_b.clicked.connect(self.back)
        self.showPlayer_b.clicked.connect(self.showPlayers)
        self.showAll_b.clicked.connect(self.showAllGame)
        self.deleteAllGames_b.clicked.connect(self.deleteAllGames)

    def back(self):
        self.close()
        self.main.show()

    def deleteAllGames(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        cur.execute('''DELETE from Game
        WHERE id BETWEEN 1 AND 100001''')
        cur.execute('''UPDATE Players
        SET Number_of_games = 0
        WHERE id BETWEEN 1 AND 1001''')

        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setItem(0, 0, QTableWidgetItem('Side'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem('Num of Bomb'))
        self.tableWidget.setItem(0, 2, QTableWidgetItem('Player'))
        self.tableWidget.setItem(0, 3, QTableWidgetItem('Result'))

        self.con.commit()

    def showGames(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute('''Select side, bombs, player, result from Game WHERE player=
        (Select id from Players WHERE PlayerName like ?)''',
                             (self.player,)).fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result) + 1)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setItem(0, 0, QTableWidgetItem('Side'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem('Num of Bomb'))
        self.tableWidget.setItem(0, 2, QTableWidgetItem('Player'))
        self.tableWidget.setItem(0, 3, QTableWidgetItem('Result'))
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i + 1, j, QTableWidgetItem(str(val)))

    def showPlayers(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute(
            '''Select PlayerName, Number_of_Games from Players WHERE id BETWEEN 1 AND 1001''').fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result) + 1)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setItem(0, 0, QTableWidgetItem('Player Name'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem('Numb of Game'))
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i + 1, j, QTableWidgetItem(str(val)))

    def showAllGame(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute(
            '''Select side, bombs, player, result from Game WHERE id BETWEEN 0 AND 1001''').fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result) + 1)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setItem(0, 0, QTableWidgetItem('Side'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem('Num of Bomb'))
        self.tableWidget.setItem(0, 2, QTableWidgetItem('Player'))
        self.tableWidget.setItem(0, 3, QTableWidgetItem('Result'))
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                if j == 2:
                    temp = cur.execute('Select PlayerName from Players WHERE id = ?', (val,)).fetchall()[0][0]
                    self.tableWidget.setItem(i + 1, j, QTableWidgetItem(temp))
                    continue
                self.tableWidget.setItem(i + 1, j, QTableWidgetItem(str(val)))
