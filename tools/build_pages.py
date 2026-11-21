#!/usr/bin/env python3
"""Builds the service pages of tomermazuz.com: one static Hebrew page per service, plus sitemap.xml.
Every fact on a page comes from the site itself (the works list, the services list, how-I-work)."""
import json, os, sys, html
from datetime import date

ROOT = sys.argv[1]
SITE = "https://www.tomermazuz.com"
WA = "https://wa.me/972503232367"
IG = "https://ig.me/m/tmstudio.tlv"
TODAY = date.today().isoformat()

WORKS = {
  "ping":   dict(n="PING", img="scenes/ping-p.webp", w=1400, h=1858, url="https://www.pingitnow.co/",
                 d="עיצבתי מחדש את אפליקציית הלקוחות ועבדתי על חוויית גילוי העסקים, קביעת התורים ורשימות ההמתנה.",
                 alt="שני מסכים מאפליקציית PING על שני אייפונים: מסך הבית ובחירת מועד לתור"),
  "barkai": dict(n="Barkai Real Estate", img="scenes/barkai.webp", w=2000, h=1333, url="https://barkai.vercel.app",
                 d="עיצבתי ופיתחתי אתר נדל״ן למשרד של סימה ברקאי, עם וידאו במסך מלא וקטלוג נכסים עם חיפוש וסינון.",
                 alt="עמוד הבית של ברקאי נכסים על מחשב נייד"),
  "alma":   dict(n="Studio Alma", img="scenes/alma-p.webp", w=1400, h=1858, url="https://studioalma.app/",
                 d="חידשתי את עיצוב אפליקציית הסטודיו והתאמתי את חוויית השימוש לעברית.",
                 alt="שני מסכים מאפליקציית Studio Alma על שני אייפונים: קביעת תור ופרופיל אישי"),
  "laymr":  dict(n="LAYMR", img="scenes/laymr.webp", w=2000, h=1333, url="https://laymr.com",
                 d="עיצבתי מחדש את חנות האופנה ב־Shopify, עם דגש על חוויית הקנייה במובייל, וידאו וחיפוש מוצרים.",
                 alt="עמוד מוצר בחנות LAYMR על מחשב נייד"),
  "limor":  dict(n="Limor Mazuz Art", img="scenes/limor.webp", w=2000, h=1333, url="https://limibylimor.com",
                 d="בניתי אתר פורטפוליו לאמנית לימור מזוז, עם גלריות שמציגות את העבודות שלה לפי קטגוריה.",
                 alt="גלריית הקרמיקה באתר של לימור מזוז על מחשב נייד"),
  "rook":   dict(n="ROOK", img="scenes/rook.webp", w=2000, h=1333, url="https://rook-workspace.com/en",
                 d="פיתחתי ושיפרתי תהליכי עבודה במערכת, כולל חשבוניות, תשלומים ועדכונים ללקוחות.",
                 alt="מסך הבית של מערכת ROOK על מחשב נייד, עם שלבי הייצור מקונספט ועד משלוח"),
  "tal":    dict(n="Tal Hayon Tennis Club", img="scenes/tal-p.webp", w=1400, h=1858, url=None,
                 d="בניתי את האפליקציה של מועדון הטניס של טל חיון: הזמנת אימונים לפי מאמן או לפי שעה, טורנירים ומעקב התקדמות אישי.",
                 alt="שני מסכים מאפליקציית מועדון הטניס של טל חיון על שני אייפונים"),
  "rahitei":dict(n="Rahitei HaShfela", img="scenes/rahitei.webp", w=2000, h=1333, url="https://rahiteihashfela.com",
                 d="בניתי אתר קטלוג לרהיטי השפלה, מפעל לריהוט משרדי, עם חיפוש לפי שם ומספר מוצר.",
                 alt="עמוד הבית של רהיטי השפלה על מחשב נייד"),
  "dor":    dict(n="Dor Sharabi", img="scenes/dor.webp", w=2000, h=1342, url="https://www.dorbrowart.com/",
                 d="עיצבתי ובניתי את האתר של דור שרעבי, סטודיו לעיצוב גבות בתל אביב, עם פתיח וידאו במסך מלא ואזורי טיפולים, עבודות ומוצרים.",
                 alt="עמוד הבית של דור שרעבי על מחשב נייד"),
  "eagle":  dict(n="Eagle Forklifts", img="scenes/eagle.webp", w=2000, h=1342, url=None,
                 d="בניתי לאיגל מלגזות מערכת לניהול השירות: פתיחת קריאות שירות, שיבוץ טכנאים ומעקב אחרי העבודה בשטח, עם לוח בקרה למנהלים ופורטל ללקוחות.",
                 alt="לוח הבקרה של מערכת השירות של איגל מלגזות על מחשב נייד, עם נתוני דמו"),
}

