import psutil
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication


class Login:

    def __init__(self):
        path = 'login.ui'
        self.ui = QUiLoader().load(path)
        self.ui.button1.clicked.connect(self.checkout)

    def checkout(self):
        username = self.ui.username.text()
        password = self.ui.password.text()
        print(username)
        print(password)
        if username == "admin" and password == "123456":
            print("登录成功")
        else:
            print("密码错误")


if __name__ == '__main__':
    app = QApplication([])
    login_1 = Login()
    login_1.ui.show()
    app.exec_()