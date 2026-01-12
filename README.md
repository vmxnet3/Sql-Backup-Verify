# 🛡️ Sql-Backup-Verify

[English](#english) | [Türkçe](#türkçe)

---

<a name="english"></a>
## 📝 English - Description
**Sql Backup Verify** is a lightweight and user-friendly tool designed for database administrators to ensure the integrity of SQL Server backup files (.bak). It's not enough to just take backups; knowing they are physically healthy and restorable is life-saving during a crisis.

### ✨ Key Features
* **Deep Scanning:** Automatically discovers .bak files in the specified directory and all subfolders.
* **RESTORE VERIFYONLY:** Uses SQL Server's native engine to verify backup readability with 100% accuracy.
* **Advanced Filtering:** Filter backups by date range; view file size and path information instantly.
* **Backup Cleanup:** Safely delete backups older than a specified number of days to reclaim disk space.
* **Disk Monitoring:** Track disk usage rates on your server via a graphical interface.
* **Professional Reporting:** Lists healthy and corrupted backups in a detailed, color-coded table.

### 🚀 How to Use?
1. Install required libraries: `pip install -r requirements.txt`
2. Launch the application: `python run_app.py`
3. Enter your SQL Server credentials and backup path in the panel to start verifying.

### 🖼️ Screenshots
![Main Interface](https://github.com/vmxnet3/Sql-Backup-Verify/raw/main/1.png)
![Backup List](https://github.com/vmxnet3/Sql-Backup-Verify/raw/main/2.png)
![Results](https://github.com/vmxnet3/Sql-Backup-Verify/raw/main/3.png)

---

<a name="türkçe"></a>
## 📝 Türkçe - Açıklama
**Sql Backup Verify**, veritabanı yöneticilerinin SQL Server yedek dosyalarının (.bak) fiziksel bütünlüğünü denetlemesi için tasarlanmış, hafif ve kullanıcı dostu bir araçtır. Sadece yedek almak yetmez; o yedeğin gerçekten çalışabilir olduğunu doğrulamak kriz anında hayat kurtarır.

### ✨ Öne Çıkan Özellikler
* **Derin Tarama:** Belirlenen ana dizin ve tüm alt dizinlerdeki .bak dosyalarını otomatik olarak bulur.
* **RESTORE VERIFYONLY:** SQL Server'ın kendi doğrulama motorunu kullanarak yedeğin okunabilirliğini %100 doğrulukla test eder.
* **Gelişmiş Filtreleme:** Yedekleri tarih aralığına göre filtreleyebilir, boyut ve yol (path) bilgilerini anlık görebilirsiniz.
* **Yedek Temizliği:** Belirlediğiniz günden daha eski yedekleri tek tıkla güvenli bir şekilde silerek disk alanı açar.
* **Canlı İzleme:** Sunucudaki disk doluluk oranlarını grafiksel arayüz üzerinden takip edebilirsiniz.
* **Profesyonel Raporlama:** İşlem sonunda sağlam ve hatalı yedekleri renkli bir tablo üzerinde detaylıca listeler.

### 🚀 Nasıl Kullanılır?
1. Gerekli kütüphaneleri yükleyin: `pip install -r requirements.txt`
2. Uygulamayı başlatın: `python run_app.py`
3. Tarayıcıda açılan panelden SQL Server bilgilerinizi ve yedek yolunu girerek doğrulamayı başlatın.

---
**Publisher:** ugur.es  
**Powered by:** Gemini
