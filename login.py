import psutil
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from qt_work import Stats


class Login:

    def __init__(self):
        path = 'login.ui'
        self.ui = QUiLoader().load(path)
        self.ui.button1.clicked.connect(self.checkout)
        self.ui.button1.setShortcut('Enter')
        self.ui.lineedit_2.setEchoMode(self.ui.lineedit_2.Password)
        self.stats = Stats()

    def checkout(self):
        username = self.ui.lineedit_1.text()
        password = self.ui.lineedit_2.text()
        print(username)
        print(password)
        if username == "admin" and password == "123456":
            print("登录成功")
            self.stats.ui.show()
            self.ui.close()
        else:
            print("密码错误")
            self.ui.lineedit_2.setToolTip("密码错误")


if __name__ == '__main__':
    app = QApplication([])
    login_1 = Login()
    login_1.ui.show()
    app.exec_()