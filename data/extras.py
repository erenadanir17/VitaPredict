"""Symptom checker data + meal plan data + interaction matrix + cost data"""

# Symptom -> possible vitamin deficiencies
SYMPTOM_MAP = {
    "Yorgunluk ve halsizlik": ["D Vitamini", "B12 Vitamini", "Demir (Ferritin)", "Magnezyum", "B1 Vitamini (Tiamin)"],
    "Sac dokulmesi": ["Demir (Ferritin)", "D Vitamini", "Cinko (Zinc)", "B12 Vitamini", "Selenyum"],
    "Uyku problemi / uykusuzluk": ["Magnezyum", "D Vitamini", "B6 Vitamini", "Omega-3"],
    "Kas kramplari ve agrilari": ["Magnezyum", "D Vitamini", "Krom", "Bakir"],
    "Konsantrasyon bozuklugu": ["B12 Vitamini", "Demir (Ferritin)", "Omega-3", "B1 Vitamini (Tiamin)", "Cinko (Zinc)"],
    "Anksiyete / kaygi": ["Magnezyum", "B6 Vitamini", "D Vitamini", "Omega-3", "Cinko (Zinc)"],
    "Depresif ruh hali": ["D Vitamini", "B12 Vitamini", "Folat (B9)", "Omega-3", "Magnezyum"],
    "Sik hastalanma": ["D Vitamini", "C Vitamini", "Cinko (Zinc)", "Selenyum", "A Vitamini"],
    "Cilt kuruluugu / egzama": ["A Vitamini", "E Vitamini", "Omega-3", "D Vitamini", "Cinko (Zinc)"],
    "Dudak catlagi": ["B2 Vitamini (Riboflavin)", "B6 Vitamini", "Demir (Ferritin)"],
    "Tirnak kirilmasi": ["Demir (Ferritin)", "Cinko (Zinc)", "Selenyum", "B12 Vitamini"],
    "Kemik / eklem agrisi": ["D Vitamini", "K Vitamini", "Magnezyum", "Bakir"],
    "Goz kuruluugu / gorMe bozuklugu": ["A Vitamini", "Omega-3", "B2 Vitamini (Riboflavin)"],
    "Dis eti kanamasi": ["C Vitamini", "K Vitamini"],
    "El ve ayaklarda uyusma / karinCalanma": ["B12 Vitamini", "B6 Vitamini", "B1 Vitamini (Tiamin)", "Magnezyum"],
    "Kalp carpintisi": ["Magnezyum", "B1 Vitamini (Tiamin)", "Demir (Ferritin)", "B12 Vitamini"],
    "Tatli krizi / asiri istah": ["Krom", "Magnezyum", "B6 Vitamini"],
    "Yaralar gec iyilesiyor": ["C Vitamini", "Cinko (Zinc)", "A Vitamini"],
    "Hafiza zayifligi": ["B12 Vitamini", "Omega-3", "D Vitamini", "B1 Vitamini (Tiamin)"],
    "Bas agrisi / migren": ["Magnezyum", "B2 Vitamini (Riboflavin)", "D Vitamini", "Demir (Ferritin)"],
}

