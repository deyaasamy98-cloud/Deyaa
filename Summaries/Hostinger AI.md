---
type: summary
aliases: [هوستينجر والـ AI]
tags: [ai, hostinger, website-builder, mcp, claude]
created: 2026-10-13
sources: 5
related: ["[[AI Video Editing]]"]
---

# Hostinger + AI: ملخص مجمّع

**مرتبط بـ:** [[AI Video Editing]]

ده ملخص لأحسن 5 مصادر، مقسّم حسب الموضوع مش حسب المصدر، والحاجات المتكررة اتشالت.
المصادر في آخر الملف.

> **ملحوظة مهمة:** Hostinger **مفيهوش أداة AI لتعديل الفيديو**. الـ AI بتاعه كله في **بناء المواقع والتطبيقات وإدارة الاستضافة**، وعشان كده الملخص ده عنهم. ملخص الـ AI في الفيديو ايديتنج في ملف لوحده: [[AI Video Editing]].

---

## 1. الصورة الكبيرة: Hostinger فيه 3 طرق تستخدم بيها الـ AI

| الأداة | بتعمل إيه | مناسبة لمين |
|---|---|---|
| **AI Website Builder** | بيعملك موقع كامل من وصف بسيط في أقل من دقيقة، وبعدين بتعدّله بالسحب والإفلات (drag & drop) | أي حد عايز موقع لبزنس أو portfolio بسرعة |
| **Hostinger Horizons** (بقى جزء من AI Builder) | "vibe coding": بتوصف تطبيق ويب، وهو يكتبه كله كود وbackend | لو عايز web app أو أداة أو لعبة بسيطة |
| **Hostinger API MCP** | بيوصّل **Claude** بحساب Hostinger بتاعك، فتقدر تدير الدومينات والـ DNS والـ VPS بالكلام | لو بتستخدم Claude وعندك VPS أو دومينات |

وفيه كمان أدوات AI صغيرة جوه الـ builder: كاتب محتوى، ومولّد صور، وصانع لوجو، ومساعد SEO، وheatmap للزوار، وKodee اللي هو مساعد الدعم الفني.

## 2. AI Website Builder: موقع في دقيقة

**الخطوات:**
1. **اكتب وصف لشغلك** أو اختار prompt جاهز زي "Create an online store". مفيش حد أقصى لطول الوصف.
2. **(اختياري) Prompt enhancer:** الـ AI يحسّن وصفك قبل ما يبني الموقع.
3. **Generate:** الموقع بيطلع في حوالي 20 ثانية.
4. **راجع الـ concept.** تقدر تعدّله أو ترجع لأي نسخة طلعت قبل كده.
5. **Edit website:** امشي على checklist الإعداد، وكمّل تعديل بالسحب والإفلات على grid.

**خلي بالك:**
- الـ AI ممكن **يتجاهل اسم البزنس بتاعك ويخترع اسم من عنده**، فراجع النصوص كلها.
- مفيش تحكم كبير في أول نسخة بتطلع، ومش هتقدر تعيد توليد section لوحده.

## 3. Hostinger Horizons: تطبيقات ويب من غير كود

**البداية:** Websites ← Create website ← **AI Builder** ← اختار **Agentic mode** ← اكتب الـ prompt ← اختار دومين (أو دومين مؤقت تغيّره بعدين).

**إيه اللي بيعمله:**
- الـ stack الافتراضي: **React + Vite** للواجهة و**Node.js** للـ backend. تقدر تطلب تقنيات تانية، بس ده ممكن يعمل مشاكل توافق.
- بيفهم prompts بأكتر من **80 لغة**، منهم العربي، وكمان بالصوت.
- تقدر **ترفع صورة أو screenshot أو PDF** وتقوله يعمل زيها.
- بيتوصل بـ **Hostinger Ecommerce** لو عايز متجر، وفيه database مدمجة (تبويب Data). وفي كورس Udemy بيشرح إزاي توصّله بـ Supabase.