STEPS = [
  ("מדברים על הרעיון", "אני שומע מה אתם רוצים לבנות, למי זה מיועד ומה הכי חשוב בגרסה הראשונה."),
  ("רואים כיוון עיצובי", "אני מכין מסכים ראשונים כדי שתוכלו לראות איך המוצר ייראה וירגיש ולתת לי פידבק."),
  ("בונים ומעלים לאוויר", "אני מפתח את המוצר, נותן לכם גרסה להתנסות בה ומשפר אותה לפי הפידבק לפני ההשקה."),
]

PAGES = [
  dict(slug="websites", nav="בניית אתרים",
       title="בניית אתרים לעסקים: אתר תדמית, קטלוג ודף נחיתה | TM Studio TLV",
       desc="בניית אתרים לעסקים בעברית: אתרי תדמית, דפי נחיתה, אתרי קטלוג ופורטפוליו, מותאמים למובייל. עיצוב ופיתוח במקום אחד, מתל אביב.",
       h1="בניית אתרים לעסקים",
       lead="אתר תדמית, דף נחיתה, קטלוג מוצרים או פורטפוליו. אני מעצב ובונה את האתר מהמסך הראשון ועד כפתור הפנייה, בעברית ומותאם לכל מסך.",
       what=[("אתר תדמית לעסק", "עמוד בית שמסביר מה העסק עושה, למי הוא מתאים ואיך פונים, עם עבודות, טיפולים או שירותים."),
             ("דף נחיתה", "עמוד אחד שמוביל לפעולה אחת: השארת פרטים, הודעה בוואטסאפ או קביעת שיחה."),
             ("אתר קטלוג", "קטלוג מוצרים או נכסים עם חיפוש וסינון, כמו באתרים של רהיטי השפלה וברקאי נכסים."),
             ("אתר פורטפוליו", "גלריות שמציגות עבודות לפי קטגוריה, לאמנים, מעצבים וסטודיו."),
             ("עיצוב מחדש לאתר קיים", "רענון לאתר שכבר עובד, בלי להתחיל מאפס."),
             ("עברית ומובייל", "ממשק מימין לשמאל שנוח לשימוש גם בטלפון.")],
       works=["barkai", "rahitei", "dor", "limor"],
       faq=[("האם האתר יהיה מותאם לטלפון?", "כן. כל אתר נבנה בעברית, מימין לשמאל, ונבדק גם בטלפון וגם במחשב."),
            ("יש לי כבר אתר. אפשר לשפר אותו?", "כן. אפשר לעצב מחדש אתר קיים ולשדרג אותו בלי להתחיל מאפס."),
            ("אפשר להוסיף לאתר קטלוג עם חיפוש?", "כן. בניתי קטלוגים עם חיפוש וסינון, למשל לרהיטי השפלה ולברקאי נכסים."),
            ("איך מתחילים?", "שולחים הודעה בוואטסאפ או באינסטגרם עם הרעיון, וקובעים שיחת היכרות קצרה.")]),
  dict(slug="apps", nav="פיתוח אפליקציות",
       title="פיתוח אפליקציות לעסקים: אייפון ואנדרואיד | TM Studio TLV",
       desc="פיתוח ועיצוב אפליקציות לעסקים לאייפון ולאנדרואיד: קביעת תורים, רשימות המתנה, הזמנות ופרופיל לקוח. מהרעיון ועד אפליקציה שעובדת.",
       h1="פיתוח אפליקציות לעסקים",
       lead="אפליקציה שהלקוחות שלכם משתמשים בה כל יום: קביעת תורים, רשימות המתנה, הזמנות ומעקב. אני מעצב את המסכים ומפתח את האפליקציה לאייפון ולאנדרואיד.",
       what=[("אפליקציה לקביעת תורים", "בחירת שירות, מועד ואיש צוות, עם תזכורות ורשימת המתנה כשאין מקום."),
             ("הזמנות ושיבוץ", "הזמנת אימונים, שיעורים או שירותים לפי מאמן, לפי שעה או לפי מקום."),
             ("פרופיל לקוח ומעקב", "היסטוריה, התקדמות אישית והעדפות, במקום אחד."),
             ("עיצוב אפליקציה", "מסכים, זרימות וחוויית שימוש, בעברית ומימין לשמאל."),
             ("עיצוב מחדש לאפליקציה קיימת", "רענון לאפליקציה שכבר עובדת, בלי להתחיל מאפס."),
             ("אייפון ואנדרואיד", "אפליקציה אחת שעובדת בשתי המערכות.")],
       works=["ping", "tal", "alma"],
       faq=[("האפליקציה תעבוד גם באייפון וגם באנדרואיד?", "כן. אני בונה את האפליקציה כך שתעבוד בשתי המערכות."),
            ("יש לי אפליקציה קיימת. אפשר לשפר אותה?", "כן. עיצבתי מחדש אפליקציות קיימות, למשל את PING ואת Studio Alma."),
            ("אפשר לראות את המסכים לפני שמתחילים לפתח?", "כן. בשלב השני אני מכין מסכים ראשונים, ואתם נותנים פידבק לפני הפיתוח."),
            ("איך מתחילים?", "שולחים הודעה בוואטסאפ או באינסטגרם עם הרעיון, וקובעים שיחת היכרות קצרה.")]),
  dict(slug="crm", nav="מערכות CRM",
       title="פיתוח מערכת CRM ומערכות לניהול העסק | TM Studio TLV",
       desc="פיתוח מערכת CRM ומערכות ניהול בהתאמה אישית לעסק: ניהול לקוחות, קריאות שירות, שיבוץ, חשבוניות, תשלומים ועדכונים ללקוחות.",
       h1="מערכת CRM ומערכות לניהול העסק",
       lead="מערכת שבנויה לפי הדרך שבה העסק שלכם עובד: ניהול לקוחות, קריאות שירות, שיבוץ עובדים, חשבוניות, תשלומים ועדכונים ללקוחות, במקום אחד.",
       what=[("ניהול לקוחות (CRM)", "כרטיס לכל לקוח, היסטוריה, פניות ומעקב, במקום אקסלים ופתקים."),
             ("קריאות שירות ושיבוץ", "פתיחת קריאה, שיבוץ טכנאי או עובד, ומעקב אחרי העבודה בשטח."),
             ("חשבוניות ותשלומים", "תהליכי עבודה של חשבוניות, גבייה ותשלומים בתוך המערכת."),
             ("עדכונים ללקוחות", "הודעות אוטומטיות ללקוח כשהסטטוס משתנה."),
             ("לוח בקרה למנהלים", "מדדי היום, עומס עבודה ומה ממתין לטיפול."),
             ("פורטל ללקוחות", "מקום שבו הלקוח רואה את הסטטוס שלו בלי להתקשר.")],
       works=["eagle", "rook"],
       faq=[("המערכת תהיה בהתאמה אישית?", "כן. המערכת נבנית לפי תהליכי העבודה של העסק שלכם, ולא להפך."),
            ("אפשר לשפר מערכת שכבר קיימת?", "כן. במערכת ROOK פיתחתי ושיפרתי תהליכים קיימים של חשבוניות, תשלומים ועדכונים ללקוחות."),
            ("המערכת תעבוד גם בטלפון?", "כן. המערכת נבנית כך שאפשר לעבוד בה גם מהשטח, בטלפון."),
            ("איך מתחילים?", "שולחים הודעה בוואטסאפ או באינסטגרם ומספרים איך העסק עובד היום, וקובעים שיחת היכרות קצרה.")]),
  dict(slug="shopify", nav="חנויות Shopify",
       title="בניית חנות Shopify ועיצוב חנות אונליין | TM Studio TLV",
       desc="בניית חנות Shopify ועיצוב מחדש לחנות אונליין קיימת, עם חוויית קנייה נוחה במובייל, וידאו וחיפוש מוצרים. בעברית ובאנגלית.",
       h1="בניית חנות Shopify",
       lead="חנות אונליין שנוח לקנות בה מהטלפון. אני מעצב ובונה חנויות Shopify חדשות, ומעצב מחדש חנויות שכבר עובדות.",
       what=[("חנות Shopify חדשה", "עמוד בית, קולקציות, עמודי מוצר ועגלה, מותאמים למותג."),
             ("עיצוב מחדש לחנות קיימת", "רענון לחנות שכבר מוכרת, בלי להתחיל מאפס."),
             ("קנייה נוחה במובייל", "עמודי מוצר וקולקציה שנבנו קודם כל לטלפון."),
             ("וידאו וחיפוש מוצרים", "וידאו בעמודי המוצר וחיפוש שעוזר למצוא מהר.")],
       works=["laymr"],
       faq=[("אפשר לשפר חנות Shopify שכבר קיימת?", "כן. את LAYMR עיצבתי מחדש על בסיס החנות הקיימת."),
            ("החנות תהיה נוחה לקנייה בטלפון?", "כן. רוב הקונים מגיעים מהטלפון, ולכן אני מתחיל מהמובייל."),
            ("איך מתחילים?", "שולחים הודעה בוואטסאפ או באינסטגרם עם קישור לחנות או לרעיון, וקובעים שיחת היכרות קצרה.")]),
  dict(slug="design", nav="עיצוב UX/UI",
       title="עיצוב אתרים ואפליקציות, UX/UI ועיצוב מחדש | TM Studio TLV",
       desc="עיצוב אתרים, דפי נחיתה ואפליקציות: עיצוב ממשק משתמש (UX/UI), עיצוב מחדש למוצר קיים והתאמה לעברית ולמובייל.",
       h1="עיצוב אתרים ואפליקציות",
       lead="עיצוב שנראה טוב ונוח לשימוש, בעברית ובכל מסך: אתרים, דפי נחיתה, אפליקציות ועיצוב מחדש למוצרים קיימים.",
       what=[("עיצוב אתרים ודפי נחיתה", "עיצוב שמותאם לעסק, מהמסך הראשון ועד כפתור הפנייה."),
             ("עיצוב אפליקציות", "מסכים, זרימות וחוויית שימוש לאפליקציות מובייל."),
             ("עיצוב מחדש למוצר קיים", "רענון לאתר, לחנות או לאפליקציה שכבר עובדים, בלי להתחיל מאפס."),
             ("התאמה לעברית ולמובייל", "ממשק מימין לשמאל שנוח לשימוש גם בטלפון.")],
       works=["laymr", "ping", "alma"],
       faq=[("אתם רק מעצבים, או גם בונים?", "שניהם. העיצוב והפיתוח נעשים במקום אחד, אז מה שמעוצב הוא מה שעולה לאוויר."),
            ("אפשר לעצב מחדש מוצר שכבר עובד?", "כן. עיצבתי מחדש את LAYMR, את PING ואת Studio Alma."),
            ("איך מתחילים?", "שולחים הודעה בוואטסאפ או באינסטגרם עם הרעיון, וקובעים שיחת היכרות קצרה.")]),
  dict(slug="ai-assistant", nav="עוזר AI לאתר",
       title="עוזר AI לאתר: צ'אטבוט חכם לעסק בעברית | TM Studio TLV",
       desc="עוזר AI לאתר העסק: צ'אטבוט שעונה למבקרים בעברית ובאנגלית על השירותים והעבודות, ומוביל אותם לפנייה.",
       h1="עוזר AI לאתר שלכם",
       lead="עוזר דיגיטלי שעונה למבקרים באתר בעברית ובאנגלית, מספר על השירותים והעבודות שלכם ומוביל אותם לפנייה. כמו העוזר שבאתר שלי.",
       what=[("עונה על שאלות המבקרים", "מה העסק עושה, למי זה מתאים ואיך מתחילים."),
             ("עברית ואנגלית", "העוזר עונה בשפה שבה פנו אליו."),
             ("מכיר את העסק שלכם", "התשובות מבוססות על השירותים, העבודות והמידע שלכם."),
             ("מוביל לפנייה", "בסוף השיחה המבקר יכול לשלוח הודעה או לקבוע שיחה.")],
       works=[],
       faq=[("איפה אפשר לראות עוזר כזה?", "בעמוד הבית של האתר הזה. לוחצים על העוזר הדיגיטלי ושואלים אותו."),
            ("העוזר עונה בעברית?", "כן, בעברית ובאנגלית."),
            ("איך מתחילים?", "שולחים הודעה בוואטסאפ או באינסטגרם עם קישור לאתר שלכם, וקובעים שיחת היכרות קצרה.")]),
]

