# Motion Graphics بـ Claude Code + Remotion: ملخص مجمّع

ده ملخص لأحسن 5 مصادر، مقسّم حسب الموضوع مش حسب الفيديو، والحاجات المتكررة اتشالت.
المصادر في آخر الملف.

---

## 1. الفكرة الأساسية

- كلود **مش بيطلّع فيديو مباشرة**. هو بيكتب **كود React**، وبعدين **Remotion** بيحوّل الكود ده لفيديو (MP4 أو فيديو بخلفية شفافة).
- مفيش timeline ولا keyframes زي After Effects. كل مشهد عبارة عن component، والحركة كلها معتمدة على **رقم الفريم الحالي**.
- المسار كله بيمشي كده: **Prompt ← كود ← Preview في Remotion Studio ← تصليح ← Render ← تستورده في برنامج المونتاج.**
- مش لازم تعرف React، بس لو فهمت إن "كل مشهد component والحركة متحكوم فيها بالفريم" هتعرف تكتب طلبات تصليح أدق بكتير.

## 2. المتطلبات

| الحاجة | ملاحظات |
|---|---|
| **Claude Code** | من التطبيق أو كـ extension في VS Code أو من الـ terminal. لازم Claude Code نفسه مش الشات العادي، لأنه هو اللي بيشتغل على جهازك ويقدر يعمل render. الحساب المجاني بيشتغل بس بحدود استخدام. |
| **Node.js** | النسخة 18 أو أحدث |
| **Git** | مطلوب للتثبيت |
| **VS Code** | اختياري، بس بيسهّل الشغل |
| **مساحة فاضية** | حوالي 600MB للمشروع والـ dependencies والمتصفح اللي Remotion بيستخدمه |
| **لينك البراند بتاعك** | الألوان بالـ hex، والخط، والنص بالظبط، واللوجو أو أي صور هتستخدمها |

**الرخصة:** Remotion مجاني للأفراد والمنظمات غير الربحية والشركات اللي فيها 3 موظفين أو أقل. أي شركة أكبر محتاجة Company License.

## 3. الإعداد

```bash
# مشروع جديد (هيسألك تضيف Remotion Agent Skills، قول yes)
npx create-video@latest my-motion-project

# أو جوه مشروع موجود
npx skills add remotion-dev/skills
```

- **الـ Skills دي مهمة.** من غيرها كلود ممكن يخترع functions مش موجودة في Remotion. لو هتثبّتها، اختار **global** عشان تشتغل في كل مشاريعك.
- الـ skills اللي هتستخدمها أكتر حاجة:
  - `/remotion-create`: تعمل composition جديدة
  - `/remotion-markup`: الحركة والـ layout والخطوط
  - `/remotion-studio`: تفتح الـ preview
  - `/remotion-render`: تعمل export
- بديل للـ skills: تحط ملف `CLAUDE.md` في فولدر المشروع فيه قواعد Remotion. كلود بيقراه أول ما تبدأ أي session.

**مشاكل التثبيت المشهورة:**
- **Windows / PowerShell execution policy error:** شغّل
  `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` واقفل الـ terminal وافتحه تاني.
- **تحذير إن `esbuild` script اتمنع:** مش هيوقفك، والـ render بيشتغل عادي.
- **أول تشغيل** هيطلب منك موافقات كتير على الأوامر، وده طبيعي. بعد كده هتقل.

## 4. إزاي تكتب Prompt كويس (أهم جزء)

كل المصادر متفقة على النقطة دي: **الـ prompt المبهم بيطلّع فيديو عادي أو زحمة.** "اعملها شكلها حلو" مش هتنفع.

**أي prompt لازم يكون فيه:**
1. **المقاس والمدة:** مثلًا 1920x1080، و30fps، و8 ثواني
2. **توقيت كل مشهد بالفريم:** "اللوجو يظهر من فريم 60 لفريم 75"
3. **النص بالظبط** زي ما هيظهر على الشاشة
4. **وصف الحركة:** stagger بين كل كلمة 3 فريمات، و spring، والعنصر يطلع لفوق 20px
5. **الألوان بالـ hex** والخلفية (gradient، أشكال blur بتتحرك...)
6. **النهاية:** مثلًا fade out في آخر نص ثانية
7. **اسم الـ composition:** `LogoReveal` أو `LowerThird`...