# Weekly meal plan templates per vitamin
MEAL_PLANS = {
    "D Vitamini": [
        {"gun": "Pzt", "ogun": "Somon fileto, ispanak salata"},
        {"gun": "Sal", "ogun": "Yumurta, mantar sote"},
        {"gun": "Car", "ogun": "Uskumru, brokoli"},
        {"gun": "Per", "ogun": "Ton baligi salata"},
        {"gun": "Cum", "ogun": "Yumurtali kahvalti, peynir"},
        {"gun": "Cmt", "ogun": "Sardalya, roka salata"},
        {"gun": "Paz", "ogun": "Balik corbasi, yesil salata"},
    ],
    "B12 Vitamini": [
        {"gun": "Pzt", "ogun": "Kirmizi et, yogurt"},
        {"gun": "Sal", "ogun": "Yumurta, sut"},
        {"gun": "Car", "ogun": "Tavuk ciğeri, pilav"},
        {"gun": "Per", "ogun": "Balik, ayran"},
        {"gun": "Cum", "ogun": "Peynirli omlet"},
        {"gun": "Cmt", "ogun": "Kofte, cacik"},
        {"gun": "Paz", "ogun": "Biftek, yogurt corbasi"},
    ],
    "Demir (Ferritin)": [
        {"gun": "Pzt", "ogun": "Mercimek corbasi, limon"},
        {"gun": "Sal", "ogun": "Ispanak yemegi, portakal"},
        {"gun": "Car", "ogun": "Kirmizi et, yesil biber"},
        {"gun": "Per", "ogun": "Kuru kayisi, ceviz"},
        {"gun": "Cum", "ogun": "Nohut yemegi, limonlu salata"},
        {"gun": "Cmt", "ogun": "Ciger sote, roka"},
        {"gun": "Paz", "ogun": "Fasulye pilaki, domates"},
    ],
    "Magnezyum": [
        {"gun": "Pzt", "ogun": "Yulaf, muz, badem"},
        {"gun": "Sal", "ogun": "Ispanak salata, avokado"},
        {"gun": "Car", "ogun": "Kuru fasulye, bitter cikolata"},
        {"gun": "Per", "ogun": "Kabak cekirdegi, yogurt"},
        {"gun": "Cum", "ogun": "Kinoa salata, ceviz"},
        {"gun": "Cmt", "ogun": "Badem sutlu smoothie"},
        {"gun": "Paz", "ogun": "Muhallebi, fistik"},
    ],
    "Folat (B9)": [
        {"gun": "Pzt", "ogun": "Ispanak boregi"},
        {"gun": "Sal", "ogun": "Mercimek corbasi, brokoli"},
        {"gun": "Car", "ogun": "Kusakusu yesil salata"},
        {"gun": "Per", "ogun": "Enginar yemegi"},
        {"gun": "Cum", "ogun": "Avokadolu tost, portakal suyu"},
        {"gun": "Cmt", "ogun": "Nohutlu salata, roka"},
        {"gun": "Paz", "ogun": "Yesillikli omlet"},
    ],
    "C Vitamini": [
        {"gun": "Pzt", "ogun": "Portakal, kivi, biber dolma"},
        {"gun": "Sal", "ogun": "Limonlu salata, cilek"},
        {"gun": "Car", "ogun": "Brokoli sote, greyfurt"},
        {"gun": "Per", "ogun": "Karnabahar graten"},
        {"gun": "Cum", "ogun": "Mevsim meyve tabagi"},
        {"gun": "Cmt", "ogun": "Biberli menemen"},
        {"gun": "Paz", "ogun": "Kivili yogurt, mandalina"},
    ],
    "Cinko (Zinc)": [
        {"gun": "Pzt", "ogun": "Kirmizi et, nohut"},
        {"gun": "Sal", "ogun": "Kabak cekirdegi, peynir"},
        {"gun": "Car", "ogun": "Tavuk sote, mercimek"},
        {"gun": "Per", "ogun": "Yumurta, fistik ezmesi"},
        {"gun": "Cum", "ogun": "Hindi eti, kinoa"},
        {"gun": "Cmt", "ogun": "Kaju, bitter cikolata"},
        {"gun": "Paz", "ogun": "Dana bonfile, fasulye"},
    ],
}

# Vitamins that should NOT be taken at the same time
CONFLICT_MATRIX = {
    ("Demir (Ferritin)", "Cinko (Zinc)"): "Ayni anda alinmamali, emilimi dusurur. 2 saat arayla alin.",
    ("Demir (Ferritin)", "Bakir"): "Birbirinin emilimini engeller. Farkli saatlerde alin.",
    ("Cinko (Zinc)", "Bakir"): "Cinko bakir emilimini dusurur. 2+ saat arayla alin.",
    ("Magnezyum", "Demir (Ferritin)"): "Magnezyum demir emilimini azaltir. Farkli ogunlerde alin.",
    ("D Vitamini", "E Vitamini"): "Yuksek doz E, D vitamini emilimini azaltabilir.",
}

