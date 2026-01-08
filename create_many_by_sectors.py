#!/usr/bin/env python3
"""
Sector-based Template Generator for LifeCloud
Creates personalized email templates for each contact in the leads database.
Generates 2 versions (A & B) per contact and saves them as TXT files.
"""

import os
import re
from pathlib import Path

# Contact data from HTML
leads_data = [
    # Municipalities
    {"name": "עיריית תל אביב-יפו", "sector": "muni", "role": "מחלקת טקסים והנצחה", "contact": "03-724-4444 | tksim@tel-aviv.gov.il", "note": "תקציב עתק, ריכוז משפחות גבוה."},
    {"name": "עיריית ירושלים", "sector": "muni", "role": "אגף הנצחת החייל", "contact": "02-629-7777 | hantzacha@jerusalem.muni.il", "note": "אתרים לאומיים בשטח העיר."},
    {"name": "עיריית חיפה", "sector": "muni", "role": "יד לבנים חיפה", "contact": "04-835-6111 | pniot@haifa.muni.il", "note": "קהילה צפונית חזקה."},
    {"name": "עיריית ראשון לציון", "sector": "muni", "role": "מזכירות העיר", "contact": "03-968-2111 | info@rishonlezion.muni.il", "note": "עיר מובילה בהנצחה דיגיטלית."},
    {"name": "עיריית באר שבע", "sector": "muni", "role": "יד לבנים ב\"ש", "contact": "08-646-3777 | pniot@br7.muni.il", "note": "מרכז הנצחה דרומי."},
    {"name": "עיריית פתח תקווה", "sector": "muni", "role": "מחלקת אירועים", "contact": "03-939-2222 | pniot@ptth.org.il", "note": "קהל יעד משמעותי."},
    {"name": "עיריית נתניה", "sector": "muni", "role": "לשכת ראש העיר", "contact": "09-860-3333 | pniot@netanya.muni.il", "note": "ריבוי אנדרטאות חוף."},
    {"name": "עיריית חולון", "sector": "muni", "role": "אגף תרבות", "contact": "03-502-7222 | pniot@holon.muni.il", "note": "דגש על חינוך ומורשת."},
    {"name": "עיריית אשדוד", "sector": "muni", "role": "מוקד עירוני", "contact": "08-854-5454 | pniot@ashdod.muni.il", "note": "פוטנציאל פרויקט רחב."},
    {"name": "עיריית רמת גן", "sector": "muni", "role": "מחלקת הנצחה", "contact": "03-612-3333 | pniot@ramat-gan.muni.il", "note": "אתרי הנצחה יחידתיים."},
    {"name": "עיריית מודיעין", "sector": "muni", "role": "מחלקת נוער והנצחה", "contact": "08-972-6000 | pniot@modiin.muni.il", "note": "אחוז גיוס גבוה מאוד."},
    {"name": "מועצה אזורית אשכול", "sector": "muni", "role": "צוותי צמיחה", "contact": "08-992-9111 | info@eshkol.info", "note": "קריטי: הנצחת אירועי ה-7.10."},
    {"name": "מועצה אזורית שער הנגב", "sector": "muni", "role": "דוברות והנצחה", "contact": "08-680-6211 | info@sng.org.il", "note": "פרויקטים קהילתיים בקיבוצים."},
    {"name": "עיריית שדרות", "sector": "muni", "role": "לשכת ראש העיר", "contact": "08-662-3333 | info@sderot.muni.il", "note": "מיקוד בגבורה אזרחית."},
    {"name": "עיריית אופקים", "sector": "muni", "role": "מזכירות", "contact": "08-681-4444 | pniot@ofaqim.muni.il", "note": "הנצחת קרבות ה-7.10 בעיר."},
    {"name": "עיריית הרצליה", "sector": "muni", "role": "מחלקת מורשת", "contact": "09-959-1515 | pniot@herzliya.muni.il", "note": "קהילה איכותית ותורמת."},
    {"name": "עיריית רעננה", "sector": "muni", "role": "אגף תרבות", "contact": "09-771-2777 | pniot@raanana.muni.il", "note": "מרכז טכנולוגי."},
    {"name": "עיריית כפר סבא", "sector": "muni", "role": "יד לבנים", "contact": "09-764-9111 | pniot@ksaba.org.il", "note": "מסורת הנצחה ארוכה."},
    {"name": "עיריית הוד השרון", "sector": "muni", "role": "מזכירות", "contact": "09-775-1234 | pniot@hod-hasharon.muni.il", "note": "קהילה מגובשת."},
    {"name": "עיריית רחובות", "sector": "muni", "role": "לשכת ראש העיר", "contact": "08-938-1111 | pniot@rehovot.muni.il", "note": "מרכז האקדמיה הישראלית."},
    {"name": "עיריית נס ציונה", "sector": "muni", "role": "מחלקת אירועים", "contact": "08-940-2020 | pniot@nz.org.il", "note": "עיר צעירה ודינמית."},
    {"name": "עיריית יבנה", "sector": "muni", "role": "מזכירות", "contact": "08-943-3030 | pniot@yavne.muni.il", "note": "מקום ההתחדשות הרוחנית."},
    {"name": "עיריית רמלה", "sector": "muni", "role": "אגף חינוך", "contact": "08-924-1212 | pniot@ramla.muni.il", "note": "עיר מעורבת."},
    {"name": "עיריית לוד", "sector": "muni", "role": "מוקד עירוני", "contact": "08-922-2222 | pniot@lod.muni.il", "note": "מורכבות חברתית."},
    {"name": "מועצה אזורית חוף אשקלון", "sector": "muni", "role": "דוברות", "contact": "08-673-8800 | info@hof-ashkelon.org.il", "note": "יישובים בעוטף עזה."},
    {"name": "עיריית אשקלון", "sector": "muni", "role": "מחלקת רווחה", "contact": "08-674-5000 | pniot@ashkelon.muni.il", "note": "עיר חוף עם מסורת."},

    # IDF Units & Associations
    {"name": "עמותת גולני", "sector": "idf", "role": "אתר הנצחה צומת גולני", "contact": "04-676-3333 | golani@golani.co.il", "note": "העמותה החזקה ביותר בצה\"ל."},
    {"name": "עמותת גבעתי", "sector": "idf", "role": "מצודת יואב", "contact": "08-672-4661 | givati@givati.org.il", "note": "פעילות ענפה בדרום."},
    {"name": "עמותת הצנחנים", "sector": "idf", "role": "בית הצנחן", "contact": "03-613-2222 | paratroops@gmail.com", "note": "מורשת קרב מפוארת. דובדבן כבר איתנו."},
    {"name": "עמותת חיל השריון", "sector": "idf", "role": "יד לשריון לטרון", "contact": "08-630-7400 | yadlashiryon@yadlashiryon.com", "note": "אתר בינלאומי."},
    {"name": "עמותת המודיעין (מלמ)", "sector": "idf", "role": "מרכז המורשת בגלילות", "contact": "03-549-7222 | info@iicc.org.il", "note": "חיבור טבעי ל'ענן' ודיגיטל."},
    {"name": "עמותת חיל האוויר", "sector": "idf", "role": "מוזיאון חצרים", "contact": "09-956-6560 | info@iaf.org.il", "note": "נכונות גבוהה לטכנולוגיה."},
    {"name": "עמותת חיל הים", "sector": "idf", "role": "מזכירות", "contact": "03-606-4444 | amutayam@gmail.com", "note": "מסורת ימית עתיקה."},
    {"name": "עמותת הנח\"ל", "sector": "idf", "role": "אתר הנצחה פרדס חנה", "contact": "04-637-8888 | nahal@nahal.org.il", "note": "חלוצי ההתיישבות."},
    {"name": "עמותת דובדבן", "sector": "idf", "role": "לקוח קיים", "contact": "03-123-4567 | duvdevan@amuta.org", "note": "לקוח קיים - להשתמש כמודל הוכחה."},
    {"name": "יחידת שלדג (עמותה)", "sector": "idf", "role": "מזכירות", "contact": "03-765-4321 | shaldag@amuta.org", "note": "יחידת קומנדו אוויר."},
    {"name": "יחידת 669 (עמותה)", "sector": "idf", "role": "מזכירות", "contact": "03-234-5678 | 669@amuta.org", "note": "חילוץ והצלה."},
    {"name": "עמותת סיירת מטכ\"ל", "sector": "idf", "role": "מזכירות", "contact": "03-345-6789 | matkal@amuta.org", "note": "יחידת העילית של הצבא."},
    {"name": "עמותת השריון 401", "sector": "idf", "role": "מזכירות", "contact": "08-456-7890 | 401@amuta.org", "note": "ברק השריון."},
    {"name": "עמותת חטיבה 7", "sector": "idf", "role": "מזכירות", "contact": "08-567-8901 | h7@amuta.org", "note": "שריון כבד."},
    {"name": "עמותת הנדסה קרבית", "sector": "idf", "role": "מזכירות", "contact": "03-678-9012 | handasa@handasa.org.il", "note": "מנהור וחבלה."},

    # Youth Movements
    {"name": "תנועת הצופים", "sector": "youth", "role": "מחלקת הנצחה ומורשת", "contact": "03-636-6444 | zofim@zofim.org.il", "note": "אתרים בכל שבט ושבט."},
    {"name": "הנוער העובד והלומד", "sector": "youth", "role": "מזכירות", "contact": "03-512-4222 | info@noal.org.il", "note": "דגש סוציאליסטי-חלוצי."},
    {"name": "בני עקיבא", "sector": "youth", "role": "הנהלה ארצית", "contact": "03-760-8900 | info@bneiakiva.org.il", "note": "ציבור דתי לאומי גדול."},
    {"name": "השומר הצעיר", "sector": "youth", "role": "הנהגה", "contact": "03-517-5111 | info@hashomer-hatzair.org", "note": "הנצחה בקיבוצים."},
    {"name": "תנועת עזרא", "sector": "youth", "role": "מזכירות", "contact": "02-673-4567 | info@ezra.org.il", "note": "תנועה דתית מזרחית."},
    {"name": "מכבי צעיר", "sector": "youth", "role": "מזכירות", "contact": "03-673-4444 | info@mtz.org.il", "note": "ספורט וחברה."},
    {"name": "האיחוד החקלאי", "sector": "youth", "role": "מזכירות", "contact": "03-789-0123 | info@ih.org.il", "note": "חקלאות וכפר."},

    # Emergency & Rescue
    {"name": "מערך הכבאות והצלה", "sector": "emergency", "role": "דוברות", "contact": "102 | 102@102.gov.il", "note": "גבורת לוחמי אש. פרויקט כבאות קיים."},
    {"name": "משטרת ישראל", "sector": "emergency", "role": "אגף משאבי אנוש", "contact": "100 | pniot@police.gov.il", "note": "הנצחת שוטרי ה-7.10."},
    {"name": "זק\"א", "sector": "emergency", "role": "דוברות והנצחה", "contact": "1220 | info@zaka.org.il", "note": "הנצחת מתנדבי גבורה."},
    {"name": "מגן דוד אדום", "sector": "emergency", "role": "יח' קשרי חוץ", "contact": "101 | mda@mda.org.il", "note": "ארגון רפואי לאומי."},
    {"name": "איחוד הצלה", "sector": "emergency", "role": "מזכירות", "contact": "1221 | info@1221.org.il", "note": "מתנדבי הצלה."}
]

