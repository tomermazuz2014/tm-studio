# -*- coding: utf-8 -*-
import re, sys
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()

T = [
# head
('תומר מזוז · TM Studio TLV | בניית אתרים, אפליקציות ומערכות לעסקים', 'Tomer Mazuz · TM Studio TLV | Websites, apps and business systems'),
('תומר מזוז (Tomer Mazuz), TM Studio TLV: בניית אתרים לעסקים, פיתוח אפליקציות, מערכות CRM וחנויות Shopify. עיצוב ופיתוח במקום אחד, מתל אביב.', 'Tomer Mazuz, TM Studio TLV: websites for businesses, app development, CRM systems and Shopify stores. Design and development in one place, from Tel Aviv.'),
('בונה אתרים, אפליקציות ומערכות לעסקים, מהרעיון הראשון ועד מוצר שעובד.', 'I build websites, apps and systems for businesses, from the first idea to a product that works.'),
('הלוגו של Tomer Mazuz, AI Digital Creator', 'Tomer Mazuz logo, AI Digital Creator'),
('מעצב ומפתח אתרים ואפליקציות', 'Web and app designer and developer'),
('בניית אתרים, אפליקציות ומערכות לעסקים: עיצוב ופיתוח במקום אחד.', 'Websites, apps and systems for businesses: design and development in one place.'),
('תל אביב-יפו', 'Tel Aviv-Yafo'),
('מערכות CRM ומערכות לניהול העסק', 'CRM and business management systems'),
('תומר מזוז, Tomer Mazuz · TM Studio TLV', 'Tomer Mazuz · TM Studio TLV'),
# turn screen
('לחוויה המלאה, האתר מוצג לרוחב המסך.', 'For the full experience, the site is shown sideways.'),
('סובבו את הטלפון לאורך', 'Turn your phone upright'),
('סובבו את הטלפון', 'Turn your phone'),
('להציג לרוחב', 'Show it sideways'),
('להמשיך לאורך', 'Stay upright'),
('הצגה לרוחב', 'Wide view'), ('הצגה לאורך', 'Upright view'),
('החלפת תצוגה: לאורך או לרוחב', 'Switch view: upright or wide'),
# hero
('מייסד TM Studio נכנס לפריים, מנופף לשלום ומצביע אל הצופה', 'The founder of TM Studio walks in, waves hello and points at you'),
('מייסד TM Studio מצביע אל הצופה', 'The founder of TM Studio points at you'),
('האתר באוויר', 'Site is live'),
# works
('סובבו את המעגל עם האצבע, לחצו על עבודה כדי לפתוח.', 'Spin the ring with your finger, tap a project to open it.'),
('גררו או גללו כדי לסובב, לחצו על עבודה כדי לפתוח.', 'Drag or scroll to spin, click a project to open it.'),
('החליקו הצידה לעוד עבודות, לחצו על עבודה כדי לפתוח.', 'Swipe sideways for more work, tap a project to open it.'),
("indexOf('החליקו')", "indexOf('Swipe')"),
('לחצו על עבודה כדי לפתוח אותה.', 'Click a project to open it.'),
(', פתיחת העבודה', ', open the project'),
('קבוצות של עבודות', 'Groups of projects'),
('קבוצה 1', 'Group 1'), ('קבוצה 2', 'Group 2'), ('קבוצה 3', 'Group 3'),
('תומר יושב מול הלפטופ, והמצלמה נכנסת לתוך המסך: אתר, אפליקציה ומערכת שבנה', 'Tomer at his laptop, and the camera goes into the screen: a website, an app and a system he built'),
('סרטון פתיחה', 'Intro film'),
('הפעלת הסרטון', 'Play the film'),
('בניית אפליקציות', 'Apps'), ('בניית מערכות', 'Systems'),
('מה נבנה יחד?', 'What shall we build?'),
('בואו נדבר על הפרויקט', "Let's talk about your project"),
('גללו למטה', 'Scroll down'),
# services
('עיצוב ופיתוח במקום אחד:', 'Design and development in one place:'),
('אתרים, חנויות, אפליקציות ומערכות', 'websites, stores, apps and systems'),
('לעסקים.', 'for businesses.'),
('עיצוב שנראה טוב ונוח לשימוש, בעברית ובכל מסך.', 'Design that looks good and is easy to use, in any language and on any screen.'),
('עיצוב אתרים ודפי נחיתה', 'Websites and landing pages'),
('עיצוב שמותאם לעסק, מהמסך הראשון ועד כפתור הפנייה.', 'Design made for your business, from the first screen to the contact button.'),
('עיצוב אפליקציות', 'App design'),
('מסכים, זרימות וחוויית שימוש לאפליקציות מובייל.', 'Screens, flows and user experience for mobile apps.'),
('עיצוב מחדש למוצר קיים', 'Redesign of an existing product'),
('רענון לאתר, לחנות או לאפליקציה שכבר עובדים, בלי להתחיל מאפס.', 'A refresh for a site, store or app that already works, without starting from scratch.'),
('התאמה לעברית ולמובייל', 'Mobile and right-to-left ready'),
('ממשק מימין לשמאל שנוח לשימוש גם בטלפון.', 'Interfaces that work in English, Hebrew and on the phone.'),
('לצפייה בעבודה', 'See the project'),
('פיתוח מקצה לקצה, מהרעיון הראשון ועד מוצר שעובד.', 'End-to-end development, from the first idea to a product that works.'),
('אתרים לעסקים', 'Business websites'),
('אתרי תדמית, קטלוגים ופורטפוליו, עם חיפוש, סינון וגלריות.', 'Brand sites, catalogs and portfolios, with search, filters and galleries.'),
('חנות אונליין עם חוויית קנייה נוחה במובייל.', 'An online store that is easy to shop on mobile.'),
('אפליקציות לעסקים, למשל לקביעת תורים ולרשימות המתנה.', 'Apps for businesses, for example bookings and waiting lists.'),
('מערכות לעסק', 'Business systems'),
('תהליכי עבודה כמו חשבוניות, תשלומים ועדכונים ללקוחות.', 'Workflows such as invoices, payments and customer updates.'),
('עוזר דיגיטלי שעונה למבקרים, כמו זה שבאתר הזה.', 'A digital assistant that answers your visitors, like the one on this site.'),
('יש לכם רעיון? ספרו לי עליו.', 'Got an idea? Tell me about it.'),
('או שאלו את העוזר הדיגיטלי', 'or ask the digital assistant'),
# how
('מהפנייה הראשונה ועד ההשקה, בשלושה שלבים.', 'From the first message to launch, in three steps.'),
('מדברים על הרעיון', 'We talk about the idea'),
('אני שומע מה אתם רוצים לבנות, למי זה מיועד ומה הכי חשוב בגרסה הראשונה.', 'I hear what you want to build, who it is for and what matters most in the first version.'),
('רואים כיוון עיצובי', 'You see a design direction'),
('אני מכין מסכים ראשונים כדי שתוכלו לראות איך המוצר ייראה וירגיש ולתת לי פידבק.', 'I make the first screens so you can see how the product will look and feel, and give me feedback.'),
('בונים ומעלים לאוויר', 'We build it and go live'),
('אני מפתח את המוצר, נותן לכם גרסה להתנסות בה ומשפר אותה לפי הפידבק לפני ההשקה.', 'I develop the product, give you a version to try, and improve it from your feedback before launch.'),
('קבעו שיחת היכרות', 'Book an intro call'),
# footer
('יש לכם רעיון?', 'Got an idea?'),
('בואו נבנה אותו.', "Let's build it."),
('אתרים, אפליקציות ומערכות לעסקים. מהשיחה הראשונה ועד מוצר שעובד, עיצוב ופיתוח במקום אחד.', 'Websites, apps and systems for businesses. From the first call to a product that works, design and development in one place.'),
('שלחו הודעה בוואטסאפ', 'Message me on WhatsApp'),
('שלחו הודעה באינסטגרם', 'Message me on Instagram'),
('הודעה באינסטגרם', 'Message on Instagram'),
('תומר מזוז בלינקדאין', 'Tomer Mazuz on LinkedIn'),
('ניווט בתחתית', 'Footer navigation'),
('© 2026 תומר מזוז ·', '© 2026 Tomer Mazuz ·'),
('הצהרת נגישות', 'Accessibility statement'),
# a11y panel
('סגירת תפריט הנגישות', 'Close the accessibility menu'),
('תפריט נגישות', 'Accessibility menu'),
('גודל טקסט', 'Text size'), ('הקטנת טקסט', 'Smaller text'), ('הגדלת טקסט', 'Larger text'),
('א−', 'A−'), ('א+', 'A+'),
('ניגודיות גבוהה', 'High contrast'), ('גווני אפור', 'Grayscale'), ('הדגשת קישורים', 'Highlight links'),
('גופן קריא', 'Readable font'), ('עצירת אנימציות', 'Stop animations'), ('סמן גדול', 'Big cursor'), ('איפוס', 'Reset'),
('אני רואה חשיבות רבה בכך שהאתר יהיה נוח ושמיש לכל אחד ואחת, כולל אנשים עם מוגבלות.', 'It matters to me that this site is easy to use for everyone, including people with disabilities.'),
('האתר נבנה לפי ההנחיות של WCAG 2.1 ברמה AA ככל האפשר: ניווט מלא במקלדת, תיאורים טקסטואליים לתמונות, התאמה לקוראי מסך, ניגודיות צבעים, התאמה לטלפונים, ואפשרות לעצור אנימציות. בתפריט הזה אפשר גם להגדיל טקסט, להגביר ניגודיות, להדגיש קישורים ולהחליף לגופן פשוט.', 'The site follows WCAG 2.1 level AA as far as possible: full keyboard navigation, text alternatives for images, screen reader support, colour contrast, phone layouts, and a way to stop animations. This menu also lets you enlarge text, raise contrast, highlight links and switch to a plain font.'),
('ייתכן שעדיין יש חלקים שאינם נגישים במלואם, כמו חלק מהסרטונים והאנימציות. נתקלתם בבעיה? ספרו לי ואתקן בהקדם:', 'Some parts may not be fully accessible yet, such as some of the videos and animations. Found a problem? Tell me and I will fix it soon:'),
('תומר מזוז ·', 'Tomer Mazuz ·'),
('וואטסאפ 050-3232367', 'WhatsApp +972 50-323-2367'),
('עודכן לאחרונה: נובמבר 2026', 'Last updated: November 2026'),
('נגישות', 'Accessibility'),
# chat
('דיוקן של תומר מזוז', 'Portrait of Tomer Mazuz'),
('העוזר הדיגיטלי של תומר · AI', "Tomer's digital assistant · AI"),
('העוזר הדיגיטלי של תומר', "Tomer's digital assistant"),
('עוזר AI · עברית ואנגלית', 'AI assistant · English and Hebrew'),
('סגירת הצ׳אט', 'Close the chat'),
('שיחה או קביעת שיחה', 'Chat or book a call'),
('שיחת היכרות עם תומר', 'Intro call with Tomer'),
('20 דקות, בטלפון או בזום: מה תרצו לבנות, ואיך מתחילים.', '20 minutes, by phone or Zoom: what you want to build, and how to start.'),
('→ חזרה', '← Back'),
('באיזה יום?', 'Which day?'),
('נושא הפנייה', 'Topic'),
('מערכת לעסק', 'Business system'),
('עיצוב מחדש', 'Redesign'),
('שלחו בקשה בוואטסאפ', 'Send the request on WhatsApp'),
('תומר יאשר את המועד בהודעה חוזרת.', 'Tomer will confirm the time in a reply.'),
('העתקת ההודעה', 'Copy the message'),
('ההודעה הועתקה', 'Message copied'),
('היי, אני העוזר הדיגיטלי של תומר. אפשר לשאול אותי על העבודות שלו או לספר לי מה תרצו לבנות.', "Hi, I'm Tomer's digital assistant. Ask me about his work, or tell me what you'd like to build."),
('יש לי רעיון לפרויקט', 'I have a project idea'),
('מה תומר בונה?', 'What does Tomer build?'),
('אפשר לראות עבודות?', 'Can I see some work?'),
('איך מתחילים?', 'How do we start?'),
('הודעה לעוזר', 'Message to the assistant'),
('כתבו הודעה…', 'Write a message…'),
('שליחה', 'Send'),
('לצפייה בפרויקט', 'See the project'),
('ההודעה לתומר. אפשר לערוך לפני השליחה:', 'Your message to Tomer. You can edit it before sending:'),
('שלחו לתומר בוואטסאפ', 'Send to Tomer on WhatsApp'),
('וואטסאפ ייפתח עם ההודעה, ותבחרו שם את איש הקשר.', 'WhatsApp opens with the message ready.'),
('יש כרגע עומס. נסו שוב בעוד רגע.', 'It is busy right now. Try again in a moment.'),
('העוזר לא מחובר כרגע. אפשר לכתוב לתומר ישירות:', 'The assistant is offline right now. You can write to Tomer directly:'),
("['ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שבת']", "['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']"),
("['א׳', 'ב׳', 'ג׳', 'ד׳', 'ה׳', 'ו׳', 'ש׳']", "['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']"),
("'יום ' + DAYS[date.getDay()] + ', ' + date.getDate() + '.' + (date.getMonth() + 1)", "DAYS[date.getDay()] + ', ' + date.getDate() + '/' + (date.getMonth() + 1)"),
("'יום ' + DAYS[pick.day.getDay()] + ', ' + pick.day.getDate() + '.' + (pick.day.getMonth() + 1) + '.' + pick.day.getFullYear()", "DAYS[pick.day.getDay()] + ', ' + pick.day.getDate() + '/' + (pick.day.getMonth() + 1) + '/' + pick.day.getFullYear()"),
("' · באיזו שעה?", "' · What time?"),
("' בשעה ' + h", "' at ' + h"),
("'היי תומר, אשמח לקבוע שיחת היכרות ב' + label() + ' בשעה ' + pick.time + '.\\nנושא: ' + pick.topic + '\\nשם: ' + nameIn.value.trim() + '\\nטלפון: ' + phoneIn.value.trim()",
 "'Hi Tomer, I would like to book an intro call on ' + label() + ' at ' + pick.time + '.\\nTopic: ' + pick.topic + '\\nName: ' + nameIn.value.trim() + '\\nPhone: ' + phoneIn.value.trim()"),
("talk('היי!')", "talk('Hi!')"), ("talk('יש לך רעיון?')", "talk('Got an idea?')"),
# works copy
('עיצבתי מחדש את אפליקציית הלקוחות ועבדתי על חוויית גילוי העסקים, קביעת התורים ורשימות ההמתנה.', 'I redesigned the customer app and worked on discovering businesses, booking appointments and waiting lists.'),
('שני מסכים מאפליקציית PING על שני אייפונים: מסך הבית ובחירת מועד לתור', 'Two screens of the PING app on two iPhones: the home screen and picking an appointment time'),
('לאתר ', 'Visit '), ('לחנות ', 'Visit '),
('עיצבתי ופיתחתי אתר נדל״ן למשרד של סימה ברקאי, עם וידאו במסך מלא וקטלוג נכסים עם חיפוש וסינון.', "I designed and built a real estate site for Sima Barkai's agency, with a full-screen video and a property catalog with search and filters."),
('עמוד הבית של ברקאי נכסים על מחשב נייד', 'The Barkai Real Estate home page on a laptop'),
('קטלוג הנכסים של ברקאי נכסים באייפון', 'The Barkai Real Estate property catalog on an iPhone'),
('קטלוג הנכסים של ברקאי נכסים במסך מלא, עם שורת חיפוש וסינון', 'The Barkai Real Estate property catalog, full screen, with search and filters'),
('חידשתי את עיצוב אפליקציית הסטודיו והתאמתי את חוויית השימוש לעברית.', "I refreshed the studio app's design and adapted the experience for Hebrew."),
('שני מסכים מאפליקציית Studio Alma על שני אייפונים: קביעת תור ופרופיל אישי', 'Two screens of the Studio Alma app on two iPhones: booking and a personal profile'),
('עיצבתי מחדש את חנות האופנה ב־Shopify, עם דגש על חוויית הקנייה במובייל, וידאו וחיפוש מוצרים.', 'I redesigned the fashion store on Shopify, focusing on mobile shopping, video and product search.'),
('עמוד מוצר בחנות LAYMR על מחשב נייד', 'A LAYMR product page on a laptop'),
('עמוד מוצר ועמוד קולקציה של LAYMR על שני אייפונים', 'A LAYMR product page and collection page on two iPhones'),
('בניתי אתר פורטפוליו לאמנית לימור מזוז, עם גלריות שמציגות את העבודות שלה לפי קטגוריה.', 'I built a portfolio site for the artist Limor Mazuz, with galleries that show her work by category.'),
('גלריית הקרמיקה באתר של לימור מזוז על מחשב נייד', "The ceramics gallery on Limor Mazuz's site on a laptop"),
('גלריית הקרמיקה של לימור מזוז באייפון', "Limor Mazuz's ceramics gallery on an iPhone"),
('פיתחתי ושיפרתי תהליכי עבודה במערכת, כולל חשבוניות, תשלומים ועדכונים ללקוחות.', 'I developed and improved workflows in the system, including invoices, payments and customer updates.'),
('מסך הבית של מערכת ROOK על מחשב נייד, עם שלבי הייצור מקונספט ועד משלוח', 'The ROOK home screen on a laptop, with production stages from concept to shipping'),
('בניתי את האפליקציה של מועדון הטניס של טל חיון: הזמנת אימונים לפי מאמן או לפי שעה, טורנירים ומעקב התקדמות אישי.', "I built the Tal Hayon Tennis Club app: book sessions by coach or by time, tournaments and personal progress tracking."),
('שני מסכים מאפליקציית מועדון הטניס של טל חיון על שני אייפונים: מסך הבית ותחילת הזמנת אימון', 'Two screens of the Tal Hayon Tennis Club app on two iPhones: the home screen and starting a booking'),
('בניתי אתר קטלוג לרהיטי השפלה, מפעל לריהוט משרדי, עם חיפוש לפי שם ומספר מוצר.', 'I built a catalog site for Rahitei HaShfela, an office furniture factory, with search by name and product number.'),
('עמוד הבית של רהיטי השפלה על מחשב נייד', 'The Rahitei HaShfela home page on a laptop'),
('קטגוריית הכיסאות המשרדיים בקטלוג של רהיטי השפלה, עם שורת חיפוש', 'The office chairs category in the Rahitei HaShfela catalog, with a search bar'),
('עיצבתי ובניתי את האתר של דור שרעבי, סטודיו לעיצוב גבות בתל אביב, עם פתיח וידאו במסך מלא ואזורי טיפולים, עבודות ומוצרים.', 'I designed and built the site for Dor Sharabi, a brow studio in Tel Aviv, with a full-screen video intro and sections for treatments, work and products.'),
('עמוד הבית של דור שרעבי על מחשב נייד', 'The Dor Sharabi home page on a laptop'),
('אזור הטיפולים באתר של דור שרעבי: כותרת, וכרטיס טיפול עם תמונה וטקסט', 'The treatments section on the Dor Sharabi site: a heading and a treatment card with a photo and text'),
('בניתי לאיגל מלגזות מערכת לניהול השירות: פתיחת קריאות שירות, שיבוץ טכנאים ומעקב אחרי העבודה בשטח, עם לוח בקרה למנהלים ופורטל ללקוחות.', 'I built a service management system for Eagle Forklifts: opening service calls, assigning technicians and tracking work in the field, with a dashboard for managers and a customer portal.'),
('לוח הבקרה של מערכת השירות של איגל מלגזות על מחשב נייד, עם נתוני דמו', "The Eagle Forklifts service dashboard on a laptop, with demo data"),
('לוח הבקרה: מדדי היום, תור הקריאות לשיבוץ ועומס הטכנאים, עם נתוני דמו', "The dashboard: today's numbers, the queue of calls to assign and technician load, with demo data"),
# short words last
('בניית אתרים לעסקים', 'Business websites'), ('בניית חנות Shopify', 'Shopify stores'), ('עיצוב אתרים ואפליקציות', 'Web and app design'),
('בניית אתרים', 'Websites'), ('פיתוח אפליקציות', 'App development'), ('מערכות CRM', 'CRM systems'),
('חנויות Shopify', 'Shopify stores'), ('עיצוב UX/UI', 'UX/UI design'), ('עוזר AI לאתר', 'AI assistant for your site'),
('אפליקציות', 'Apps'), ('אפליקציה', 'App'), ('מערכת', 'System'), ('אתר', 'Website'), ('אחר', 'Other'),
('שירותים', 'Services'), ('ניווט', 'Navigation'), ('סגירה', 'Close'), ('שם', 'Name'), ('טלפון', 'Phone'),
('אינסטגרם', 'Instagram'), ('תל אביב', 'Tel Aviv'), ('תומר מזוז', 'Tomer Mazuz'),
]
for a, b in sorted(T, key=lambda x: -len(x[0])):
    if "'" not in a: b = b.replace("'", '\u2019')   # a typographic apostrophe never closes a JS string
    s = s.replace(a, b)

