from ast import get_source_segment
from email.mime import application
from unittest import result
from PyQt5 import QtWidgets
import sys
import time
import datetime
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from sklearn.feature_selection import SelectFromModel
from GorselEkle import GorselEkle
from psutil import cpu_count
from MainWindow import Ui_GirisEkrani
from SifreUnut import Ui_SifreUnuttum
from signUp import Ui_signUp
from addQuestion import Ui_SoruEkle
from ciktial import Ui_ciktiAl
from admin import Ui_admin
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
        self.loginUi.txtSifre.setEchoMode(QtWidgets.QLineEdit.Password)
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
            if userType == 1:
                self.showAdminEntry()
                
            
        else:
            self.showMessageBox('error','giris basarisiz')
        
    def showMessageBox(self,title,message):

        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()
    
    #admin******************************************

    def showAdminEntry(self):
        self.adminWindow = QtWidgets.QDialog()
        self.adminForm = Ui_admin()
        self.adminForm.setupUi(self.adminWindow)
        self.adminWindow.show()
        
        connection = sqlite3.connect("examination.db")
        cur = connection.cursor()
        self.adminForm.tableWidget.setRowCount(100)
        tablerow = 0
        for row in cur.execute("SELECT Qid, questionText, isActive FROM questions WHERE isActive = ?",(0,)):
            self.adminForm.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.adminForm.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.adminForm.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
            tablerow+=1
        
        
        result = connection.execute("SELECT Qid, questionText, isActive FROM questions WHERE isActive = ?",(0,))
        values = result.fetchall()
        rowPosition = self.adminForm.tableWidget.rowCount()
        
        connection.close()
        
        for satirIndeks, satirVeri in enumerate(values):
            self.adminForm.tableWidget.insertRow(rowPosition)
            for sutunIndeks, sutunVeri in enumerate (satirVeri):
                
                self.adminForm.tableWidget.setItem(satirIndeks,sutunIndeks,QtWidgets.QTableWidgetItem(str(sutunVeri)) )
                
        self.adminForm.pushButton.clicked.connect(self.degis)

    def degis(self):
        secili = self.adminForm.tableWidget.selectedItems()
        secili_id = int(secili[0].text())

        connection = sqlite3.connect("examination.db")
        connection.cursor()
        connection.execute("UPDATE questions SET isActive= ? WHERE Qid =?",(1,secili_id))
        connection.commit()
        connection.close()
        self.adminWindow.close()
        self.showAdminEntry()
    
    
    
    
    #---------------------------------------------admin bitiş---------------------------------------------------
    
    
    
    
    
    
    
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



    #########################################################ÖĞRENCİ EKRANI BAŞLANGIÇ####################################################################
    
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
        
        self.studentEntryForm.ayarlar_btn.clicked.connect(self.ShowUserSettings)
        self.studentEntryForm.istatistik_btn.clicked.connect(self.ShowStats)
        global g_qid
        g_qid=0
        global g_soru
        global sigma_g_soru
        sigma_g_soru = 0
        g_soru = 0
        global answers
        answers= []
        self.studentEntryForm.zayifKonu_btn.clicked.connect(self.ExtQuestions)
        self.studentEntryForm.sigma_btn.clicked.connect(self.SigmaQuestions)
    #---------------------------------------------------sigma ekrani baslangic------------------------------
    def SigmaQuestions(self):
        self.connections = sqlite3.connect('examination.db')
        self.connections.cursor()
        self.results = self.connections.execute("SELECT * FROM questions ORDER BY random() LIMIT 10")
        self.sigmaQuestions = self.results.fetchall()
        self.sigmaCorrectAnswers = []
        self.showSigmaModule(sigma_g_soru)
    
    
    
    
    def showSigmaModule(self,sigma_g_soru):
        self.ShowSigmaWindow = QtWidgets.QDialog()
        self.ShowSigmaForm = Ui_sigma()
        self.ShowSigmaForm.setupUi(self.ShowSigmaWindow)
        self.ShowSigmaWindow.show()
        
        self.ShowSigmaForm.question_txt.setText(self.sigmaQuestions[sigma_g_soru][3])
        self.ShowSigmaForm.a_txt.setText(self.sigmaQuestions[sigma_g_soru][5])
        self.ShowSigmaForm.b_txt.setText(self.sigmaQuestions[sigma_g_soru][6])
        self.ShowSigmaForm.c_txt.setText(self.sigmaQuestions[sigma_g_soru][7])
        self.ShowSigmaForm.d_txt.setText(self.sigmaQuestions[sigma_g_soru][8])

        if not self.sigmaQuestions[sigma_g_soru][4] == '0':
            path = self.sigmaQuestions[sigma_g_soru][4]
            self.pixmap = QPixmap(path)
            self.ShowSigmaForm.image_lbl.setPixmap(self.pixmap)
            self.ShowSigmaForm.image_lbl.setScaledContents(True)
        else:
            self.ShowSigmaForm.image_lbl.setText(" ")
        self.ShowSigmaForm.submit_btn.clicked.connect(lambda: self.submitButton(sigma_g_soru))

    def submitButton(self,sigma_g_soru):
        sigma_g_soru+=1
        self.ShowSigmaWindow.close()
        if sigma_g_soru == 10:
            self.ShowSigmaWindow.close()
            self.showStudentEntry()
        else:
            self.showSigmaModule(sigma_g_soru)
    #----------------------------------------------exam ekrani baslangic---------------------------------------------------------------
        #---------------------------------------------DB'DEN VERİ CEKME------------------------------------------------------------
    
    def ExtQuestions(self):
        
        self.connection = sqlite3.connect('examination.db')
        self.connection.cursor()
        self.result = self.connection.execute("SELECT * FROM questions ORDER BY random() LIMIT 10")
        self.questions = self.result.fetchall()
        self.correctAnswers = []
    
        for i in self.questions:
            self.correctAnswers.append(i[9])
        self.ShowExam(g_soru)
    
    def ShowExam(self,g_soru):
        self.ShowExamWindow = QtWidgets.QDialog()
        self.ShowExamForm = Ui_sigma()
        self.ShowExamForm.setupUi(self.ShowExamWindow)
        self.ShowExamWindow.show()
        
        global g_NumberQ
        g_NumberQ = len(self.questions)
        CurrentQuestionID = self.questions[g_soru][0]
        
        self.ShowExamForm.question_txt.setText(self.questions[g_soru][3])
        self.ShowExamForm.a_txt.setText(self.questions[g_soru][5])
        self.ShowExamForm.b_txt.setText(self.questions[g_soru][6])
        self.ShowExamForm.c_txt.setText(self.questions[g_soru][7])
        self.ShowExamForm.d_txt.setText(self.questions[g_soru][8])

        if not self.questions[g_soru][4] == '0':
            path = self.questions[g_soru][4]
            self.pixmap = QPixmap(path)
            self.ShowExamForm.image_lbl.setPixmap(self.pixmap)
            self.ShowExamForm.image_lbl.setScaledContents(True)
        else:
            self.ShowExamForm.image_lbl.setText(" ")
        self.ShowExamForm.submit_btn.clicked.connect(lambda: self.sumbitbutton(g_soru))
        
        

    def sumbitbutton(self,g_soru): 
        answer= ""
        g_soru+=1
        if self.ShowExamForm.a_radio.isChecked():
            answer = 'A'
        elif self.ShowExamForm.b_radio.isChecked():
            answer = 'B'
        elif self.ShowExamForm.c_radio.isChecked():
            answer = 'C'
        elif self.ShowExamForm.d_radio.isChecked():
            answer = 'D'
        

        
        
        answers.append(answer)
        self.ShowExamWindow.close()
        
        if g_soru == 10:
            self.ShowExamWindow.close()
        
            dogruSayisi = 0
            yanlisSayisi = 0
            for i in range(10):
                if self.correctAnswers[i] == answers[i]:
                    dogruSayisi +=1
                else:
                    yanlisSayisi +=1
            self.showMessageBox("SONUC",f"Sinav bitti dogru cevap sayisi {dogruSayisi}, yanlis cevap sayisi {yanlisSayisi} ")
            self.showStudentEntry()

        else:
            rightAnswer = self.questions[g_soru][9]
            Lid = self.questions[g_soru][1]
            Uid = self.questions[g_soru][2]
            if self.questions[g_soru][9] == answer:
                isTrue = 1
            else:
                isTrue = 0
        
            self.saveData(answer,rightAnswer, Lid, Uid, isTrue)
            self.ShowExam(g_soru)
