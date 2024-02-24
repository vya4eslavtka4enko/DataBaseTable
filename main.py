import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QLabel,QApplication,QMainWindow,
                             QTableWidget,QTableWidgetItem,QDialog,
                             QVBoxLayout,QLineEdit,QComboBox,QPushButton,QToolBar)
from PyQt6.QtGui import QAction, QIcon
import sqlite3
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Managment System")
        self.setFixedWidth(500)
        self.setFixedHeight(300)
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        search_menu_item = self.menuBar().addMenu('&Serch')

        add_student_action = QAction(QIcon('icons/add.png'),"Add Student",self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About",self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        search_action = QAction(QIcon('icons/search.png'),'Search Student',self)
        search_action.triggered.connect(self.search_student)
        search_menu_item.addAction(search_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Id','Name',"Course","Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        #Create ToolBar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)
    def load_data(self):
        connection = sqlite3.connect('database.db')
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number,row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        print(list(result))
        connection.close()
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search_student(self):
        search_dialog = SearchDialog()
        search_dialog.exec()

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add student data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        #add student name widget
        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        #add combo box of courses
        self.course_name = QComboBox()
        course = ["Biology","Math","Astronomy","Physics"]
        self.course_name.addItems(course)
        layout.addWidget(self.course_name)
        self.setLayout(layout)
        #add mobile
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)
        #add submit button
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)


    def add_student(self):
        name = self.student_name.text()
        courses = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO students (name,course,mobile) VALUES (?,?,?)',
                       (name,courses,mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search Student')
        self.setFixedWidth(500)
        self.setFixedHeight(300)
        layout_new = QVBoxLayout()

        self.search_line = QLineEdit()
        self.search_line.setPlaceholderText('Search')
        layout_new.addWidget(self.search_line)

        self.button_search = QPushButton("Search")
        layout_new.addWidget(self.button_search)

        self.button_search.clicked.connect(self.search_student_function)
        self.setLayout(layout_new)


    def search_student_function(self):
        name = self.search_line.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name=?",(name,))
        rows = list(result)
        print(rows)
        items = main_window.table.findItems(name,Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_window.table.item(item.row(),1).setSelected(True)
        cursor.close()
        connection.close()


app = QApplication(sys.argv)
main_window=MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())