# Estimated monthly supplement costs (TRY)
SUPPLEMENT_COSTS = {
    "D Vitamini": {"min": 50, "max": 120},
    "B12 Vitamini": {"min": 60, "max": 150},
    "Folat (B9)": {"min": 40, "max": 100},
    "Demir (Ferritin)": {"min": 50, "max": 130},
    "Magnezyum": {"min": 80, "max": 200},
    "Cinko (Zinc)": {"min": 40, "max": 100},
    "B6 Vitamini": {"min": 30, "max": 80},
    "C Vitamini": {"min": 30, "max": 90},
    "A Vitamini": {"min": 40, "max": 100},
    "E Vitamini": {"min": 50, "max": 120},
    "Omega-3": {"min": 100, "max": 250},
    "B1 Vitamini (Tiamin)": {"min": 30, "max": 80},
    "B2 Vitamini (Riboflavin)": {"min": 30, "max": 80},
    "Selenyum": {"min": 40, "max": 100},
    "K Vitamini": {"min": 50, "max": 120},
    "Bakir": {"min": 30, "max": 80},
    "Krom": {"min": 30, "max": 70},
    "Iyot (TSH)": {"min": 0, "max": 0},
}

# Daily fun facts
VITAMIN_FACTS = [
    {"vit": "D Vitamini", "fact": "Turkiye'de yetiskinlerin %75'inde D vitamini eksikligi var. Gunes isigi en iyi kaynak ama kislari neredeyse imkansiz."},
    {"vit": "B12 Vitamini", "fact": "B12 eksikligi yillar icinde sessizce ilerler. Belirtiler ortaya ciktiginda sinir hasari baslamisOlabilir."},
    {"vit": "Demir (Ferritin)", "fact": "Cay ve kahve demir emilimini %60'a kadar azaltir. Yemeklerden 1 saat sonra icin."},
    {"vit": "Magnezyum", "fact": "Stres magnezyum tuketir, magnezyum eksikligi stresi artirir. Kisir dongu! Takviye bu donguyu kirar."},
    {"vit": "Folat (B9)", "fact": "Turkiye'de ekmege folat eklenmesi zorunlu. Yine de hamile kadinlarin %40'inda eksiklik gorulur."},
    {"vit": "C Vitamini", "fact": "Insanlar C vitamini uretemez! Memelilerin cogu kendi uretir ama biz, maymunlar ve kobaylar uretemez."},
    {"vit": "Omega-3", "fact": "Beynin %60'i yagdan olusur ve bunun buyuk kismi DHA (Omega-3). Hafiza icin en onemli besin."},
    {"vit": "Cinko (Zinc)", "fact": "Cinko 300'den fazla enzimin calismasi icin gerekli. Tat ve koku alma duyusu cinko olmadan calismaz."},
    {"vit": "A Vitamini", "fact": "Havuc gece gorusunu iyilestirir soylentisi 2. Dunya Savasi'nda radar teknolojisini gizlemek icin uyduruldu."},
    {"vit": "Magnezyum", "fact": "Turkiye'deki topraklarda magnezyum orani son 50 yilda %30 azaldi. Sebzelerden yeterli almak artik cok zor."},
    {"vit": "B12 Vitamini", "fact": "B12 sadece hayvansal gidalarda bulunur. Vegan beslenenlerin %90'inda eksiklik gorulur."},
    {"vit": "D Vitamini", "fact": "D vitamini aslinda bir hormon! Vucut 1000'den fazla geni D vitamini ile kontrol eder."},
    {"vit": "Selenyum", "fact": "Turkiye'nin bati bolgeleri selenyum fakir topraklara sahip. Doguda yetisen gidalar daha zengin."},
    {"vit": "E Vitamini", "fact": "E vitamini cildin dogal gunes koruyucusu. UV hasarina karsi iceriden koruma saglar."},
    {"vit": "K Vitamini", "fact": "K vitamini olmadan kan pihtilasmaz. Adi Almanca 'Koagulation' (pihtilasma) kelimesinden gelir."},
]