#------------------------------istatistik başlangıc--------------------------------------------
    def saveData(self,answer,rightAnswer, Lid, Uid, isTrue):
        
        connection = sqlite3.connect('examination.db')
        connection.cursor()
        result = connection.execute("SELECT DISTINCT lessonName FROM lessons WHERE Lid = ?",(Lid,))
        value = result.fetchone()
        lesson = value[0]
        result = connection.execute("SELECT DISTINCT unitName FROM units WHERE Uid = ?",(Uid,)) 
        value = result.fetchone()
    
        unit = value[0]
        connection.execute("Insert Into studentstats (id, answer,rightanswer,lesson,unit,result) VALUES(?,?,?,?,?,?)",(currentUserID, str(answer),rightAnswer, lesson, str(unit), int(isTrue)))
        connection.commit()
        connection.close()

    def ShowStats(self):
        self.ShowStatsWindow = QtWidgets.QDialog()
        self.ShowStatsForm = Ui_ciktiAl()
        self.ShowStatsForm.setupUi(self.ShowStatsWindow)
        self.ShowStatsWindow.show()
        connection = sqlite3.connect('examination.db')
        connection.cursor()
        result = connection.execute("SELECT lessonName FROM lessons")
            
        values = result.fetchall()
        connection.close()
        for i in range(len(values)):
            self.ShowStatsForm.dersSec_cmb.addItem(values[i][0])
        
        self.ShowStatsForm.dersSec_cmb.activated[str].connect(self.showDersstats)
        
        connection = sqlite3.connect('examination.db')
        connection.cursor()
        result = connection.execute("SELECT unitName FROM units")
            
        values = result.fetchall()
        connection.close()
        for i in range(len(values)):
            self.ShowStatsForm.konuSec_cmb.addItem(values[i][0])

        self.ShowStatsForm.konuSec_cmb.activated[str].connect(self.showKonustats)
        self.ShowStatsForm.pushButton.clicked.connect(self.cikti)
    
    

    def showDersstats(self):
        currentLesson = self.ShowStatsForm.dersSec_cmb.currentText()
        connection = sqlite3.connect('examination.db')
        connection.cursor()
        result = connection.execute("SELECT count(*) fROM studentstats WHERE result = 0 and lesson = ?",(currentLesson,))
        value = result.fetchone()
        yanlisSayisi = value[0]
        result = connection.execute("SELECT count(*) fROM studentstats WHERE result = 1 and lesson = ?",(currentLesson,))
        value = result.fetchone()
        dogruSayisi = value[0]
        self.ShowStatsForm.textBrowser_2.setText(str(dogruSayisi))
        self.ShowStatsForm.textBrowser_4.setText(str(yanlisSayisi))

    def showKonustats(self):
        currentKonu = self.ShowStatsForm.konuSec_cmb.currentText()
        connection = sqlite3.connect("examination.db")
        connection.cursor()
        result = connection.execute("SELECT count(*) FROM studentstats WHERE result = 0 and unit =?",(currentKonu,))
        value = result.fetchone()
        yanlisSayisi = value[0]
        result = connection.execute("SELECT count(*) FROM studentstats WHERE result = 1 and unit =?",(currentKonu,))
        value = result.fetchone()
        dogruSayisi = value[0]
        self.ShowStatsForm.textBrowser.setText(str(dogruSayisi))
        self.ShowStatsForm.textBrowser_3.setText(str(yanlisSayisi))
        self.ShowStatsForm.textBrowser_5.append(f"{currentKonu} dogru sayisi: {dogruSayisi} yanlis sayisi: {yanlisSayisi}\n")
    
    def cikti(self):
        
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.ShowStatsForm.textBrowser_5.print_(printer)
        
 
 
        def printpreviewDialog(self):
            printer = QPrinter(QPrinter.HighResolution)
            previewDialog = QPrintPreviewDialog(printer, self)
            previewDialog.paintRequested.connect(self.printPreview)
            previewDialog.exec_()
 
 
        def printPreview(self, printer):
            self.textEdit.print_(printer)  
#----------------------------------------------istatistik bitiş------------------------------------------------------------------

         
##################################################EXAM EKRANI BİTİŞ####################################################################################


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
