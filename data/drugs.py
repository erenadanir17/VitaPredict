PSYCH_DRUGS = {
    "SSRI (Antidepresanlar)": {
        "examples": ["Sertralin (Lustral)", "Fluoksetin (Prozac)", "Essitalopram (Cipralex)"],
        "mechanism": "Serotonin geri alimini bloke eder.",
        "vitamin_interactions": [
            {"vitamin": "Folat (B9)", "effect": "critical", "description": "Folat eksikligi serotonin sentezini bozar. SSRI etkisiz kalir.", "recommendation": "Folat seviyeni kontrol ettir."},
            {"vitamin": "B12 Vitamini", "effect": "critical", "description": "B12 olmadan folat aktif forma donusemez.", "recommendation": "B12 ve folat birlikte kontrol edilmeli."},
            {"vitamin": "D Vitamini", "effect": "important", "description": "D vitamini serotonin reseptor yogunlugunu etkiler.", "recommendation": "D vitamini 30 ng/mL uzerinde tutulmali."},
            {"vitamin": "Omega-3", "effect": "important", "description": "Omega-3 sinaps membranlarini saglikli tutar.", "recommendation": "Haftada 2-3 kez yagli balik."},
            {"vitamin": "Magnezyum", "effect": "moderate", "description": "Magnezyum serotonin reseptor duyarliligini artirir.", "recommendation": "Gunluk 200-400mg magnezyum."},
        ],
    },
    "SNRI (Dual Antidepresanlar)": {
        "examples": ["Venlafaksin (Efexor)", "Duloksetin (Cymbalta)"],
        "mechanism": "Serotonin ve noradrenalin geri alimini bloke eder.",
        "vitamin_interactions": [
            {"vitamin": "B6 Vitamini", "effect": "critical", "description": "B6 hem serotonin hem noradrenalin sentezinde kofaktor.", "recommendation": "B6 seviyesi kontrol edilmeli."},
            {"vitamin": "Folat (B9)", "effect": "critical", "description": "Folat monoamin norotransmitter sentezinin kofaktoru.", "recommendation": "Metilfolat tercih edilmeli."},
            {"vitamin": "Magnezyum", "effect": "important", "description": "Magnezyum noradrenerjik sistem duzenleyicisi.", "recommendation": "Gunluk 300-400mg magnezyum."},
        ],
    },
    "Benzodiazepinler (Anksiyolitikler)": {
        "examples": ["Alprazolam (Xanax)", "Diazepam (Diazem)", "Lorazepam (Ativan)"],
        "mechanism": "GABA reseptorlerini aktive ederek sinir sistemini yatistirir.",
        "vitamin_interactions": [
            {"vitamin": "Magnezyum", "effect": "critical", "description": "Magnezyum dogal GABA agonisti. Benzodiazepin ihtiyacini azaltabilir.", "recommendation": "Magnezyum takviyesi doktor kontrolunde dozu azaltabilir."},
            {"vitamin": "B6 Vitamini", "effect": "important", "description": "B6 GABA sentezinde dogrudan gorev alir.", "recommendation": "B6 seviyesi normal tutulmali."},
            {"vitamin": "D Vitamini", "effect": "moderate", "description": "D vitamini GABA uretimini duzenler.", "recommendation": "D vitamini 30-50 ng/mL arasinda tutulmali."},
        ],
    },
    "Antipsikotikler": {
        "examples": ["Ketiapin (Seroquel)", "Olanzapin (Zyprexa)", "Aripiprazol (Abilify)"],
        "mechanism": "Dopamin reseptorlerini bloke eder.",
        "vitamin_interactions": [
            {"vitamin": "D Vitamini", "effect": "critical", "description": "Antipsikotik kullananlarin %70-80 inde D vitamini eksikligi var.", "recommendation": "Duzenli D vitamini takibi sart."},
            {"vitamin": "B12 Vitamini", "effect": "important", "description": "Antipsikotikler B12 emilimini etkileyebilir.", "recommendation": "3 ayda bir B12 kontrolu."},
            {"vitamin": "Omega-3", "effect": "important", "description": "Omega-3 metabolik yan etkileri azaltabilir.", "recommendation": "Gunluk 2g Omega-3."},
        ],
    },
    "Mood Stabilizatorler": {
        "examples": ["Lityum", "Valproat (Depakin)", "Lamotrijin (Lamictal)"],
        "mechanism": "Noronal uyarilabilirligi duzenler.",
        "vitamin_interactions": [
            {"vitamin": "Folat (B9)", "effect": "critical", "description": "Valproat ve karbamazepin folat seviyesini dusurur.", "recommendation": "Folat takviyesi alinmali."},
            {"vitamin": "D Vitamini", "effect": "critical", "description": "Antiepileptik mood stabilizatorler D vitamini metabolizmasini hizlandirir.", "recommendation": "6 ayda bir D vitamini kontrolu."},
        ],
    },
    "Psikostimulanlar (DEHB ilaclari)": {
        "examples": ["Metilfenidat (Ritalin/Concerta)", "Atomoksetin (Strattera)"],
        "mechanism": "Dopamin ve noradrenalin geri alimini bloke eder.",
        "vitamin_interactions": [
            {"vitamin": "Demir (Ferritin)", "effect": "critical", "description": "Ferritin dusuk olursa DEHB semptomlari agirlesir. Dopamin sentezi icin demir sart.", "recommendation": "Ferritin 40 ng/mL uzerinde tutulmali."},
            {"vitamin": "Cinko (Zinc)", "effect": "critical", "description": "Cinko dopamin tasiyici protein regulasyonunda rol oynar.", "recommendation": "Cinko takviyesi ilac etkinligini artirabilir."},
            {"vitamin": "Omega-3", "effect": "important", "description": "Omega-3 prefrontal korteks fonksiyonunu destekler.", "recommendation": "Gunluk 1-2g Omega-3."},
            {"vitamin": "Magnezyum", "effect": "important", "description": "Stimulanlar magnezyum atilimini artirabilir.", "recommendation": "Magnezyum seviyesi takip edilmeli."},
        ],
    },
}

