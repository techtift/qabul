from fpdf import FPDF
import os
from user.models.student import Student
from university.models.application import StudentApplication
from datetime import datetime,timedelta
class ContractPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.multi_cell(0, 8, "To‘lov-kontrakt asosida (ikki tomonlama) mutaxassis tayyorlashga", align="C")
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "SHARTNOMA", ln=True, align="C")
        self.set_font("Arial", "", 12)
        self.cell(0, 10, f"№ {self.data.get('contract_id', '00000000')}", ln=True, align="C")
        self.ln(5)

    def __init__(self, data):
        super().__init__()
        self.data = data

def make_pdf(user_id):

    user = Student.objects.get(user_id=user_id)
    studentaplication=StudentApplication.objects.filter(student_id=user_id).first()\

    data = {
        "contract_id": user.pinfl,
        "contract_date": user.contract_date.strftime("%d") if user.contract_date else "01",
        "contract_month": user.contract_date.strftime("%B") if user.contract_date else "yanvar",
        "full_name": user.full_name,
        "passport_number": user.passport_number,
    }
    today = datetime.today()
    day = today.strftime("%d")
    month = today.strftime("%B").lower()
    # 2. 📄 PDF yaratish
    pdf = ContractPDF(data)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font("Arial", "", "arial.ttf", uni=True)
    pdf.set_font("Arial", size=11)

    pdf.cell(95, 6, "Toshkent sh.", ln=0)
    pdf.cell(95, 6, f"2025 yil “{day}” {month}", ln=1, align="R")
    pdf.ln(5)

    intro = (
        f"O‘zbekiston Respublikasi Oliy ta’lim, fan va innovatsiya vazirligi tomonidan taqdim etilgan "
        f"323677-sonli litsenziya va Ustav asosida faoliyat ko’rsatayotgan “Toshkent xalqaro moliyaviy boshqaruv "
        f"va texnologiyalar Universiteti” MCHJ (keyingi o’rinlarda “Universitet”) nomidan Rektor Nodirov Azizxon "
        f"Asrorovich bir tomondan, {user.last_name} {user.first_name} {"o'g'li" if user.gender=="1" else "qizi" } (F.I.SH.) (pasport seriya va raqami: {user.passport_number}) "
        f"(keyingi o’rinlarda “Ta’lim oluvchi”) ikkinchi tomondan, birgalikda “Tomonlar” deb ataladigan shaxslar "
        f"mazkur kontraktni quyidagicha tuzdilar:"
    )
    pdf.multi_cell(0, 8, intro, align="J")
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Ⅰ. SHARTNOMA PREDMETI", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 7,
                   "1.1. “Universitet” ta’lim xizmatini ko‘rsatishni, “Ta’lim oluvchi” o‘qish uchun belgilangan to‘lovni "
                   "o‘z vaqtida amalga oshirishni va tasdiqlangan o‘quv reja bo‘yicha darslarga to‘liq qatnashish hamda "
                   "ta’lim olishni o‘z zimasiga oladi. “Ta’lim oluvchi”ning ta’lim olish bo’yicha ma’lumotlari quyidagicha:"
                   )

    # Ta’lim oluvchi haqida malumotlar
    def add_label_value(label, value):
        pdf.set_font("Arial", "", 11)
        pdf.cell(60, 6, label)
        pdf.set_fill_color(255, 255, 0)
        pdf.cell(0, 6, value, ln=True, fill=True)

    add_label_value("Ta’lim bosqichi:", app.program.name)
    add_label_value("Ta’lim shakli:", app.study_type.name)
    study_duration = "4-yil" if app.program.name == "Bakalavr" else "2-yil"
    add_label_value("O‘qish muddati:", study_duration)
    course = f"{app.transfer_level}-kurs" if app.is_transfer else "1-kurs"
    add_label_value("O‘quv kursi:", course)
    study_lang = "O‘zbek tili" if app.lang == "uz" else "Rus tili"
    add_label_value("Ta’lim tili:", study_lang)
    add_label_value("Ta’lim yo‘nalishi:", app.faculty.name if app.faculty else "")

    pdf.ln(2)
    pdf.multi_cell(0, 7,
                   "1.2. “Universitet”ga o‘qishga qabul qilingan “Ta’lim oluvchi” O‘zbekiston Respublikasining "
                   "“Ta’lim to‘g‘risida”gi Qonuni va Davlat ta’lim standartlariga asosan Universitet tomonidan "
                   "ishlab chiqilgan o‘quv rejalar va fan sillabuslari asosida ta’lim oladilar."
                   )
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Ⅱ. TA’LIM XIZMATINI KO‘RSATISH NARXI,", ln=1)
    pdf.cell(0, 8, "   TO‘LASH MUDDATI VA TARTIBI", ln=1)
    price = app.faculty.faculty_night_price if app.study_type.id == 2 else app.faculty.faculty_day_price
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 7, (
        f"2.1. Shartnomaning umumiy miqdori {price} soʻmni tashkil etadi va to’liq miqdorida amalga oshiriladi.\n"
        "2.1.1. Shartnomaning 2.1-bandida ko’rsatilgan pul mablag’larining to’lovi quyidagi muddatlarda "
        "4 (to’rt) qismga bo’lib amalga oshirilishi mumkin:\n"
        "Kuzgi semestr uchun:\n"
        "- Birinchi to’lov: Belgilangan to’lov miqdorining 25 foizini shartnoma imzolangan kundan boshlab 10 ish kuni ichida;\n"
        "- Ikkinchi to’lov: Belgilangan to’lov miqdorining qolgan qismidan 25 foizini 2025-yil 15-dekabr kuniga qadar;\n"
        "Bahorgi semestr uchun:\n"
        "- Uchinchi to’lov: Belgilangan to’lov miqdorining qolgan qismidan 25 foizini 2026-yil 15-fevral;\n"
        "- To’rtinchi to’lov: Belgilangan to’lov miqdorining qolgan 25 foizini 2026-yil 15-aprel kuniga qadar."
    ), align="J")

    pdf.ln(2)

    pdf.multi_cell(0, 7, (
        "2.2. “Ta’lim oluvchi” mazkur Shartnomaning 2.1-bandida belgilangan shartnoma summasini “Universitet” hisob "
        "raqamiga oldindan 100 (yuz) foiz to’lovni amalga oshirishi mumkin. Shuningdek, ushbu pul mablag’lari Ta’lim oluvchi "
        "uchun davlat yoki boshqa jamg’armalar tomonidan qoplab beriladigan taqdirda shartnomaning 2.1.1-bandida ko‘rsatilgan "
        "muddatlardan farqli ravishda qoblab berilishi mumkin hamda ushbu pul mablag’larning o‘tkazishni so‘nggi muddati, "
        "Shartnomaning 2.1.1-bandida belgilangan eng so’nggi muddatdan o‘tib ketmasligi lozim."
    ), align="J")
    pdf.multi_cell(0, 7, (
        """2.3. Shartnomada belgilangan to’lov muddatlari oxirgi kuni dam olish va rasmiy bayram kuniga to’g’ri kelib qolgan taqdirda to’lovning oxirgi kuni keyingi ish kuni hisoblanadi.
2.4. O’zbekiston Respublikasi Prezidenti farmoni bilan “Ish haqi, pensiyalar, stipendiyalar va nafaqalar miqdori” oshirilganda, Soliq kodeksiga soliq to’lovlari oshishi bilan bog’liq bo’lgan o’zgatirishlar kiritilganda, shuningdek, Universitetning o’qitish bilan bog’liq xarajatlar oshganda “Universitet” Shartnomaning 2.1-bandida belgilangan shartnoma miqdori bir tomonlama o’zgartirish huqiqini o’zida saqlab qoladi.
2.5. “Ta’lim oluvchi” Shartnomaning 2.1.1-bandida belgilangan muddatda birinchi to’lovni to’liq to’lagan taqdirda talabalar safiga qabul qilish/kursdan-kursga o’tkazish to’g’risida buyruq rasmiylashtiriladi.
2.6. Ta’lim xizmatini ko‘rsatish narxi har o’quv yili boshlanishidan avval “Universitet” tomonidan tasdiqlanadi.
2.7. “Universitet” “Ta’lim oluvchi”ga stipendiya to’lash majburiyatini o’z zimmasiga olmaydi.
2.8. “Ta’lim oluvchi” o’tilgan fanlarni qoniqarsiz o’zlashtirganligi natijasida “Universitet” tomonidan qayta o’qitilgan fanlar bo’yicha ta’lim xarajatlarini to’liq to’laydi.
Ta’lim oluvchining fanlar bo‘yicha qayta ta’lim olish jarayoni, ya’ni har bir fanni o‘qitish yoki qayta o‘qitish tartibi O‘zbekiston Respublikasi Vazirlar Mahkamasining 2020-yil 31-dekabrdagi 824-sonli qarori bilan tasdiqlangan “Oliy ta’lim muassasalarida o‘quv jarayoniga kredit-modul tizimini joriy etish tartibi to‘g‘risida”gi Nizom hamda Universitetning “Toshkent xalqaro moliyaviy boshqaruv va texnologiyalar universitetida ta’limning kredit tizimi asosida talabalar bilimini nazorat qilish va baholash Tartibi” bilan alohida shartnoma tuzish orqali tartibga solinadi.
2.9. Talabani kursdan kursga o’tkazish to’g’risidagi buyruq “Universitet” tomonidan fanlarni o’zlashtirgan (GPA 2,4 dan yuqori) hamda shartnoma summasini to’liq amalga oshirganidan so’ng (kontrakt qarzdorlik mavjud bo’lmagan) taqdirda amalga oshiriladi.
2.10. To’lov summalarini qaytarish tartibi quyidagicha:
2.10.1. “Ta’lim oluvchi” tomonidan o’quv yili semestri boshlanishidan (semestr boshlanish sanasi: Tasdiqlangan o‘quv rejasi va o’quv grafigiga muvofiq) oldin (kunduzgi/sirtqi yoki boshqa ta’lim shaklidan qat’iy nazar) shartnomani o’z xohishiga binoan bir tomonlama bekor qilish va to’lov summasini qaytarish haqida ariza yozgan taqdirda mazkur shartnomaning 2.1.1-bandidagi birinchi to’lov summasi qaytarib berilmaydi.
Shuningdek, “Ta’lim oluvchi” tomonidan mazkur shartnomaning 2.1.1-bandidagi ikkinchi to’lov summasi va bahorgi semestri uchun amalga oshirilgan to’lovlar to’liq miqdorini qaytarib beriladi.
2.10.2. “Ta’lim oluvchi” tomonidan o’quv yili bahorgi semestri boshlanganidan (semestr boshlanish sanasi: Tasdiqlangan o‘quv rejasi va o’quv grafigiga muvofiq) keyin (kunduzgi/sirtqi yoki boshqa ta’lim shaklidan qat’iy nazar) shartnomani o’z xohishiga binoan bir tomonlama bekor qilish va to’lov summasini qaytarish haqida ariza yozgan taqdirda mazkur shartnomaning 2.1.1-bandidagi to’lov summasi qaytarib berilmaydi.
2.10.3. “Ta’lim oluvchi” tomonidan shartnomani o’z xohishiga binoan bir tomonlama bekor qilish va to’lov summasini qaytarish haqida “Ta’lim oluvchi” Universitetga bevosita kelib, shaxsni tasdiqlovchi hujjat va shartnoma nusxasini ilova qilgan holda yozma ariza bilan murojaat qoldiradi va murojaatlari bo’yicha javobni mas’ul xodimlar tomonidan telefon orqali xabar beriladi.
2.11. “Ta’lim oluvchi” tomonidan keyingi o’quv yilining semestrlari uchun amalga oshirilgan ortiqcha to’lovlar saqlab qolinadi va “Universitet” tomonidan keyingi o’quv yili uchun qayta hisob-kitob qilishni kafolatlaydi.
2.12. “Ta’lim oluvchi” o’z xohishiga ko’ra va boshqa holatlarga ko’ra o’qishni davom ettirmasa “Universitet” oldidagi moliyaviy majburiyatlardan ozod etilmaydi.
2.13. “Ta’lim oluvchi” va uchinchi shaxs (to'lovchi, bank, vasiy, homiy va b.)  shartnoma to’lov bilan bog’liq bo’lgan yuridik va moliyaviy majburiyatlari o’zaro mustaqil hal etiladilar. Bu holatda “Universitet” hech qanday majburiyatlarni o’z zimmasiga olmaydi.
2.14. Ta’lim xizmatini ko’rsatish joyi “Universitet” joylashgan bino va/yoki “Universitet” tomonidan belgilangan joy hisoblanadi. Ba’zi hollarda “Universitet” masofaviy/onlayn ta’lim shakliga o’zgartirish huquqiga ega. Ushbu o’zgarish shartnoma to’lov miqdoriga ta’sir qilmaydi.
2.15. “Ta’lim oluvchi” o’qish jarayonida talabalar safidan chetlashtirilganda (o‘z xohishiga binoan, o‘qishning boshqa ta’lim muassasasiga ko‘chirilishi munosabati bilan, o‘quv intizomini va Universitetning Ichki tartib-qoidalari hamda Odob-axloq kodeksini buzganligi uchun, bir semestr davomida darslarni uzrli sabablarsiz 74 soatdan ortiq qoldirganligi sababli, o‘qish uchun belgilangan to‘lov o‘z vaqtida amalga oshirilmaganligi sababli) “Universitet” oldidagi shartnoma bo’yicha qarzdorligi to’liq qoplangandan so’ng “Ta’lim oluvchi”ning hujjatlari qaytarib beriladi.
“Ta’lim oluvchi” talabalar safidan chetlashtirilgan sanaga qadar o’tgan o’quv davri uchun shartnoma summasi hisoblanib ta’lim oluvchining qarzdorligi aniqlanganda Universitetning foydasiga undiriladi.
2.16. “Universitet” tomonidan Tasdiqlangan o‘quv rejasi va o’quv grafigi “Universitet” rasmiy veb sayti, Hemis yoki boshqa elektron platformalarida, shuningdek, Universitetning rasmiy telegram kanali orqali e’lon berilishi va Ta’lim oluvchilar uchun xabardor qilish hisoblanadi. 
2.17. Shartnoma shartlari bilan tanishtirilgan Ta’lim oluvchi, shartnomaning 2.16-bandida belgilangan tartibda xabardor qilinganidan so’ng, o‘quv rejasi va o’quv grafigi yuzasidan unga e’lon qilinmaganligi to‘g’risida e’tiroz bildirishga haqli emas.
2.18. Universitetga o‘qishni ko‘chirish bo‘yicha tavsiya etilgan Ta’lim oluvchining tegishli kurs o‘quv rejalari o‘rtasida fanlar farqi aniqlangan taqdirda, GPA ko‘rsatkichi 2,4 yoki undan yuqori bo'lsa fanlar farqi kredit-modul tizimi asosida hisob-kitob qilinib, to‘lov amalga oshirilgandan so‘ng qayta ta’lim olishga ruxsat beriladi. Ta’lim oluvchining GPA ko‘rsatkichi 2,4 dan past bo‘lgan holatda tegishli yo‘nalish bo‘yicha GPA ko‘rsatkichi 2,4 yoki undan yuqori bo‘lgan kursga qadar pasaytiriladi va fanlar farqi kredit-modul tizimi asosida hisob-kitob qilinadi.

"""), align="J")
    pdf.set_font("Arial", "B", 12)
    pdf.multi_cell(0, 7, "Ⅲ. TOMONLARNING MAJBURIYATLARI", align="C")

    pdf.multi_cell(0, 7, ("""
3.1. “Universitet” quyidagi majburiyatlarga ega: 
“Ta’lim oluvchi” tomonidan shartnomada belgilangan to‘lovni o‘z vaqtida amalga oshirgandan so‘ng, “Ta’lim oluvchi”ni talabalar safiga qabul qilish to’g’risida yoki “Talaba”ni kursdan-kursga ko’chirish to’g’risida buyruq rasmiylashtirish; 
“Ta’lim oluvchi”ga ta’lim olishi uchun O‘zbekiston Respublikasining Davlat ta’lim standartlari va “Universitet Ustavi” asosida zarur shart-sharoitlar yaratib berish va sifatli ta’lim berish; 
“Ta’lim oluvchi”ning Universitetda ta’lim olish bilan bog’liq bo’lgan huquq va erkinliklari, qonuniy manfaatlari hamda ta’lim muassasasi Ustaviga muvofiq professor-o‘qituvchilar tomonidan o‘zlarining funksional vazifalarini to‘laqonli bajarishini ta’minlash; 
“Ta’lim oluvchi”ni tahsil olayotgan ta’lim yo‘nalishi (mutaxassisligi) bo‘yicha tasdiqlangan o‘quv rejasi va dasturlariga muvofiq Davlat ta’lim standarti talablari darajasida tayyorlash;
“Ta’lim oluvchi”ga Shartnomaning 2.1-bandida belgilangan shartnoma summasi o’zgarganda va shartnoma summasining qolgan belgilangan muddati uchun to‘lovlarini to’lashi haqida xabar berish;
3.2. “Ta’lim oluvchi” quyidagi majburiyatlarga ega: 
Shartnomaning 2.1-bandida belgilangan mablag’larni to’lashga yoki mazkur Shartnomaning
2.1.1-bandida belgilangan tartibda to‘lab borish;
O’zbekiston Respublikasi Prezidenti farmoni bilan “Ish haqi, pensiyalar, stipendiyalar va nafaqalar miqdori” oshirilganda, Soliq kodeksiga soliq to’lovlari oshishi bilan bog’liq bo’gan o’zgatirishlar kiritilganda, Universitetning o’qitish xarajatlari oshganda va boshqa holatlarda Shartnomaning 2.1-bandida belgilangan shartnoma summasi Universitet tomonidan bir tomonlama o’zgartirilganda to‘lov farqini to‘lash;
“Ta’lim oluvchi” belgilangan to‘lov miqdorini to‘laganlik to‘g‘risidagi to’lov topshiriqnomasining nusxasini o‘z vaqtida Universitetga topshirish;
Ta’lim yo‘nalishi (mutaxassisligi)ning tegishli malaka tavsifnomasiga muvofiq barcha zarur bilimlarni puxta egallash, dars mashg‘ulotlarida to’liq qatnashish;
“Universitet” Professor-o‘qituvchilar va xodimlarini hurmat qilish;
“Universitet”ning texnik va boshqa vositalariga, jihozlariga va boshqa mol-mulkiga ehtiyotkorlik bilan munosabatda bo’lishi va zarar yetkazmaslik. Agar Ta’lim oluvchi tomonidan Universitet 
mol-mulkiga zarar yetkazilgan taqdirda, ularni bartaraf etish yoki to’liq miqdorida qoplab berish;
“Universitet” Ichki tartib qoidalari va Odob-ahloq kodeksi hamda boshqa ichki-me’yoriy hujjatlarida belgilangan tartib qoidalariga so’zsiz rioya qilish;
“Universitet” Odob-axloq kodeksida belgilangan kiyinish uslubiga qat’iy rioya qilish;
“Universitet” tomonidan yaratilgan o’quv platformasi bo’yicha bajarilishi kerak bo’lgan barcha tegishli harakatlarni bajarib borish (sinovlardan o’tish, fanlarni topshirish);
Shartnomani bir tomonlama bekor qilish niyati haqida “Universitet”ni bir oy oldin yozma ravishda ogohlantirish;
darslarga ishtirok etish uchun “Universitet” binosiga belgilangan vaqtda yetib kelish va dars tugagan vaqtda “Universitet” binosini tark etish (bunda kutubxonadan foydalanish vaqti hamda o’quv jarayoni bilan bog’liq qo’shimcha mashg’ulotlar mustasno).
"""), align="J")
    pdf.set_font("Arial", "B", 12)
    pdf.multi_cell(0, 7, "Ⅳ. TOMONLARNING HUQUQLARI", align="C")

    pdf.multi_cell(0, 7,("""
4.1. “Universitet” quyidagi huquqlarga ega: 
“Ta’lim oluvchi”ning oraliq va yakuniy nazoratlarni topshirish, qayta topshirish tartibi hamda vaqtlarini belgilash;
“Universitet” ichki-me’yoriy hujjatlariga asosan “Talaba”ga rag‘batlantiruvchi yoki intizomiy choralarni qo‘llash;
“Ta’lim oluvchi” o‘quv yili semestrlarida yakuniy nazoratlarni topshirish, qayta topshirish natijalariga ko‘ra akademik qarzdor bo‘lib qolsa uni kursdan-kursga qoldirish;
“Ta’lim oluvchi”ning darslarga sababsiz qatnashmaslik, intizomni buzish, “Universitet”ning Ichki tartib, Odob-axloq kodeksi va boshqa ichki-me’yoriy hujjatlarida belgilangan tartib va qoidalarga rioya qilmaganda, shuningdek, shartnomada belgilangan to‘lovni o‘z vaqtida amalga oshirilmaganda “Ta’lim oluvchi”ni talabalar safidan chetlashtirish;
“Ta’lim oluvchi” Shartnomaning 2.1-bandida belgilangan muddatda to’lovlarni amalga oshirmasa darsga kiritmasligi mumkin;
“Ta’lim oluvchi”dan Universitet Ichki tartib qoidalari va Odob-axloq kodeksi hamda boshqa ichki-me’yoriy hujjatlariga rioya qilishni talab qilish;
O‘zbekiston Respublikasi hukumat komissiyasi yoki “Universitet” tomonidan karantin izolyatsiyasi e’lon qilinganida va boshqa cheklovli holatlarda, onlayn/masofadan o’qish uchun sharoitlarni mustaqil tashkil etish (barqaror Internet aloqasi, uskunalar va boshqalar);
Universitetga o‘qishni ko‘chirish bo‘yicha kelgan Ta’lim oluvchilarning fanlari va o‘qitilgan darslari o‘rtasida tafovutlar aniqlanganida, Universitetda ma’lum bir kursga qabul qilish tartibi O‘zbekiston Respublikasi Vazirlar Mahkamasining 2020-yil 31-dekabrdagi 824-sonli qarori bilan tasdiqlangan “Oliy ta’lim muassasalarida o‘quv jarayoniga kredit-modul tizimini joriy etish tartibi to‘g‘risida”gi Nizom hamda Universitetning “Toshkent xalqaro moliyaviy boshqaruv va texnologiyalar universitetida ta’limning kredit tizimi asosida talabalar bilimini nazorat qilish va baholash Tartibi” asosida muvofiqlashtirish; 
“Ta’lim oluvchi” Universitet Ichki tartib qoidalari va Odob-axloq kodeksida belgilangan kiyinish uslubiga rioya qilmagan taqdirda Universitet binosiga kiritmaslik.
4.2. “Ta’lim oluvchi” quyidagi huquqlarga ega: 
O‘zbekiston Respublikasining “Ta’lim to‘g‘risida”gi Qonuni va davlat ta’lim standartlarga muvofiq ishlab chiqilgan o‘quv rejalar va fan dasturlari asosida ta’lim olish;
Shartnomaning 2.1.1-bandida belgilangan miqdorida qismlarga bo’lib to’lamasdan oldindan 
100 (yuz) foizgacha to‘lash;
Shartnomaning 2.1-bandida belgilangan miqdorida naqd pul, bank plastik kartasi, bankdagi omonat hisob raqami orqali, ish joyidan (agar mavjud bo’lsa) oylik ish haqidan o‘tkazishi yoki banklardan ta’lim krediti olish orqali to‘lovni amalga oshirishi;
Professor-o‘qituvchilarning o‘z funksional vazifalarini bajarishidan yoki ta’lim muassasasidagi shart-sharoitlardan norozi bo‘lgan taqdirda ta’lim muassasasi rahbariyatiga yozma shaklda murojaat qilish;
“Universitet”ning moddiy-texnik bazasidan kelib chiqib kredit-modul tizimiga asosan, tahsil olayotgan ta’lim yo’nalishi o’quv rejasida ko’rsatilgan tanlov fanlarini tanlash;
“Universitet” tomonidan Ta’lim oluvchilar uchun tashkil etiladigan ilmiy, madaniy-marifiy, badiiy, ijodiy tadbir va tanlovlarda larida ishtirok etish;
Universitetga taklif etiladigan mashxur spiker/lektorlarning ma’ruza, leksiya va seminarlarida ishtirok etish.
4.3. “Ta’lim oluvchi” quyidagilarni o’z zimmasiga oladi:
“Universitet”ning texnik va boshqa vositalariga, jihozlariga va boshqa mol-mulkiga ehtiyotkorlik bilan munosabatda bo’lishi va zarar yetkazmaslik. Agar Ta’lim oluvchi tomonidan Universitet 
mol-mulkiga zarar yetkazilgan taqdirda, ularni bartaraf etish yoki to’liq miqdorida qoplab berish;
Shaxsiy profilini “Universitet” ichki nazorat bazasi orqali rasmiy veb-saytda zarur shaxsiy ma’lumotlar bilan o’z vaqtida to’ldirish va yangilab borish;
“Universitet”ning ichki hujjatlarida ko’rsatilgan keyingi o’quv yili uchun ro‘yxatdan o‘tish bo‘yicha yo‘riqnomalarni va akademik xodimlar tomonidan taqdim etilgan yo‘riqnomalarni o‘z vaqtida bajarish;
O‘zining shaxsi haqidagi va oqibat keltirib chiqaradigan hujjatlari o’zgarish yuz bergan taqdirda, shuningdek, yashash (vaqtinchalik) manzili o’zgargan taqdirda bu haqda “Universitet” mas’ul xodimlariga xabar berish;
Universitet bilan aloqalarni uzmaslik hamda dars jadvaliga asosan dars mashg’ulotlari boshlanishidan oldin Universitetga yetib kelish;
“Universitet” tomonidan Tasdiqlangan o‘quv rejasi va o’quv grafigi “Universitet” rasmiy veb sayti, Hemis yoki boshqa elektron platformalarida, shuningdek, Universitetning rasmiy telegram kanali orqali dars mashg’ulotlari haqidagi e’lonlarni kuzatib borish.
Shartnoma shartlari bilan tanishtirilgan Ta’lim oluvchi, o‘quv rejasi va o’quv grafigi to’g’risida belgilangan tartibda xabardor qilinganidan so’ng, ushbu xaqida unga e’lon qilinmaganligi to’g’risida e’tiroz bildirishga haqli emas.
“Universitet” Buxgalteriyasiga o’qish uchun to’lov to’langanligini tasdiqlovchi hujjatni taqdim etish;
O’zbekiston Respublikasi qonunchiligida ta’qiqlangan siyosiy, diniy va boshqa tashkilotlar, yot oqimlarda yoxud yig’ilishlar, mitinglar, ko’cha yurishlari yoki namoyishlarda ishtirok etmaslik.
"""), align="J")
    pdf.set_font("Arial", "B", 12)
    pdf.multi_cell(0, 7, "Ⅴ. TOMONLARNING JAVOBGARLIGI", align="C")

    pdf.multi_cell(0, 7,("""
5.1. Mazkur shartnoma bo’yicha bir taraf shartnoma shartlarini bajarmasa yoki lozim darajada bajarmasa, ikkinchi taraf oldida O‘zbekiston Respublikasining amaldagi qonun hujjatlarida nazarda tutilgan tartibda javobgar bo‘ladi.
5.2. “Ta’lim oluvchi” “Universitet”ning Ichki tartib qoidalari, Odob-axloq kodeksi va boshqa ichki-me’yoriy hujjatlariga to’liq rioya qilishi lozim bo’ladi. Mazkur ichki-me’yoriy hujjatlarda belgilangan tartib va qoidalarga rioya qilmaganda “Ta’lim oluvchi”ga nisbatan “Universitet” tomonidan o’rnatilgan tartibda Ta’lim oluvchilar safidan chetlatishgacha bo’lgan choralar ko'rilishi mumkin.
5.3. Mazkur shartnomada ko’zda tutilmagan boshqa javobgarlik choralari O’zbekiston Respublikasining amaldagi qonunchiligiga muvofiq belgilanadi.
"""), align="J")
    pdf.set_font("Arial", "B", 12)
    pdf.multi_cell(0, 7, "Ⅵ. FORS-MAJOR", align="C")

    pdf.multi_cell(0, 7,("""
6.1. Tomonlarga bog‘liq bo‘lmagan holatlarda (fors-major), yaʼni tabiiy ofatlar, texnogen, epidemik yoki epizodik, urush harakatlari, ish tashlash va h.k. yuz berganda, agar Tomonlardan biri shu hodisa tufayli shartnoma shartlarini bajara olmasa, Tomonga nisbatan javobgarlik choralari ko‘rilmaydi. Fors-major hodisasi yuz bergani va shu sababli shartnoma sharti bajarilishi imkoniyati yo‘qligi hujjat bilan tasdiqlangan bo‘lishi kerak.
6.2. Tomonlar shartnomani bajarmaslik yoki kechiktirmaslik yoki bajarmaslik oqibatlari yoki ushbu shartnoma bajarilishining kechikishi uchun, agar bu Shartnoma ishtirokchilariga bog’liq bo’lmagan hollarda sodir bo’lgan har qanday voqea, shu jumladan, faqat davlat organi yoki ma’muriyati tomonidan qabul qilingan tabiiy ofat, urush yoki favqulodda holat bilan cheklanmagan holda, ular Tomonlar tomonidan ushbu shartnoma bo’yicha o’z majburiyatlarini bajarishga imkon bermagan hollarda boshqa shaxs oldida javobgar bo’lmaydilar.
6.3. Shartnoma tomonlardan qaysi biri uchun majburiyatlarni yengib bo’lmaydigan kuchlar (fors-major) holatlar ma’lum bo’lsa, darhol ikkinchi tomonni 10 ish kuni ichida ogohlantirishi lozim. Ushbu holatda “Universitet” masofaviy uslubda ta’lim berish imkonini yo’lga qo’yish huquqiga ega va “Ta’lim oluvchi” bu uslubda ta’lim olishga roziligini bildiradi. Ushbu holatda “Universitet” “Ta’lim oluvchi”ga
10 ish kuni ichida masofaviy ta’lim shaklini taklif qiladi. “Ta’lim oluvchi” ushbu taklifga 10 ish kuni ichida yozma tarzda javob qaytarishi lozim bo’ladi, aks holda ushbu shartnoma bekor qilingan deb hisoblanadi. “Ta’lim oluvchi” masofaviy shaklda o’qishni davom ettirishga norozilik bildirsa shartnoma shartlari bajarilmagan deb hisoblanadi va shartnoma bekor qilinadi, to’lov qaytarilmaydi. 
6.4. Fors-major holatlari ta’limni masofaviy amalga oshirishga imkon bersa tomonlar o’z majburiyatlarini masofaviy ta’limga asosan amalga oshiradilar. Bunda “Ta’lim oluvchi” masofaviy ta’lim olish uchun talab qilingan barcha texnik va boshqa jihatdan sharoitni yaratishni o’z zimmasiga oladi.
"""), align="J")
    pdf.set_font("Arial", "B", 12)
    pdf.multi_cell(0, 7, "Ⅶ. SHARTNOMANING AMAL QILISH MUDDATI, UNGA O’ZGARTIRISH", align="C")
    pdf.multi_cell(0, 7, "VA QO’SHIMCHALAR KIRITISH HAMDA BEKOR QILISH TARTIBI", align="C")
    pdf.multi_cell(0, 7,("""
7.1. Mazkur shartnoma rasmiylashtirilgandan soʻng kuchga kiradi va tomonlar o’z majburiyatlarini to’liq bajarib bo’lgunga qadar amal qiladi.
7.2. Mazkur shartnoma shartlariga tomonlar kelishuviga ko’ra o‘zgartirish va qo‘shimchalar kiritilishi mumkin. O‘zgartirish va qo‘shimchalar faqat yozma ravishda qo’shimcha kelishuv tuzish orqali amalga oshiriladi. Shartnomaning 2.6-bandi bilan bog’liq qismiga “Universitet” tomonidan bir tomonlama o’zgartirilishi mumkin.
7.3. Shartnoma quyidagi hollarda bekor qilinishi mumkin: 
Tomonlarning o‘zaro kelishuviga binoan, “Ta’lim oluvchi”ning o’z xohishiga binoan, “Ta’lim oluvchi” “Universitet” tashabbusi bilan bir tomonlama bekor qilinishi mumkin;
Tomonlardan biri o‘z majburiyatlarini bajarmaganda yoki lozim darajada bajarmaganda;
“Ta’lim oluvchi” “Universitet”ning ichki hujjatlarida belgilangan qoidalarni bir marta qo’pol yoki muntazam ravishda buzgan, huquqbuzarlik va/yoki jinoyat sodir etgan hollarda shartnomani bir tomonlama bekor qilish;
“Ta’lim oluvchi” tomonidan qabul imtihonlarida aldash, ayyorlik, tovlamachilik, firibgarlik va boshqa shunga o’xshash belgilangan tartibga zid yo’llar bilan o’qishga qabul qilinganligi aniqlanganda;
“Ta’lim oluvchi” o'qish davrida korrupsiya yoki korrupsiya holatlari bilan bog’liq huquqbuzarlikni amalga oshirgani aniqlanganda;
“Ta’lim oluvchi” vafot etsa.
7.4. “Universitet”ning boshqa bino/joyga ko’chirilishi, masofaviy ta’lim shakliga o’tishi taraflar ixtiyoriga bog’liq bo'lmagan holat hisoblanmaydi va “Ta’lim oluvchi” “Universitet”ning talabiga ko’ra boshqa bino/joyga va/yoki masofaviy ta’lim shaklida o’qishni davom ettirishi kerak bo'ladi. Ushbu holatda “Ta’lim oluvchi” ushbu shartlarga rozi bo’lmasa va o’qishni davom ettirmasa “Universitet” shartnomani bir tomonlama bekor qilib amalga oshirilgan to’lovni qaytarmaydi.
"""), align="J")
    pdf.set_font("Arial", "B", 12)
    pdf.multi_cell(0, 7, "Ⅷ. YAKUNIY QOIDALAR VA NIZOLARNI HAL QILISH TARTIBI", align="L")
    pdf.multi_cell(0, 7,("""
8.1. Ushbu shartnomani bajarish jarayonida kelib chiqishi mumkin bo‘lgan nizo va ziddiyatlar tomonlar o‘rtasida muzokaralar olib borish yo‘li bilan hal etiladi. 
8.2. Muzokaralar olib borish yo‘li bilan nizoni hal etish imkoniyati bo‘lmagan taqdirda, tomonlar nizolarni hal etish uchun amaldagi qonunchilikka muvofiq “Universitet” joylashgan hududdagi fuqarolik sudiga murojaat etishlari mumkin. 
8.3. “Universitet” axborotlar va xabarnomalarni internetdagi veb-saytida, rasmiy sahifalar, axborot tizimida yoki e’lonlar taxtasida e’lon joylashtirish orqali xabar berishi mumkin. 
8.4. Shartnoma 2 (ikki) nusxada, tomonlarning har biri uchun bir nusxadan tuzildi va ikkala nusxa ham bir xil huquqiy kuchga ega.
"""
    ), align="J")


    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "IX. TOMONLARNING REKVIZITLARI VA IMZOLARI:", ln=True, align="C")


    pdf.set_font("Arial", "", 11)
    pdf.set_fill_color(255, 255, 255)
    pdf.cell(95, 10, '“UNIVERSITET”', 1, 0, 'C')
    pdf.cell(95, 10, '“TA’LIM OLUVCI”', 1, 1, 'C')

    pdf.set_font("Arial", "B", 11)
    pdf.cell(95, 10, "Toshkent xalqaro moliyaviy boshqaruv va texnologiyalar Universiteti", 1, 0, 'C')
    pdf.set_font("Arial", "", 11)
    pdf.cell(95, 10, "F.I.SH.: _______________________________________", 1, 1)

    universitet_info = [
                ("Manzil:", "Toshkent shahri, Uchtepa tumani, Ko'hna choponota MFY, 13-massiv, 6-uy"),
                ("x/r:", "2020 8000 2055 7030 90 03"),
                ("Bank:", '"Ipoteka-Bank" ATIB Yakkasaroy filiali'),
                ("MFO:", "01017"),
                ("INN:", "309890596"),
                ("Rektor:", "A.Nodirov Imzo")
            ]

    for label, value in universitet_info:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(20, 8, label, 0, 0)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(75, 8, value, 0)

    pdf.set_xy(105, 40)
    pdf.cell(30, 8, "Tug’ilgan sana:", 0)
    pdf.set_fill_color(255, 255, 0)
    pdf.cell(40, 8, user.birth_date, 0, 1, fill=True)

    pdf.set_x(105)
    pdf.cell(50, 8, "Passport seriyasi va raqami :", 0)
    pdf.set_fill_color(255, 255, 0)
    pdf.cell(40, 8, user.passport_number, 0, 1, fill=True)

    pdf.set_x(105)
    pdf.cell(50, 8, "Tel.:", 0)
    pdf.cell(40, 8, user.phone_number, 0, 1)

    pdf.set_x(105)
    pdf.cell(50, 8, "Yashash manzili:", 0, 1)
    pdf.set_x(105)
    pdf.cell(85, 8, '“____________________________________”', 0, 1)
    pdf.set_x(105)
    pdf.cell(85, 8, '__________________ Imzo', 0, 1)
    output_dir = "pdf_outputs"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, f"{user_id}.pdf")
    pdf.output(pdf_path)

    return pdf_path