**مثال (Lower Third):**
> Composition اسمها `LowerThird`، مقاسها 1920x1080، و30fps، و150 فريم. الاسم مكتوب bold 36px أبيض، والمسمى الوظيفي regular 24px لونه #aaaaaa. فيه accent bar عرضه 4px بيدخل من الشمال بـ spring ويخلص عند فريم 15. الاسم يعمل fade ويطلع 10px بين فريم 10 و25، والمسمى بين 18 و33. يفضل ثابت لحد فريم 120 وبعدين يخرج بالعكس في 20 فريم. خلفيته pill نص شفافة.

**تريكات:**
- **طريقة Pinterest:** لاقي تصميم عاجبك، وحط صورته في Claude Code، وقوله يعمله animation بنفس الستايل.
- **خلّي كلود يكتبلك الـ prompt:** قوله النتيجة اللي عايزها، وهو يطلعلك prompt مفصّل.
- **العربي بيشتغل:** أي لغة غير الإنجليزي ممكن تستخدمها في النص (في الفيديو اتجرّبت الفارسي)، بس تأكد إن الخط بيدعم اللغة.
- **`inputProps`:** بيخليك تعمل component واحد وتطلّع منه نسخ كتير. مثلًا lower thirds لكذا شخص من نفس الكود.

## 5. المشاريع الكبيرة: ابني النظام الأول

للفيديوهات الطويلة اللي فيها مشاهد كتير، ماتطلبش كل حاجة في prompt واحد. اشتغل على مراحل، وكل مرحلة تطلع ملف markdown يبقى المرجع:

1. **القواعد التقنية:** ملف فيه الـ rules اللي كلود يمشي عليها
2. **الـ Art Direction:** الإحساس العام والقيود. **عرّف الكلمات المطاطة** زي "clean" و"modern" بالظبط، عشان كلود مايخمّنش هو يقصد إيه.
3. **الـ Storyboard والـ Timeline:** كل مشهد مدته قد إيه ودوره إيه، وبيمشي على ترتيب: hook، ثم الرسالة الأساسية، ثم لقطات بتدعمها، ثم النهاية. الملف ده هو المرجع الأساسي.
4. **قائمة مواصفات الـ assets:** الأشكال والألوان، من غير ما تعمل أي visuals لسه
5. **توليد الـ assets:** **على دفعات حسب النوع**، لأن ده بيقلل الهلوسة ويحافظ على الستايل
6. **Motion primitives:** حركات ثابتة بتتكرر في الفيديو كله. سيب كلود يقترحها وماتدخلش في التفاصيل الصغيرة.
7. **التجميع وكود المشاهد:** **كل مشهد لوحده** عشان التصليح يبقى أسهل

القاعدة هنا: **افصل قرارات التصميم عن منطق المشاهد**، واتعامل مع كلود كأنه فريق صغير انت مديره.

## 6. المراجعة والتصليح

- **Preview:** شغّل `npx remotion studio` (أو `/remotion-studio`) واتفرّج على الفيديو بالسرعة العادية. الحتت الميتة، زي 3 ثواني من غير حركة، باينة جدًا في الـ preview ومش هتاخد بالك منها وانت بتقرا الكود.
- **Render لفريم واحد بس** قبل ما تعمل render للفيديو كله:
  `npx remotion still src/index.ts MyComp out/frame-70.png --frame=70`
- **اكتب التصليح بالأرقام:** "زوّد الـ damping لـ 20 وقلّل الـ stiffness لـ 80"، أو "ضيف fade-in مدته 15 فريم يبدأ من فريم 65".
- **أول نسخة غالبًا هتطلع flat، وده طبيعي.** ماتقبلش أول نتيجة.

**أشهر المشاكل وحلولها:**

