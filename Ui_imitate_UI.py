# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'imitate_UI.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QTextBrowser, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(445, 315)
        self.interface_label = QLabel(Form)
        self.interface_label.setObjectName(u"interface_label")
        self.interface_label.setGeometry(QRect(20, 30, 71, 21))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.interface_label.setFont(font)
        self.interface_edit = QLineEdit(Form)
        self.interface_edit.setObjectName(u"interface_edit")
        self.interface_edit.setGeometry(QRect(20, 60, 141, 21))
        self.gateway_label = QLabel(Form)
        self.gateway_label.setObjectName(u"gateway_label")
        self.gateway_label.setGeometry(QRect(20, 100, 81, 21))
        self.gateway_label.setFont(font)
        self.gateway_edit = QLineEdit(Form)
        self.gateway_edit.setObjectName(u"gateway_edit")
        self.gateway_edit.setGeometry(QRect(20, 130, 141, 21))
        self.target_label = QLabel(Form)
        self.target_label.setObjectName(u"target_label")
        self.target_label.setGeometry(QRect(20, 170, 81, 21))
        self.target_label.setFont(font)
        self.target_edit = QLineEdit(Form)
        self.target_edit.setObjectName(u"target_edit")
        self.target_edit.setGeometry(QRect(20, 200, 141, 21))
        self.Description_label = QLabel(Form)
        self.Description_label.setObjectName(u"Description_label")
        self.Description_label.setGeometry(QRect(190, 10, 111, 31))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.Description_label.setFont(font1)
        self.Description_text = QTextBrowser(Form)
        self.Description_text.setObjectName(u"Description_text")
        self.Description_text.setGeometry(QRect(190, 50, 231, 171))
        self.attack_button = QPushButton(Form)
        self.attack_button.setObjectName(u"attack_button")
        self.attack_button.setGeometry(QRect(40, 250, 81, 31))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.attack_button.setFont(font2)
        self.scan_button = QPushButton(Form)
        self.scan_button.setObjectName(u"scan_button")
        self.scan_button.setGeometry(QRect(260, 250, 81, 31))
        font3 = QFont()
        font3.setPointSize(10)
        self.scan_button.setFont(font3)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.interface_label.setText(QCoreApplication.translate("Form", u"Interface:", None))
        self.gateway_label.setText(QCoreApplication.translate("Form", u"Gateway:", None))
        self.target_label.setText(QCoreApplication.translate("Form", u"Target_ip:", None))
        self.Description_label.setText(QCoreApplication.translate("Form", u"Description:", None))
        self.attack_button.setText(QCoreApplication.translate("Form", u"ARP Attack", None))
        self.scan_button.setText(QCoreApplication.translate("Form", u"Scan Hosts", None))
    # retranslateUi