INTERACTION_ALERTS = [
    {"condition": ["B12 Vitamini", "Folat (B9)"], "drug_class": "SSRI (Antidepresanlar)", "alert": "KRITIK: B12 ve Folat birlikte eksikse antidepresan etkisi ciddi sekilde azalir!", "detail": "Serotonin sentezi icin B6 + B12 + Folat uclusu gerekli.", "severity": "critical"},
    {"condition": ["D Vitamini"], "drug_class": "Benzodiazepinler (Anksiyolitikler)", "alert": "D Vitamini eksikligi anksiyete ilaclarinin etkisini azaltir!", "detail": "D vitamini serotonin ve GABA sistemiyle dogrudan iliskili.", "severity": "important"},
    {"condition": ["Magnezyum"], "drug_class": "Benzodiazepinler (Anksiyolitikler)", "alert": "Magnezyum dogal sakinlestiricidir - benzodiazepin ihtiyacini azaltabilir.", "detail": "Magnezyum GABA reseptorlerini aktive eder.", "severity": "moderate"},
    {"condition": ["Demir (Ferritin)", "Cinko (Zinc)"], "drug_class": "Psikostimulanlar (DEHB ilaclari)", "alert": "KRITIK: Demir ve Cinko eksikligi DEHB ilaclarinin etkinligini ciddi sekilde dusurur!", "detail": "Dopamin sentezi demire, regulasyon cinkoya bagli.", "severity": "critical"},
    {"condition": ["D Vitamini"], "drug_class": "Antipsikotikler", "alert": "Antipsikotik kullananlarin cogunda D vitamini eksikligi var!", "detail": "Ilac metabolizmayi yavaslatir, D vitamini ihtiyaci artar.", "severity": "critical"},
    {"condition": ["Folat (B9)"], "drug_class": "Mood Stabilizatorler", "alert": "Mood stabilizatorler folat seviyesini dusurur!", "detail": "Bu ilaclar folat metabolizmasini bozar.", "severity": "critical"},
]
