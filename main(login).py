from email.mime import application
from PyQt5 import QtWidgets
import sys

from psutil import cpu_count
from MainWindow import Ui_GirisEkrani
from SifreUnut import Ui_SifreUnuttum
from signUp import Ui_signUp
from addQuestion import Ui_SoruEkle
from dersEkle import Ui_dersEkle
from konuEkle import  Ui_addSection
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
        elif self.loginUi.rdBtnOgrenci.isChecked():
            userType = 2
        elif self.loginUi.rdBtnSinavSorumlusu.isChecked():
            userType = 3
        db = sqlite3.connect('examination.db')
        cursor = db.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username =? AND password=? AND userType = ?",(username,password,userType))
        row = cursor.fetchone()
        db.close() # close sonradan eklendi 
        if row:
            self.showMessageBox('basarili','giris basarili')
            if userType == 3:
                self.addQuestionShow()
                
            
        else:
            self.showMessageBox('error','giris basarisiz')
        
    def showMessageBox(self,title,message):

        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()
    
    def addQuestionShow(self): #sinav sorumlusunun soru ekleme kısmı
        #--------------------------------------------------------------------------------
        self.addQuestionWindow = QtWidgets.QDialog()
        self.addQuestionForm = Ui_SoruEkle()        

        def showLessons(self): #database'deki dersleri combobox'ta göstermek
            connection = sqlite3.connect('examination.db')
            connection.cursor()
            result = connection.execute("SELECT lessonName FROM lessons")
            
            values = result.fetchall()
            connection.close()
            print(values)
            for i in range(len(values)):
                self.addQuestionForm.DersSec_cmbox.addItem(values[i][0])
        
        def showUnits(self): #database'deki uniteleri combobox'ta göstermek
            
        
            connection = sqlite3.connect('examination.db')
            connection.cursor()
            result = connection.execute("SELECT unitName FROM units")
            
            values = result.fetchall()
            connection.close()
            for i in range(len(values)):
                self.addQuestionForm.KonuSec_cmbox.addItem(values[i][0])
                    
        self.addQuestionForm.setupUi(self.addQuestionWindow)

        #showLessons(self) #self sonradan eklendi
        showUnits(self)
        showLessons(self)
        self.addQuestionWindow.show()
        #---------------------------------------------------------------------------------
        
        #-------------------SINAV SORUMLUSU EKRANI BUTON BAĞLANTILARI--------------------
        self.addQuestionForm.DersEkle_btn.clicked.connect(self.showdersEkle)
        self.addQuestionForm.KonuEkle_btn.clicked.connect(self.showAddSection)
        self.addQuestionForm.Kaydet_btn.clicked.connect(self.saveQuestion)
        #--------------------------------------------------------------------------------


    # --------------------------VERİTABANINA YENİ BİR DERS EKLEME BAŞLANGIÇ-----------------------------------------           
    def showdersEkle(self):    #icerde olmuyor
        self.showDersEkleWindow = QtWidgets.QDialog()
        self.showDersEkleForm = Ui_dersEkle()
        self.showDersEkleForm.setupUi(self.showDersEkleWindow)
        self.showDersEkleWindow.show()
        self.showDersEkleForm.dersEkle_btn.clicked.connect(self.dersEkle)
            
    def dersEkle(self):
        lessonName = self.showDersEkleForm.lineEdit.text()
        print(lessonName)
        connection = sqlite3.connect('examination.db')
        connection.cursor()
        connection.execute("INSERT INTO lessons (lessonName) VALUES(?)",(lessonName,))
        connection.commit()
        connection.close()
        
        self.showDersEkleWindow.close()
        
        self.addQuestionShow() # ? eklenen dersin güncel olarak gözükmesi icin addQuestionShow'u tekrar cagırmamız gerek
    
    #--------------------------------------VERİ TABANINA YENİ BİR DERS EKLEME BİTİŞ------------------------------------------

    #--------------------------------------VERİTABANINA DERSE BAĞLI KONU EKLEME BAŞLANGIÇ----------------------------------------
    def showAddSection(self):
        self.addSectionWindow = QtWidgets.QDialog()
        self.addSectionForm = Ui_addSection()
        self.addSectionForm.setupUi(self.addSectionWindow)
        self.addSectionWindow.show()
       
        def showLesson(self): # konu eklenecek dersi secmek icin combobox'ta göstermek 
            connection = sqlite3.connect('examination.db')
            connection.cursor()
            result = connection.execute("SELECT lessonName FROM lessons")
            
            values = result.fetchall()
            connection.close()
            for i in range(len(values)):
                 self.addSectionForm.konEkle_cmb.addItem(values[i][0])
            
        showLesson(self)
        self.addSectionForm.konuEkle_btn.clicked.connect(self.AddSection)

    def AddSection(self):
        LessonText = self.addSectionForm.konEkle_cmb.currentText()
        unitName = self.addSectionForm.konuEkle_txt.text()
        connection = sqlite3.connect('examination.db')
        connection.cursor()
        result = connection.execute("SELECT DISTINCT  lid FROM lessons Where lessonName = ?",(LessonText,))
        value = result.fetchall()
        Lid = value[0][0]
        connection.execute("Insert Into units (Lid, unitName) VALUES(?,?)",(Lid, unitName))
        connection.commit()
        connection.close()
        self.addSectionWindow.close()
        self.addQuestionShow()
        

    # ------------------------------------VERİ TABANINA DERSE BAĞLI KONU EKLEME BİTİŞ------------------------------------------------------------------

    def addImage(self):
        pass

    def saveQuestion(self):
        LessonText = self.addQuestionForm.DersSec_cmbox.currentText()
        SectionText = self.addQuestionForm.KonuSec_cmbox.currentText()
        questionText = self.addQuestionForm.SoruMetni_txt.text()
        chooseA = self.addQuestionForm.Asikki_txt.text()
        chooseB = self.addQuestionForm.Bsikki_txt.text()
        chooseC = self.addQuestionForm.Csikki_txt.text()
        chooseD = self.addQuestionForm.Dsikki_txt.text()
        rightAnswer = self.addQuestionForm.RightAnswer_cmbox.currentText()
        
        connection = sqlite3.connect('examination.db')
        connection.cursor()
        result = connection.execute("SELECT DISTINCT  lid FROM lessons Where lessonName = ?",(LessonText,))
        value = result.fetchall()
        Lid = value[0][0]
        result = connection.execute("SELECT DISTINCT Uid FROM units WHERE unitName = ?",(SectionText,))
        value = result.fetchall()
        Uid = value[0][0]

        connection.execute("INSERT INTO questions (Lid, Uid, questionText, chooseA, chooseB, chooseC, chooseD, rightAnswer) VALUES (?,?,?,?,?,?,?,?)",(Lid,Uid,questionText,chooseA,chooseB,chooseC,chooseD,rightAnswer))
        connection.commit()
        connection.close()

        self.showMessageBox("Basarili", "Soru Basariyla Eklendi")
        

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
        
        print(row)
        if row:
            connection = sqlite3.connect('examination.db')
            connection.execute("UPDATE users SET password = ? WHERE userName = ? AND validationAnswer = ?",(newPassword, username,validation))
            connection.commit()
            connection.close()
            self.showMessageBox('basarili','sifreniz basariyla yenilendi')
            self.sifreUnutWindow.close()
        
        else:
            self.showMessageBox('error','giris bilgileri yanlis')
        
        connection.close()     
        
def app():
    app = QtWidgets.QApplication(sys.argv)
    win = myApp()
    win.show()
    sys.exit(app.exec_())

app()
