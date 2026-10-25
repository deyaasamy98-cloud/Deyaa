# Deyaa: Obsidian Vault

الـ repo ده هو الـ Obsidian vault. أي ملخص أو بحث بيطلع من محادثات Claude بيتحفظ هنا، وبيوصل لـ Obsidian لوحده.

- `Home.md`: الصفحة الرئيسية، وفيها لينكات كل النوتس
- `Summaries/`: الملخصات المجمّعة
- `Templates/`: قوالب النوتس
- `CLAUDE.md`: القواعد اللي Claude بيمشي عليها وهو بيحفظ

## ربطه بـ Obsidian (مرة واحدة بس)

### على الكمبيوتر
1. نزّل [Git](https://git-scm.com/downloads) لو مش عندك.
2. اعمل clone للـ repo في أي فولدر:
   ```bash
   git clone https://github.com/deyaasamy98-cloud/Deyaa.git
   ```
3. افتح Obsidian ← **Open folder as vault** ← اختار فولدر `Deyaa`.
4. Settings ← **Community plugins** ← Turn on ← Browse ← دوّر على **Git** (إضافة Vinzent03) ← Install ← Enable.
5. في إعدادات إضافة Git:
   - **Auto pull interval:** خليها `10` دقايق
   - **Pull on startup:** شغّلها
   - **Auto commit-and-sync interval:** خليها `10` لو عايز التعديلات اللي بتعملها في Obsidian ترجع للـ repo
6. (اختياري) Settings ← **Templates** ← Template folder location: `Templates`
7. (اختياري) Settings ← Files and links ← Default file to open: `Home`

### على الموبايل
إضافة Git شغالة على الموبايل بس أبطأ. البديل الأسهل إنك تستخدم Obsidian Sync، أو تعمل sync للفولدر بأي خدمة cloud من الكمبيوتر.

## ملحوظة عن الـ branches
Obsidian بيعمل pull من الـ branch اللي انت عامله checkout، وده غالبًا `main`. محادثات Claude بتشتغل على branches جانبية، فعشان النوتس توصل لـ Obsidian لازم الـ branch يتعمله merge في `main`.
