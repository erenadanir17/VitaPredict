from data.vitamins import VITAMINS
from data.drugs import PSYCH_DRUGS, INTERACTION_ALERTS


def analyze_vitamin(name, value):
    info = VITAMINS.get(name)
    if not info:
        return None
    min_n = info["min_normal"]
    max_n = info["max_normal"]

    if name == "Iyot (TSH)":
        if value > max_n:
            ratio = (value - max_n) / max_n
            if ratio > 0.5:
                status, status_label = "urgent", "ACIL MUDAHALE"
            elif ratio > 0.25:
                status, status_label = "critical", "KRITIK"
            else:
                status, status_label = "deficient", "YUKSEK"
            severity_score = min(ratio * 100, 100)
        elif value < min_n:
            status, status_label = "deficient", "DUSUK TSH"
            severity_score = 30
        else:
            status, status_label = "normal", "NORMAL"
            severity_score = 0
    else:
        range_span = max_n - min_n
        borderline_threshold = min_n + range_span * 0.15

        if value >= min_n and value <= max_n:
            if value <= borderline_threshold:
                status, status_label = "borderline", "SINIRDA"
                severity_score = 15
            else:
                status, status_label = "normal", "NORMAL"
                severity_score = 0
        elif value > max_n:
            status, status_label = "excess", "YUKSEK"
            severity_score = min((value - max_n) / max_n * 100, 80)
        else:
            deficit_pct = (min_n - value) / min_n * 100
            if deficit_pct >= 70:
                status, status_label = "urgent", "ACIL MUDAHALE"
                severity_score = 100
            elif deficit_pct >= 40:
                status, status_label = "critical", "KRITIK"
                severity_score = 75
            else:
                status, status_label = "deficient", "DUSUK"
                severity_score = 40

    # Progress: 0 = no value, 100 = at min_normal, >100 = above min
    if min_n > 0:
        progress = min(value / min_n * 100, 150)
    else:
        progress = 100

    result = {
        "name": name, "letter": info["letter"], "color": info["color"],
        "value": value, "unit": info["unit"],
        "min_normal": min_n, "max_normal": max_n,
        "status": status, "status_label": status_label,
        "severity_score": round(severity_score, 1),
        "progress": round(progress, 1),
        "category": info["category"],
        "group": info.get("group", "other"),
        "affected_systems": info["affected_systems"],
        "brain_effect": info["brain_effect"],
        "food_sources": info["food_sources"],
        "supplement": info.get("supplement", {}),
        "synergies": info.get("synergies", []),
    }
    if status in ("urgent", "critical", "deficient", "borderline"):
        result["deficiency_symptoms"] = info["deficiency_symptoms"]
        result["recovery_benefits"] = info["recovery_benefits"]
    return result


def analyze_all(user_values):
    results = []
    deficient_vitamins = []
    normal_vitamins = []
    for name, value in user_values.items():
        if value is None:
            continue
        r = analyze_vitamin(name, value)
        if r:
            results.append(r)
            if r["status"] in ("urgent", "critical", "deficient"):
                deficient_vitamins.append(r)
            elif r["status"] == "borderline":
                deficient_vitamins.append(r)
            else:
                normal_vitamins.append(r)

    n_urgent = sum(1 for v in deficient_vitamins if v["status"] == "urgent")
    n_critical = sum(1 for v in deficient_vitamins if v["status"] == "critical")
    n_low = sum(1 for v in deficient_vitamins if v["status"] == "deficient")
    n_borderline = sum(1 for v in deficient_vitamins if v["status"] == "borderline")

    affected = set()
    for v in deficient_vitamins:
        affected.update(v["affected_systems"])

    # Summary text
    summary = _build_summary(deficient_vitamins, normal_vitamins, n_urgent, n_critical, n_low)

    # Synergy recommendations
    synergy_recs = _find_synergies(deficient_vitamins)

    # Chart data
    chart_data = []
    for r in results:
        chart_data.append({
            "name": r["name"], "letter": r["letter"], "color": r["color"],
            "value": r["value"], "min_normal": r["min_normal"],
            "max_normal": r["max_normal"], "progress": r["progress"],
            "status": r["status"],
        })

    return {
        "results": results,
        "deficient": deficient_vitamins,
        "normal": normal_vitamins,
        "affected_systems": list(affected),
        "count_total": len(results),
        "count_deficient": len(deficient_vitamins),
        "count_normal": len(normal_vitamins),
        "count_urgent": n_urgent,
        "count_critical": n_critical,
        "count_low": n_low,
        "count_borderline": n_borderline,
        "summary": summary,
        "synergy_recs": synergy_recs,
        "chart_data": chart_data,
    }