# Template data from HTML - version A & B
templates = {
    "muni": {
        "subject": "הנצחה דיגיטלית ב[שם העיר] עם  Life Cloud - תמיר הספל",
        "body": """לכבוד [תפקיד/מחלקה],

שמי תמיר הספל, אני מנכ"ל של Life cloud
חברת ההנצחה הדיגיטלית הראשונה בישראל 

אנחנו גאים להציע את שרותינו בתור פלטפורמה ייחודית להנצחה דיגיטלית, המאפשרת להנציח את הסיפור של החיים של
נופלי ונפטרי [שם העיר], ולהוסיף זיכרונות בכל עת ומכל מקום,
על ידי עמוד הנצחה דיגיטלי המכיל :"תמונות", "סרטונים" 
,"אפשרויות לחברים ומשפחה לחלוק סיפורים אודות הנפטר" וכן אפשרויות להדליק נרות
ולהניח פרחים באופן דיגיטאלי עבורו
מלבד ההנצחה עצמה אנחנו מציעים ברקוד ייחודי ואיכותי שאותו ניתן להניח בקבר המנוח או במקום משמעותי אחר
וכך כל באי המקום יוכלו להחשף לסיפור בלחיצת כפתור אחת.
עם ניסיון של שנים בבניית פרוייקטים משמעותיים לנצחה כמו יד לבנים טבריה
 (נשמח לשלוח לכם תמונות מהפרוייקט אם תבקשו כמובן), 
 הנצחת נרצחי הנובה, יחידת דובדבן ועוד רבים שבחרו להנציח דרכנו את האהובים שלהם,
אני כותב לכם  בהצעה לשיתוף פעולה להנציח את נופלי העיר [שם העיר] באופן משמעותי ומכובד. 
.
יום הזיכרון השנה יהיה באפריל, ואנחנו מתחילים פרויקטים כבר מעכשיו
מצרף קישור לאתר שלנו:
 https://www.lifecloud-qr.com/
מתי יתאים לכם לדבר בבקשה?

אנחנו זמינים עבורכם תמיד במייל:
office@lifecloud-qr.com
או במספרים: 0523705058 (משרדי)
0545344947 (אישי, ותרגישו חופשי לפנות)
אם תרצו, נשמח להגיע לפגישה להרחיב על השירותים שלנו ולחשוב יחד כיצד נוכל להנגיש את ההנצחה והזכרונות באופן משמעותי עבור המשפחות ב[שם העיר]

תודה רבה ושנה בטוחה וטובה!
תמיר הספל
 מנכ"ל  LIFE CLOUD
"""
    },
    "muni2": {
"subject": "בניית הנצחה דיגיטאלית ב [שם העיר] עם חברת Life Cloud",
"body": """לכבוד [תפקיד/מחלקה],
שמי תמיר הספל, אני מנכ"ל של Life cloud
חברת ההנצחה הדיגיטלית הראשונה בישראל 
אנחנו מלווים פרוייקטים ברשויות מקומיות על מנת להנציח את נופלי העיר, ואת הסיפור האנושי שמאחוריהם.
יום הזיכרון השנה יהיה באפריל, כלומר אנחנו מתחילים פרויקטים כבר מעכשיו
הרעיון פשוט: ליד המצבה/אנדרטה מוצב QR עמיד, שמוביל לעמוד זיכרון עשיר—תמונות, סרטונים, קטעי קול, סיפורים של חברים ומשפחה, ונקודות "רגעים" לאורך החיים. במקום שהזיכרון יישאר שורה באבן, הוא הופך ל"עולם ומלואו" שממשיך לחיות דרך הקהילה.

ברמה התפעולית זה עובד מהר: מגדירים אתרים, אוספים חומרים בצורה מסודרת (אפשר גם עם ליווי עריכה), ומטמיעים בשטח בלוז קצר.
עם ניסיון של שנים בבניית פרוייקטים משמעותיים לנצחה כמו יד לבנים טבריה , (נשמח לשלוח לכם תמונות מהפרוייקט אם תבקשו כמובן), הנצחת נרצחי הנובה, יחידת דובדבן ועוד רבים שבחרו להנציח דרכנו את האהובים שלהם,
אנחנו נשמח לתאם שיחה השבוע ויחד להנציח את נופלי [שם העיר] באופן משמעותי ומכובד. 
.אם זה בסדר מבחינתכם, אנחנו נשמח לתאם שיחה השבוע 
או שתפנו אותנו לגורם שניתן לדבר עימו
בברכת שנה טובה ובטוחה
תמיר הספל ,
 מנכ"ל LIFE CLOUD  
מייל:  office@lifecloud-qr.com
משרד: 0523705058 
אישי: 0545344947
"""
    },
    "idf": {
        "subject": "שימור מורשת הלוחמים של [שם היחידה] עם חברת Life Cloud - תמיר הספל",
        "body": """שלום [תפקיד/מחלקה],

שמי תמיר הספל, אני מנכ"ל של Life cloud
חברת ההנצחה הדיגיטלית הראשונה בישראל 

אנחנו מציעים פלטפורמה ייחודית להנצחה דיגיטאלית, שמאפשרת לשמור את סיפורי הגבורה והחיים של הלוחמים ולהוסיף זיכרונות בכל עת.
אנחנו מייצרים ברקוד איכותי שניתן להציב באנדרטאות של היחידה או בפינות המורשת, מה שמאפשר לכל חייל או מבקר
להיחשף לסיפור המלא של הנופל בתוך שנייה.

עבדנו על פרוייקטים משמעותיים כגון  הנצחת לוחמי דובדבן וחללי הנובה - פרויקטים שבהם היה לנו חשוב
להפוך את הזיכרון למשהו חי, נגיש ופתוח לכולם .

נשמח מאוד להציע לכם שיתוף פעולה להנצחת נופלי [שם היחידה] לקראת יום הזיכרון הקרוב החל באפריל.
אנחנו נשמח לתאם שיחה השבוע במידת הניתן
 וכמובן אם תרצו נשמח להיפגש, להכיר ולחשוב יחד איך להנגיש את המורשת שלכם בצורה הכי עוצמתית שיש.

אפשר להתרשם כאן מעמוד שנעשה עבור עמותת השייטת
https://www.lifecloud-qr.com/organization-profile/62baf5cff10da082cb5d58b4

בברכת שנה טובה ובטוחה
תמיר הספל ,
 מנכ"ל LIFE CLOUD  
מייל:  office@lifecloud-qr.com
משרד: 0523705058 
אישי: 0545344947

"""
    },
    "idf2": {
        "subject": "לשמר את מורשת [שם היחידה/העמותה] עם חברת  Life Cloud",
        "body": """לכבוד [תפקיד/מחלקה],

שמי תמיר הספל, אני מנכ"ל של Life cloud
חברת ההנצחה הדיגיטלית הראשונה בישראל 
אני כותב מתוך כבוד גדול למה שאתם עושים בשימור המורשת של [שם הארגון]. 
האתגר שאנחנו שומעים שוב ושוב הוא לא רק "להנציח" ,
 אלא כיצד להנגיש את הסיפור המלא, בצורה שמרגישה חיה ולא טקסית בלבד.

אנחנו מספקים פלטפורמת הנצחה דיגיטלית ובה עמודי מורשת וזיכרון,
 ("קיר") שבו חברים מהפלוגה/מחזור וכן משפחה ומכרים,
 מוסיפים סיפורים ותמונות לאורך שנים,
 ואפשרות לייצר ציר-זמן שמחבר בין נקודות השירות והאישיות.
בנוסף אנחנו מספקים QR לעמודים אלו אשר יותקנו באתרי ההנצחה הקיימים או הקברים ,
 שיובילו לעמודי הנופלים.

זה יוצר חוויה ייחודית ומדהימה עבור כל מי שהכיר את הנופלים ואלו שרוצים ללמוד על מורשתם, סריקה אחת,
 ומקבלים מפגש אמיתי עם האדם, לא רק עם האבן.
נשמח לתאם שיחה עימכם
אם תרצו, נקבע הדגמה ונראה איך זה נראה בשטח עבור ארגונים שכבר שיתפנו איתם פעולה.
אפשר להתרשם כאן מעמוד שנעשה עבור עמותת השייטת:
https://www.lifecloud-qr.com/organization-profile/62baf5cff10da082cb5d58b4

בברכת שנה טובה ובטוחה
תמיר הספל ,
 מנכ"ל LIFE CLOUD  
מייל:  office@lifecloud-qr.com
משרד: 0523705058 
אישי: 0545344947


"""
    },
    "youth": {
        "subject": "פרויקט הנצחה עבור חניכי ובוגרי [שם התנועה] עם חברת Life Cloud",
        "body": """לכבוד [תפקיד/מחלקה],

שמי תמיר הספל, אני מנכ"ל של Life cloud
חברת ההנצחה הדיגיטלית הראשונה בישראל 

אנחנו עוסקים בהנצחה דיגיטלית שנועדה לחבר את הדור הצעיר לסיפורים שמאחורי האבנים.
הפלטפורמה שלנו מאפשרת להקים דף זיכרון חי עם תמונות וסרטונים,
שנגיש דרך ברקוד ייחודי שאנחנו מציבים באתרי הנצחה או בפינות הזיכרון של התנועה.

עבדנו על פרוייקטים רגישים וחשובים כמו יד לבנים בטבריה, ונרצחי הנובה, ואנחנו רואים כמה זה משמעותי
לבני נוער ולחניכים (כמו כן למשפחת הנופלים ומכריהם)שפשוט סורקים את הקוד ומתחברים לסיפור האישי.

נשמח לתאם שיחה עימכם ולהציע שיתוף פעולה להנצחת בוגרי [שם התנועה] לקראת יום הזיכרון. 
אם תרצו, נקבע הדגמה ונראה איך זה נראה בשטח עבור ארגונים שכבר שיתפנו איתם פעולה,
ולהראות לכם איך זה עובד ולראות איך מחברים את החניכים למורשת שלכם.

אפשר להתרשם כאן מעמוד שנעשה עבור עמותת השייטת:
https://www.lifecloud-qr.com/organization-profile/62baf5cff10da082cb5d58b4

בברכת שנה טובה ובטוחה
תמיר הספל ,
 מנכ"ל LIFE CLOUD  
מייל:  office@lifecloud-qr.com
משרד: 0523705058 
אישי: 0545344947

"""
    },
    "youth2": {
        "subject": "להפוך את יום הזיכרון ב־[שם התנועה] עם חברת Life Cloud למפגש חינוכי פעיל",
        "body": """שלום [תפקיד/מחלקה],
שמי תמיר הספל, אני מנכ"ל של Life cloud
חברת ההנצחה הדיגיטלית הראשונה בישראל 
ב־[שם הארגון] אתם מחנכים דרך חוויה, שייכות וסיפור.
בדיוק שם הנצחה יכולה להפוך ממשהו ש"שומעים עליו" למשהו ש"פוגשים".
אנחנו מציעים פתרון שמאפשר להציב בפינת זיכרון/לוח הנצחה QR 
קטן ומכבד, שמוביל לעמוד סיפור חיים: תמונות, סרטונים, קטעי קול,
משפטים של חברים, "רגעים" לאורך השנים,
וספר אורחים שבו חניכים ובוגרים יכולים להשאיר זיכרון אישי או תובנה—באישור וליווי מבוגרים.
זה לא בא להחליף טקס—זה נותן לו עומק.

 החניכים לא רק עומדים מול לוח; הם נוגעים בסיפור, מבינים מי היה האדם ומה הוא השאיר אחריו.

אם מתאים, אשמח לשיחה קצרה כדי להתאים פעילות/תוכן לפי הגילאים והמסגרת אצלכם.
אפשר להתרשם כאן מעמוד שנעשה עבור עמותת השייטת:
https://www.lifecloud-qr.com/organization-profile/62baf5cff10da082cb5d58b4

בברכת שנה טובה ובטוחה
תמיר הספל ,
 מנכ"ל LIFE CLOUD  
מייל:  office@lifecloud-qr.com
משרד: 0523705058 
אישי: 0545344947
"""
    },
    "emergency": {
        "subject": "הנצחה מכובדת ודיגיטלית לנופלי [שם הארגון] עם חברת Life Cloud - תמיר הספל",
        "body": """לכבוד [תפקיד/מחלקה],

שמי תמיר הספל, אני מנכ"ל של Life cloud
חברת ההנצחה הדיגיטלית הראשונה בישראל 

אנחנו מציעים פלטפורמה ייחודית לשמירת זכרונות המאפשרת להנגיש את סיפורי הגבורה של הנופלים
 דרך ברקוד איכותי שמוצב במקומות משמעותיים. 
סריקה אחת והסיפור המלא של המנוח נפתח בנייד עם תמונות, סרטונים וזכרונות.

יש לנו ניסיון רב בפרוייקטים לאומיים ורגישים כמו הנצחת נרצחי הנובה, לוחמי דובדבן ויד לבנים טבריה.
לאור הניסיון הזה, אנחנו פונים אליכם בהצעה לשיתוף פעולה להנציח את נופלי [שם הארגון] באופן משמעותי ומכובד.
אם מתאים, אשמח לשיחה קצרה כדי להתאים פעילות/תוכן לפי הגילאים והמסגרת אצלכם.
כמו כן, נשמח להגיע לפגישה, להרחיב על השירותים שלנו ולחשוב יחד איך נוכל להנציח את הגיבורים שלכם בצורה הכי ראויה שיש.

אפשר להתרשם כאן מעמוד שנעשה עבור עמותת השייטת:
https://www.lifecloud-qr.com/organization-profile/62baf5cff10da082cb5d58b4

בברכת שנה טובה ובטוחה
תמיר הספל ,
 מנכ"ל LIFE CLOUD  
מייל:  office@lifecloud-qr.com
משרד: 0523705058 
אישי: 0545344947

"""
    },
    "emergency2": {
        "subject": "הנצחת לוחמי/מתנדבי [שם הארגון] עם חברת Life Cloud ",
        "body": """לכבוד [תפקיד/מחלקה],
שמי תמיר הספל, אני מנכ"ל של Life cloud
חברת ההנצחה הדיגיטלית הראשונה בישראל
ואני פונה אליכם בהערכה עמוקה לפעילות של [שם הארגון] ולמחיר האנושי שהיא לעיתים גובה.

הצעה שלנו מתמקדת בשאלה אחת: איך שומרים את סיפור החיים וזכרונם ולא רק את נסיבות מותו,
כך שגם בעוד שנים, משפחות, חברים והציבור יוכלו לפגוש את האדם שמאחורי המדים.

הפתרון מבוסס על QR שמוצב באתר הנצחה/בבית עלמין ומוביל
לעמוד מורשת: תמונות, סרטונים, סיפורים של הצוות, נקודות זמן מרכזיות,
וספר אורחים שמאפשר לקהילה להשאיר זיכרון בצורה מסודרת ומכבדת.
    
אפשר גם לייצר סדר עבודה שמקל על המשפחות באיסוף החומרים (כולל ליווי עריכה, לפי צורך).

יש לנו ניסיון רב בפרוייקטים לאומיים ורגישים כמו הנצחת נרצחי הנובה, לוחמי דובדבן ויד לבנים טבריה.
לאור הניסיון הזה, אנחנו פונים אליכם בהצעה לשיתוף פעולה להנציח את נופלי [שם הארגון] באופן משמעותי ומכובד.
כמו כן, נשמח להגיע לפגישה, להרחיב על השירותים שלנו ולחשוב יחד איך נוכל להנציח
את הגיבורים שלכם בצורה הכי ראויה שיש.

אפשר להתרשם כאן מעמוד שנעשה עבור עמותת השייטת:
https://www.lifecloud-qr.com/organization-profile/62baf5cff10da082cb5d58b4

בברכת שנה טובה ובטוחה
תמיר הספל ,
 מנכ"ל LIFE CLOUD  
מייל:  office@lifecloud-qr.com
משרד: 0523705058 
אישי: 0545344947

"""
    }
}





