# ExaminationApp
Yazılım Yapımı Dönem Projesi

Hazırlayan: Utku Doğan

ExaminationApp Python PyQt5, QtDesigner ve Sqlite veritabanı kullanılarak oluşturulmuş bir desktop programıdır. Asıl sınav için öğretme amacıyla 6-sigma olarak adlandırılan belirli aralıklarla soruyu öğrencinin karşısına getirip, altı kez üst üste bilince öğrenmiş saydığı bir algoritma kullanır.

çalıştırmak için programla ayni dizinde "examination.db" dosyasi olmalı. main(login).py dosyasi ile calistirabilirsiniz

# VeriTabanı

Tablolar

![image](https://user-images.githubusercontent.com/59983461/169146478-2f8986f7-fe68-47b8-9b6d-565ba3bee0fe.png)

![image](https://user-images.githubusercontent.com/59983461/169146542-900dd011-f017-446b-bf67-a26561b35610.png)


# Ekran Görüntüleri

## Giris Ekrani

![image](https://user-images.githubusercontent.com/59983461/169146894-80c1c9b3-55a1-4213-81dc-9189da84aed0.png)

## Kayit Ol 

![image](https://user-images.githubusercontent.com/59983461/169147007-286be57e-e383-486c-8e9d-160ecd4cb571.png)

## Sifremi Unuttum 

![image](https://user-images.githubusercontent.com/59983461/169147059-41559eaf-37f2-4a40-9e53-557da2d08d6c.png)

## Ogrenci Giris

1
![image](https://user-images.githubusercontent.com/59983461/169147208-3f0c3cea-648f-4e06-890a-85dcb433dd08.png)

## Exam Ekranı ve Sigma öğrenme Ekranı

![image](https://user-images.githubusercontent.com/59983461/169147319-93a0a738-2e4b-4b89-8677-fc931efad24e.png)

## istatistik

![image](https://user-images.githubusercontent.com/59983461/169147458-38aa4593-1095-46f6-9fc0-8a9dcb713418.png)

## ogrenci ayar

![image](https://user-images.githubusercontent.com/59983461/169147519-7e5c384d-5a6d-432d-94da-96d7e7f2475d.png)

## sinav sorumlusu soru ekleme

![image](https://user-images.githubusercontent.com/59983461/169147715-f91b335d-63da-4e4c-bb0c-8154dae03517.png)

# admin soru onay page

![image](https://user-images.githubusercontent.com/59983461/169147759-c6af5cba-62aa-4f70-8972-dac30dfff52f.png)



# ALGORITMA

bir öğrencinin soruyu tamamen bilmiş (öğrenmiş) sayılabilmesi için o soruyu belli periyotlarla üst üste 6 kez bilmesi gerek.
periyodumuz 1 gün, 1 hafta, 1 ay, 3 ay, 6 ay, 1 yıl olsun 
öğrencinin karşısına her gün 10 soru çıkacak bu sorular rastgele çıkacak. 

örneğin:


##1. gün
-------------------------------------------------------------------------------------------
rastgele çıkan sorular: 1 - 3 - 4 - 7 - 23 - 98 - 32 - 74 - 24 - 12 
ilk defa bildiği sorular: 1 - 98 - 32 olsun 



##2. gün 
-------------------------------------------------------------------------------------------

rastgele çıkacak sorular: 2 - 14 - 16 - 72 - 44 - 45 - 35 - 26 - 22 - 9 - 10
+
dün ilk defa bildiği sorular (1 gün, 1 hafta, 1 ay, 3 ay, 6 ay, 1 yıl döngüsündeki ilk adım): 1 - 98 - 32

yani totalde karşısına çıkacak sorular: 2 - 14 - 16 - 72 - 44 - 45 - 35 - 26 - 22 - 9 - 10 - 1 - 98 - 32

bildiği sorular 1 - 32 - 2 - 9 olsun. (bu periyotta (1 gün periyodu) 98'i üst üste ikinci kez bilemedigi icin onun icin sürec sıfırlandı) 1 ve 32 için haftaya cıkacak (ikinci adım)



##3. gün
-------------------------------------------------------------------------------------------
rastgele çıkan sorular: 34 - 82 - 75 - 14 - 98 (tekrar çıkabilir) - 31 - 13 - 47 - 88 - 77
+
dün ilk defa bildiği sorular (1 gün, 1 hafta, 1 ay, 3 ay, 6 ay, 1 yıl döngüsündeki ilk adım): 2 - 9

yani totalde karşısına çıkacak sorular: 34 - 82 - 75 - 14 - 98 (tekrar çıkabilir) - 31 - 13 - 47 - 88 - 77 - 2 - 9

bildiği sorular ?
.
.
.
.
.
.
##8. gün
------------------------------------------------------------------------------------------
rastgele çıkacak sorular: 54 - 53 - 73 - 21 - 42 - 56 - 43 - 22 - 66- 55
+
dün ilk defa bildiği sorular (1 gün, 1 hafta, 1 ay, 3 ay, 6 ay, 1 yıl döngüsündeki ilk adım): ? 

yani totalde karşısına çıkacak sorular: 54 - 53 - 73 - 21 - 42 - 56 - 43 - 22 - 66- 55 + ? 

bildiği sorular: 53 - 21 olsun 


##9.gün
------------------------------------------------------------------------------------------
rastgele çıkacak sorular: 11 - 12 - 15 - 63 - 76 - 32 - 54 - 39 - 49 - 99
dün ilk defa bildiği sorular 53 - 21
bir hafta önce ikinci kez bildiği sorular: 1 - 32 
yani totalde karşısına çıkacak sorular:  11 - 12 - 15 - 63 - 76 - 32 - 54 - 39 - 49 - 99 - 53 - 21 - 1 - 32 