CSS = """
@font-face{font-family:"Ploni";src:url("/fonts/ploni-400.woff2") format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:"Ploni";src:url("/fonts/ploni-700.woff2") format("woff2");font-weight:700;font-display:swap}
@font-face{font-family:"Ploni";src:url("/fonts/ploni-900.woff2") format("woff2");font-weight:900;font-display:swap}
@font-face{font-family:"Oswald";src:url("/fonts/oswald-var.woff2") format("woff2");font-weight:200 700;font-display:swap;unicode-range:U+0041-005A,U+0061-007A,U+0030-0039}
:root{--bg:#fff;--ink:#1D2014;--muted:#585C48;--olive:#434C17;--accent:#515C1B;--accent-hi:#606D22;--cream:#F3EEDD;--line:#E3E4D8;--wrap:min(1120px,100% - 48px);--ease:cubic-bezier(.23,1,.32,1)}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:400 17px/1.65 "Oswald","Ploni",Arial,sans-serif}
a{color:inherit}
img{display:block;max-width:100%;height:auto}
.wrap{width:var(--wrap);margin-inline:auto}
.skip{position:absolute;inset-inline-start:-999px}.skip:focus{inset-inline-start:12px;top:12px;background:#fff;padding:8px 12px;z-index:9}
header.top{border-bottom:1px solid var(--line)}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:20px;min-height:72px;flex-wrap:wrap;padding-block:10px}
.brand img{width:150px}
nav.svc{display:flex;flex-wrap:wrap;gap:4px 18px;font-size:.92rem}
nav.svc a{text-decoration:none;color:var(--muted);padding:4px 0;background:linear-gradient(currentColor,currentColor) 0 100%/0 1px no-repeat;transition:background-size .25s var(--ease),color .2s}
nav.svc a:hover,nav.svc a[aria-current]{color:var(--ink);background-size:100% 1px}
.hero{padding-block:clamp(56px,10vw,120px) clamp(40px,6vw,72px)}
.crumb{font-size:.85rem;color:var(--muted);margin:0 0 18px}
.crumb a{text-decoration:none}.crumb a:hover{text-decoration:underline}
h1{font-weight:900;font-size:clamp(2.4rem,6vw,4.6rem);line-height:1.02;letter-spacing:-.01em;margin:0 0 22px;max-width:16ch}
.lead{font-size:clamp(1.08rem,1.6vw,1.28rem);color:var(--muted);max-width:52ch;margin:0 0 32px}
.actions{display:flex;flex-wrap:wrap;gap:12px}
.btn{display:inline-flex;align-items:center;gap:10px;min-height:52px;padding:0 26px;border-radius:999px;background:var(--accent);color:#fff;text-decoration:none;font-weight:700;transition:background .2s,transform .16s var(--ease)}
.btn:hover{background:var(--accent-hi)}.btn:active{transform:scale(.97)}
.btn.ghost{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1.5px var(--ink)}
.btn.ghost:hover{background:var(--cream)}
section{padding-block:clamp(48px,7vw,88px)}
section.band{background:var(--cream)}
h2{font-weight:900;font-size:clamp(1.7rem,3.4vw,2.6rem);line-height:1.1;margin:0 0 32px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:28px 36px;list-style:none;margin:0;padding:0}
.grid h3{font-size:1.15rem;margin:0 0 6px;font-weight:700}
.grid p{margin:0;color:var(--muted)}
.grid li{border-top:2px solid var(--ink);padding-top:16px}
.works{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,420px),1fr));gap:36px}
.work{margin:0}
.work .ph{overflow:hidden;border-radius:14px;background:#EBEDDD;aspect-ratio:3/2}
.work .ph img{width:100%;height:100%;object-fit:cover;transition:transform .5s var(--ease)}
.work.tall .ph img{object-position:50% 30%}
.work:hover .ph img{transform:scale(1.03)}
.work h3{font:700 1.3rem/1.2 "Oswald","Ploni",sans-serif;margin:16px 0 6px;direction:ltr;text-align:right}
.work p{margin:0 0 8px;color:var(--muted)}
.work a.go{font-weight:700;text-decoration:none;color:var(--accent)}
.work a.go:hover{text-decoration:underline}
ol.steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:28px;counter-reset:s}
ol.steps li{counter-increment:s}
ol.steps li::before{content:"0" counter(s);display:block;font:600 2.4rem/1 "Oswald",sans-serif;color:var(--accent);margin-bottom:10px}
ol.steps h3{margin:0 0 6px;font-size:1.15rem}
ol.steps p{margin:0;color:var(--muted)}
.faq details{border-top:1px solid #CFD2BC;padding:18px 0}
.faq details:last-child{border-bottom:1px solid #CFD2BC}
.faq summary{cursor:pointer;font-weight:700;font-size:1.08rem;list-style:none;display:flex;justify-content:space-between;gap:16px}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";font:400 1.5rem/1 "Oswald",sans-serif;transition:transform .2s var(--ease)}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq p{margin:10px 0 0;color:var(--muted);max-width:64ch}
.cta{text-align:center}
.cta h2{margin-bottom:14px}.cta p{color:var(--muted);margin:0 0 28px}.cta .actions{justify-content:center}
.more{display:flex;flex-wrap:wrap;gap:10px;list-style:none;padding:0;margin:0}
.more a{display:inline-block;padding:10px 18px;border-radius:999px;box-shadow:inset 0 0 0 1px #CFD2BC;text-decoration:none;transition:background .2s}
.more a:hover{background:var(--cream)}
footer{border-top:1px solid var(--line);padding-block:32px;color:var(--muted);font-size:.9rem}
footer .wrap{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px}
footer a{text-decoration:none}footer a:hover{text-decoration:underline}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:4px}
@media (max-width:640px){body{font-size:16px}.brand img{width:120px}header.top .wrap{flex-wrap:nowrap;flex-direction:column;align-items:flex-start;gap:6px}nav.svc{font-size:.88rem;gap:16px;flex-wrap:nowrap;overflow-x:auto;width:100%;padding-bottom:4px;scrollbar-width:none;white-space:nowrap}}
"""

