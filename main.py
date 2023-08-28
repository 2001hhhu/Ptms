# 这是一个示例 Python 脚本。
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QMessageBox
from PySide2.QtUiTools import QUiLoader
from qt_work import Stats
from network_state import Network
# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。



# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':

    app = QApplication([])
    stats = Stats()
    stats.ui.show()
    app.exec_()

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
