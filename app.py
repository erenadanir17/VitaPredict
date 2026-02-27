import streamlit as st
import plotly.graph_objects as go
from data.vitamins import VITAMINS
from data.drugs import PSYCH_DRUGS
from utils.analyzer import analyze_all, check_drug_interactions, get_combined_recovery_timeline
from utils.styles import get_main_css
from utils.pdf_report import generate_pdf
from data.extras import SYMPTOM_MAP, MEAL_PLANS, CONFLICT_MATRIX, SUPPLEMENT_COSTS, VITAMIN_FACTS, TR_AVERAGES, FOOD_PORTIONS, QUIZ_QUESTIONS, TR_BRANDS, SIMULATION
from datetime import datetime
import random

st.set_page_config(page_title="VitaPredict", page_icon="V", layout="wide", initial_sidebar_state="expanded")
st.markdown(get_main_css(), unsafe_allow_html=True)

vit_count = len(VITAMINS)
drug_count = len(PSYCH_DRUGS)

st.markdown(f'''
<div class="hero">
    <h1>Vita<span>Predict</span></h1>
    <p class="sub">Vitamin tahlilini gir, vucudunda neler degisecegini gor</p>
    <div class="badge-count">
        {vit_count} Vitamin & Mineral
        <span class="sep"></span>
        {drug_count} Ilac Sinifi
        <span class="sep"></span>
        Kisisel Analiz
    </div>
</div>
''', unsafe_allow_html=True)

# ============ SIDEBAR ============
with st.sidebar:
    st.markdown("### Kisisel Profil")
    col_a, col_b = st.columns(2)
    with col_a:
        age = st.number_input("Yas", min_value=0, max_value=120, value=0, step=1, key="age")
    with col_b:
        gender = st.selectbox("Cinsiyet", ["Secilmedi", "Erkek", "Kadin"], key="gender")

    lifestyle = st.multiselect(
        "Yasam Tarzi",
        ["Sigara kullaniyorum", "Alkol kullaniyorum", "Vegan / Vejetaryen",
         "Hamile / Emziren", "Duzensiz beslenme", "Yogun spor yapiyorum",
         "Stresli calisma hayati", "Gunes isigi az aliyorum"],
        key="lifestyle"
    )

    st.markdown("---")
    st.markdown("### Tahlil Sonuclarin")
    st.caption("Sadece bildigin degerleri gir.")
    user_values = {}

    vitamins_list = [(n, i) for n, i in VITAMINS.items() if i["category"] == "Vitamin"]
    minerals_list = [(n, i) for n, i in VITAMINS.items() if i["category"] == "Mineral"]
    others_list = [(n, i) for n, i in VITAMINS.items() if i["category"] not in ("Vitamin", "Mineral")]

    st.markdown("---")
    st.markdown("**Vitaminler**")
    for name, info in vitamins_list:
        val = st.number_input(
            f"{info['letter']} | {name} ({info['unit']})",
            min_value=0.0, max_value=float(info['max_normal']) * 5.0,
            value=0.0, step=0.1, key=f"v_{name}", format="%.1f",
            help=f"Normal: {info['min_normal']} - {info['max_normal']} {info['unit']}"
        )
        if val > 0:
            user_values[name] = val

    st.markdown("---")
    st.markdown("**Mineraller**")
    for name, info in minerals_list:
        val = st.number_input(
            f"{info['letter']} | {name} ({info['unit']})",
            min_value=0.0, max_value=float(info['max_normal']) * 5.0,
            value=0.0, step=0.1, key=f"v_{name}", format="%.1f",
            help=f"Normal: {info['min_normal']} - {info['max_normal']} {info['unit']}"
        )
        if val > 0:
            user_values[name] = val

    if others_list:
        st.markdown("---")
        st.markdown("**Diger**")
        for name, info in others_list:
            val = st.number_input(
                f"{info['letter']} | {name} ({info['unit']})",
                min_value=0.0, max_value=float(info['max_normal']) * 5.0,
                value=0.0, step=0.1, key=f"v_{name}", format="%.1f",
                help=f"Normal: {info['min_normal']} - {info['max_normal']} {info['unit']}"
            )
            if val > 0:
                user_values[name] = val

    st.markdown("---")
    st.markdown("### Kullandigin Ilaclar")
    selected_drugs = []
    for dn, di in PSYCH_DRUGS.items():
        if st.checkbox(dn, key=f"d_{dn}"):
            selected_drugs.append(dn)
    st.markdown("---")
    go_btn = st.button("Analiz Et", use_container_width=True, type="primary")

    st.markdown("---")
    demo_btn = st.button("Demo Modu", use_container_width=True, help="Ornek tahlil sonuclariyla uygulamayi gor")
    if demo_btn:
        demo_values = {
            "D Vitamini": 8.0, "B12 Vitamini": 180.0, "Folat (B9)": 3.2,
            "Demir (Ferritin)": 9.0, "Magnezyum": 1.75, "Cinko (Zinc)": 55.0,
            "C Vitamini": 0.8, "Omega-3": 4.5, "B6 Vitamini": 12.0,
            "Selenyum": 70.0
        }
        for k, v in demo_values.items():
            user_values[k] = v
        go_btn = True

    st.markdown("---")
    st.markdown("### Su Hesaplayici")
    weight = st.number_input("Kilonuz (kg)", min_value=0, max_value=200, value=0, step=1, key="weight")
    if weight > 0:
        water_ml = weight * 35
        water_l = round(water_ml / 1000, 1)
        cups = int(water_l / 0.25)
        cups_display = min(cups, 12)
        cup_html = ''.join(['<span class="water-cup filled">💧</span>' for _ in range(cups_display)])
        cup_html += ''.join(['<span class="water-cup">💧</span>' for _ in range(12 - cups_display)])
        st.markdown(f'''
        <div class="water-card">
            <div class="water-val">{water_l}L</div>
            <div class="water-unit">gunluk su ihtiyaci ({cups} bardak)</div>
            <div class="water-cups">{cup_html}</div>
        </div>
        ''', unsafe_allow_html=True)


