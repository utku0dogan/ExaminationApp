from email.mime import application
from PyQt5 import QtWidgets
import sys

from GorselEkle import GorselEkle
from psutil import cpu_count
from MainWindow import Ui_GirisEkrani
from SifreUnut import Ui_SifreUnuttum
from signUp import Ui_signUp
from addQuestion import Ui_SoruEkle
from dersEkle import Ui_dersEkle
from konuEkle import  Ui_addSection
from StudentEntryPage import Ui_StudentEntry
from sigma import Ui_sigma
from ayarlar import Ui_Ayarlar
import sqlite3
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,QLabel, QApplication)
from PyQt5.QtGui import QPixmap

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
        global currentUserID
        db.close() # close sonradan eklendi 
        if row:
            connection = sqlite3.connect('examination.db')
            connection.cursor()
            result = connection.execute("SELECT DISTINCT  id FROM users WHERE username =? AND password=? AND userType = ?",(username,password,userType))
            value = result.fetchall()
            currentUserID = value[0][0]
            connection.close()
            self.showMessageBox('basarili','giris basarili')
            if userType == 3:
                
                self.addQuestionShow()
            if userType == 2:
                self.showStudentEntry()
                
            
        else:
            self.showMessageBox('error','giris basarisiz')
        
    def showMessageBox(self,title,message):

        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()
    #------------------------------------SINAV SORUMLUSUNUN SORU EKLEME EKRANI BAŞLANGIÇ----------------------------------------------------------------
    
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

        
        showUnits(self)
        showLessons(self) #self sonradan eklendi
        self.addQuestionWindow.show()
        #---------------------------------------------------------------------------------
        
        #-------------------SINAV SORUMLUSU EKRANI BUTON BAĞLANTILARI--------------------
        self.addQuestionForm.DersEkle_btn.clicked.connect(self.showdersEkle)
        self.addQuestionForm.KonuEkle_btn.clicked.connect(self.showAddSection)
        self.addQuestionForm.Kaydet_btn.clicked.connect(self.saveQuestion)
        self.addQuestionForm.GorselEkle_btn.clicked.connect(self.GorselEkle)
        
        #--------------------------------------------------------------------------------
     #------------------------------------SINAV SORUMLUSUNUN SORU EKLEME EKRANI BİTİŞ----------------------------------------------------------------

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
    
    #--------------------------------------GÖRSEL EKLEME BAŞLANGIÇ-----------------------------------------------------------
    def GorselEkle(self):
        a = GorselEkle()
        path = a.openFileNameDialog()
        self.addQuestionForm.gorselPath_txt.setText(path)
    #--------------------------------------GÖRSEL EKLEME BİTİŞ-----------------------------------------------------------------
        

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

    # ------------------------------------SORUYU KAYDETME BAŞLANGIÇ-------------------------------------------------------------------
    def saveQuestion(self):
        LessonText = self.addQuestionForm.DersSec_cmbox.currentText()
        SectionText = self.addQuestionForm.KonuSec_cmbox.currentText()
        questionText = self.addQuestionForm.SoruMetni_txt.toPlainText()
        chooseA = self.addQuestionForm.Asikki_txt.text()
        chooseB = self.addQuestionForm.Bsikki_txt.text()
        chooseC = self.addQuestionForm.Csikki_txt.text()
        chooseD = self.addQuestionForm.Dsikki_txt.text()
        rightAnswer = self.addQuestionForm.RightAnswer_cmbox.currentText()
        imagePath = self.addQuestionForm.gorselPath_txt.text()
        
        
        connection = sqlite3.connect('examination.db')
        connection.cursor()
        result = connection.execute("SELECT DISTINCT  lid FROM lessons Where lessonName = ?",(LessonText,))
        value = result.fetchall()
        Lid = value[0][0]
        result = connection.execute("SELECT DISTINCT Uid FROM units WHERE unitName = ?",(SectionText,))
        value = result.fetchall()
        Uid = value[0][0]
        if imagePath == '':
            connection.execute("INSERT INTO questions (Lid, Uid, questionText, imagePath, chooseA, chooseB, chooseC, chooseD, rightAnswer) VALUES (?,?,?,?,?,?,?,?,?)",(Lid,Uid,questionText,'0',chooseA,chooseB,chooseC,chooseD,rightAnswer))
        else:
            connection.execute("INSERT INTO questions (Lid, Uid, questionText, imagePath, chooseA, chooseB, chooseC, chooseD, rightAnswer) VALUES (?,?,?,?,?,?,?,?,?)",(Lid,Uid,questionText,imagePath,chooseA,chooseB,chooseC,chooseD,rightAnswer))
        connection.commit()
        connection.close()

        self.showMessageBox("Basarili", "Soru Basariyla Eklendi")
        self.addQuestionForm.Asikki_txt.clear()
        self.addQuestionForm.Bsikki_txt.clear()
        self.addQuestionForm.Csikki_txt.clear()
        self.addQuestionForm.Dsikki_txt.clear()
        self.addQuestionForm.gorselPath_txt.clear()
        self.addQuestionForm.SoruMetni_txt.clear()
    #---------------------------------------------------------SORUYU KAYDETME BİTİŞ----------------------------------------------------------------



    #---------------------------------------------------------ÖĞRENCİ EKRANI BAŞLANGIÇ-------------------------------------------------------------
    def showStudentEntry(self):
        self.studentEntryWindow = QtWidgets.QDialog()
        self.studentEntryForm = Ui_StudentEntry()
        self.studentEntryForm.setupUi(self.studentEntryWindow)
        connection = sqlite3.connect('examination.db')
        connection.cursor()
        
        result = connection.execute("SELECT userName FROM users WHERE id = ?",(currentUserID,))
        value = result.fetchall()
        currentUserName = value[0][0]
        connection.close()
        self.studentEntryForm.welcome_lbl.setText("Hos geldiniz, " + currentUserName + ' basarilar...')
        self.studentEntryWindow.show()
        self.studentEntryForm.sigma_btn.clicked.connect(self.showSigmaModule)
        self.studentEntryForm.ayarlar_btn.clicked.connect(self.ShowUserSettings)


    def showSigmaModule(self):
        self.sigmaWindow = QtWidgets.QDialog()
        self.sigmaForm = Ui_sigma()
        self.sigmaForm.setupUi(self.sigmaWindow)
        
            
        
        self.extractQuestionDB()
    
    def extractQuestionDB(self):
        
        connection = sqlite3.connect('examination.db')
        connection.cursor()
        result = connection.execute("SELECT Qid FROM questions")
        values = result.fetchall()
        
        connection.close()
        Qid = []
        for i in range(len(values)):
            Qid.append(values[i][0])
        print(Qid)

        for i in range(len(Qid)):
            connection = sqlite3.connect('examination.db')
            connection.cursor()
            result = connection.execute("SELECT imagePath FROM questions WHERE Qid = ?",(Qid[i],))
            value = result.fetchone()
            connection.close()
            if value[0][0] == '0':
                connection = sqlite3.connect('examination.db')
                connection.cursor()
                result = connection.execute("SELECT questionText, chooseA, chooseB, choosec, chooseD  FROM questions WHERE Qid = ?",(Qid[i],))
                values = result.fetchone()
                connection.close()
                
                self.showQuestion(values)
                
            else:
                connection = sqlite3.connect('examination.db')
                connection.cursor()
                result = connection.execute("SELECT questionText, chooseA, chooseB, choosec, chooseD, imagePath  FROM questions WHERE Qid = ?",(Qid[i],))
                values = result.fetchone()
                connection.close()
                
                self.showQuestion(values)

    def showQuestion(self, values):
        if len(values) == 5:
            self.sigmaForm.question_txt.setText(values[0])
            self.sigmaForm.a_txt.setText(values[1])
            self.sigmaForm.b_txt.setText(values[2])
            self.sigmaForm.c_txt.setText(values[3])
            self.sigmaForm.d_txt.setText(values[4])
            
            self.sigmaWindow.show()
            
        if len(values) == 6:
            self.sigmaForm.question_txt.setText(values[0])
            self.sigmaForm.a_txt.setText(values[1])
            self.sigmaForm.b_txt.setText(values[2])
            self.sigmaForm.c_txt.setText(values[3])
            self.sigmaForm.d_txt.setText(values[4])
            path = values[5]
            
            self.pixmap = QPixmap(path)
            self.sigmaForm.image_lbl.setPixmap(self.pixmap)
            self.sigmaForm.image_lbl.setScaledContents(True)
            
            self.sigmaWindow.show()
            

        
    def ShowUserSettings(self):

        self.settingsWindow = QtWidgets.QDialog()
        self.settingsForm = Ui_Ayarlar()
        self.settingsForm.setupUi(self.settingsWindow)

        self.settingsWindow.show()

        self.settingsForm.kaydet_btn.clicked.connect(self.AyarKaydet)

    def AyarKaydet(self):
        birDongu = self.settingsForm.birDongu_txt.text()
        ikiDongu = self.settingsForm.ikiDongu_txt.text()
        ucDongu = self.settingsForm.ucDongu_txt.text()
        dortDongu = self.settingsForm.dortDongu_txt.text()
        besDongu = self.settingsForm.besDongu_txt.text()
        altiDongu = self.settingsForm.altiDongu_txt.text()
        connection = sqlite3.connect('examination.db')
        connection.cursor()
        connection.execute(f"UPDATE settings SET first = {birDongu}, second = {ikiDongu}, third = {ucDongu}, fourth = {dortDongu}, fifth = {besDongu}, sixth = {altiDongu} WHERE id = ?",(currentUserID,))
        connection.commit()
        connection.close()
        self.showMessageBox("Basarili","Ayarlar basariyla degisti")
        
        self.settingsWindow.close()
        







    #-------------------------------------------------------ÖĞRENCİ EKRANI BİTİŞ------------------------------------------------------------------



    #---------------------------------------------------------KAYIT BAŞLANGIÇ----------------------------------------------------------------------
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

        if userType == 2:
            connection = sqlite3.connect('examination.db')
            connection.cursor()
            result = connection.execute("SELECT id From users Where userName = ? AND password = ?",(username, password))
            value = result.fetchone()
            id = value[0]
            
            connection.execute("INSERT INTO settings (id) VALUES (?)",(id,))
            connection.commit()
            connection.close()
        self.showMessageBox('Bilgi', f'{username} Kayit İslemi Basarili, {self.signUpForm.cmbKullaniciTip.currentText()} olarak Giris Yapabilirsiniz.')
        self.signUpWindow.close()

    #---------------------------------------------------------------KAYIT BİTİŞ---------------------------------------------------------------------
    

    #----------------------------------------------------------ŞİFRE UNUT BAŞLANGIÇ-----------------------------------------------------------------
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
    #--------------------------------------------------------ŞİFRE UNUT BİTİŞ----------------------------------------------------------------------   


def app():
    app = QtWidgets.QApplication(sys.argv)
    win = myApp()
    win.show()
    sys.exit(app.exec_())

app()
