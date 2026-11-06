"""Dashboard Analisis Pasar Kerja Analitik Indonesia — data riil Kalibrr."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Job Market Analytics Indonesia",
                   page_icon="📈", layout="wide",
                   initial_sidebar_state="expanded")

# ---- Clean minimal palette: satu aksen ungu + netral ----
C_MAIN, C_CYAN = "#7C3AED", "#0E7490"
C_GREEN, C_AMBER = "#16A34A", "#D97706"
C_PINK, C_RED = "#B05A78", "#DC2626"
PALETTE = ["#7C3AED", "#94A3B8", "#64748B", "#475569",
           "#0E7490", "#A5B4C5", "#B05A78", "#CBD5E1"]

st.markdown("""
<style>
    .block-container {padding-top:1.2rem;padding-bottom:2.5rem;max-width:1320px;}
    [data-testid="stAppViewContainer"] {background:#F5F7FB;}
    [data-testid="stSidebar"] {background:#FFFFFF;border-right:1px solid #E8ECF2;}
    [data-testid="stSidebar"] * {color:#334155 !important;}
    [data-testid="stSidebar"] .stMultiSelect label {font-weight:600;}

    /* ---------- Hero: soft gradient + chips ---------- */
    .hero {position:relative;overflow:hidden;
        background:linear-gradient(115deg,#FFFFFF 42%,#F3EEFF 100%);
        border:1px solid #E6EAF2;border-radius:18px;
        padding:1.5rem 1.7rem 1.35rem;margin:0 0 1.35rem;
        box-shadow:0 4px 18px rgba(15,23,42,.05);}
    .hero::after {content:"";position:absolute;right:-70px;top:-90px;
        width:260px;height:260px;border-radius:50%;
        background:radial-gradient(circle,rgba(124,58,237,.14) 0%,transparent 70%);}
    .hero .eyebrow {font-size:.7rem;font-weight:800;letter-spacing:1.6px;
        text-transform:uppercase;color:#7C3AED;margin-bottom:.35rem;}
    .hero h1 {margin:0;font-size:1.6rem;font-weight:800;
        letter-spacing:-.3px;color:#0F172A;}
    .hero p {margin:.45rem 0 .75rem;font-size:.92rem;color:#5B6B83;
        max-width:60rem;}
    .hero .chip {display:inline-block;font-size:.71rem;font-weight:600;
        background:rgba(255,255,255,.8);border:1px solid #E2E8F0;
        border-radius:999px;padding:.22rem .7rem;margin:0 .4rem .1rem 0;
        color:#475569;}
    .hero .chip b {color:#0F172A;}

    /* ---------- KPI cards ---------- */
    .kpi-grid {display:grid;gap:.9rem;margin-bottom:.5rem;
               grid-template-columns:repeat(5,1fr);}
    .kpi {background:#FFFFFF;border:1px solid #E8ECF2;border-radius:14px;
          padding:.95rem 1.05rem .85rem;min-width:0;position:relative;
          overflow:hidden;box-shadow:0 1px 3px rgba(15,23,42,.05);
          transition:transform .16s ease,box-shadow .16s ease;}
    .kpi:hover {transform:translateY(-3px);
        box-shadow:0 8px 20px rgba(15,23,42,.09);}
    .kpi::before {content:"";position:absolute;top:0;left:0;right:0;
        height:3px;background:linear-gradient(90deg,#7C3AED,#7C3AED55);}
    .kpi .top {display:flex;align-items:center;gap:.45rem;}
    .kpi .icon {font-size:.95rem;}
    .kpi .label {font-size:.72rem;font-weight:700;color:#64748B;
                 text-transform:uppercase;letter-spacing:.5px;}
    .kpi .value {font-size:1.7rem;font-weight:800;color:#0F172A;
                 line-height:1.15;margin:.3rem 0 .1rem;word-break:break-word;}
    .kpi .sub {font-size:.76rem;color:#94A3B8;}

    /* ---------- Section pill ---------- */
    .sec-pill {display:inline-flex;align-items:center;gap:.45rem;
               font-size:.78rem;font-weight:800;letter-spacing:.6px;
               text-transform:uppercase;color:#475569;
               background:#FFFFFF;border:1px solid #E8ECF2;
               padding:.32rem .85rem;border-radius:999px;
               margin:.8rem 0 .45rem;
               box-shadow:0 1px 2px rgba(15,23,42,.04);}
    .sec-pill .dot {width:8px;height:8px;border-radius:50%;
        background:#7C3AED;box-shadow:0 0 0 3px rgba(124,58,237,.15);}

    /* ---------- Insight tinted ---------- */
    .insight {border-radius:12px;padding:.85rem 1.05rem;font-size:.88rem;
              margin:.65rem 0;border:1px solid;line-height:1.55;}
    .insight.blue {background:#EFF6FF;border-color:#BFDBFE;color:#1E3A8A;}
    .insight.green {background:#F0FDF4;border-color:#BBF7D0;color:#14532D;}
    .insight.amber {background:#FFFBEB;border-color:#FDE68A;color:#78350F;}
    .insight.red {background:#FEF2F2;border-color:#FECACA;color:#7F1D1D;}
    .insight.purple {background:#F5F3FF;border-color:#DDD6FE;color:#4C1D95;}

    /* ---------- Tabs: segmented control ---------- */
    .stTabs [data-baseweb="tab-list"] {gap:.35rem;border-bottom:none;
        background:#FFFFFF;padding:.35rem;border-radius:14px;
        border:1px solid #E8ECF2;width:fit-content;max-width:100%;
        box-shadow:0 1px 3px rgba(15,23,42,.04);}
    .stTabs [data-baseweb="tab"] {border-radius:10px;padding:.5rem 1rem;
        font-weight:600;font-size:.9rem;color:#64748B;border:none;}
    .stTabs [aria-selected="true"] {background:#7C3AED !important;
        color:#FFFFFF !important;}
    .stTabs [data-baseweb="tab-highlight"] {display:none;}

    [data-testid="stExpander"] {background:#FFFFFF;border-radius:12px;
        border:1px solid #E8ECF2;}
    [data-testid="stDataFrame"] {border-radius:12px;overflow:hidden;
        border:1px solid #E8ECF2;background:#FFFFFF;}
    div[data-testid="stMetric"] {background:#FFFFFF;border:1px solid #E8ECF2;
        border-radius:12px;padding:.6rem .9rem;}
    div[data-testid="stSelectbox"] label {font-weight:600;}

    /* ---------- Footer ---------- */
    .footer {margin-top:2.2rem;padding-top:1rem;
        border-top:1px solid #E6EAF2;font-size:.75rem;color:#94A3B8;
        display:flex;justify-content:space-between;flex-wrap:wrap;gap:.4rem;}
    .footer b {color:#64748B;}

    /* ---------- Responsive ---------- */
    @media (max-width:1000px) {
        .kpi-grid {grid-template-columns:repeat(3,1fr);}
        .stTabs [data-baseweb="tab"] {padding:.4rem .65rem;font-size:.82rem;}
    }
    @media (max-width:640px) {
        .block-container {padding-left:.8rem;padding-right:.8rem;}
        .kpi-grid {grid-template-columns:repeat(2,1fr);gap:.6rem;}
        .kpi {padding:.8rem .8rem .7rem;}
        .kpi .value {font-size:1.3rem;}
        .hero {padding:1.1rem 1.15rem;}
        .hero h1 {font-size:1.25rem;}
        .hero p {font-size:.85rem;}
        .hero .chip {font-size:.66rem;padding:.18rem .55rem;}
        .sec-pill {font-size:.7rem;}
        .insight {font-size:.82rem;padding:.7rem .8rem;}
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load():
    lv = pd.read_csv("data/processed/lowongan.csv",
                     parse_dates=["tgl_posting", "tgl_tutup"])
    sk = pd.read_csv("data/processed/job_skill.csv")
    return lv, sk


lv_all, sk_all = load()


def chart(fig):
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Inter, Segoe UI, sans-serif", size=13,
                  color="#334155"),
        margin=dict(t=40, b=30, l=10, r=10))
    fig.update_xaxes(showgrid=False, zeroline=False, automargin=True)
    fig.update_yaxes(gridcolor="#EEF2F6", zeroline=False, automargin=True)
    st.plotly_chart(fig, width="stretch")


def table(df, **kw):
    st.dataframe(df, width="stretch", hide_index=True, **kw)


_TONE = {"": "purple", "pos": "green", "warn": "amber", "risk": "red",
         "blue": "blue"}


def insight(text, tone=""):
    st.markdown(
        f'<div class="insight {_TONE.get(tone, "purple")}">💡 {text}</div>',
        unsafe_allow_html=True)


def sec(icon, text, color=None):
    st.markdown(
        f'<div class="sec-pill"><span class="dot"></span>{icon} {text}</div>',
        unsafe_allow_html=True)


def md(isi_md):
    with st.container():
        st.markdown(isi_md)


# ---------------- Sidebar filter ---------------- #
st.sidebar.markdown("## 🎛️ Filter Data")
st.sidebar.caption("Semua visual mengikuti filter ini")

dom_list = sorted(lv_all.domain.dropna().unique())
dom_pilih = st.sidebar.multiselect("Segmen", dom_list, default=dom_list)
fam_list = sorted(lv_all[lv_all.domain.isin(dom_pilih)].role_family.unique())
fam_pilih = st.sidebar.multiselect("Keluarga Peran", fam_list, default=fam_list)
prov_list = sorted(lv_all.provinsi.dropna().unique())
prov_pilih = st.sidebar.multiselect("Provinsi", prov_list, default=prov_list)
sen_list = ["Junior / Entry", "Mid", "Senior / Lead"]
sen_pilih = st.sidebar.multiselect("Senioritas", sen_list, default=sen_list)
st.sidebar.divider()
st.sidebar.caption("📊 Data riil: Kalibrr + LinkedIn guest API, "
                   "diambil via endpoint publik · lihat docs/SUMBER_DATA.md")

lv = lv_all[(lv_all.domain.isin(dom_pilih)) &
            (lv_all.role_family.isin(fam_pilih)) &
            (lv_all.provinsi.isin(prov_pilih) | lv_all.provinsi.isna()) &
            (lv_all.senioritas.isin(sen_pilih))]
if lv.empty:
    st.warning("Tidak ada data untuk kombinasi filter ini — "
               "longgarkan filter di sidebar.")
    st.stop()
sk = sk_all[sk_all.id_lowongan.isin(lv.id_lowongan)]
n = len(lv)

# ---------------- Hero + KPI ---------------- #
st.markdown("""
<div class="hero">
  <div class="eyebrow">Portfolio Project · Real-World Data Analytics</div>
  <h1>📈 Indonesia IT & Data Job Market</h1>
  <p>Peta pasar kerja digital Indonesia dari lowongan <b>riil</b> Kalibrr +
     LinkedIn — skill demand, gaji, lokasi, dan pola perekrutan
     di 8 domain IT.</p>
  <span class="chip"><b>1.630</b> lowongan</span>
  <span class="chip"><b>8</b> domain</span>
  <span class="chip"><b>6.882</b> baris skill</span>
  <span class="chip">📅 Okt 2026</span>
  <span class="chip">DATA RIIL — bukan sintetis</span>
</div>
""", unsafe_allow_html=True)

top_skill = sk.skill.value_counts().idxmax() if len(sk) else "-"
pct_gaji = lv.gaji_max_jt.notna().mean()
kpis = [
    ("📄", "Lowongan Relevan", f"{n:,}", f"{lv.domain.nunique()} segmen"),
    ("📊", "Peran Data", f"{(lv.domain=='Data & Analytics').mean():.0%}",
     "share domain data & analytics"),
    ("🧩", "Skill Terdeteksi", f"{sk.skill.nunique()}", f"top: {top_skill}"),
    ("💰", "Tampilkan Gaji", f"{pct_gaji:.0%}",
     "hanya Kalibrr — transparansi rendah"),
    ("🏠", "Remote / Hybrid", f"{lv.remote.mean()+lv.hybrid.mean():.0%}",
     f"{lv.remote.sum()} remote · {lv.hybrid.sum()} hybrid"),
]
st.markdown('<div class="kpi-grid">' + "".join(
    f'<div class="kpi"><div class="top"><span class="icon">{i}</span>'
    f'<span class="label">{a}</span></div>'
    f'<div class="value">{b}</div><div class="sub">{c}</div></div>'
    for i, a, b, c in kpis) + "</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🗺️ Pasar", "🧩 Skill Demand", "💰 Gaji & Lokasi",
     "🏢 Perusahaan & Waktu", "🔍 Explorer"])

# ================= TAB 1: PASAR ================= #
with tab1:
    c1, c2 = st.columns([3, 2])
    with c1:
        sec("🗂️", "Segmen & Keluarga Peran")
        dom = lv.domain.value_counts().reset_index()
        dom.columns = ["domain", "n"]
        chart(px.bar(dom, x="n", y="domain", orientation="h",
                     color="n", color_continuous_scale="Purples",
                     labels={"n": "Lowongan", "domain": ""})
              .update_layout(coloraxis_showscale=False, height=150,
                             yaxis=dict(autorange="reversed")))
        fam = lv.role_family.value_counts().head(12).reset_index()
        fam.columns = ["role", "n"]
        chart(px.bar(fam, x="n", y="role", orientation="h",
                     color="n", color_continuous_scale="Purples",
                     labels={"n": "Lowongan", "role": ""})
              .update_layout(coloraxis_showscale=False, height=320,
                             yaxis=dict(autorange="reversed")))
    with c2:
        sec("📊", "Senioritas & Tipe Kerja")
        sen = lv.senioritas.value_counts().reindex(sen_list).dropna()
        chart(px.bar(sen.reset_index().rename(
                     columns={"senioritas": "Level", "count": "n"}),
                     x="Level", y="n", color="Level",
                     color_discrete_sequence=[C_MAIN, "#94A3B8", "#475569"],
                     labels={"n": "Lowongan"})
              .update_layout(showlegend=False, height=160))
        tipe = lv.tipe.value_counts().reset_index()
        tipe.columns = ["tipe", "n"]
        chart(px.pie(tipe, names="tipe", values="n", hole=.55,
                     color_discrete_sequence=PALETTE)
              .update_layout(height=160, margin=dict(t=10)))
    insight(f"Dari {n:,} lowongan yang menuntut profil analitik, "
            f"**{lv.peran_analyst.mean():.0%}** benar-benar berjudul analyst/data — "
            f"sisanya adalah peran adjacent (sales, ops, IT) yang tetap menuntut "
            f"skill analitik. Dominasi **{lv.role_family.value_counts().idxmax()}** "
            f"menunjukkan pasar menamai peran ini dengan beragam label.")
    c3, c4 = st.columns(2)
    with c3:
        sec("🌏", "Provinsi")
        prov = lv.provinsi.value_counts().head(10).reset_index()
        prov.columns = ["provinsi", "n"]
        chart(px.bar(prov, x="n", y="provinsi", orientation="h",
                     color="n", color_continuous_scale="Purples",
                     labels={"n": "Lowongan", "provinsi": ""})
              .update_layout(coloraxis_showscale=False, height=320,
                             yaxis=dict(autorange="reversed")))
    with c4:
        sec("🏙️", "Fresh Grad & Remote")
        fg = lv.fresh_grad_ok.mean()
        chart(px.bar(x=["Fresh-grad friendly", "Remote", "Hybrid"],
                     y=[fg, lv.remote.mean(), lv.hybrid.mean()],
                     color_discrete_sequence=[C_GREEN, C_MAIN, C_CYAN],
                     labels={"x": "", "y": "Share lowongan"})
              .update_layout(showlegend=False, height=320,
                             yaxis_tickformat=".0%"))
    insight(f"**{fg:.0%}** lowongan terbuka untuk fresh graduate — pintu masuk "
            f"lebar. Tapi remote murni hanya **{lv.remote.mean():.0%}** "
            f"(hybrid {lv.hybrid.mean():.0%}): pasar analitik Indonesia "
            f"masih on-site centric.", "warn")

# ================= TAB 2: SKILL DEMAND ================= #
with tab2:
    c1, c2 = st.columns([3, 2])
    n_desc = lv.id_lowongan.isin(sk.id_lowongan).sum()
    st.caption(f"Basis: {n_desc} lowongan dengan deskripsi lengkap "
               f"(Kalibrr {lv[lv.sumber=='kalibrr'].id_lowongan.isin(sk.id_lowongan).sum()}"
               f"/{len(lv[lv.sumber=='kalibrr'])}, LinkedIn subset — "
               f"LinkedIn di-throttle saat fetch detail)")
    with c1:
        sec("🧩", "Skill Paling Diminta")
        skill_n = (sk.skill.value_counts()
                   .rename_axis("skill").reset_index(name="n"))
        skill_n["persen"] = skill_n.n / n_desc
        chart(px.bar(skill_n.head(15), x="persen", y="skill",
                     orientation="h", color="persen",
                     color_continuous_scale="Purples",
                     labels={"persen": "Share lowongan", "skill": ""})
              .update_layout(coloraxis_showscale=False, height=420,
                             xaxis_tickformat=".0%",
                             yaxis=dict(autorange="reversed")))
    with c2:
        sec("🥇", "Skill per Keluarga Peran")
        fam_pil = st.selectbox("Peran", sorted(lv.role_family.unique()),
                               key="fam_skill")
        ids = lv[lv.role_family == fam_pil].id_lowongan
        s_top = (sk[sk.id_lowongan.isin(ids)].skill.value_counts()
                 .head(8).reset_index())
        s_top.columns = ["skill", "n"]
        chart(px.bar(s_top, x="n", y="skill", orientation="h",
                     color_discrete_sequence=[C_MAIN],
                     labels={"n": "Lowongan", "skill": ""})
              .update_layout(height=330, yaxis=dict(autorange="reversed")))
    insight(f"**{top_skill}** adalah skill #1 — muncul di "
            f"**{skill_n.iloc[0].persen:.0%}** lowongan. Urutan skill "
            f"ini adalah roadmap belajar: kuasai yang paling sering "
            f"diminta dulu, bukan yang paling hype.")
    sec("🔗", "Kombinasi Skill (co-occurrence)", C_CYAN)
    st.caption("Skill yang paling sering diminta BERSAMAAN dalam satu lowongan")
    co = (sk.merge(sk, on="id_lowongan")
            .query("skill_x < skill_y")
            .groupby(["skill_x", "skill_y"]).size()
            .reset_index(name="n").nlargest(12, "n"))
    if len(co):
        co["pair"] = co.skill_x + " + " + co.skill_y
        chart(px.bar(co, x="n", y="pair", orientation="h",
                     color="n", color_continuous_scale="Purples",
                     labels={"n": "Frekuensi", "pair": ""})
              .update_layout(coloraxis_showscale=False, height=380,
                             yaxis=dict(autorange="reversed")))
        insight(f"Combo terkuat: **{co.iloc[0]['pair']}** — "
                f"paket minimal employable dari {n_desc} lowongan "
                f"ber-deskripsi.", "pos")

# ================= TAB 3: GAJI & LOKASI ================= #
with tab3:
    bergaji = lv.dropna(subset=["gaji_max_jt"])
    if len(bergaji) >= 5:
        c1, c2 = st.columns(2)
        with c1:
            sec("💰", "Rentang Gaji per Keluarga Peran")
            g = (bergaji.groupby("role_family")
                 .agg(n=("id_lowongan", "count"),
                      min=("gaji_min_jt", "median"),
                      max=("gaji_max_jt", "median"))
                 .query("n >= 2").sort_values("max"))
            fig = go.Figure()
            fig.add_bar(y=g.index, x=g["max"] - g["min"], base=g["min"],
                        orientation="h", marker_color=C_MAIN,
                        name="rentang median")
            fig.update_layout(height=340, xaxis_title="Rp juta/bulan (median)",
                              yaxis_title="", showlegend=False)
            chart(fig)
        with c2:
            sec("📈", "Gaji per Senioritas")
            gs = (bergaji.groupby("senioritas")
                  .agg(n=("id_lowongan", "count"),
                       max=("gaji_max_jt", "median")).reset_index())
            chart(px.bar(gs, x="senioritas", y="max", color="senioritas",
                         color_discrete_sequence=[C_MAIN, "#94A3B8", "#475569"],
                         labels={"max": "Median gaji max (Rp jt/bln)",
                                 "senioritas": ""})
                  .update_layout(showlegend=False, height=340))
        insight(f"Median gaji maksimum: **Rp{bergaji.gaji_max_jt.median():.1f} "
                f"juta/bln**. Hanya **{pct_gaji:.0%}** lowongan menampilkan "
                f"gaji — angka ini bias ke perusahaan yang transparan, "
                f"bukan representasi pasar penuh.", "warn")
    else:
        st.info("Terlalu sedikit lowongan bergaji di filter ini untuk dianalisis.")
    sec("💎", "Skill dengan Gaji Tertinggi", C_GREEN)
    sp = (sk.merge(bergaji[["id_lowongan", "gaji_max_jt"]], on="id_lowongan")
            .groupby("skill").agg(n=("id_lowongan", "count"),
                                  gaji=("gaji_max_jt", "median"))
            .query("n >= 3").sort_values("gaji").reset_index())
    if len(sp):
        chart(px.bar(sp, x="gaji", y="skill", orientation="h",
                     color="gaji", color_continuous_scale="Greens",
                     labels={"gaji": "Median gaji max (Rp jt)", "skill": ""})
              .update_layout(coloraxis_showscale=False, height=340,
                             yaxis=dict(autorange="reversed")))
        insight(f"Skill berbayar tertinggi: **{sp.iloc[-1]['skill']}** — "
                f"medan dimana skill teknis terkonversi jadi rupiah.", "pos")

# ================= TAB 4: PERUSAHAAN & WAKTU ================= #
with tab4:
    c1, c2 = st.columns(2)
    with c1:
        sec("🏭", "Industri Perekrut")
        ind = lv.industri.value_counts().head(12).reset_index()
        ind.columns = ["industri", "n"]
        chart(px.bar(ind, x="n", y="industri", orientation="h",
                     color="n", color_continuous_scale="Purples",
                     labels={"n": "Lowongan", "industri": ""})
              .update_layout(coloraxis_showscale=False, height=380,
                             yaxis=dict(autorange="reversed")))
    with c2:
        sec("🏢", "Perusahaan Paling Aktif")
        comp = lv.perusahaan.value_counts().head(12).reset_index()
        comp.columns = ["perusahaan", "n"]
        chart(px.bar(comp, x="n", y="perusahaan", orientation="h",
                     color="n", color_continuous_scale="Purples",
                     labels={"n": "Lowongan", "perusahaan": ""})
              .update_layout(coloraxis_showscale=False, height=380,
                             yaxis=dict(autorange="reversed")))
    sec("📅", "Tren Posting per Bulan")
    tr = (lv.dropna(subset=["tgl_posting"])
            .assign(bulan=lambda d: d.tgl_posting.dt.to_period("M").astype(str))
            .groupby("bulan").size().reset_index(name="n"))
    chart(px.area(tr, x="bulan", y="n",
                  labels={"n": "Lowongan diposting", "bulan": ""})
          .update_traces(line_color=C_MAIN, fillcolor="rgba(124,58,237,.15)")
          .update_layout(height=300))
    insight("Posting date ≠ tanggal lowongan dibuka perusahaan — ini tanggal "
            "aktivasi di platform. Tren menunjukkan siklus rekrutmen "
            "di job board, bukan demand agregat ekonomi.")

# ================= TAB 5: EXPLORER ================= #
with tab5:
    sec("🔍", "Jelajah Lowongan")
    cari = st.text_input("Cari judul / perusahaan", "")
    kol = st.multiselect("Kolom",
        ["judul", "sumber", "domain", "role_family", "perusahaan",
         "industri", "kota", "provinsi", "tipe", "senioritas", "pengalaman",
         "pendidikan", "gaji_min_jt", "gaji_max_jt", "remote", "hybrid",
         "fresh_grad_ok", "tgl_posting"],
        default=["judul", "perusahaan", "kota", "role_family",
                 "senioritas", "gaji_max_jt", "tgl_posting"])
    view = lv.copy()
    if cari:
        m = (view.judul.str.contains(cari, case=False, na=False) |
             view.perusahaan.str.contains(cari, case=False, na=False))
        view = view[m]
    st.caption(f"{len(view):,} lowongan")
    table(view[kol].sort_values("tgl_posting", ascending=False))
    st.download_button("⬇️ Unduh CSV hasil filter",
                       view[kol].to_csv(index=False).encode(),
                       "lowongan_filter.csv", "text/csv")

st.sidebar.caption("Data diambil 27 Okt 2026 · 2 tabel relasional: "
                   "lowongan 1—n job_skill")

# ---------------- Footer ---------------- #
st.markdown(
    '<div class="footer"><span><b>Indonesia IT & Data Job Market</b> — '
    'portfolio project · data RIIL Kalibrr + LinkedIn guest API</span>'
    '<span>Streamlit · Plotly · SQLite · pandas</span></div>',
    unsafe_allow_html=True)