# ==== Profile alerts ====
def get_profile_alerts(age, gender, lifestyle, deficient_names):
    alerts = []
    ls = set(lifestyle)
    if gender == "Kadin":
        if "Demir (Ferritin)" in deficient_names:
            alerts.append(("Fe", "Kadinlarda demir eksikligi cok yaygindir. Adet donemlerinde kayip artar. <strong>Ferritin 40+ ng/mL</strong> hedefleyin."))
        if "Folat (B9)" in deficient_names:
            alerts.append(("B9", "Kadinlarda folat ihtiyaci yuksektir. Gebelik planliyorsan <strong>metilfolat</strong> takviyesi sart."))
        if age > 45:
            alerts.append(("D", "Menopoz doneminde <strong>D vitamini ve Kalsiyum</strong> ihtiyaci belirgin artar."))
    if gender == "Erkek" and age > 50:
        alerts.append(("Zn", "50 yas uzerinde <strong>cinko</strong> ihtiyaci artar. Prostat ve testosteron icin onemli."))
    if age > 60:
        alerts.append(("B12", "60+ yasta <strong>B12 emilimi</strong> dogal olarak azalir. Dil alti veya enjeksiyon formu daha etkili."))
        alerts.append(("D", "Yas ilerledikce ciltte D vitamini uretimi duser. <strong>Takviye neredeyse zorunlu.</strong>"))
    if age > 0 and age < 25:
        alerts.append(("Fe", "Genc yasta buyume icin <strong>demir ve cinko</strong> ihtiyaci yukselir."))
    if "Sigara kullaniyorum" in ls:
        alerts.append(("C", "Sigara <strong>C vitamini</strong> ihtiyacini %40 arttirir. Ekstra 200mg/gun alin."))
    if "Alkol kullaniyorum" in ls:
        alerts.append(("B1", "Alkol <strong>B1 (Tiamin)</strong> emilimini ciddi sekilde bozar."))
        alerts.append(("Mg", "Alkol <strong>magnezyum</strong> atilimini arttirir."))
    if "Vegan / Vejetaryen" in ls:
        alerts.append(("B12", "Vegan beslenmede <strong>B12 takviyesi</strong> mutlaka gerekli."))
        alerts.append(("Fe", "Bitkisel demir emilimi dusuk. <strong>C vitamini</strong> ile birlikte alin."))
    if "Hamile / Emziren" in ls:
        alerts.append(("B9", "Hamilelikte <strong>folat</strong> en kritik vitamin. En az 600mcg/gun."))
        alerts.append(("Fe", "Hamilelikte kan hacmi artar, <strong>demir</strong> ihtiyaci iki katina cikar."))
    if "Yogun spor yapiyorum" in ls:
        alerts.append(("Mg", "Yogun egzersiz <strong>magnezyum</strong> kaybini arttirir."))
        alerts.append(("Fe", "Sporcularda <strong>demir</strong> ihtiyaci %30 artar."))
    if "Stresli calisma hayati" in ls:
        alerts.append(("Mg", "Stres <strong>magnezyum</strong> depolarini hizla tuketir."))
        alerts.append(("C", "Kortizol uretimi <strong>C vitamini</strong> ihtiyacini arttirir."))
    if "Gunes isigi az aliyorum" in ls:
        alerts.append(("D", "Guneslenme az ise <strong>D vitamini</strong> takviyesi zorunlu."))
    return alerts


STATUS_MAP = {
    "urgent":     {"badge": "badge-urgent",     "val_color": "#f43f5e", "bar": "#f43f5e", "accent": "#f43f5e"},
    "critical":   {"badge": "badge-critical",   "val_color": "#f59e0b", "bar": "#f59e0b", "accent": "#f59e0b"},
    "deficient":  {"badge": "badge-deficient",  "val_color": "#eab308", "bar": "#eab308", "accent": "#eab308"},
    "borderline": {"badge": "badge-borderline", "val_color": "#3b82f6", "bar": "#3b82f6", "accent": "#3b82f6"},
    "normal":     {"badge": "badge-normal",     "val_color": "#22c55e", "bar": "#22c55e", "accent": "#22c55e"},
    "excess":     {"badge": "badge-deficient",  "val_color": "#f59e0b", "bar": "#f59e0b", "accent": "#f59e0b"},
}


