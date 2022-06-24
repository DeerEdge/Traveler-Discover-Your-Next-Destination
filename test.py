import os
import sys

from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets


def main():

    print(
        f"PyQt5 version: {QtCore.PYQT_VERSION_STR}, Qt version: {QtCore.QT_VERSION_STR}"
    )

    app = QtWidgets.QApplication(sys.argv)
    # filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, filter="PDF (*.pdf)")
    filename = os.path.abspath('Application Files/FBLA Manual + Documentation.pdf')
    # if not filename:
    #     print("please select the .pdf file")
    #     sys.exit(0)
    view = QtWebEngineWidgets.QWebEngineView()
    settings = view.settings()
    settings.setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
    url = QtCore.QUrl.fromLocalFile(filename)
    view.load(url)
    view.resize(640, 480)
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()