ARROW = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>'
e = html.escape

GTAG = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gtag.html"), encoding="utf-8").read().strip()

def page(p):
    url = f"{SITE}/{p['slug']}/"
    nav = "".join(f'<a href="/{q["slug"]}/"{" aria-current=\"page\"" if q is p else ""}>{e(q["nav"])}</a>' for q in PAGES)
    what = "".join(f"<li><h3>{e(a)}</h3><p>{e(b)}</p></li>" for a, b in p["what"])
    works = ""
    if p["works"]:
        cards = []
        for k in p["works"]:
            w = WORKS[k]; tall = w["h"] > w["w"]
            go = f'<a class="go" href="{w["url"]}" target="_blank" rel="noopener">לאתר {e(w["url"].split("//")[1].rstrip("/").replace("www.",""))}</a>' if w["url"] else ""
            cards.append(f'<figure class="work{" tall" if tall else ""}"><div class="ph"><img src="/{w["img"]}" alt="{e(w["alt"])}" width="{w["w"]}" height="{w["h"]}" loading="lazy" decoding="async"></div>'
                         f'<figcaption><h3>{e(w["n"])}</h3><p>{e(w["d"])}</p>{go}</figcaption></figure>')
        works = f'<section aria-labelledby="w-h"><div class="wrap"><h2 id="w-h">עבודות לדוגמה</h2><div class="works">{"".join(cards)}</div></div></section>'
    steps = "".join(f"<li><h3>{e(a)}</h3><p>{e(b)}</p></li>" for a, b in STEPS)
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in p["faq"])
    more = "".join(f'<li><a href="/{q["slug"]}/">{e(q["nav"])}</a></li>' for q in PAGES if q is not p)
    ld = [
      {"@context": "https://schema.org", "@type": "Service", "name": p["h1"], "serviceType": p["nav"], "description": p["desc"], "url": url,
       "areaServed": {"@type": "Country", "name": "Israel"}, "availableLanguage": ["he", "en"],
       "provider": {"@type": "ProfessionalService", "@id": f"{SITE}/#studio", "name": "TM Studio TLV", "url": SITE + "/"}},
      {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
         {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
         {"@type": "ListItem", "position": 1, "name": "TM Studio TLV", "item": SITE + "/"},
         {"@type": "ListItem", "position": 2, "name": p["nav"], "item": url}]},
    ]
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
{GTAG}
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(p["title"])}</title>
<meta name="description" content="{e(p["desc"])}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="he" href="{url}">
<link rel="alternate" hreflang="en" href="{SITE}/en/{p['slug']}/">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="TM Studio TLV">
<meta property="og:locale" content="he_IL">
<meta property="og:title" content="{e(p["title"])}">
<meta property="og:description" content="{e(p["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="/fonts/ploni-900.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/ploni-400.woff2" as="font" type="font/woff2" crossorigin>
{lds}
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">דילוג לתוכן</a>
<header class="top"><div class="wrap">
  <a class="brand" href="/" aria-label="TM Studio TLV, לעמוד הבית"><img src="/logo.svg" alt="Tomer Mazuz · TM Studio TLV" width="900" height="225"></a>
  <nav class="svc" aria-label="שירותים">{nav}<a href="/en/{p['slug']}/" hreflang="en" lang="en">EN</a></nav>