# Turkish population averages (approximate, for comparison)
TR_AVERAGES = {
    "D Vitamini": {"avg": 18, "unit": "ng/mL", "low_pct": 75, "note": "Turkiye'de her 4 kisiden 3'u eksik"},
    "B12 Vitamini": {"avg": 320, "unit": "pg/mL", "low_pct": 40, "note": "Ozellikle genc kadinlarda yaygin"},
    "Demir (Ferritin)": {"avg": 45, "unit": "ng/mL", "low_pct": 35, "note": "Adet goren kadinlarda %50 eksik"},
    "Folat (B9)": {"avg": 7, "unit": "ng/mL", "low_pct": 25, "note": "Ekmege folat eklenmesiyle azaldi"},
    "Magnezyum": {"avg": 1.9, "unit": "mg/dL", "low_pct": 30, "note": "Stresli yasam eksikligi artirir"},
    "Cinko (Zinc)": {"avg": 85, "unit": "ug/dL", "low_pct": 20, "note": "Erkeklerde daha yaygin normal"},
    "C Vitamini": {"avg": 0.9, "unit": "mg/dL", "low_pct": 15, "note": "Meyve tuketimi iyi olan bolgelerde dusuk"},
    "Omega-3": {"avg": 5.5, "unit": "indeks %", "low_pct": 60, "note": "Turkiye'de balik tuketimi cok dusuk"},
}

# Food portions to meet daily requirements
FOOD_PORTIONS = {
    "D Vitamini": [
        {"food": "Somon", "portion": "100g", "amount": "15 mcg", "pct": 75},
        {"food": "Yumurta", "portion": "2 adet", "amount": "2 mcg", "pct": 10},
        {"food": "Mantar", "portion": "100g", "amount": "7 mcg", "pct": 35},
        {"food": "Ton Baligi", "portion": "100g", "amount": "5 mcg", "pct": 25},
    ],
    "B12 Vitamini": [
        {"food": "Dana Ciger", "portion": "100g", "amount": "70 mcg", "pct": 100},
        {"food": "Somon", "portion": "100g", "amount": "4.7 mcg", "pct": 100},
        {"food": "Yumurta", "portion": "2 adet", "amount": "1.5 mcg", "pct": 63},
        {"food": "Yogurt", "portion": "200g", "amount": "1.3 mcg", "pct": 54},
    ],
    "Demir (Ferritin)": [
        {"food": "Kirmizi Et", "portion": "100g", "amount": "2.7 mg", "pct": 34},
        {"food": "Ispanak", "portion": "100g", "amount": "2.7 mg", "pct": 34},
        {"food": "Mercimek", "portion": "100g", "amount": "3.3 mg", "pct": 41},
        {"food": "Kuru Kayisi", "portion": "50g", "amount": "1.5 mg", "pct": 19},
    ],
    "Magnezyum": [
        {"food": "Kabak Cekirdegi", "portion": "30g", "amount": "150 mg", "pct": 38},
        {"food": "Bitter Cikolata", "portion": "30g", "amount": "50 mg", "pct": 13},
        {"food": "Badem", "portion": "30g", "amount": "80 mg", "pct": 20},
        {"food": "Ispanak", "portion": "100g", "amount": "79 mg", "pct": 20},
    ],
    "C Vitamini": [
        {"food": "Kirmizi Biber", "portion": "1 adet", "amount": "190 mg", "pct": 100},
        {"food": "Kivi", "portion": "1 adet", "amount": "70 mg", "pct": 78},
        {"food": "Portakal", "portion": "1 adet", "amount": "70 mg", "pct": 78},
        {"food": "Brokoli", "portion": "100g", "amount": "89 mg", "pct": 99},
    ],
    "Cinko (Zinc)": [
        {"food": "Dana Eti", "portion": "100g", "amount": "4.8 mg", "pct": 44},
        {"food": "Kabak Cekirdegi", "portion": "30g", "amount": "2.2 mg", "pct": 20},
        {"food": "Nohut", "portion": "100g", "amount": "2.5 mg", "pct": 23},
        {"food": "Kaju", "portion": "30g", "amount": "1.6 mg", "pct": 15},
    ],
    "Folat (B9)": [
        {"food": "Ispanak", "portion": "100g", "amount": "194 mcg", "pct": 49},
        {"food": "Mercimek", "portion": "100g", "amount": "181 mcg", "pct": 45},
        {"food": "Avokado", "portion": "1 adet", "amount": "163 mcg", "pct": 41},
        {"food": "Brokoli", "portion": "100g", "amount": "63 mcg", "pct": 16},
    ],
    "Omega-3": [
        {"food": "Somon", "portion": "100g", "amount": "2.3g", "pct": 100},
        {"food": "Uskumru", "portion": "100g", "amount": "2.7g", "pct": 100},
        {"food": "Ceviz", "portion": "30g", "amount": "2.6g ALA", "pct": 100},
        {"food": "Sardalya", "portion": "100g", "amount": "1.5g", "pct": 75},
    ],
}