| المشكلة | الحل |
|---|---|
| النص بيتكسر على سطرين | صغّر الخط وحط `whiteSpace: "nowrap"` |
| الحركة بتهتز (jitter) | امنع `Math.random()` واحسب أي قيمة عشوائية من رقم الفريم |
| الصور أو الملفات مش بتحمّل | حطها في `public/` واستخدم `staticFile()` |
| الخط طالع fallback مش الخط بتاعك | استخدم `@remotion/google-fonts` أو `loadFont()` واتأكد بـ still |
| الـ composition مش ظاهرة | اتأكد إنها متسجلة في `src/Root.tsx` |
| الـ preview بيقع | غالبًا TypeScript error. انسخ الـ error وابعته لكلود |
| كل العناصر بتتحرك نفس الحركة | خلّي كل نوع عنصر ليه easing مختلف |
| الفيديو شكله flat | قسّمه طبقات foreground وmidground وbackground بسرعات مختلفة |

## 7. الـ Render والتصدير

```bash
npx remotion render src/index.ts MyComp out/video.mp4
```

| الهدف | الإعداد |
|---|---|
| ويب أو سوشيال | `--codec=h264` |
| **خلفية شفافة** عشان تحطه فوق فيديو | `--codec=prores-4444` |
| جودة أعلى | `--crf=18` |
| 4K من 1080p | `--scale=2` |

- **الوقت:** أول render حوالي دقيقة لأنه بينزّل المتصفح ويعمل bundle. أي render بعد كده لفيديو 8 ثواني بياخد حوالي 15 ثانية.
- بعد كده استورده في **Premiere** أو **Final Cut** أو **CapCut**، وضيف عليه sound effects زي swoosh.
- **الصوت:** Remotion بيشغّل ملفات موسيقى أو voice-over انت بتجيبها وبيظبط التوقيت عليها، بس مش بيعمل صوت لوحده. للـ voice-over استخدم أداة تانية زي ElevenLabs، وحط الـ API key في ملف `.env`.

## 8. هو كويس في إيه ومش كويس في إيه

**كويس في:**
- Title cards وkinetic typography
- Lower thirds
- Captions
- Charts متحركة، زي chart بيطلع من 0% لـ 78%
- Explainers وأشكال UI، زي search bar أو calendar أو أزرار subscribe
- نسخ متعددة من نفس التصميم بمقاسات أو لغات مختلفة

ميزة كبيرة كمان إن التعديل رخيص: تغيير كلمة أو لون بيبقى سطر واحد.

**مش كويس في:**
- الإضاءة والـ materials
- الـ particles التقيلة
- الـ 3D الحقيقي، إلا لو جبته كـ asset جاهز

ولو عايز hook أو logo reveal يبهر في أول ثانيتين، ممكن يبقى أسرع إنك تستخدم clip جاهز وتحطه بـ `<OffthreadVideo>`.

---

## الخلاصة في 5 نقط

1. ثبّت **Remotion Agent Skills**، لأن من غيرها كلود بيخترع.
2. **الـ prompt لازم يكون بالأرقام:** فريمات، وhex، وpx، ونص بالظبط.
3. للمشاريع الكبيرة: **اعمل Art Direction وStoryboard الأول**، وبعدين اكتب كود كل مشهد لوحده.
4. اشتغل في loop: **preview، ثم still لفريم واحد، ثم تصليح بالأرقام، ثم render.**
5. استخدمه للـ 2D والتايبوجرافي والـ UI. للـ 3D والإضاءة استخدم assets جاهزة.

---

### المصادر
- [Claude Code + Remotion = FREE Motion Graphics Tutorial](https://videohighlight.com/v/kXmY6yQa5q4) (ملخص فيديو يوتيوب)
- [How I Created a Professional Motion Graphics Video With Claude Code + Remotion Skills](https://videohighlight.com/v/xAUifztpib8) (ملخص فيديو يوتيوب)
- [Claude Code Just Changed YouTube Videos Forever (Tutorial)](https://videohighlight.com/v/idVMGLzrrnU) (ملخص فيديو يوتيوب)
- [Claude Remotion Tutorial: Motion Graphics With Claude Code](https://autoae.online/blog/claude-code-remotion-tutorial) (مقال)
- [Remotion + Claude Code: Animated Logo Reveals and Motion Graphics](https://mindstudio.ai/blog/remotion-claude-code-animated-logo-reveals-motion-graphics) (مقال)

> ملحوظة: الفيديوهات التلاتة اتلخصت من ملخصات مكتوبة ليها مش من الفيديو نفسه. الأوامر اتراجعت على المقالات، ولو حصل أي اختلاف ارجع لـ [docs الرسمية بتاعة Remotion](https://www.remotion.dev/docs).
