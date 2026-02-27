def get_main_css():
    return """<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

:root{
    --bg:#050510;--surface:#0a0a1a;--surface2:#0f0f24;
    --border:rgba(139,92,246,0.08);--border-h:rgba(139,92,246,0.2);
    --text:#e2e8f0;--text2:#64748b;--text3:#334155;
    --purple:#8b5cf6;--purple-g:rgba(139,92,246,0.08);
    --teal:#2dd4bf;--teal-g:rgba(45,212,191,0.08);
    --red:#f43f5e;--orange:#f59e0b;--yellow:#eab308;--green:#22c55e;
    --blue:#3b82f6;
    --glow-purple:0 0 20px rgba(139,92,246,0.15);
    --glow-teal:0 0 20px rgba(45,212,191,0.12);
}

*{font-family:'Space Grotesk',sans-serif;box-sizing:border-box}

/* -- NUKE ALL STREAMLIT UI -- */
header[data-testid="stHeader"]{display:none !important;height:0 !important;min-height:0 !important}
#MainMenu,footer,div[data-testid="stToolbar"],div[data-testid="stDecoration"],
.stDeployButton,div[data-testid="stStatusWidget"],div[data-testid="manage-app-button"],
.viewerBadge_container__r5tak,.stActionButton,[data-testid="baseButton-header"]{display:none !important}
div[data-testid="stSidebarCollapsedControl"]{top:0.5rem !important}
.block-container{padding-top:1rem !important}

.stApp{background:var(--bg)}
section[data-testid="stSidebar"]{background:var(--surface);border-right:1px solid var(--border)}
section[data-testid="stSidebar"] > div{padding-top:1rem}
h1,h2,h3,h4{color:var(--text) !important}
p,li,span,label,div{color:var(--text2)}
hr{border-color:var(--border) !important}

/* -- HERO with animated gradient border -- */
.hero{
    background:var(--surface);position:relative;
    border-radius:24px;padding:2.5rem 2rem;text-align:center;margin-bottom:1.5rem;
    border:1px solid var(--border);overflow:hidden
}
.hero::before{
    content:'';position:absolute;inset:-1px;border-radius:24px;padding:1px;
    background:linear-gradient(135deg,var(--purple),var(--teal),var(--purple));
    -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
    -webkit-mask-composite:xor;mask-composite:exclude;
    animation:borderGlow 4s linear infinite;background-size:300% 300%
}
@keyframes borderGlow{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.hero h1{font-size:2.5rem;font-weight:700;color:#fff !important;margin:0;position:relative;letter-spacing:-1px}
.hero h1 span{background:linear-gradient(135deg,var(--purple),var(--teal));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero .sub{color:var(--text2) !important;font-size:.9rem;margin-top:.4rem;position:relative}
.hero .badge-count{
    display:inline-flex;gap:12px;align-items:center;
    background:var(--purple-g);backdrop-filter:blur(10px);
    padding:8px 20px;border-radius:100px;font-size:.75rem;color:var(--purple);
    margin-top:1rem;position:relative;border:1px solid rgba(139,92,246,0.15);
    font-family:'JetBrains Mono',monospace;font-weight:700
}
.hero .badge-count .sep{width:1px;height:14px;background:rgba(139,92,246,0.2)}

/* -- Welcome Steps -- */
.welcome-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:1.5rem 0}
.w-card{
    background:var(--surface);border:1px solid var(--border);
    border-radius:20px;padding:1.8rem 1.4rem;position:relative;overflow:hidden;transition:all .3s
}
.w-card:hover{border-color:var(--border-h);transform:translateY(-3px);box-shadow:var(--glow-purple)}
.w-card .accent{position:absolute;top:0;left:0;width:3px;height:100%;border-radius:0 3px 3px 0}
.w-card .num{font-family:'JetBrains Mono',monospace;font-size:2.5rem;font-weight:700;color:var(--text3);margin-bottom:.3rem}
.w-card .title{font-size:.95rem;font-weight:600;color:var(--text)}
.w-card .desc{font-size:.75rem;color:var(--text2);margin-top:.3rem;line-height:1.5}

/* -- Feature Pills -- */
.feat-row{display:flex;gap:10px;margin:1.5rem 0;flex-wrap:wrap}
.feat{
    flex:1;min-width:120px;
    background:var(--surface);border:1px solid var(--border);
    border-radius:14px;padding:1rem;text-align:center;transition:all .2s
}
.feat:hover{border-color:var(--border-h)}
.feat .ico{font-size:1.3rem;margin-bottom:.3rem}
.feat .ft{font-size:.78rem;font-weight:600;color:var(--text)}
.feat .fd{font-size:.65rem;color:var(--text3);margin-top:.15rem}

/* -- Vitamin Grid (welcome) -- */
.vit-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px;margin:1rem 0}
.vit-item{
    background:var(--surface);border:1px solid var(--border);
    border-radius:12px;padding:.6rem .8rem;display:flex;align-items:center;gap:8px;transition:all .2s
}
.vit-item:hover{border-color:var(--border-h);box-shadow:var(--glow-purple)}
.vit-dot{width:30px;height:30px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.6rem;color:#fff;flex-shrink:0}
.vit-label{font-size:.7rem;color:var(--text2);line-height:1.2}

/* -- Profile Card -- */
.prof-card{
    background:var(--surface);border:1px solid var(--border);border-radius:20px;padding:1.2rem 1.5rem;margin:1rem 0;
    position:relative;overflow:hidden
}
.prof-card::before{
    content:'';position:absolute;top:0;left:0;width:100%;height:3px;
    background:linear-gradient(90deg,var(--purple),var(--teal))
}
.prof-title{font-size:.85rem;font-weight:600;color:var(--purple);margin-bottom:.6rem;text-transform:uppercase;letter-spacing:1px;font-family:'JetBrains Mono',monospace}
.prof-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.prof-item{background:var(--purple-g);border-radius:12px;padding:.7rem;text-align:center}
.prof-val{font-size:1rem;font-weight:700;color:var(--text)}
.prof-lbl{font-size:.6rem;color:var(--text2);margin-top:2px;text-transform:uppercase;letter-spacing:.5px}

/* -- Score Gauge (unique ring) -- */
.score-wrap{text-align:center;padding:1rem 0}
.score-ring{
    width:160px;height:160px;border-radius:50%;display:inline-flex;align-items:center;
    justify-content:center;flex-direction:column;position:relative
}
.score-ring::before{
    content:'';position:absolute;inset:-3px;border-radius:50%;
    background:conic-gradient(var(--ring-color) var(--ring-pct), rgba(255,255,255,0.03) 0);
    -webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 4px),#fff calc(100% - 3px));
    mask:radial-gradient(farthest-side,transparent calc(100% - 4px),#fff calc(100% - 3px))
}
.score-ring::after{
    content:'';position:absolute;inset:0;border-radius:50%;background:var(--surface);
    box-shadow:inset 0 0 30px rgba(0,0,0,0.5)
}
.score-inner{position:relative;z-index:1}
.score-num{font-family:'JetBrains Mono',monospace;font-size:3rem;font-weight:700;color:#fff;line-height:1}
.score-lbl{font-size:.65rem;color:var(--text2);margin-top:2px;text-transform:uppercase;letter-spacing:1.5px}

/* -- Metrics -- */
.metrics{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin:1rem 0}
.m-box{
    background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:.8rem .5rem;text-align:center;
    position:relative;overflow:hidden
}
.m-box::before{content:'';position:absolute;bottom:0;left:0;width:100%;height:2px}
.m-box.red::before{background:var(--red)}.m-box.orange::before{background:var(--orange)}
.m-box.yellow::before{background:var(--yellow)}.m-box.green::before{background:var(--green)}
.m-box.blue::before{background:var(--blue)}
.m-num{font-family:'JetBrains Mono',monospace;font-size:1.6rem;font-weight:700}
.m-lbl{font-size:.6rem;color:var(--text3);margin-top:2px;text-transform:uppercase;letter-spacing:.5px}

/* -- Summary Banner -- */
.summary-box{
    background:var(--surface);border:1px solid var(--border);border-radius:16px;
    padding:1rem 1.2rem;margin:.8rem 0;position:relative;overflow:hidden
}
.summary-box::before{content:'';position:absolute;top:0;left:0;width:3px;height:100%;background:var(--purple)}
.summary-text{font-size:.82rem;color:var(--text2);line-height:1.7}

/* -- Vitamin Cards -- */
.v-card{
    background:var(--surface);border:1px solid var(--border);
    border-radius:16px;padding:1rem 1.2rem;margin:8px 0;display:flex;align-items:center;gap:14px;
    transition:all .25s;position:relative;overflow:hidden
}
.v-card:hover{border-color:var(--border-h);box-shadow:var(--glow-purple)}
.v-card .accent-left{position:absolute;left:0;top:0;width:3px;height:100%}
.v-icon{width:42px;height:42px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.7rem;color:#fff;flex-shrink:0;box-shadow:0 4px 12px rgba(0,0,0,0.3)}
.v-info{flex:1;min-width:0}
.v-name{font-size:.9rem;font-weight:600;color:var(--text)}
.v-range{font-size:.65rem;color:var(--text3);margin-top:1px;font-family:'JetBrains Mono',monospace}
.v-right{text-align:right;flex-shrink:0}
.v-val{font-size:1.05rem;font-weight:700;font-family:'JetBrains Mono',monospace}
.v-badge{display:inline-block;padding:3px 10px;border-radius:100px;font-size:.6rem;font-weight:700;letter-spacing:.5px;margin-top:3px}
.badge-urgent{background:rgba(244,63,94,0.1);color:var(--red);border:1px solid rgba(244,63,94,0.15)}
.badge-critical{background:rgba(245,158,11,0.08);color:var(--orange);border:1px solid rgba(245,158,11,0.12)}
.badge-deficient{background:rgba(234,179,8,0.08);color:var(--yellow);border:1px solid rgba(234,179,8,0.12)}
.badge-borderline{background:rgba(59,130,246,0.08);color:var(--blue);border:1px solid rgba(59,130,246,0.12)}
.badge-normal{background:rgba(34,197,94,0.08);color:var(--green);border:1px solid rgba(34,197,94,0.12)}

/* -- Progress Bar -- */
.pbar-wrap{width:100%;height:4px;background:rgba(255,255,255,0.04);border-radius:2px;margin-top:6px;overflow:hidden}
.pbar{height:100%;border-radius:2px;transition:width .6s ease;position:relative}
.pbar::after{content:'';position:absolute;right:0;top:-1px;width:6px;height:6px;border-radius:50%;background:inherit;box-shadow:0 0 6px currentColor}

/* -- Supplement Cards -- */
.supp-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:1rem 0}
.supp-card{
    background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:1rem 1.2rem;
    transition:all .2s;position:relative;overflow:hidden
}
.supp-card:hover{border-color:var(--border-h)}
.supp-card::before{content:'';position:absolute;top:0;left:0;width:100%;height:2px}
.supp-header{display:flex;align-items:center;gap:10px;margin-bottom:.6rem}
.supp-dot{width:32px;height:32px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.6rem;color:#fff;flex-shrink:0}
.supp-name{font-size:.85rem;font-weight:600;color:var(--text)}
.supp-status{font-size:.58rem;font-weight:700;padding:3px 8px;border-radius:100px;letter-spacing:.5px}
.supp-row{display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid var(--border)}
.supp-label{font-size:.7rem;color:var(--text3);font-family:'JetBrains Mono',monospace}
.supp-value{font-size:.72rem;color:var(--text);font-weight:500}
.supp-note{font-size:.68rem;color:var(--teal);margin-top:8px;padding:6px 10px;background:var(--teal-g);border-radius:8px;border:1px solid rgba(45,212,191,0.1)}

/* -- Personal Alerts -- */
.p-alert{
    background:var(--surface);border:1px solid rgba(139,92,246,0.1);
    border-radius:14px;padding:.8rem 1rem;margin:6px 0;display:flex;align-items:flex-start;gap:10px;
    transition:all .2s
}
.p-alert:hover{border-color:var(--border-h)}
.p-alert-ico{
    width:28px;height:28px;border-radius:8px;background:var(--purple-g);
    display:flex;align-items:center;justify-content:center;
    font-size:.7rem;font-weight:700;color:var(--purple);flex-shrink:0;
    font-family:'JetBrains Mono',monospace;border:1px solid rgba(139,92,246,0.15)
}
.p-alert-text{font-size:.78rem;color:var(--text2);line-height:1.5}
.p-alert-text strong{color:var(--teal)}

/* -- Synergy Cards -- */
.syn-card{
    background:var(--surface);border:1px solid var(--border);
    border-radius:14px;padding:.8rem 1rem;margin:6px 0
}
.syn-title{font-size:.78rem;font-weight:600;color:var(--purple);margin-bottom:6px;font-family:'JetBrains Mono',monospace}
.syn-chips{display:flex;flex-wrap:wrap;gap:5px}
.syn-chip{padding:4px 10px;border-radius:100px;font-size:.65rem;font-weight:600;font-family:'JetBrains Mono',monospace}
.syn-chip.missing{background:rgba(244,63,94,0.06);border:1px solid rgba(244,63,94,0.12);color:var(--red)}
.syn-chip.ok{background:rgba(34,197,94,0.06);border:1px solid rgba(34,197,94,0.12);color:var(--green)}
.syn-chip{background:var(--purple-g);border:1px solid rgba(139,92,246,0.12);color:var(--purple)}

/* -- Recovery Cards -- */
.r-card{
    background:var(--surface);border:1px solid rgba(45,212,191,0.08);
    border-radius:14px;padding:.7rem 1rem;margin:5px 0;display:flex;justify-content:space-between;align-items:center
}
.r-text{font-size:.82rem;color:var(--text);font-weight:500}
.r-time{
    background:var(--teal-g);color:var(--teal);padding:4px 12px;border-radius:100px;
    font-size:.65rem;font-weight:700;white-space:nowrap;
    font-family:'JetBrains Mono',monospace;border:1px solid rgba(45,212,191,0.1)
}

/* -- Alert Cards -- */
.a-card{border-radius:14px;padding:1rem 1.2rem;margin:6px 0;position:relative;overflow:hidden}
.a-card::before{content:'';position:absolute;left:0;top:0;width:3px;height:100%}
.a-card.critical{background:rgba(244,63,94,0.04);border:1px solid rgba(244,63,94,0.1)}.a-card.critical::before{background:var(--red)}
.a-card.important{background:rgba(245,158,11,0.04);border:1px solid rgba(245,158,11,0.1)}.a-card.important::before{background:var(--orange)}
.a-card.moderate{background:rgba(59,130,246,0.04);border:1px solid rgba(59,130,246,0.1)}.a-card.moderate::before{background:var(--blue)}
.a-title{font-size:.85rem;font-weight:600;color:var(--text);margin-bottom:3px}
.a-desc{font-size:.75rem;color:var(--text2);line-height:1.5}

/* -- Brain Box -- */
.brain-box{
    background:var(--surface);border:1px solid rgba(139,92,246,0.1);border-radius:14px;
    padding:1rem 1.2rem;margin:6px 0;position:relative;overflow:hidden
}
.brain-box::before{content:'';position:absolute;top:0;left:0;width:100%;height:2px;background:linear-gradient(90deg,var(--purple),transparent)}
.brain-title{font-weight:600;color:var(--purple);font-size:.85rem;margin-bottom:4px}
.brain-text{font-size:.8rem;color:var(--text2);line-height:1.6}

/* -- Food Chips -- */
.food-chip{
    display:inline-block;background:var(--surface);border:1px solid var(--border);
    padding:5px 12px;border-radius:100px;font-size:.72rem;margin:2px;color:var(--text);
    transition:all .2s
}
.food-chip:hover{border-color:var(--border-h);color:var(--teal)}

/* -- Symptoms -- */
.s-dot{width:6px;height:6px;border-radius:50%;display:inline-block;margin-right:8px;flex-shrink:0}
.s-row{display:flex;align-items:center;padding:6px 0;border-bottom:1px solid var(--border)}
.s-text{font-size:.8rem;color:var(--text)}
.s-sys{font-size:.62rem;color:var(--text3);margin-left:auto;padding-left:8px;white-space:nowrap;font-family:'JetBrains Mono',monospace}

/* -- Systems Grid -- */
.sys-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(90px,1fr));gap:6px;margin:.8rem 0}
.sys-item{
    background:var(--surface);border:1px solid var(--border);border-radius:12px;
    padding:.6rem .3rem;text-align:center;transition:all .2s
}
.sys-item:hover{border-color:var(--border-h)}
.sys-ico{font-size:.8rem;font-weight:700;color:var(--purple);font-family:'JetBrains Mono',monospace}
.sys-name{font-size:.6rem;color:var(--text3);margin-top:2px}

/* -- Timeline -- */
.tl-h{
    font-family:'JetBrains Mono',monospace;font-size:.8rem;font-weight:700;color:var(--teal);
    padding:.6rem 0 .2rem;border-bottom:1px solid var(--border);margin-top:.6rem
}

/* -- Section Title -- */
.sec{
    font-size:1.05rem;font-weight:700;color:var(--text);margin:1.8rem 0 .6rem;
    display:flex;align-items:center;gap:10px
}
.sec::before{content:'';width:4px;height:20px;border-radius:2px;background:linear-gradient(180deg,var(--purple),var(--teal))}
.sec::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,var(--border),transparent)}

/* -- Disclaimer -- */
.disc{
    background:var(--surface);border:1px solid var(--border);border-radius:14px;
    padding:.8rem 1rem;margin:2rem 0 1rem;font-size:.7rem;color:var(--text3);
    position:relative;overflow:hidden
}
.disc::before{content:'';position:absolute;top:0;left:0;width:100%;height:2px;background:linear-gradient(90deg,var(--orange),transparent)}

/* -- Tab Polish -- */
.stTabs [data-baseweb="tab-list"]{background:transparent;gap:4px;border-bottom:1px solid var(--border)}
.stTabs [data-baseweb="tab"]{background:transparent;border-radius:8px 8px 0 0;color:var(--text2);font-size:.78rem;font-family:'Space Grotesk',sans-serif}
.stTabs [aria-selected="true"]{background:var(--purple-g) !important;color:var(--purple) !important;border-bottom:2px solid var(--purple) !important}

/* -- Sidebar Polish -- */
section[data-testid="stSidebar"] .stNumberInput>div>div>input{
    background:var(--bg) !important;border:1px solid var(--border) !important;
    color:var(--text) !important;border-radius:10px !important;font-family:'JetBrains Mono',monospace !important
}
section[data-testid="stSidebar"] label{font-size:.78rem !important;color:var(--text2) !important}

/* -- Daily Schedule -- */
.sched-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:1rem 0}
.sched-col{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:1rem;position:relative;overflow:hidden}
.sched-col::before{content:'';position:absolute;top:0;left:0;width:100%;height:3px}
.sched-col.morning::before{background:linear-gradient(90deg,#f59e0b,#fbbf24)}
.sched-col.noon::before{background:linear-gradient(90deg,#3b82f6,#60a5fa)}
.sched-col.evening::before{background:linear-gradient(90deg,#8b5cf6,#a78bfa)}
.sched-time{font-family:'JetBrains Mono',monospace;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:.6rem}
.sched-col.morning .sched-time{color:#f59e0b}
.sched-col.noon .sched-time{color:#3b82f6}
.sched-col.evening .sched-time{color:#8b5cf6}
.sched-pill{
    display:flex;align-items:center;gap:8px;padding:6px 8px;margin:4px 0;
    background:rgba(255,255,255,0.02);border-radius:10px;border:1px solid var(--border)
}
.sched-pill .sp-dot{width:22px;height:22px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:.5rem;font-weight:700;color:#fff;flex-shrink:0}
.sched-pill .sp-name{font-size:.72rem;color:var(--text);font-weight:500}
.sched-pill .sp-dose{font-size:.62rem;color:var(--text3);font-family:'JetBrains Mono',monospace}
.sched-empty{font-size:.7rem;color:var(--text3);text-align:center;padding:.5rem 0}

/* -- Symptom Checker -- */
.sym-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:8px;margin:1rem 0}
.sym-btn{
    background:var(--surface);border:1px solid var(--border);border-radius:12px;
    padding:.7rem .9rem;display:flex;align-items:center;gap:8px;cursor:pointer;transition:all .2s
}
.sym-btn:hover{border-color:var(--border-h);box-shadow:var(--glow-purple)}
.sym-btn.active{border-color:var(--teal);background:var(--teal-g)}
.sym-ico{font-family:'JetBrains Mono',monospace;font-size:.75rem;font-weight:700;color:var(--purple);width:24px;text-align:center}
.sym-name{font-size:.75rem;color:var(--text);font-weight:500}
.sym-cat{font-size:.58rem;color:var(--text3)}

/* -- Symptom Results -- */
.sym-result{
    background:var(--surface);border:1px solid rgba(45,212,191,0.1);
    border-radius:16px;padding:1.2rem;margin:.8rem 0;position:relative;overflow:hidden
}
.sym-result::before{content:'';position:absolute;top:0;left:0;width:100%;height:3px;background:linear-gradient(90deg,var(--teal),var(--purple))}
.sym-vit-row{display:flex;align-items:center;gap:10px;padding:6px 0;border-bottom:1px solid var(--border)}
.sym-vit-row:last-child{border-bottom:none}
.sym-vit-dot{width:26px;height:26px;border-radius:7px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.55rem;color:#fff;flex-shrink:0}
.sym-vit-name{font-size:.8rem;color:var(--text);font-weight:500;flex:1}
.sym-vit-count{font-family:'JetBrains Mono',monospace;font-size:.7rem;color:var(--teal);font-weight:700}
.sym-match-bar{width:60px;height:4px;background:rgba(255,255,255,0.04);border-radius:2px;overflow:hidden}
.sym-match-fill{height:100%;border-radius:2px;background:var(--teal)}

/* -- Meal Plan -- */
.meal-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;margin:1rem 0}
.meal-card{
    background:var(--surface);border:1px solid var(--border);border-radius:16px;
    padding:1rem 1.2rem;position:relative;overflow:hidden;transition:all .2s
}
.meal-card:hover{border-color:var(--border-h)}
.meal-card::before{content:'';position:absolute;top:0;left:0;width:3px;height:100%}
.meal-header{display:flex;align-items:center;gap:8px;margin-bottom:.6rem}
.meal-dot{width:28px;height:28px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.55rem;color:#fff;flex-shrink:0}
.meal-vname{font-size:.85rem;font-weight:600;color:var(--text)}
.meal-row{display:flex;justify-content:space-between;align-items:center;padding:5px 0;border-bottom:1px solid var(--border)}
.meal-row:last-child{border-bottom:none}
.meal-time{font-size:.62rem;color:var(--text3);font-family:'JetBrains Mono',monospace;text-transform:uppercase;min-width:55px}
.meal-food{font-size:.72rem;color:var(--text);flex:1;padding:0 8px}
.meal-portion{font-size:.62rem;color:var(--teal);font-family:'JetBrains Mono',monospace;white-space:nowrap}

/* -- Page tabs -- */
.page-tabs{display:flex;gap:6px;margin-bottom:1.5rem}
.page-tab{
    flex:1;background:var(--surface);border:1px solid var(--border);border-radius:12px;
    padding:.8rem;text-align:center;cursor:pointer;transition:all .2s
}
.page-tab:hover{border-color:var(--border-h)}
.page-tab .pt-ico{font-size:1.1rem;margin-bottom:.2rem}
.page-tab .pt-name{font-size:.78rem;font-weight:600;color:var(--text)}
.page-tab .pt-desc{font-size:.6rem;color:var(--text3)}

/* -- Symptom Checker -- */
.sym-result{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:1rem;margin:8px 0;position:relative;overflow:hidden}
.sym-result::before{content:'';position:absolute;left:0;top:0;width:3px;height:100%}
.sym-vit{font-size:.85rem;font-weight:600;color:var(--text);margin-bottom:2px}
.sym-bar-wrap{height:6px;background:rgba(255,255,255,0.04);border-radius:3px;margin-top:6px;overflow:hidden}
.sym-bar{height:100%;border-radius:3px;background:var(--purple)}
.sym-count{font-size:.65rem;color:var(--text3);font-family:'JetBrains Mono',monospace;margin-top:3px}

/* -- Meal Plan -- */
.meal-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:6px;margin:1rem 0}
.meal-day{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:.6rem;text-align:center;transition:all .2s}
.meal-day:hover{border-color:var(--border-h)}
.meal-day-name{font-family:'JetBrains Mono',monospace;font-size:.65rem;font-weight:700;color:var(--purple);text-transform:uppercase;letter-spacing:1px;margin-bottom:.4rem}
.meal-food{font-size:.68rem;color:var(--text2);line-height:1.4}
.meal-vit-title{font-size:.82rem;font-weight:600;color:var(--text);margin:8px 0 4px;display:flex;align-items:center;gap:6px}
.meal-vit-dot{width:18px;height:18px;border-radius:5px;display:inline-flex;align-items:center;justify-content:center;font-size:.5rem;font-weight:700;color:#fff}

/* -- Conflict Matrix -- */
.conf-card{
    background:rgba(244,63,94,0.04);border:1px solid rgba(244,63,94,0.1);
    border-radius:14px;padding:.8rem 1rem;margin:6px 0;display:flex;align-items:center;gap:12px;
    position:relative;overflow:hidden
}
.conf-card::before{content:'';position:absolute;left:0;top:0;width:3px;height:100%;background:var(--red)}
.conf-vs{font-family:'JetBrains Mono',monospace;font-size:.65rem;color:var(--red);font-weight:700;background:rgba(244,63,94,0.1);padding:2px 8px;border-radius:6px;flex-shrink:0}
.conf-text{font-size:.78rem;color:var(--text2);line-height:1.4}
.conf-names{font-size:.82rem;font-weight:600;color:var(--text);margin-bottom:2px}

/* -- Cost Card -- */
.cost-wrap{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:1rem 0}
.cost-card{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:1rem;display:flex;align-items:center;gap:12px}
.cost-icon{width:40px;height:40px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.65rem;color:#fff;flex-shrink:0}
.cost-info{flex:1}
.cost-name{font-size:.82rem;font-weight:600;color:var(--text)}
.cost-range{font-family:'JetBrains Mono',monospace;font-size:.75rem;color:var(--teal);font-weight:700}
.cost-total{
    background:linear-gradient(135deg,rgba(139,92,246,0.08),rgba(45,212,191,0.06));
    border:1px solid var(--border-h);border-radius:16px;padding:1.2rem;text-align:center;margin:1rem 0
}
.cost-total-lbl{font-size:.7rem;color:var(--text2);text-transform:uppercase;letter-spacing:1px}
.cost-total-val{font-family:'JetBrains Mono',monospace;font-size:1.8rem;font-weight:700;color:var(--teal);margin-top:.2rem}

/* -- Health Score Gauge -- */
.health-gauge{text-align:center;margin:1rem 0}
.hg-ring{
    width:180px;height:180px;border-radius:50%;display:inline-flex;align-items:center;
    justify-content:center;flex-direction:column;position:relative
}
.hg-ring::before{
    content:'';position:absolute;inset:-4px;border-radius:50%;
    background:conic-gradient(var(--hg-color) var(--hg-pct), rgba(255,255,255,0.03) 0);
    -webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 5px),#fff calc(100% - 4px));
    mask:radial-gradient(farthest-side,transparent calc(100% - 5px),#fff calc(100% - 4px))
}
.hg-ring::after{content:'';position:absolute;inset:0;border-radius:50%;background:var(--surface);box-shadow:inset 0 0 40px rgba(0,0,0,0.5)}
.hg-inner{position:relative;z-index:1}
.hg-num{font-family:'JetBrains Mono',monospace;font-size:3.2rem;font-weight:700;line-height:1}
.hg-label{font-size:.6rem;color:var(--text2);text-transform:uppercase;letter-spacing:2px;margin-top:2px}
.hg-desc{font-size:.78rem;color:var(--text2);margin-top:.6rem}

/* -- Season Card -- */
.season-card{
    background:var(--surface);border:1px solid var(--border);border-radius:16px;
    padding:1rem 1.2rem;margin:8px 0;position:relative;overflow:hidden
}
.season-card::before{content:'';position:absolute;top:0;left:0;width:100%;height:3px}
.season-card.winter::before{background:linear-gradient(90deg,#60a5fa,#3b82f6)}
.season-card.summer::before{background:linear-gradient(90deg,#f59e0b,#f97316)}
.season-card.spring::before{background:linear-gradient(90deg,#22c55e,#10b981)}
.season-card.autumn::before{background:linear-gradient(90deg,#d97706,#b45309)}
.season-title{font-size:.85rem;font-weight:700;color:var(--text);margin-bottom:4px}
.season-text{font-size:.78rem;color:var(--text2);line-height:1.5}

/* -- History comparison -- */
.hist-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:1rem 0}
.hist-card{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:1rem;text-align:center}
.hist-label{font-size:.65rem;color:var(--text3);text-transform:uppercase;letter-spacing:1px;margin-bottom:.3rem}
.hist-val{font-family:'JetBrains Mono',monospace;font-size:1.4rem;font-weight:700}
.hist-change{font-size:.7rem;font-weight:700;margin-top:2px}

/* -- Animations -- */
@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
@keyframes countUp{from{opacity:0;transform:scale(0.5)}to{opacity:1;transform:scale(1)}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.6}}
@keyframes shimmer{0%{background-position:-200% 0}100%{background-position:200% 0}}
.v-card,.supp-card,.syn-card,.p-alert,.r-card,.conf-card,.season-card,.cost-card,.meal-day,.sys-item{animation:fadeUp .4s ease both}
.v-card:nth-child(1){animation-delay:.05s}.v-card:nth-child(2){animation-delay:.1s}
.v-card:nth-child(3){animation-delay:.15s}.v-card:nth-child(4){animation-delay:.2s}
.m-num{animation:countUp .5s ease both}
.m-box:nth-child(1) .m-num{animation-delay:.1s}.m-box:nth-child(2) .m-num{animation-delay:.2s}
.m-box:nth-child(3) .m-num{animation-delay:.3s}.m-box:nth-child(4) .m-num{animation-delay:.4s}
.m-box:nth-child(5) .m-num{animation-delay:.5s}
.hg-num{animation:countUp .6s ease both;animation-delay:.2s}
.hero{animation:fadeUp .5s ease both}
.w-card{animation:fadeUp .4s ease both}
.w-card:nth-child(1){animation-delay:.1s}.w-card:nth-child(2){animation-delay:.2s}.w-card:nth-child(3){animation-delay:.3s}

/* -- Badges / Achievements -- */
.badge-grid{display:flex;flex-wrap:wrap;gap:10px;margin:1rem 0;justify-content:center}
.ach-badge{
    background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:.8rem 1rem;
    text-align:center;min-width:110px;transition:all .3s;animation:fadeUp .4s ease both;position:relative;overflow:hidden
}
.ach-badge:hover{border-color:var(--border-h);transform:translateY(-3px);box-shadow:var(--glow-purple)}
.ach-badge.earned{border-color:rgba(45,212,191,0.25)}
.ach-badge.earned::after{
    content:'';position:absolute;top:0;left:0;width:100%;height:100%;
    background:linear-gradient(90deg,transparent,rgba(45,212,191,0.04),transparent);
    background-size:200% 100%;animation:shimmer 3s infinite
}
.ach-ico{font-size:1.6rem;margin-bottom:.3rem}
.ach-name{font-size:.7rem;font-weight:600;color:var(--text)}
.ach-desc{font-size:.58rem;color:var(--text3);margin-top:1px}
.ach-badge.locked{opacity:.35;filter:grayscale(1)}
.ach-badge.locked .ach-ico{filter:grayscale(1)}

/* -- Body Map -- */
.body-map{display:flex;justify-content:center;align-items:center;gap:2rem;margin:1rem 0;flex-wrap:wrap}
.body-svg{position:relative;width:160px;flex-shrink:0}
.body-organs{flex:1;min-width:200px}
.organ-row{display:flex;align-items:center;gap:8px;padding:5px 0;border-bottom:1px solid var(--border)}
.organ-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0;animation:pulse 2s infinite}
.organ-name{font-size:.78rem;font-weight:600;color:var(--text)}
.organ-vitamins{font-size:.65rem;color:var(--text3);font-family:'JetBrains Mono',monospace}

/* -- Mobile Responsive -- */
@media(max-width:768px){
    .hero h1{font-size:1.6rem}
    .hero .sub{font-size:.75rem}
    .welcome-grid{grid-template-columns:1fr}
    .feat-row{flex-direction:column}
    .metrics{grid-template-columns:repeat(3,1fr)}
    .supp-grid{grid-template-columns:1fr}
    .cost-wrap{grid-template-columns:1fr}
    .meal-grid{grid-template-columns:repeat(3,1fr)}
    .sched-grid{grid-template-columns:1fr}
    .vit-grid{grid-template-columns:repeat(auto-fill,minmax(110px,1fr))}
    .prof-grid{grid-template-columns:repeat(3,1fr)}
    .body-map{flex-direction:column;align-items:center}
    .hist-grid{grid-template-columns:1fr}
    .hg-ring{width:140px;height:140px}
    .hg-num{font-size:2.4rem}
    .score-ring{width:120px;height:120px}
    .score-num{font-size:2.2rem}
    .sec{font-size:.9rem}
    .v-card{flex-wrap:wrap}
}
@media(max-width:480px){
    .hero{padding:1.5rem 1rem}
    .hero h1{font-size:1.3rem}
    .metrics{grid-template-columns:repeat(2,1fr)}
    .badge-grid{gap:6px}
    .ach-badge{min-width:80px;padding:.5rem .6rem}
    .ach-ico{font-size:1.2rem}
}

/* -- Daily Fact Card -- */
.fact-card{
    background:linear-gradient(135deg,rgba(139,92,246,0.06),rgba(45,212,191,0.04));
    border:1px solid var(--border-h);border-radius:20px;padding:1.2rem 1.5rem;margin:1.5rem 0;
    position:relative;overflow:hidden;animation:fadeUp .5s ease both
}
.fact-card::before{content:'';position:absolute;top:0;left:0;width:100%;height:3px;background:linear-gradient(90deg,var(--purple),var(--teal))}
.fact-tag{font-family:'JetBrains Mono',monospace;font-size:.6rem;font-weight:700;color:var(--teal);text-transform:uppercase;letter-spacing:2px;margin-bottom:.4rem}
.fact-text{font-size:.88rem;color:var(--text);line-height:1.6}
.fact-vit{font-size:.7rem;color:var(--purple);margin-top:.4rem;font-weight:600}

/* -- Food Portions -- */
.fp-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:.6rem 0}
.fp-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:.7rem;text-align:center;transition:all .2s}
.fp-card:hover{border-color:var(--border-h)}
.fp-food{font-size:.78rem;font-weight:600;color:var(--text)}
.fp-portion{font-size:.62rem;color:var(--text3);font-family:'JetBrains Mono',monospace}
.fp-pct-wrap{height:4px;background:rgba(255,255,255,0.04);border-radius:2px;margin-top:6px;overflow:hidden}
.fp-pct-bar{height:100%;border-radius:2px;background:var(--teal)}
.fp-pct-label{font-size:.58rem;color:var(--teal);font-family:'JetBrains Mono',monospace;margin-top:2px}

/* -- TR Comparison -- */
.tr-card{
    background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:.8rem 1rem;margin:6px 0;
    display:flex;align-items:center;gap:12px;animation:fadeUp .4s ease both
}
.tr-rank{
    width:48px;height:48px;border-radius:50%;display:flex;align-items:center;justify-content:center;
    flex-direction:column;flex-shrink:0;border:2px solid
}
.tr-rank-num{font-family:'JetBrains Mono',monospace;font-size:.8rem;font-weight:700;line-height:1}
.tr-rank-lbl{font-size:.45rem;color:var(--text3);text-transform:uppercase}
.tr-info{flex:1}
.tr-name{font-size:.82rem;font-weight:600;color:var(--text)}
.tr-bar-wrap{height:6px;background:rgba(255,255,255,0.04);border-radius:3px;margin-top:4px;position:relative;overflow:visible}
.tr-bar{height:100%;border-radius:3px;position:relative}
.tr-avg-line{position:absolute;top:-4px;width:2px;height:14px;background:var(--purple);border-radius:1px}
.tr-note{font-size:.62rem;color:var(--text3);margin-top:3px}

/* -- Share Box -- */
.share-box{
    background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:1rem;
    font-family:'JetBrains Mono',monospace;font-size:.7rem;color:var(--text2);
    line-height:1.6;white-space:pre-wrap;margin:.5rem 0
}

/* -- Encyclopedia -- */
.enc-card{
    background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:1rem;
    margin:6px 0;transition:all .2s;cursor:pointer
}
.enc-card:hover{border-color:var(--border-h);box-shadow:var(--glow-purple)}
.enc-header{display:flex;align-items:center;gap:10px}
.enc-dot{width:36px;height:36px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.6rem;color:#fff;flex-shrink:0}
.enc-name{font-size:.88rem;font-weight:600;color:var(--text)}
.enc-cat{font-size:.6rem;color:var(--text3);font-family:'JetBrains Mono',monospace}
.enc-body{margin-top:.6rem;padding-top:.6rem;border-top:1px solid var(--border)}
.enc-row{display:flex;justify-content:space-between;padding:3px 0;font-size:.72rem}
.enc-label{color:var(--text3)}.enc-val{color:var(--text);font-weight:500;font-family:'JetBrains Mono',monospace}
@media(max-width:768px){
    .fp-grid{grid-template-columns:repeat(2,1fr)}
}

/* -- Quiz -- */
.quiz-card{
    background:var(--surface);border:1px solid var(--border);border-radius:18px;
    padding:1.2rem 1.5rem;margin:1rem 0;position:relative;overflow:hidden
}
.quiz-card::before{content:'';position:absolute;top:0;left:0;width:100%;height:3px;background:linear-gradient(90deg,var(--purple),var(--teal),var(--blue))}
.quiz-q{font-size:.95rem;font-weight:600;color:var(--text);margin-bottom:.8rem;line-height:1.5}
.quiz-num{font-family:'JetBrains Mono',monospace;font-size:.6rem;color:var(--purple);margin-bottom:.4rem;text-transform:uppercase;letter-spacing:1.5px}
.quiz-result{border-radius:12px;padding:.8rem 1rem;margin-top:.8rem;font-size:.8rem;line-height:1.5}
.quiz-result.correct{background:rgba(34,197,94,0.06);border:1px solid rgba(34,197,94,0.15);color:var(--green)}
.quiz-result.wrong{background:rgba(244,63,94,0.06);border:1px solid rgba(244,63,94,0.15);color:var(--red)}
.quiz-score-bar{display:flex;gap:4px;margin:1rem 0}
.quiz-dot{width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.6rem;font-weight:700;color:#fff}
.quiz-dot.right{background:var(--green)}.quiz-dot.wrong{background:var(--red)}.quiz-dot.pending{background:rgba(255,255,255,0.06);color:var(--text3)}

/* -- Brand Cards -- */
.brand-card{
    background:var(--surface);border:1px solid var(--border);border-radius:14px;
    padding:.8rem 1rem;margin:6px 0;animation:fadeUp .4s ease both
}
.brand-header{display:flex;align-items:center;gap:8px;margin-bottom:.5rem}
.brand-name{font-size:.85rem;font-weight:600;color:var(--text)}
.brand-list{display:flex;flex-wrap:wrap;gap:5px;margin:.4rem 0}
.brand-pill{
    background:var(--purple-g);border:1px solid rgba(139,92,246,0.12);
    padding:4px 10px;border-radius:100px;font-size:.68rem;color:var(--purple);
    font-family:'JetBrains Mono',monospace;font-weight:600
}
.brand-tip{font-size:.72rem;color:var(--teal);margin-top:.4rem;padding:5px 8px;background:var(--teal-g);border-radius:8px;border:1px solid rgba(45,212,191,0.08)}

/* -- Simulation Timeline -- */
.sim-timeline{position:relative;padding-left:24px;margin:1rem 0}
.sim-timeline::before{content:'';position:absolute;left:8px;top:0;width:2px;height:100%;background:linear-gradient(180deg,var(--purple),var(--teal))}
.sim-period{position:relative;margin-bottom:1rem}
.sim-dot{position:absolute;left:-20px;top:4px;width:12px;height:12px;border-radius:50%;border:2px solid var(--surface)}
.sim-label{font-family:'JetBrains Mono',monospace;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:.3rem}
.sim-items{display:flex;flex-wrap:wrap;gap:4px}
.sim-item{
    background:rgba(255,255,255,0.02);border:1px solid var(--border);
    padding:4px 10px;border-radius:8px;font-size:.72rem;color:var(--text2)
}

/* -- Water Calc -- */
.water-card{
    background:linear-gradient(135deg,rgba(59,130,246,0.06),rgba(45,212,191,0.04));
    border:1px solid rgba(59,130,246,0.12);border-radius:16px;padding:1rem;text-align:center;margin:1rem 0
}
.water-val{font-family:'JetBrains Mono',monospace;font-size:2rem;font-weight:700;color:#3b82f6}
.water-unit{font-size:.7rem;color:var(--text2)}
.water-cups{display:flex;justify-content:center;gap:3px;margin-top:.5rem}
.water-cup{font-size:1rem;opacity:.3}.water-cup.filled{opacity:1}
</style>"""