</div></header>
<main id="main">
<div class="hero"><div class="wrap">
  <p class="crumb"><a href="/">TM Studio TLV</a> / {e(p["nav"])}</p>
  <h1>{e(p["h1"])}</h1>
  <p class="lead">{e(p["lead"])}</p>
  <div class="actions">
    <a class="btn" href="{WA}" target="_blank" rel="noopener">שלחו הודעה בוואטסאפ {ARROW}</a>
    <a class="btn ghost" href="{IG}" target="_blank" rel="noopener">או באינסטגרם</a>
  </div>
</div></div>
<section class="band" aria-labelledby="what-h"><div class="wrap">
  <h2 id="what-h">מה אפשר לבנות</h2>
  <ul class="grid">{what}</ul>
</div></section>
{works}
<section class="band" aria-labelledby="how-h"><div class="wrap">
  <h2 id="how-h">איך זה עובד</h2>
  <ol class="steps">{steps}</ol>
</div></section>
<section class="faq" aria-labelledby="faq-h"><div class="wrap">
  <h2 id="faq-h">שאלות נפוצות</h2>
  {faq}
</div></section>
<section class="cta band" aria-labelledby="cta-h"><div class="wrap">
  <h2 id="cta-h">יש לכם רעיון? ספרו לי עליו.</h2>
  <p>עיצוב ופיתוח במקום אחד, מהרעיון הראשון ועד מוצר שעובד.</p>
  <div class="actions">
    <a class="btn" href="{WA}" target="_blank" rel="noopener">שלחו הודעה בוואטסאפ {ARROW}</a>
    <a class="btn ghost" href="/">לכל העבודות באתר</a>
  </div>