# Vitamin Quiz
QUIZ_QUESTIONS = [
    {"q": "Hangi vitamin aslinda bir hormondur?", "options": ["A Vitamini", "D Vitamini", "C Vitamini", "E Vitamini"], "answer": 1, "explain": "D vitamini vucut tarafindan uretilir ve 1000+ geni kontrol eder."},
    {"q": "Insanlar hangi vitamini kendi vucudunda uretemez?", "options": ["D Vitamini", "K Vitamini", "C Vitamini", "B12 Vitamini"], "answer": 2, "explain": "Memelilerin cogu C vitamini uretir ama insanlar, maymunlar ve kobaylar uretemez."},
    {"q": "Cay icmek hangi mineralin emilimini en cok azaltir?", "options": ["Cinko", "Demir", "Magnezyum", "Kalsiyum"], "answer": 1, "explain": "Caydaki taninler demir emilimini %60'a kadar dusurur. Yemekten 1 saat sonra icin."},
    {"q": "Beynin yaklasik yuzde kaci yagdan olusur?", "options": ["%20", "%40", "%60", "%80"], "answer": 2, "explain": "Beynin %60'i yag ve bunun buyuk kismi DHA (Omega-3). Hafiza icin kritik."},
    {"q": "Hangi vitamin gece gorusunu etkiler?", "options": ["C Vitamini", "A Vitamini", "E Vitamini", "K Vitamini"], "answer": 1, "explain": "A vitamini retinol formunda retinada gorev yapar. Eksikliginde gece korlugu olusur."},
    {"q": "Sigara icmek hangi vitaminin ihtiyacini %40 arttirir?", "options": ["B12", "D Vitamini", "C Vitamini", "Folat"], "answer": 2, "explain": "Sigara dumani C vitaminini hizla tuketir. Sigara icenler ekstra 200mg/gun almali."},
    {"q": "Hangi mineral 300'den fazla enzimde gorev alir?", "options": ["Demir", "Cinko", "Magnezyum", "Selenyum"], "answer": 2, "explain": "Magnezyum vudutte en cok kullanilan minerallerden. Kas, sinir, enerji hepsinde rol oynar."},
    {"q": "K vitamininin adi nereden gelir?", "options": ["Kemik", "Koagulation", "Kalium", "Keratin"], "answer": 1, "explain": "K vitamini Almanca 'Koagulation' (pihtilasma) kelimesinden gelir."},
    {"q": "Turkiye'de en yaygin vitamin eksikligi hangisi?", "options": ["B12", "Demir", "D Vitamini", "C Vitamini"], "answer": 2, "explain": "Turkiye'de yetiskinlerin %75'inde D vitamini eksikligi var."},
    {"q": "Hangisi demir emilimini arttirir?", "options": ["Cay", "Sut", "C Vitamini", "Kahve"], "answer": 2, "explain": "C vitamini bitkisel demirin emilimini 6 kat arttirir. Yemekle birlikte portakal/limon tuketin."},
]