def clean_filename(name):
    """Clean organization name for use as filename"""
    # Remove problematic characters and replace spaces
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = name.replace(' ', '_')
    name = name.replace('"', '').replace("'", "")
    return name

def extract_contact_info(contact_string):
    """Extract phone and email from contact string"""
    parts = contact_string.split(" | ")
    phone = parts[0] if len(parts) > 0 else "לא זמין"
    email = parts[1] if len(parts) > 1 else "לא זמין"
    return phone, email

def create_personalized_template(lead, template_key, version_label):
    """Create personalized template content"""
    template = templates[template_key]
    
    # Get organization name and role for personalized addressing
    org_name = lead["name"]
    role_dept = lead["role"]
    phone, email = extract_contact_info(lead["contact"])
    
    # Replace placeholders in subject and body
    subject = template["subject"]
    body = template["body"]
    
    # Common replacements
    subject = subject.replace("[שם העיר]", org_name.replace("עיריית ", "").replace("מועצה אזורית ", ""))
    subject = subject.replace("[שם היחידה]", org_name)
    subject = subject.replace("[שם התנועה]", org_name)
    subject = subject.replace("[שם הארגון]", org_name)
    subject = subject.replace("[שם היחידה/העמותה]", org_name)
    
    body = body.replace("[תפקיד/מחלקה]", role_dept)
    body = body.replace("[שם הארגון]", org_name)
    body = body.replace("[שם העיר]", org_name.replace("עיריית ", "").replace("מועצה אזורית ", ""))
    body = body.replace("[שם היחידה]", org_name)
    body = body.replace("[שם התנועה]", org_name)
    body = body.replace("[שם היחידה/העמותה]", org_name)
    body = body.replace("[שם אתר/אנדרטה/בית עלמין]", f"אתרי ההנצחה של {org_name}")
    
    # Add contact information at the top
    contact_header = f"מייל לקוח: {email}\nוואטסאפ לקוח: {phone}\n"
    
    return f"{contact_header}נושא: {subject}\n\n{body}"