</div></section>
<section aria-labelledby="more-h"><div class="wrap">
  <h2 id="more-h">עוד שירותים</h2>
  <ul class="more">{more}</ul>
</div></section>
</main>
<footer><div class="wrap">
  <span>תומר מזוז · TM Studio TLV · תל אביב</span>
  <span><a href="{WA}" target="_blank" rel="noopener">וואטסאפ</a> · <a href="https://www.instagram.com/tmstudio.tlv/" target="_blank" rel="noopener">אינסטגרם</a> · <a href="https://www.linkedin.com/in/tomermazuz1/" target="_blank" rel="noopener">לינקדאין</a> · <a href="/">עמוד הבית</a></span>
</div></footer>
</body>
</html>
"""

from en_data import WORKS_EN, STEPS_EN, PAGES_EN
EN_ARROW = ARROW.replace('M19 12H5M11 6l-6 6 6 6', 'M5 12h14M13 6l6 6-6 6')

def page_en(p):
    q = PAGES_EN[p["slug"]]
    url = f"{SITE}/en/{p['slug']}/"; he = f"{SITE}/{p['slug']}/"
    nav = "".join(f'<a href="/en/{r["slug"]}/"{" aria-current=\"page\"" if r is p else ""}>{e(PAGES_EN[r["slug"]]["nav"])}</a>' for r in PAGES)
    what = "".join(f"<li><h3>{e(a)}</h3><p>{e(b)}</p></li>" for a, b in q["what"])
    works = ""
    if p["works"]:
        cards = []
        for k in p["works"]:
            w = WORKS[k]; d, alt = WORKS_EN[k]; tall = w["h"] > w["w"]
            go = f'<a class="go" href="{w["url"]}" target="_blank" rel="noopener">Visit {e(w["url"].split("//")[1].rstrip("/").replace("www.",""))}</a>' if w["url"] else ""
            cards.append(f'<figure class="work{" tall" if tall else ""}"><div class="ph"><img src="/{w["img"]}" alt="{e(alt)}" width="{w["w"]}" height="{w["h"]}" loading="lazy" decoding="async"></div>'
                         f'<figcaption><h3>{e(w["n"])}</h3><p>{e(d)}</p>{go}</figcaption></figure>')
        works = f'<section aria-labelledby="w-h"><div class="wrap"><h2 id="w-h">Selected work</h2><div class="works">{"".join(cards)}</div></div></section>'
    steps = "".join(f"<li><h3>{e(a)}</h3><p>{e(b)}</p></li>" for a, b in STEPS_EN)
    faq = "".join(f"<details><summary>{e(x)}</summary><p>{e(y)}</p></details>" for x, y in q["faq"])
    more = "".join(f'<li><a href="/en/{r["slug"]}/">{e(PAGES_EN[r["slug"]]["nav"])}</a></li>' for r in PAGES if r is not p)
    ld = [
      {"@context": "https://schema.org", "@type": "Service", "name": q["h1"], "serviceType": q["nav"], "description": q["desc"], "url": url,
       "areaServed": "Worldwide", "availableLanguage": ["en", "he"],
       "provider": {"@type": "ProfessionalService", "@id": f"{SITE}/#studio", "name": "TM Studio TLV", "url": SITE + "/en"}},
      {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
         {"@type": "Question", "name": x, "acceptedAnswer": {"@type": "Answer", "text": y}} for x, y in q["faq"]]},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
         {"@type": "ListItem", "position": 1, "name": "TM Studio TLV", "item": SITE + "/en"},
         {"@type": "ListItem", "position": 2, "name": q["nav"], "item": url}]},
    ]
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    css = CSS.replace(".work h3{font:700 1.3rem/1.2 \"Oswald\",\"Ploni\",sans-serif;margin:16px 0 6px;direction:ltr;text-align:right}", ".work h3{font:700 1.3rem/1.2 \"Oswald\",\"Ploni\",sans-serif;margin:16px 0 6px}")
    return f"""<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
{GTAG}
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(q["title"])}</title>
<meta name="description" content="{e(q["desc"])}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="he" href="{he}">
<link rel="alternate" hreflang="en" href="{url}">
<link rel="alternate" hreflang="x-default" href="{he}">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="TM Studio TLV">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{e(q["title"])}">
<meta property="og:description" content="{e(q["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
{lds}
<style>{css}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap">
  <a class="brand" href="/en" aria-label="TM Studio TLV, home"><img src="/logo.svg" alt="Tomer Mazuz · TM Studio TLV" width="900" height="225"></a>
  <nav class="svc" aria-label="Services">{nav}<a href="/{p['slug']}/" hreflang="he" lang="he">עב</a></nav>