s = s.replace('>050-323-2367<', '>+972 50-323-2367<')
# language, direction for text, links between the two versions
s = s.replace('<html lang="he" dir="rtl">', '<html lang="en" dir="rtl" class="is-en">', 1)
s = s.replace('<link rel="canonical" href="https://www.tomermazuz.com/">',
 '<link rel="canonical" href="https://www.tomermazuz.com/en">\n<link rel="alternate" hreflang="he" href="https://www.tomermazuz.com/">\n<link rel="alternate" hreflang="en" href="https://www.tomermazuz.com/en">\n<link rel="alternate" hreflang="x-default" href="https://www.tomermazuz.com/">', 1)
s = s.replace('<meta property="og:url" content="https://www.tomermazuz.com/">', '<meta property="og:url" content="https://www.tomermazuz.com/en">', 1)
s = s.replace('<meta property="og:locale" content="he_IL">', '<meta property="og:locale" content="en_US">', 1)
# service page links are Hebrew pages: in English they stay on this page
s = re.sub(r'href="/(websites|apps|crm|shopify|design|ai-assistant)/"', r'href="/en/\1/"', s)
# English reads left to right inside the same layout
css = '''
/* ---------- English: the layout stays, the words read left to right ---------- */
html.is-en p, html.is-en h1, html.is-en h2, html.is-en h3, html.is-en h4, html.is-en li, html.is-en label, html.is-en .say,
html.is-en .toast, html.is-en .lead, html.is-en .btn, html.is-en .nav-link, html.is-en input, html.is-en textarea,
html.is-en .chat-msg, html.is-en .bubble, html.is-en .works-hint, html.is-en .foot-word, html.is-en .a11y-panel { direction: ltr; }
html.is-en body { font-family: var(--font-en, var(--font-sans)); }
html.is-en .nav, html.is-en .actions, html.is-en .how-steps, html.is-en .svc-list, html.is-en .foot-bar { direction: ltr; }
@media (min-width: 761px), (orientation: landscape) { html.is-en .lead { margin-left: 0; margin-right: auto; } }
html.is-en .chat, html.is-en .a11y-panel, html.is-en #a11y { direction: ltr; }
html.is-en .chat-tabs { direction: rtl; }
html.is-en .copy { text-align: left; }
html.is-en .copy h1[dir="ltr"] { text-align: left; }
html.is-en .lead::after { margin-inline-start: 0 !important; }
html.is-en .btn svg, html.is-en .btn .arr { transform: scaleX(-1); }
@media (max-width: 760px) and (orientation: portrait) { html.is-en .copy, html.is-en .copy h1[dir="ltr"] { text-align: center; } html.is-en .actions .handle { align-self: flex-end; } }
'''
s = s.replace('</style>', css + '</style>', 1)
s = s.replace('<a class="nav-link lang-sw" href="/en" hreflang="en" lang="en" aria-label="English version">EN</a>', '<a class="nav-link lang-sw" href="/" hreflang="he" lang="he" aria-label="גרסה בעברית">עב</a>', 1)
open(out, 'w', encoding='utf-8').write(s)
left = sorted(set(h.strip() for h in re.findall(r'[^<>"`{}=;\n]*[֐-׿][^<>"`{}=;\n]*', re.sub(r'<!--.*?-->|/\*.*?\*/', '', s, flags=re.S)) if h.strip()))
print(len(left)); print('\n'.join(left))