def main():
    """Main function to generate all templates"""
    # Create templates directory if it doesn't exist
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)
    
    print("🚀 יוצר טמפלטים מותאמים אישית...")
    print(f"📁 הקבצים יישמרו בתיקיית: {templates_dir.absolute()}")
    print("-" * 60)
    
    total_files = 0
    
    for lead in leads_data:
        org_name = lead["name"]
        sector = lead["sector"]
        
        # Clean organization name for filename
        clean_org_name = clean_filename(org_name)
        
        # Determine template keys based on sector
        if sector == "muni":
            template_keys = ["muni", "muni2"]
        elif sector == "idf":
            template_keys = ["idf", "idf2"]
        elif sector == "youth":
            template_keys = ["youth", "youth2"]
        elif sector == "emergency":
            template_keys = ["emergency", "emergency2"]
        else:
            print(f"⚠️  מגזר לא מזוהה: {sector} עבור {org_name}")
            continue
        
        # Create version A and B
        versions = [("א", template_keys[0]), ("ב", template_keys[1])]
        
        for version_label, template_key in versions:
            # Create personalized content
            content = create_personalized_template(lead, template_key, version_label)
            
            # Create filename
            filename = f"{clean_org_name}_{version_label}.txt"
            filepath = templates_dir / filename
            
            # Write to file
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ נוצר: {filename}")
                total_files += 1
                
            except Exception as e:
                print(f"❌ שגיאה ביצירת {filename}: {e}")
    
    print("-" * 60)
    print(f"🎉 הסתיים! נוצרו {total_files} קבצי טמפלטים")
    print(f"📂 מיקום: {templates_dir.absolute()}")
    print("💡 עצה: בדוק את הקבצים ועדכן את הפרטים הספציפיים לפני השליחה")

if __name__ == "__main__":
    main()