</div></header>
<main id="main">
<div class="hero"><div class="wrap">
  <p class="crumb"><a href="/en">TM Studio TLV</a> / {e(q["nav"])}</p>
  <h1>{e(q["h1"])}</h1>
  <p class="lead">{e(q["lead"])}</p>
  <div class="actions">
    <a class="btn" href="{WA}" target="_blank" rel="noopener">Message me on WhatsApp {EN_ARROW}</a>
    <a class="btn ghost" href="{IG}" target="_blank" rel="noopener">or on Instagram</a>
  </div>
</div></div>
<section class="band" aria-labelledby="what-h"><div class="wrap">
  <h2 id="what-h">What we can build</h2>
  <ul class="grid">{what}</ul>
</div></section>
{works}
<section class="band" aria-labelledby="how-h"><div class="wrap">
  <h2 id="how-h">How it works</h2>
  <ol class="steps">{steps}</ol>
</div></section>
<section class="faq" aria-labelledby="faq-h"><div class="wrap">
  <h2 id="faq-h">Questions</h2>
  {faq}
</div></section>
<section class="cta band" aria-labelledby="cta-h"><div class="wrap">
  <h2 id="cta-h">Got an idea? Tell me about it.</h2>
  <p>Design and development in one place, from the first idea to a product that works.</p>
  <div class="actions">
    <a class="btn" href="{WA}" target="_blank" rel="noopener">Message me on WhatsApp {EN_ARROW}</a>
    <a class="btn ghost" href="/en">See all the work</a>
  </div>