# Turkish supplement brand suggestions
TR_BRANDS = {
    "D Vitamini": {"brands": ["Solgar D3 1000 IU", "NBL D3 1000", "Orzax Ocean D3"], "tip": "Damla form kucuk cocuklar icin, kapsul yetiskinler icin. Yagla birlikte al."},
    "B12 Vitamini": {"brands": ["Solgar Methylcobalamin 1000mcg", "NBL B12", "Now Foods B12 Dil Alti"], "tip": "Metilkobalamin formu en iyi emilir. Dil alti tablet veya spray tercih et."},
    "Demir (Ferritin)": {"brands": ["Solgar Gentle Iron", "Ferro Sanol Duodenal", "Now Foods Iron"], "tip": "Demir bisglisinatt mide yakmaz. Ac karnina C vitamini ile birlikte al."},
    "Magnezyum": {"brands": ["Solgar Magnesium Citrate", "NBL Magnezyum", "Orzax Ocean Mg"], "tip": "Sitrat veya glisinatt formu en iyi emilir. Oksit formundan kacin."},
    "Folat (B9)": {"brands": ["Solgar Folate", "Jarrow Methyl Folate", "Thorne 5-MTHF"], "tip": "Folik asit degil metilfolat tercih et. MTHFR mutasyonu olanlarda onemli."},
    "Cinko (Zinc)": {"brands": ["Solgar Zinc Picolinate", "Now Foods Zinc", "NBL Cinko"], "tip": "Pikolinat formu en iyi emilir. Ac karnina al, bakir dengesine dikkat."},
    "C Vitamini": {"brands": ["Ester-C 1000mg", "Solgar Vitamin C", "Now Foods C-1000"], "tip": "Ester-C mideye daha yumusak. Bolen dozlarda al (sabah-aksam 500mg)."},
    "Omega-3": {"brands": ["Nordic Naturals Ultimate", "Solgar Omega-3", "Orzax Ocean Plus"], "tip": "EPA+DHA toplami 1000mg+ olmali. Balik kokusuz kapsul tercih et."},
}

# Before/after simulation data
SIMULATION = {
    "D Vitamini": {
        "1_ay": ["Yorgunluk hafifler", "Uyku kalitesi artar"],
        "3_ay": ["Kemik agrilari azalir", "Bagisiklik guclenir", "Ruh hali duzelmege baslar"],
        "6_ay": ["Kemik yogunlugu artar", "Kas gucu belirgin iyilesir", "Kronik yorgunluk gecer"],
    },
    "B12 Vitamini": {
        "1_ay": ["Enerji seviyesi artar", "Uyusma/karincalanma azalir"],
        "3_ay": ["Hafiza ve konsantrasyon duzilir", "Depresif belirtiler azalir"],
        "6_ay": ["Sinir hasari iyilesir", "Kan degerleri tamamen normallesir"],
    },
    "Demir (Ferritin)": {
        "1_ay": ["Nefes darligi azalir", "Bas donmesi gecer"],
        "3_ay": ["Sac dokulmesi durur", "Enerji belirgin artar", "Tirnak guclenir"],
        "6_ay": ["Ferritin deposu dolar", "Egzersiz kapasitesi artar"],
    },
    "Magnezyum": {
        "1_ay": ["Kas kramplari biter", "Uyku kalitesi artar", "Anksiyete azalir"],
        "3_ay": ["Bas agrilari sikligi duser", "Stres toleransi artar"],
        "6_ay": ["Kalp ritmi duzelir", "Kemik sagligi iyilesir"],
    },
    "Folat (B9)": {
        "1_ay": ["Yorgunluk azalir", "Ruh hali duzilir"],
        "3_ay": ["Hucre yenilenmesi hizlanir", "Homosistein duser"],
        "6_ay": ["DNA onarim kapasitesi artar"],
    },
    "Omega-3": {
        "1_ay": ["Eklem sertligi azalir", "Cilt nemLenir"],
        "3_ay": ["Konsantrasyon artar", "Trigliserit duser", "Goz kurulugy azalir"],
        "6_ay": ["Beyin fonksiyonlari belirgin iyilesir", "Kardiyovaskuler risk azalir"],
    },
    "Cinko (Zinc)": {
        "1_ay": ["Tat ve koku duyusu duzilir", "Yaralar daha hizli iyilesir"],
        "3_ay": ["Bagisiklik guclenir", "Cilt problemleri azalir"],
        "6_ay": ["Hormonal denge iyilesir", "Sac ve tirnak guclenir"],
    },
}