**أوضاع المحرر:**
- **Preview:** تشوف الموقع وتجرّبه، ومنه زرار تبديل الجهاز عشان تشوف شكله على الموبايل
- **Select & Edit:** تختار عنصر (أو كذا عنصر بـ Shift) وتعدّله بإيدك، أو تدي الـ AI تعليمات للعنصر ده بس
- **Code:** تشوف الملفات وتعدّل الكود بنفسك
- **Data:** الـ backend، لو ضفته

**إزاي تكتب Prompt كويس:**
- كل ما الـ prompt كان **محدد أكتر**، النتيجة بتبقى أحسن، وده متكرر في كل المصادر.
- ارفع **صور reference** للتصميم اللي عايزه.
- استخدم **Reply** على جزء معين من رد الـ AI عشان توجّهه للنقطة دي بالظبط.
- للتعديلات الصغيرة، استخدم **Select & Edit** بدل ما تكتب الـ prompt كله من الأول.
- راجع بعد كل رد. لو حاجة باظت، فيه **Restore** لكل ملف لوحده.

**Horizons مايقدرش يعمل:** ألعاب 3D، أو browser extensions، أو تطبيقات بنوك وتداول، أو تطبيقات موبايل native (iOS/Android).

**أمثلة اتعملت بيه:** لعبة Tic-Tac-Toe، ومحاكي لبزنس كوكيز، ومواقع كاملة، كلها من غير ما حد يكتب سطر كود.

## 4. توصيل Claude بـ Hostinger عن طريق MCP

لو بتستخدم Claude، دي أقوى حاجة في الملف: هتقدر تدير الاستضافة كلها بالكلام.

**الخطوات:**
1. ثبّت **Node.js 20 أو أحدث**، وبعدين:
   ```bash
   npm install -g hostinger-api-mcp
   ```
2. اعمل **API token**: hPanel ← Profile ← Account Information ← **API** ← Generate token.
   - **انسخه فورًا**، لأنه مش هيظهر تاني.
   - جرّبه بأمر الـ cURL اللي موجود تحت في نفس الصفحة.
3. في **Claude Desktop**: Settings ← Developer ← **Edit Config**، وضيف:
   ```json
   {
     "mcpServers": {
       "hostinger-api": {
         "command": "hostinger-api-mcp",
         "env": { "DEBUG": "false", "APITOKEN": "YOUR API TOKEN" }
       }
     }
   }
   ```
4. اعمل restart لـ Claude، واتأكد إن Hostinger ظاهر **running** في قايمة Developer.
5. جرّب تسأله حاجة زي: *"What's the uptime of my newest VPS?"*

**Claude يقدر يعمل إيه بعد كده:**
- **الدومينات:** يسجّل دومين، ويعرض الدومينات بتاعتك، ويجيب بيانات WHOIS، ويظبط الـ forwarding
- **الـ DNS:** يعدّل ويمسح الـ records، ويعمل snapshots ويرجّع منها
- **الـ VPS:** يشتري plan، ويرجّع backup، ويثبّت نظام تشغيل، ويلخّص تقارير فحص الـ malware
- **الحساب:** يعرض المنتجات ويعمل طلبات شراء

**الأمان:**
- خلّي **مدة الـ token قصيرة** وجدّدها كل فترة.
- الـ token متخزن **نص عادي** في ملف الـ config، فماتشاركش الملف ده مع حد.
- خلي `DEBUG` على `false`.
- خلي بالك إن Claude **يقدر يشتري ويغيّر DNS**، فراجع أي عملية قبل ما توافق عليها.

## 5. الأسعار والـ AI Credits

| الخطة | سعر العرض (48 شهر) | التجديد |
|---|---|---|
| Premium | حوالي ‎$1.95 لـ ‎$2.99 في الشهر | **‎$10.99 في الشهر** |
| Business | حوالي ‎$2.75 لـ ‎$3.99 في الشهر | **‎$16.99 في الشهر** |