</div></section>
<section aria-labelledby="more-h"><div class="wrap">
  <h2 id="more-h">More services</h2>
  <ul class="more">{more}</ul>
</div></section>
</main>
<footer><div class="wrap">
  <span>Tomer Mazuz · TM Studio TLV · Tel Aviv</span>
  <span><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a> · <a href="https://www.instagram.com/tmstudio.tlv/" target="_blank" rel="noopener">Instagram</a> · <a href="https://www.linkedin.com/in/tomermazuz1/" target="_blank" rel="noopener">LinkedIn</a> · <a href="/en">Home</a></span>
</div></footer>
</body>
</html>
"""

for p in PAGES:
    d = os.path.join(ROOT, p["slug"]); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(p))
    d = os.path.join(ROOT, "en", p["slug"]); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page_en(p))

pairs = [(SITE + "/", SITE + "/en")] + [(f"{SITE}/{p['slug']}/", f"{SITE}/en/{p['slug']}/") for p in PAGES]
def alt(h, en): return f'<xhtml:link rel="alternate" hreflang="he" href="{h}"/><xhtml:link rel="alternate" hreflang="en" href="{en}"/>'
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + \
     "".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod>{alt(h, en)}</url>\n" for h, en in pairs for u in (h, en)) + "</urlset>\n"
open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
print("built", [p["slug"] for p in PAGES], "+ en")