def _build_summary(deficient, normal, n_urg, n_crit, n_low):
    total = len(deficient) + len(normal)
    if not deficient:
        return f"Tebrikler! Girdigin {total} vitaminin tamami normal aralikta."
    n_border = sum(1 for v in deficient if v["status"] == "borderline")
    if n_border > 0:
        names = [v["name"] for v in deficient if v["status"] == "borderline"]
        parts_extra = [f"{n_border} vitaminin sinirda ({', '.join(names)}) - hafif takviye onerililr"]
    else:
        parts_extra = []

    parts = []
    if n_urg > 0:
        names = [v["name"] for v in deficient if v["status"] == "urgent"]
        parts.append(f"{n_urg} vitaminin acil mudahale gerektiriyor ({', '.join(names)})")
    if n_crit > 0:
        names = [v["name"] for v in deficient if v["status"] == "critical"]
        parts.append(f"{n_crit} vitaminin kritik seviyede ({', '.join(names)})")
    if n_low > 0:
        names = [v["name"] for v in deficient if v["status"] == "deficient"]
        parts.append(f"{n_low} vitaminin normalin altinda ({', '.join(names)})")

    worst = max(deficient, key=lambda x: x["severity_score"])

    text = f"{total} vitamin girdin. " + ". ".join(parts) + "."
    text += f" Oncelik: {worst['name']} en kritik durumda."

    all_systems = set()
    for v in deficient:
        all_systems.update(v["affected_systems"])
    if all_systems:
        text += f" Etkilenen sistemler: {', '.join(list(all_systems)[:5])}."

    return text


def _find_synergies(deficient):
    recs = []
    deficient_names = {v["name"] for v in deficient}
    seen = set()

    for v in deficient:
        for syn in v.get("synergies", []):
            pair = tuple(sorted([v["name"], syn]))
            if pair in seen:
                continue
            seen.add(pair)

            syn_info = VITAMINS.get(syn, {})
            syn_letter = syn_info.get("letter", "?")
            syn_color = syn_info.get("color", "#888")

            if syn in deficient_names:
                urgency = "high"
                note = f"Ikisi de eksik! Birlikte takviye sart."
            else:
                urgency = "info"
                note = f"{v['name']} emilimi icin {syn} gerekli."

            recs.append({
                "vit1": v["name"], "letter1": v["letter"], "color1": v["color"],
                "vit2": syn, "letter2": syn_letter, "color2": syn_color,
                "urgency": urgency, "note": note,
            })

    recs.sort(key=lambda x: 0 if x["urgency"] == "high" else 1)
    return recs


def check_drug_interactions(deficient_names, selected_drugs):
    alerts = []
    for a in INTERACTION_ALERTS:
        if a["drug_class"] in selected_drugs:
            matching = [v for v in a["condition"] if v in deficient_names]
            if matching:
                alerts.append({"alert": a["alert"], "detail": a["detail"], "severity": a["severity"], "vitamins": matching, "drug": a["drug_class"]})
    detailed = []
    for drug_name in selected_drugs:
        drug_info = PSYCH_DRUGS.get(drug_name)
        if not drug_info:
            continue
        for inter in drug_info["vitamin_interactions"]:
            if inter["vitamin"] in deficient_names:
                detailed.append({"drug": drug_name, "vitamin": inter["vitamin"], "effect": inter["effect"], "description": inter["description"], "recommendation": inter["recommendation"]})
    return {"alerts": alerts, "detailed": detailed}


def get_combined_recovery_timeline(deficient_vitamins):
    timeline = []
    seen = set()
    for v in deficient_vitamins:
        if "recovery_benefits" not in v:
            continue
        for b in v["recovery_benefits"]:
            key = b["benefit"]
            if key not in seen:
                seen.add(key)
                timeline.append({"vitamin": v["name"], "letter": v["letter"], "color": v["color"], "benefit": b["benefit"], "timeline": b["timeline"], "system": b["system"]})
    order = {"1-2 hafta": 1, "2-4 hafta": 2, "4-6 hafta": 3, "4-8 hafta": 4, "6-8 hafta": 5, "4-12 hafta": 6, "6-12 hafta": 7, "8-12 hafta": 8, "2-3 ay": 9, "2-4 ay": 10, "3-6 ay": 11}
    timeline.sort(key=lambda x: order.get(x["timeline"], 99))
    return timeline