# ============ WELCOME ============
if not go_btn and not user_values:

    st.markdown('''
    <div class="welcome-grid">
        <div class="w-card">
            <div class="accent" style="background:linear-gradient(180deg,#8b5cf6,#2dd4bf)"></div>
            <div class="num">01</div>
            <div class="title">Profilini Olustur</div>
            <div class="desc">Yas, cinsiyet ve yasam tarzi faktorlerini gir. Kisisel risk analizin icin gerekli.</div>
        </div>
        <div class="w-card">
            <div class="accent" style="background:linear-gradient(180deg,#2dd4bf,#3b82f6)"></div>
            <div class="num">02</div>
            <div class="title">Tahlilini Gir</div>
            <div class="desc">Kan tahlilindeki vitamin ve mineral degerlerini gir. Sadece bildigin degerleri yeter.</div>
        </div>
        <div class="w-card">
            <div class="accent" style="background:linear-gradient(180deg,#3b82f6,#f43f5e)"></div>
            <div class="num">03</div>
            <div class="title">Raporunu Al</div>
            <div class="desc">Eksiklik analizi, takviye plani, sinerji haritasi ve kisisel uyarilar.</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('''
    <div class="feat-row">
        <div class="feat"><div class="ico" style="color:#f43f5e">&#9679;</div><div class="ft">3 Seviye Tespit</div><div class="fd">Dusuk, Kritik, Acil</div></div>
        <div class="feat"><div class="ico" style="color:#3b82f6">&#9679;</div><div class="ft">Sinirda Uyarisi</div><div class="fd">Alt sinira yakinsa uyar</div></div>
        <div class="feat"><div class="ico" style="color:#2dd4bf">&#9679;</div><div class="ft">Takviye Plani</div><div class="fd">Doz, form, zamanlama</div></div>
        <div class="feat"><div class="ico" style="color:#8b5cf6">&#9679;</div><div class="ft">Kisisel Profil</div><div class="fd">Yas ve yasam tarzina gore</div></div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown(f'''<div class="sec">{vit_count} Desteklenen Vitamin & Mineral</div>''', unsafe_allow_html=True)
    grid = '<div class="vit-grid">'
    for name, info in VITAMINS.items():
        grid += f'''<div class="vit-item"><div class="vit-dot" style="background:{info['color']}">{info['letter']}</div><div class="vit-label">{name}</div></div>'''
    grid += '</div>'
    st.markdown(grid, unsafe_allow_html=True)

    # -- DAILY FACT --
    today_idx = datetime.now().toordinal() % len(VITAMIN_FACTS)
    fact = VITAMIN_FACTS[today_idx]
    fact_info = VITAMINS.get(fact["vit"], {})
    st.markdown(f'''
    <div class="fact-card">
        <div class="fact-tag">Gunun Bilgisi</div>
        <div class="fact-text">{fact["fact"]}</div>
        <div class="fact-vit">{fact_info.get("letter", "?")} {fact["vit"]}</div>
    </div>
    ''', unsafe_allow_html=True)

    # -- ENCYCLOPEDIA --
    st.markdown('''<div class="sec">Vitamin Ansiklopedisi</div>''', unsafe_allow_html=True)
    st.caption("Herhangi bir vitamini sec, detayini gor:")
    enc_selected = st.selectbox("Vitamin sec:", ["Secilmedi"] + list(VITAMINS.keys()), key="enc_sel", label_visibility="collapsed")
    if enc_selected != "Secilmedi":
        ei = VITAMINS[enc_selected]
        brain = ei.get("brain_effect", "")
        foods = ", ".join(ei.get("food_sources", [])[:5])
        supp = ei.get("supplement", {})
        supp_text = f'{supp.get("dose","-")} | {supp.get("form","-")}' if supp else "-"
        st.markdown(f'''
        <div class="enc-card">
            <div class="enc-header">
                <div class="enc-dot" style="background:{ei['color']}">{ei['letter']}</div>
                <div><div class="enc-name">{enc_selected}</div><div class="enc-cat">{ei['category']}</div></div>
            </div>
            <div class="enc-body">
                <div class="enc-row"><span class="enc-label">Normal Aralik</span><span class="enc-val">{ei['min_normal']} - {ei['max_normal']} {ei['unit']}</span></div>
                <div class="enc-row"><span class="enc-label">Onerilen Takviye</span><span class="enc-val">{supp_text}</span></div>
                <div class="enc-row"><span class="enc-label">Besin Kaynaklari</span><span class="enc-val">{foods}</span></div>
                <div class="enc-row"><span class="enc-label">Beyin Etkisi</span><span class="enc-val" style="white-space:normal;text-align:right;max-width:60%">{brain[:120]}...</span></div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    # -- SYMPTOM CHECKER --
    st.markdown('''<div class="sec">Belirtilerini Sec</div>''', unsafe_allow_html=True)
    st.caption("Tahlil sonucun yoksa belirtilerinden tahmin edelim:")
    selected_symptoms = st.multiselect(
        "Yasadigin belirtileri sec:",
        list(SYMPTOM_MAP.keys()),
        key="symptoms",
        label_visibility="collapsed"
    )

    if selected_symptoms:
        vit_scores = {}
        for sym in selected_symptoms:
            for vit in SYMPTOM_MAP.get(sym, []):
                vit_scores[vit] = vit_scores.get(vit, 0) + 1
        ranked = sorted(vit_scores.items(), key=lambda x: -x[1])
        max_score = ranked[0][1] if ranked else 1

        for vit_name, score in ranked:
            info = VITAMINS.get(vit_name, {})
            pct = int((score / len(selected_symptoms)) * 100)
            st.markdown(f'''
            <div class="sym-result" style="--accent:{info.get('color','#8b5cf6')}">
                <div style="position:absolute;left:0;top:0;width:3px;height:100%;background:{info.get('color','#8b5cf6')}"></div>
                <div class="sym-vit">{info.get('letter','?')} | {vit_name}</div>
                <div class="sym-bar-wrap"><div class="sym-bar" style="width:{pct}%;background:{info.get('color','#8b5cf6')}"></div></div>
                <div class="sym-count">{score}/{len(selected_symptoms)} belirtiyle eslesiyor</div>
            </div>''', unsafe_allow_html=True)

    # -- QUIZ --
    st.markdown('''<div class="sec">Vitamin Quiz</div>''', unsafe_allow_html=True)
    st.caption("Vitamin bilgini test et!")
    if "quiz_idx" not in st.session_state:
        st.session_state.quiz_idx = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_answers = []

    qi = st.session_state.quiz_idx
    if qi < len(QUIZ_QUESTIONS):
        q = QUIZ_QUESTIONS[qi]
        st.markdown(f'''
        <div class="quiz-card">
            <div class="quiz-num">Soru {qi+1} / {len(QUIZ_QUESTIONS)}</div>
            <div class="quiz-q">{q["q"]}</div>
        </div>''', unsafe_allow_html=True)
        answer = st.radio("Cevabini sec:", q["options"], key=f"quiz_{qi}", label_visibility="collapsed")
        if st.button("Cevapla", key=f"quiz_btn_{qi}"):
            chosen = q["options"].index(answer)
            correct = chosen == q["answer"]
            st.session_state.quiz_answers.append(correct)
            if correct:
                st.session_state.quiz_score += 1
                st.markdown(f'<div class="quiz-result correct">Dogru! {q["explain"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="quiz-result wrong">Yanlis! Dogru cevap: {q["options"][q["answer"]]}. {q["explain"]}</div>', unsafe_allow_html=True)
            st.session_state.quiz_idx += 1
    else:
        sc = st.session_state.quiz_score
        total = len(QUIZ_QUESTIONS)
        dots = ""
        for i, correct in enumerate(st.session_state.quiz_answers):
            cls = "quiz-dot right" if correct else "quiz-dot wrong"
            dots += f'<div class="{cls}">{i+1}</div>'
        st.markdown(f'''
        <div class="quiz-card">
            <div class="quiz-num">Sonuc</div>
            <div class="quiz-q">Skorun: {sc}/{total}</div>
            <div class="quiz-score-bar">{dots}</div>
        </div>''', unsafe_allow_html=True)
        if st.button("Tekrar Oyna", key="quiz_reset"):
            st.session_state.quiz_idx = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_answers = []

    st.markdown('''<div class="disc">Bu uygulama bilgilendirme amaclidir, tibbi tavsiye yerine gecmez.</div>''', unsafe_allow_html=True)


elif go_btn and not user_values:
    st.warning("Sol panelden en az bir vitamin degeri gir!")


# ============ RESULTS ============
else:
    report = analyze_all(user_values)
    n_def = report["count_deficient"]
    n_urg = report["count_urgent"]
    n_crit = report["count_critical"]
    n_low = report["count_low"]
    n_bord = report["count_borderline"]
    n_norm = report["count_normal"]
    n_total = report["count_total"]

    # Ring color
    if n_urg > 0:
        ring_color = "#f43f5e"
    elif n_crit > 0:
        ring_color = "#f59e0b"
    elif n_low > 0:
        ring_color = "#eab308"
    elif n_bord > 0:
        ring_color = "#3b82f6"
    else:
        ring_color = "#22c55e"

    normal_pct = int((n_norm / n_total) * 100) if n_total > 0 else 100

    # -- Profile --
    has_profile = age > 0 or gender != "Secilmedi" or len(lifestyle) > 0
    if has_profile:
        g_text = gender if gender != "Secilmedi" else "-"
        a_text = str(age) if age > 0 else "-"
        l_text = str(len(lifestyle)) if lifestyle else "0"
        st.markdown(f'''
        <div class="prof-card">
            <div class="prof-title">Kisisel Profil</div>
            <div class="prof-grid">
                <div class="prof-item"><div class="prof-val">{a_text}</div><div class="prof-lbl">Yas</div></div>
                <div class="prof-item"><div class="prof-val">{g_text}</div><div class="prof-lbl">Cinsiyet</div></div>
                <div class="prof-item"><div class="prof-val">{l_text}</div><div class="prof-lbl">Risk Faktoru</div></div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    # -- Score + Metrics --
    col_s, col_m = st.columns([1, 2])
    with col_s:
        st.markdown(f'''
        <div class="score-wrap">
            <div class="score-ring" style="--ring-color:{ring_color};--ring-pct:{normal_pct}%">
                <div class="score-inner">
                    <div class="score-num">{n_def}</div>
                    <div class="score-lbl">Eksik</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    with col_m:
        st.markdown(f'''
        <div class="metrics">
            <div class="m-box red"><div class="m-num" style="color:#f43f5e">{n_urg}</div><div class="m-lbl">Acil</div></div>
            <div class="m-box orange"><div class="m-num" style="color:#f59e0b">{n_crit}</div><div class="m-lbl">Kritik</div></div>
            <div class="m-box yellow"><div class="m-num" style="color:#eab308">{n_low}</div><div class="m-lbl">Dusuk</div></div>
            <div class="m-box blue"><div class="m-num" style="color:#3b82f6">{n_bord}</div><div class="m-lbl">Sinirda</div></div>
            <div class="m-box green"><div class="m-num" style="color:#22c55e">{n_norm}</div><div class="m-lbl">Normal</div></div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown(f'''<div class="summary-box"><div class="summary-text">{report["summary"]}</div></div>''', unsafe_allow_html=True)

    # -- Personal Alerts --
    if has_profile:
        deficient_names = [v["name"] for v in report["deficient"]]
        p_alerts = get_profile_alerts(age, gender, lifestyle, deficient_names)
        if p_alerts:
            st.markdown('<div class="sec">Kisisel Risk Uyarilari</div>', unsafe_allow_html=True)
            for ico, text in p_alerts:
                st.markdown(f'''
                <div class="p-alert">
                    <div class="p-alert-ico">{ico}</div>
                    <div class="p-alert-text">{text}</div>
                </div>''', unsafe_allow_html=True)

    # -- CHARTS --
    if len(report["results"]) >= 2:
        st.markdown('<div class="sec">Vitamin Seviyeleri</div>', unsafe_allow_html=True)
        chart = report["chart_data"]
        names = [c["letter"] for c in chart]
        pcts = [round((c["value"]/c["min_normal"])*100,1) if c["min_normal"]>0 else 100 for c in chart]
        colors = [STATUS_MAP.get(c["status"],{}).get("bar","#64748b") for c in chart]

        col_bar, col_radar = st.columns(2)

        with col_bar:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=names, y=pcts, marker_color=colors, marker_line_width=0,
                text=[f"{v}%" for v in pcts], textposition="outside",
                textfont=dict(size=9, color="#64748b", family="JetBrains Mono")
            ))
            fig.add_hline(y=100, line_dash="dash", line_color="#8b5cf6", line_width=1.5,
                           annotation_text="Normal", annotation_font_color="#8b5cf6",
                           annotation_font_size=9)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#64748b", family="Space Grotesk"),
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=20), height=300,
                yaxis=dict(gridcolor="rgba(255,255,255,0.03)", zerolinecolor="rgba(255,255,255,0.03)", title=None),
                xaxis=dict(gridcolor="rgba(255,255,255,0.03)")
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with col_radar:
            capped = [min(p, 150) for p in pcts]
            radar = go.Figure()
            radar.add_trace(go.Scatterpolar(
                r=capped + [capped[0]], theta=names + [names[0]],
                fill='toself', fillcolor='rgba(139,92,246,0.1)',
                line=dict(color='#8b5cf6', width=2),
                marker=dict(color=colors + [colors[0]], size=7),
                name="Senin Degerin"
            ))
            radar.add_trace(go.Scatterpolar(
                r=[100]*len(names) + [100], theta=names + [names[0]],
                fill='none',
                line=dict(color='rgba(45,212,191,0.4)', width=1, dash='dash'),
                name="Normal"
            ))
            radar.update_layout(
                polar=dict(
                    bgcolor='rgba(0,0,0,0)',
                    radialaxis=dict(visible=True, range=[0, 150], gridcolor='rgba(255,255,255,0.03)',
                                    tickfont=dict(size=8, color='#334155'), linecolor='rgba(255,255,255,0.03)'),
                    angularaxis=dict(gridcolor='rgba(255,255,255,0.05)',
                                     tickfont=dict(size=10, color='#64748b', family='JetBrains Mono'))
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                margin=dict(l=40, r=40, t=20, b=20), height=300,
                font=dict(family="Space Grotesk")
            )
            st.plotly_chart(radar, use_container_width=True, config={"displayModeBar": False})

    # -- Deficient + Borderline --
    problem_vitamins = [v for v in report["deficient"] if v["status"] != "borderline"]
    borderline_vitamins = [v for v in report["deficient"] if v["status"] == "borderline"]

    if problem_vitamins:
        st.markdown('<div class="sec">Eksik Vitaminler</div>', unsafe_allow_html=True)
        for v in sorted(problem_vitamins, key=lambda x: -x["severity_score"]):
            sm = STATUS_MAP.get(v["status"], STATUS_MAP["deficient"])
            pct = min((v["value"]/v["min_normal"])*100,100) if v["min_normal"]>0 else 0
            st.markdown(f'''
            <div class="v-card">
                <div class="accent-left" style="background:{sm['accent']}"></div>
                <div class="v-icon" style="background:{v['color']}">{v['letter']}</div>
                <div class="v-info">
                    <div class="v-name">{v['name']}</div>
                    <div class="v-range">{v['min_normal']} - {v['max_normal']} {v['unit']}</div>
                    <div class="pbar-wrap"><div class="pbar" style="width:{pct}%;background:{sm['bar']};color:{sm['bar']}"></div></div>
                </div>
                <div class="v-right">
                    <div class="v-val" style="color:{sm['val_color']}">{v['value']} <span style="font-size:.7rem;opacity:.6">{v['unit']}</span></div>
                    <div class="v-badge {sm['badge']}">{v['status_label']}</div>
                </div>
            </div>''', unsafe_allow_html=True)

    if borderline_vitamins:
        st.markdown('<div class="sec">Sinirda Vitaminler</div>', unsafe_allow_html=True)
        st.caption("Normal araligin en alt sinirinda. Hafif takviye ile desteklenmeli.")
        for v in borderline_vitamins:
            sm = STATUS_MAP["borderline"]
            pct = min((v["value"]/v["min_normal"])*100,100) if v["min_normal"]>0 else 0
            st.markdown(f'''
            <div class="v-card">
                <div class="accent-left" style="background:{sm['accent']}"></div>
                <div class="v-icon" style="background:{v['color']}">{v['letter']}</div>
                <div class="v-info">
                    <div class="v-name">{v['name']}</div>
                    <div class="v-range">{v['min_normal']} - {v['max_normal']} {v['unit']}</div>
                    <div class="pbar-wrap"><div class="pbar" style="width:{pct}%;background:{sm['bar']};color:{sm['bar']}"></div></div>
                </div>
                <div class="v-right">
                    <div class="v-val" style="color:{sm['val_color']}">{v['value']} <span style="font-size:.7rem;opacity:.6">{v['unit']}</span></div>
                    <div class="v-badge {sm['badge']}">{v['status_label']}</div>
                </div>
            </div>''', unsafe_allow_html=True)

    # -- Normal --
    if report["normal"]:
        st.markdown('<div class="sec">Normal Vitaminler</div>', unsafe_allow_html=True)
        for v in report["normal"]:
            pct = min((v["value"]/v["max_normal"])*100,100) if v["max_normal"]>0 else 100
            st.markdown(f'''
            <div class="v-card">
                <div class="accent-left" style="background:#22c55e"></div>
                <div class="v-icon" style="background:{v['color']}">{v['letter']}</div>
                <div class="v-info">
                    <div class="v-name">{v['name']}</div>
                    <div class="v-range">{v['min_normal']} - {v['max_normal']} {v['unit']}</div>
                    <div class="pbar-wrap"><div class="pbar" style="width:{pct}%;background:#22c55e;color:#22c55e"></div></div>
                </div>
                <div class="v-right">
                    <div class="v-val" style="color:#22c55e">{v['value']} <span style="font-size:.7rem;opacity:.6">{v['unit']}</span></div>
                    <div class="v-badge badge-normal">NORMAL</div>
                </div>
            </div>''', unsafe_allow_html=True)

    # -- Supplement Plan --
    all_need_supp = report["deficient"]
    if all_need_supp:
        st.markdown('<div class="sec">Takviye Plani</div>', unsafe_allow_html=True)
        supp_html = '<div class="supp-grid">'
        for v in all_need_supp:
            info = VITAMINS.get(v["name"], {})
            supp = info.get("supplement")
            if supp:
                sm = STATUS_MAP.get(v["status"], STATUS_MAP["deficient"])
                supp_html += f'''
                <div class="supp-card" style="--accent:{sm['accent']}">
                    <div class="supp-header">
                        <div class="supp-dot" style="background:{v['color']}">{v['letter']}</div>
                        <div class="supp-name">{v['name']}</div>
                        <div class="supp-status" style="color:{sm['val_color']};background:{sm['accent']}15;border:1px solid {sm['accent']}30;margin-left:auto">{v['status_label']}</div>
                    </div>
                    <div class="supp-row"><div class="supp-label">DOZ</div><div class="supp-value">{supp['dose']}</div></div>
                    <div class="supp-row"><div class="supp-label">FORM</div><div class="supp-value">{supp['form']}</div></div>
                    <div class="supp-row"><div class="supp-label">NE ZAMAN</div><div class="supp-value">{supp['timing']}</div></div>
                    <div class="supp-note">{supp['note']}</div>
                </div>'''
        supp_html += '</div>'
        st.markdown(supp_html, unsafe_allow_html=True)

        # -- DAILY SCHEDULE --
        st.markdown('<div class="sec">Gunluk Takviye Programi</div>', unsafe_allow_html=True)
        morning, noon, evening = [], [], []
        for v in all_need_supp:
            info = VITAMINS.get(v["name"], {})
            supp = info.get("supplement")
            if not supp:
                continue
            timing = supp.get("timing", "").lower()
            item = {"letter": v["letter"], "color": v["color"], "name": v["name"], "dose": supp["dose"]}
            if any(w in timing for w in ["sabah", "ac karnina"]):
                morning.append(item)
            elif any(w in timing for w in ["aksam", "yatmadan"]):
                evening.append(item)
            else:
                noon.append(item)

        def sched_pills(items):
            if not items:
                return '<div class="sched-empty">-</div>'
            h = ""
            for it in items:
                h += f'''<div class="sched-pill"><div class="sp-dot" style="background:{it['color']}">{it['letter']}</div><div><div class="sp-name">{it['name']}</div><div class="sp-dose">{it['dose']}</div></div></div>'''
            return h

        st.markdown(f'''
        <div class="sched-grid">
            <div class="sched-col morning"><div class="sched-time">Sabah</div>{sched_pills(morning)}</div>
            <div class="sched-col noon"><div class="sched-time">Ogle</div>{sched_pills(noon)}</div>
            <div class="sched-col evening"><div class="sched-time">Aksam</div>{sched_pills(evening)}</div>
        </div>
        ''', unsafe_allow_html=True)

    # -- Synergy --
    if report["deficient"]:
        st.markdown('<div class="sec">Vitamin Sinerjisi</div>', unsafe_allow_html=True)
        deficient_names = {v["name"] for v in report["deficient"]}
        normal_names = {v["name"] for v in report["normal"]}
        for v in report["deficient"]:
            info = VITAMINS.get(v["name"], {})
            synergy = info.get("synergy", [])
            if synergy:
                chips = ""
                for s in synergy:
                    if s in deficient_names:
                        chips += f'''<span class="syn-chip missing">{s} (eksik!)</span>'''
                    elif s in normal_names:
                        chips += f'''<span class="syn-chip ok">{s}</span>'''
                    else:
                        chips += f'''<span class="syn-chip">{s}</span>'''
                st.markdown(f'''
                <div class="syn-card">
                    <div class="syn-title">{v['letter']} {v['name']} + birlikte al:</div>
                    <div class="syn-chips">{chips}</div>
                </div>''', unsafe_allow_html=True)

    # -- Detail --
    if report["deficient"]:
        st.markdown('<div class="sec">Detayli Analiz</div>', unsafe_allow_html=True)
        for v in report["deficient"]:
            with st.expander(f"{v['letter']} | {v['name']} -- {v['status_label']}", expanded=False):
                t1, t2, t3, t4 = st.tabs(["Belirtiler", "Iyilesme", "Beyin Etkisi", "Besinler"])
                with t1:
                    if "deficiency_symptoms" in v:
                        html = ""
                        for s in v["deficiency_symptoms"]:
                            dc = {"high":"#f43f5e","mid":"#f59e0b","low":"#3b82f6"}.get(s["severity"],"#64748b")
                            html += f'''<div class="s-row"><div class="s-dot" style="background:{dc}"></div><div class="s-text">{s["symptom"]}</div><div class="s-sys">{s["system"]}</div></div>'''
                        st.markdown(html, unsafe_allow_html=True)
                with t2:
                    if "recovery_benefits" in v:
                        for b in v["recovery_benefits"]:
                            st.markdown(f'''<div class="r-card"><div class="r-text">{b["benefit"]}</div><div class="r-time">{b["timeline"]}</div></div>''', unsafe_allow_html=True)
                with t3:
                    st.markdown(f'''<div class="brain-box"><div class="brain-title">{v["name"]} ve Beyin</div><div class="brain-text">{v["brain_effect"]}</div></div>''', unsafe_allow_html=True)
                with t4:
                    fh = " ".join([f'''<span class="food-chip">{f}</span>''' for f in v["food_sources"]])
                    st.markdown(fh, unsafe_allow_html=True)

        st.markdown('<div class="sec">Iyilesme Zaman Cizelgesi</div>', unsafe_allow_html=True)
        timeline = get_combined_recovery_timeline(report["deficient"])
        ct = ""
        for item in timeline:
            if item["timeline"] != ct:
                ct = item["timeline"]
                st.markdown(f'''<div class="tl-h">{ct}</div>''', unsafe_allow_html=True)
            st.markdown(f'''<div class="r-card"><div class="r-text"><span style="display:inline-block;width:22px;height:22px;border-radius:6px;background:{item['color']};color:#fff;text-align:center;line-height:22px;font-size:.55rem;font-weight:700;margin-right:8px">{item['letter']}</span>{item["benefit"]}</div><div class="r-time">{item["vitamin"]}</div></div>''', unsafe_allow_html=True)

    # -- Drug Interactions --
    if selected_drugs and report["deficient"]:
        st.markdown('<div class="sec">Ilac-Vitamin Etkilesimleri</div>', unsafe_allow_html=True)
        dn = [v["name"] for v in report["deficient"]]
        inter = check_drug_interactions(dn, selected_drugs)
        if inter["alerts"]:
            for a in inter["alerts"]:
                st.markdown(f'''<div class="a-card {a['severity']}"><div class="a-title">{a['alert']}</div><div class="a-desc">{a['detail']}</div></div>''', unsafe_allow_html=True)
        if inter["detailed"]:
            for d in inter["detailed"]:
                ec = {"critical":"#f43f5e","important":"#f59e0b","moderate":"#3b82f6"}.get(d["effect"],"#64748b")
                st.markdown(f'''
                <div class="v-card" style="border-left:3px solid {ec}">
                    <div class="v-info"><div class="v-name">{d["drug"]}</div><div class="v-range">{d["vitamin"]}</div></div>
                    <div style="flex:2;padding-left:12px"><div style="font-size:.8rem;color:#e2e8f0">{d["description"]}</div><div style="font-size:.75rem;color:#2dd4bf;margin-top:4px">{d["recommendation"]}</div></div>
                </div>''', unsafe_allow_html=True)

    # -- Systems --
    if report["affected_systems"]:
        st.markdown('<div class="sec">Etkilenen Sistemler</div>', unsafe_allow_html=True)
        sg = '<div class="sys-grid">'
        for s in report["affected_systems"]:
            sg += f'''<div class="sys-item"><div class="sys-ico">{s[:2]}</div><div class="sys-name">{s}</div></div>'''
        sg += '</div>'
        st.markdown(sg, unsafe_allow_html=True)

    # -- HEALTH SCORE --
    health_score = max(0, min(100, int(100 - (n_urg * 25 + n_crit * 15 + n_low * 8 + n_bord * 3))))
    if health_score >= 80:
        hs_color, hs_desc = "#22c55e", "Harika! Vitamin dengein oldukca iyi."
    elif health_score >= 60:
        hs_color, hs_desc = "#3b82f6", "Fena degil ama bazi vitaminlere dikkat etmelisin."
    elif health_score >= 40:
        hs_color, hs_desc = "#f59e0b", "Dikkat! Birden fazla eksiklik var."
    else:
        hs_color, hs_desc = "#f43f5e", "Kritik! Acil takviye ve doktor kontrolu gerekli."

    st.markdown(f'''<div class="sec">Saglik Skoru</div>''', unsafe_allow_html=True)
    st.markdown(f'''
    <div class="health-gauge">
        <div class="hg-ring" style="--hg-color:{hs_color};--hg-pct:{health_score}%">
            <div class="hg-inner">
                <div class="hg-num" style="color:{hs_color}">{health_score}</div>
                <div class="hg-label">/ 100</div>
            </div>
        </div>
        <div class="hg-desc">{hs_desc}</div>
    </div>
    ''', unsafe_allow_html=True)

    # -- ACHIEVEMENTS --
    st.markdown('''<div class="sec">Basari Rozetleri</div>''', unsafe_allow_html=True)
    achievements = [
        ("shield", "Tam Koruma", "Tum vitaminler normal", n_def == 0 and n_total >= 5),
        ("muscle", "Demir Savasci", "Demir seviyesi normal", "Demir (Ferritin)" not in [v["name"] for v in report["deficient"]]),
        ("sun", "Gunes Cocugu", "D vitamini normal", "D Vitamini" not in [v["name"] for v in report["deficient"]]),
        ("brain", "Beyin Gucu", "B12 ve Omega-3 tamam", "B12 Vitamini" not in [v["name"] for v in report["deficient"]] and "Omega-3" not in [v["name"] for v in report["deficient"]]),
        ("chart", "Veri Gurusu", "5+ vitamin girdin", n_total >= 5),
        ("target", "Hedef Odakli", "10+ vitamin girdin", n_total >= 10),
        ("heart", "Kalp Dostu", "Magnezyum normal", "Magnezyum" not in [v["name"] for v in report["deficient"]]),
        ("star", "Yildiz Skor", "Saglik skoru 80+", health_score >= 80),
    ]
    badge_icons = {"shield":"🛡️","muscle":"💪","sun":"☀️","brain":"🧠","chart":"📊","target":"🎯","heart":"❤️","star":"⭐"}
    earned_count = sum(1 for a in achievements if a[3])
    badges_html = '<div class="badge-grid">'
    for key, name, desc, earned in achievements:
        cls = "ach-badge earned" if earned else "ach-badge locked"
        badges_html += f'''<div class="{cls}"><div class="ach-ico">{badge_icons[key]}</div><div class="ach-name">{name}</div><div class="ach-desc">{desc}</div></div>'''
    badges_html += '</div>'
    st.markdown(badges_html, unsafe_allow_html=True)
    st.caption(f"{earned_count}/{len(achievements)} rozet kazanildi")

    # -- BODY MAP --
    if report["affected_systems"]:
        ORGAN_MAP = {
            "Sinir Sistemi": {"color": "#8b5cf6", "ico": "🧠"},
            "Kemik": {"color": "#60a5fa", "ico": "🦴"},
            "Kas": {"color": "#f43f5e", "ico": "💪"},
            "Bagisiklik": {"color": "#22c55e", "ico": "🛡️"},
            "Cilt": {"color": "#f59e0b", "ico": "🧴"},
            "Kalp-Damar": {"color": "#ef4444", "ico": "❤️"},
            "Sindirim": {"color": "#2dd4bf", "ico": "🫁"},
            "Enerji Metabolizmasi": {"color": "#fbbf24", "ico": "⚡"},
            "Hormonal": {"color": "#a78bfa", "ico": "🔬"},
            "Kan": {"color": "#dc2626", "ico": "🩸"},
            "Goz": {"color": "#3b82f6", "ico": "👁️"},
            "Tiroid": {"color": "#f97316", "ico": "🦋"},
            "Ruh Hali": {"color": "#c084fc", "ico": "🧘"},
        }
        st.markdown('''<div class="sec">Vucut Haritasi</div>''', unsafe_allow_html=True)

        deficient_names = {v["name"] for v in report["deficient"]}
        body_html = '<div class="body-map"><div class="body-organs">'
        for sys_name in report["affected_systems"]:
            om = ORGAN_MAP.get(sys_name, {"color": "#64748b", "ico": "•"})
            related = [v["letter"] for v in report["deficient"] if sys_name in v.get("affected_systems", [])]
            rel_str = ", ".join(related) if related else ""
            body_html += f'''
            <div class="organ-row">
                <div class="organ-dot" style="background:{om['color']}"></div>
                <span style="font-size:1rem;margin-right:4px">{om['ico']}</span>
                <div>
                    <div class="organ-name">{sys_name}</div>
                    <div class="organ-vitamins">Eksik: {rel_str}</div>
                </div>
            </div>'''
        body_html += '</div></div>'
        st.markdown(body_html, unsafe_allow_html=True)

    # -- CATEGORY DONUT --
    if len(report["results"]) >= 3:
        st.markdown('''<div class="sec">Kategori Dagilimi</div>''', unsafe_allow_html=True)
        cat_counts = {}
        for v in report["results"]:
            cat = v.get("category", "Diger")
            cat_counts[cat] = cat_counts.get(cat, 0) + 1
        status_counts = {"Normal": n_norm, "Sinirda": n_bord, "Dusuk": n_low, "Kritik": n_crit, "Acil": n_urg}
        status_counts = {k: v for k, v in status_counts.items() if v > 0}

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            donut1 = go.Figure(go.Pie(
                labels=list(cat_counts.keys()), values=list(cat_counts.values()),
                hole=0.65, marker=dict(colors=["#8b5cf6","#2dd4bf","#3b82f6","#f59e0b"]),
                textinfo="label+value", textfont=dict(size=11, color="#e2e8f0")
            ))
            donut1.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False, margin=dict(l=10,r=10,t=10,b=10), height=220,
                font=dict(family="Space Grotesk"),
                annotations=[dict(text="Kategori", x=0.5, y=0.5, font_size=11, font_color="#64748b", showarrow=False)]
            )
            st.plotly_chart(donut1, use_container_width=True, config={"displayModeBar": False})
        with col_d2:
            s_colors = {"Normal":"#22c55e","Sinirda":"#3b82f6","Dusuk":"#eab308","Kritik":"#f59e0b","Acil":"#f43f5e"}
            donut2 = go.Figure(go.Pie(
                labels=list(status_counts.keys()), values=list(status_counts.values()),
                hole=0.65, marker=dict(colors=[s_colors.get(k,"#64748b") for k in status_counts]),
                textinfo="label+value", textfont=dict(size=11, color="#e2e8f0")
            ))
            donut2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False, margin=dict(l=10,r=10,t=10,b=10), height=220,
                font=dict(family="Space Grotesk"),
                annotations=[dict(text="Durum", x=0.5, y=0.5, font_size=11, font_color="#64748b", showarrow=False)]
            )
            st.plotly_chart(donut2, use_container_width=True, config={"displayModeBar": False})

    # -- CONFLICT MATRIX --
    if len(report["deficient"]) >= 2:
        deficient_set = {v["name"] for v in report["deficient"]}
        conflicts_found = []
        for (v1, v2), msg in CONFLICT_MATRIX.items():
            if v1 in deficient_set and v2 in deficient_set:
                conflicts_found.append((v1, v2, msg))
        if conflicts_found:
            st.markdown('''<div class="sec">Birlikte Alinmamasi Gerekenler</div>''', unsafe_allow_html=True)
            for v1, v2, msg in conflicts_found:
                i1, i2 = VITAMINS.get(v1, {}), VITAMINS.get(v2, {})
                st.markdown(f'''
                <div class="conf-card">
                    <div class="conf-vs">VS</div>
                    <div>
                        <div class="conf-names">{i1.get('letter','?')} {v1}  &  {i2.get('letter','?')} {v2}</div>
                        <div class="conf-text">{msg}</div>
                    </div>
                </div>''', unsafe_allow_html=True)

    # -- MEAL PLAN --
    if report["deficient"]:
        has_meal = [v for v in report["deficient"] if v["name"] in MEAL_PLANS]
        if has_meal:
            st.markdown('''<div class="sec">Haftalik Yemek Onerisi</div>''', unsafe_allow_html=True)
            for v in has_meal[:3]:
                plan = MEAL_PLANS[v["name"]]
                info = VITAMINS.get(v["name"], {})
                st.markdown(f'''<div class="meal-vit-title"><span class="meal-vit-dot" style="background:{info.get('color','#8b5cf6')}">{info.get('letter','?')}</span>{v["name"]}</div>''', unsafe_allow_html=True)
                grid_h = '<div class="meal-grid">'
                for day in plan:
                    grid_h += f'''<div class="meal-day"><div class="meal-day-name">{day["gun"]}</div><div class="meal-food">{day["ogun"]}</div></div>'''
                grid_h += '</div>'
                st.markdown(grid_h, unsafe_allow_html=True)

    # -- COST ESTIMATE --
    if report["deficient"]:
        st.markdown('''<div class="sec">Tahmini Aylik Maliyet</div>''', unsafe_allow_html=True)
        total_min, total_max = 0, 0
        cost_html = '<div class="cost-wrap">'
        for v in report["deficient"]:
            cost = SUPPLEMENT_COSTS.get(v["name"])
            if cost and cost["max"] > 0:
                total_min += cost["min"]
                total_max += cost["max"]
                cost_html += f'''
                <div class="cost-card">
                    <div class="cost-icon" style="background:{v['color']}">{v['letter']}</div>
                    <div class="cost-info">
                        <div class="cost-name">{v['name']}</div>
                        <div class="cost-range">{cost['min']} - {cost['max']} TL</div>
                    </div>
                </div>'''
        cost_html += '</div>'
        st.markdown(cost_html, unsafe_allow_html=True)

        if total_max > 0:
            st.markdown(f'''
            <div class="cost-total">
                <div class="cost-total-lbl">Tahmini Aylik Toplam</div>
                <div class="cost-total-val">{total_min} - {total_max} TL</div>
            </div>
            ''', unsafe_allow_html=True)

    # -- SEASONAL TIPS --
    month = datetime.now().month
    if month in (12, 1, 2):
        season_cls, season_name = "winter", "Kis"
        season_tips = [
            "D vitamini uretimi azalir, takviye zorunlu hale gelir.",
            "Soguk alginligina karsi C vitamini ve Cinko dozunu artirmayi dusun.",
            "Kisa gunlerde melatonin uretimi etkilenir, Magnezyum uyku kalitesine yardimci olur.",
        ]
    elif month in (3, 4, 5):
        season_cls, season_name = "spring", "Ilkbahar"
        season_tips = [
            "Kis boyunca biriken eksiklikleri kontrol etmek icin ideal zaman.",
            "Alerji sezonunda C vitamini dogal antihistaminik etkisi gosterir.",
            "Gunes isigi artiyor, D vitamini uretimi yeniden basliyor.",
        ]
    elif month in (6, 7, 8):
        season_cls, season_name = "summer", "Yaz"
        season_tips = [
            "Terle mineral kaybi artar, Magnezyum ve Cinko takviyesine dikkat.",
            "Gunes isigi bol, D vitamini icin 15-20dk guneslenme yeterli.",
            "Sicakta B grubu vitaminler enerji metabolizmasini destekler.",
        ]
    else:
        season_cls, season_name = "autumn", "Sonbahar"
        season_tips = [
            "Kis oncesi D vitamini depolarini doldurmak icin son sans.",
            "Bagisiklik icin Cinko, C vitamini ve Selenyum takviyesi baslat.",
            "Gun isigi kisaliyor, ruh hali icin Omega-3 destegi dusun.",
        ]

    st.markdown(f'''<div class="sec">{season_name} Mevsim Onerileri</div>''', unsafe_allow_html=True)
    for tip in season_tips:
        st.markdown(f'''
        <div class="season-card {season_cls}">
            <div class="season-text">{tip}</div>
        </div>''', unsafe_allow_html=True)

    # -- HISTORY --
    if "history" not in st.session_state:
        st.session_state.history = []

    current = {"date": datetime.now().strftime("%d.%m.%Y %H:%M"), "score": health_score, "deficient": n_def, "total": n_total}

    if st.session_state.history:
        last = st.session_state.history[-1]
        if last["score"] != health_score or last["deficient"] != n_def:
            st.session_state.history.append(current)
    else:
        st.session_state.history.append(current)

    if len(st.session_state.history) >= 2:
        st.markdown('''<div class="sec">Onceki Analizle Karsilastirma</div>''', unsafe_allow_html=True)
        prev = st.session_state.history[-2]
        score_diff = health_score - prev["score"]
        def_diff = n_def - prev["deficient"]
        sc_color = "#22c55e" if score_diff >= 0 else "#f43f5e"
        dc_color = "#22c55e" if def_diff <= 0 else "#f43f5e"
        sc_arrow = "+" if score_diff > 0 else ""
        dc_arrow = "+" if def_diff > 0 else ""

        st.markdown(f'''
        <div class="hist-grid">
            <div class="hist-card">
                <div class="hist-label">Saglik Skoru</div>
                <div class="hist-val" style="color:{sc_color}">{health_score}</div>
                <div class="hist-change" style="color:{sc_color}">{sc_arrow}{score_diff} oncekine gore</div>
            </div>
            <div class="hist-card">
                <div class="hist-label">Eksik Vitamin</div>
                <div class="hist-val" style="color:{dc_color}">{n_def}</div>
                <div class="hist-change" style="color:{dc_color}">{dc_arrow}{def_diff} oncekine gore</div>
            </div>
        </div>
        <div style="font-size:.65rem;color:#334155;text-align:center;margin-top:.3rem">Onceki analiz: {prev["date"]}</div>
        ''', unsafe_allow_html=True)

    st.markdown('''<div class="disc">Bu uygulama bilgilendirme amaclidir, tibbi tavsiye yerine gecmez. Vitamin takviyeleri ve ilac degisiklikleri icin mutlaka doktorunuza danisin.</div>''', unsafe_allow_html=True)

    # -- TR COMPARISON --
    tr_cards = []
    for v in report["results"]:
        tr = TR_AVERAGES.get(v["name"])
        if tr:
            tr_cards.append((v, tr))
    if tr_cards:
        st.markdown('''<div class="sec">Turkiye Karsilastirmasi</div>''', unsafe_allow_html=True)
        for v, tr in tr_cards:
            avg = tr["avg"]
            val = v["value"]
            max_val = max(avg * 2, v["max_normal"])
            val_pct = min((val / max_val) * 100, 100) if max_val > 0 else 50
            avg_pct = min((avg / max_val) * 100, 100) if max_val > 0 else 50
            if val < avg * 0.7:
                rank_color, rank_text = "#f43f5e", "Dusuk"
            elif val < avg:
                rank_color, rank_text = "#f59e0b", "Ort. Alti"
            elif val < avg * 1.3:
                rank_color, rank_text = "#3b82f6", "Ort."
            else:
                rank_color, rank_text = "#22c55e", "Ort. Ustu"
            st.markdown(f'''
            <div class="tr-card">
                <div class="tr-rank" style="border-color:{rank_color}">
                    <div class="tr-rank-num" style="color:{rank_color}">{rank_text}</div>
                </div>
                <div class="tr-info">
                    <div class="tr-name">{v['letter']} {v['name']}: {val} {v['unit']}</div>
                    <div class="tr-bar-wrap">
                        <div class="tr-bar" style="width:{val_pct}%;background:{rank_color}"></div>
                        <div class="tr-avg-line" style="left:{avg_pct}%"></div>
                    </div>
                    <div class="tr-note">TR ortalama: {avg} {tr['unit']} | Eksiklik orani: %{tr['low_pct']} | {tr['note']}</div>
                </div>
            </div>''', unsafe_allow_html=True)

    # -- FOOD PORTIONS --
    if report["deficient"]:
        has_fp = [v for v in report["deficient"] if v["name"] in FOOD_PORTIONS]
        if has_fp:
            st.markdown('''<div class="sec">Besin Porsiyon Tablosu</div>''', unsafe_allow_html=True)
            st.caption("Gunluk ihtiyacini karsilamak icin ne kadar yemelisin:")
            for v in has_fp[:4]:
                portions = FOOD_PORTIONS[v["name"]]
                info = VITAMINS.get(v["name"], {})
                st.markdown(f'''<div class="meal-vit-title"><span class="meal-vit-dot" style="background:{info.get('color','#8b5cf6')}">{info.get('letter','?')}</span>{v["name"]}</div>''', unsafe_allow_html=True)
                fp_html = '<div class="fp-grid">'
                for p in portions:
                    fp_html += f'''
                    <div class="fp-card">
                        <div class="fp-food">{p["food"]}</div>
                        <div class="fp-portion">{p["portion"]} = {p["amount"]}</div>
                        <div class="fp-pct-wrap"><div class="fp-pct-bar" style="width:{p['pct']}%"></div></div>
                        <div class="fp-pct-label">%{p["pct"]} gunluk</div>
                    </div>'''
                fp_html += '</div>'
                st.markdown(fp_html, unsafe_allow_html=True)

    # -- SHARE --
    st.markdown('''<div class="sec">Sonuclarini Paylas</div>''', unsafe_allow_html=True)
    share_lines = [f"VitaPredict Analiz Sonucum", f"Saglik Skoru: {health_score}/100", f"Toplam: {n_total} vitamin girildi"]
    if n_urg > 0:
        share_lines.append(f"Acil: {n_urg}")
    if n_crit > 0:
        share_lines.append(f"Kritik: {n_crit}")
    if n_low > 0:
        share_lines.append(f"Dusuk: {n_low}")
    if n_bord > 0:
        share_lines.append(f"Sinirda: {n_bord}")
    share_lines.append(f"Normal: {n_norm}")
    if report["deficient"]:
        eksik_names = ", ".join([v["letter"] + " " + v["name"] for v in report["deficient"][:5]])
        share_lines.append(f"Eksikler: {eksik_names}")
    share_text = "\n".join(share_lines)
    st.markdown(f'<div class="share-box">{share_text}</div>', unsafe_allow_html=True)
    st.code(share_text, language=None)

    # -- SIMULATION --
    if report["deficient"]:
        has_sim = [v for v in report["deficient"] if v["name"] in SIMULATION]
        if has_sim:
            st.markdown('''<div class="sec">Oncesi / Sonrasi Simulasyonu</div>''', unsafe_allow_html=True)
            st.caption("Takviye alirsan zaman icinde neler degisir:")
            for v in has_sim[:3]:
                sim = SIMULATION[v["name"]]
                info = VITAMINS.get(v["name"], {})
                st.markdown(f'''<div class="meal-vit-title"><span class="meal-vit-dot" style="background:{info.get('color','#8b5cf6')}">{info.get('letter','?')}</span>{v["name"]}</div>''', unsafe_allow_html=True)
                sim_html = '<div class="sim-timeline">'
                periods = [("1 Ay", sim.get("1_ay", []), "#3b82f6"), ("3 Ay", sim.get("3_ay", []), "#8b5cf6"), ("6 Ay", sim.get("6_ay", []), "#22c55e")]
                for label, items, color in periods:
                    sim_html += f'<div class="sim-period"><div class="sim-dot" style="background:{color}"></div><div class="sim-label" style="color:{color}">{label}</div><div class="sim-items">'
                    for it in items:
                        sim_html += f'<div class="sim-item">{it}</div>'
                    sim_html += '</div></div>'
                sim_html += '</div>'
                st.markdown(sim_html, unsafe_allow_html=True)

    # -- BRAND RECOMMENDATIONS --
    if report["deficient"]:
        has_brand = [v for v in report["deficient"] if v["name"] in TR_BRANDS]
        if has_brand:
            st.markdown('''<div class="sec">Turkiye Takviye Onerileri</div>''', unsafe_allow_html=True)
            st.caption("Eczane ve online satin alma icin populer markalar:")
            for v in has_brand:
                br = TR_BRANDS[v["name"]]
                info = VITAMINS.get(v["name"], {})
                pills = ''.join([f'<span class="brand-pill">{b}</span>' for b in br["brands"]])
                st.markdown(f'''
                <div class="brand-card">
                    <div class="brand-header">
                        <div class="enc-dot" style="background:{info.get('color','#8b5cf6')};width:28px;height:28px;font-size:.5rem">{info.get('letter','?')}</div>
                        <div class="brand-name">{v["name"]}</div>
                    </div>
                    <div class="brand-list">{pills}</div>
                    <div class="brand-tip">{br["tip"]}</div>
                </div>''', unsafe_allow_html=True)

    # -- PDF DOWNLOAD --
    st.markdown('<div class="sec">Raporu Indir</div>', unsafe_allow_html=True)
    profile_data = None
    if has_profile:
        profile_data = {"age": age if age > 0 else None, "gender": gender, "lifestyle": lifestyle}
    pdf_bytes = generate_pdf(report, profile=profile_data)
    st.download_button(
        label="PDF Rapor Indir",
        data=pdf_bytes,
        file_name="vitapredict_rapor.pdf",
        mime="application/pdf",
        use_container_width=True,
        type="primary"
    )
