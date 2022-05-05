from email.mime import application
from PyQt5 import QtWidgets
import sys
from MainWindow import Ui_GirisEkrani
from SifreUnut import Ui_SifreUnuttum
from signUp import Ui_signUp
import sqlite3

class myApp(QtWidgets.QMainWindow):

    def __init__(self):
        super(myApp, self).__init__()
        self.loginUi = Ui_GirisEkrani()
        self.loginUi.setupUi(self)
        self.loginUi.btnGiris.clicked.connect(self.login)
        self.loginUi.btnKayit.clicked.connect(self.signUpShow)
        self.loginUi.btnSifremiUnuttum.clicked.connect(self.ShowSifreUnut)

    
    def login(self):
    
        username = self.loginUi.txtKullaniciAd.text()
        password = self.loginUi.txtSifre.text()
        userType = 0
        if self.loginUi.rdBtnAdmin.isChecked():
            userType = 1
            print("a")
        elif self.loginUi.rdBtnOgrenci.isChecked():
            userType = 2
        elif self.loginUi.rdBtnSinavSorumlusu.isChecked():
            userType = 3
        db = sqlite3.connect('examination.db')
        cursor = db.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username =? AND password=? AND userType = ?",(username,password,userType))
        row = cursor.fetchone()
        
        if row:
            self.showMessageBox('basarili','giris basarili')
        else:
            self.showMessageBox('error','giris basarisiz')
        


    def showMessageBox(self,title,message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()
    
    def signUpShow(self):
        self.signUpWindow = QtWidgets.QDialog()
        self.signUpForm = Ui_signUp()
        self.signUpForm.setupUi(self.signUpWindow)
        self.signUpWindow.show()
        self.signUpForm.pushButton.clicked.connect(self.signUp)

    def signUp(self):
        name = self.signUpForm.txtiSim.text()
        surname = self.signUpForm.txtSoyisim.text()
        username = self.signUpForm.txtKullaniciAd.text()
        password = self.signUpForm.txtSifre.text()
        validation = self.signUpForm.txtGuvenlikAnswer.text()
        userType = 0
        if self.signUpForm.cmbKullaniciTip.currentText()== 'admin':
            userType = 1
        elif self.signUpForm.cmbKullaniciTip.currentText() == 'ogrenci':
            userType = 2
        elif self.signUpForm.cmbKullaniciTip.currentText() == 'sinav sorumlusu':
            userType = 3

        connection = sqlite3.connect('examination.db')
        connection.cursor()
        
        

            
        connection.execute("INSERT INTO USERS (userType, name, surname, userName, password, validationAnswer) VALUES(?,?,?,?,?,?)",(userType,name,surname,username,password,validation))
            
        connection.commit()
        connection.close()
        self.showMessageBox('Bilgi', f'{username} Kayit İslemi Basarili, {self.signUpForm.cmbKullaniciTip.currentText()} olarak Giris Yapabilirsiniz.')
        self.signUpWindow.close()
        
    def ShowSifreUnut(self):
        self.sifreUnutWindow = QtWidgets.QDialog()
        self.sifreUnutForm = Ui_SifreUnuttum()
        self.sifreUnutForm.setupUi(self.sifreUnutWindow)
        self.sifreUnutWindow.show()
        self.sifreUnutForm.btnSifreDegis.clicked.connect(self.SifreUnut)
    
    def SifreUnut(self):
        validation = self.sifreUnutForm.txtGuvenlik.text()
        username = self.sifreUnutForm.txtKullanici.text()
        newPassword = self.sifreUnutForm.txtYeniSifre.text()
        


        connection = sqlite3.connect('examination.db')
        
        
        result = connection.execute("SELECT * FROM users WHERE username =? AND validationAnswer=?",(username,validation))
        row = result.fetchone()
        connection.close()
        print(row)
        if row:
            connection = sqlite3.connect('examination.db')
            connection.execute("UPDATE users SET password = ? WHERE userName = ? AND validationAnswer = ?",(newPassword, username,validation))
            connection.commit()
            connection.close()
            self.showMessageBox('basarili','sifreniz basariyla yenilendi')
            self.sifreUnutWindow.close()
            
        else:
            self.showMessageBox('error','giris basarisiz')
            
        

def app():
    app = QtWidgets.QApplication(sys.argv)
    win = myApp()
    win.show()
    sys.exit(app.exec_())

app()