- **مفيش خطة مجانية.** فيه **trial لمدة 14 يوم** وضمان استرجاع فلوسك خلال 30 يوم.
- **أغلب أدوات الـ AI موجودة في خطة Business بس.** ده منها كاتب المحتوى، ومولّد الصفحات، ومساعد SEO، والتجارة الإلكترونية.
- **الـ Credits:** كل رد من Horizons بيستهلك credits، وكمان Select & Edit بيستهلك. **الـ Restore مش بيرجّعلك الـ credits.** باقات الـ credits الإضافية بتبتدي من 50 credit بـ ‎$4.99.
- الأسعار مختلفة من مصدر للتاني وبتتغير مع العروض، **فاتأكد منها على موقع Hostinger قبل ما تشتري.**

## 6. المميزات والعيوب

**المميزات:**
- سريع جدًا في عمل الموقع (أقل من دقيقة)
- سهل على المبتدئين
- سعر البداية رخيص
- دومين وSSL مجانًا
- دعم فني 24/7 بالشات
- uptime بنسبة 99.9%

**العيوب:**
- **التجديد غالي جدًا**، ممكن يزيد أكتر من 4 أضعاف بعد العرض
- مفيش app marketplace، والـ integrations قليلة
- مش هتقدر تنقل الموقع لأي builder تاني
- التحكم في التصميم أقل من Wix وSquarespace
- التجارة الإلكترونية محدودة (أقصى حاجة 1,000 منتج، ومفيش subscriptions)
- مفيش دعم بالتليفون أو الإيميل

## 7. نصايح عملية

1. **جرّب في الـ 14 يوم المجانيين** قبل ما تدفع.
2. **احسب سعر التجديد** مش سعر العرض بس، واختار أطول مدة تقدر عليها.
3. لو محتاج أدوات الـ AI كلها أو متجر، **اختار Business** على طول.
4. في Horizons **خطّط تعديلاتك قبل ما تكتبها**، لأن الـ credits بتخلص والـ Restore مش بيرجّعها.
5. **راجع شكل الموقع على الموبايل** قبل ما تعمل Publish.
6. لو المتجر بتاعك هيكبر، **Shopify** أنسب. ولو عايز صفحة واحدة بسيطة، **Carrd** أرخص.

---

## الخلاصة في 5 نقط

1. **Website Builder** لو عايز موقع بسرعة، و**Horizons** لو عايز تطبيق ويب، و**MCP** لو عايز تدير الاستضافة من Claude.
2. **الـ prompt المحدد وصور الـ reference** بيفرقوا جدًا في النتيجة.
3. **الـ credits بتخلص والـ Restore مش بيرجّعها**، فاعمل تعديلاتك بـ Select & Edit.
4. **سعر التجديد** هو الرقم الحقيقي اللي تحسب عليه، مش سعر العرض.
5. الأفضل للمبتدئين والبزنس الصغير. لو محتاج حاجة أكبر، شوف بدائل.

---

### المصادر
- [Hostinger Horizons: How to Get Started](https://www.hostinger.com/support/10505889-hostinger-horizons-how-to-get-started) (Hostinger الرسمي)
- [How to run your own Hostinger API MCP server](https://www.hostinger.com/tutorials/how-to-run-hostinger-api-mcp-server) (Hostinger الرسمي)
- [Hostinger Website Builder Review 2026](https://websitebuilderexpert.com/website-builders/hostinger-website-builder-review) (Website Builder Expert)
- [Hostinger Review](https://tech.co/website-builders/hostinger-review) (Tech.co)
- [Kevin Stratvert: Hostinger AI Tools + Horizons tutorials](https://kevinstratvert.com/tag/hostinger-horizons-tutorial/) (فيديوهات يوتيوب)

> ملحوظة: صفحة Kevin Stratvert فيها مقتطفات من فيديوهاته بس، مش الشرح كله. وأي أسعار في الملف ممكن تكون اتغيرت بسبب العروض.
