"""Bangun notebooks/02_statistik_job_market.ipynb — uji statistik data riil."""
import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.cells = [
    nbf.v4.new_markdown_cell(
        "# Statistik — Job Market Indonesia\n"
        "Dataset kecil & riil: uji dilakukan dengan sadar batasannya — "
        "semua kesimpulan disertai keterbatasan, bukan overclaim."),
    nbf.v4.new_code_cell(
        "import pandas as pd\nimport numpy as np\n"
        "from scipy import stats\nimport matplotlib.pyplot as plt\n"
        "import seaborn as sns\nsns.set_theme(style='whitegrid')\n"
        "lv = pd.read_csv('../data/processed/lowongan.csv')\n"
        "sk = pd.read_csv('../data/processed/job_skill.csv')"),

    nbf.v4.new_markdown_cell(
        "## 1. Apakah judul 'analyst' berhubungan dengan senioritas?\n"
        "Chi-square: `peran_analyst` × `senioritas`"),
    nbf.v4.new_code_cell(
        "ct = pd.crosstab(lv.peran_analyst, lv.senioritas)\n"
        "chi2, p, dof, _ = stats.chi2_contingency(ct)\n"
        "n_ = ct.values.sum()\n"
        "v = np.sqrt(chi2 / (n_ * (min(ct.shape) - 1)))\n"
        "print(ct)\n"
        "print(f'chi2={chi2:.1f}, p={p:.4f}, dof={dof}, CramérV={v:.3f}')\n"
        "print('p<0.05:', p < 0.05)"),

    nbf.v4.new_markdown_cell(
        "## 2. Apakah lowongan analyst lebih terbuka ke fresh grad?\n"
        "Chi-square: `peran_analyst` × `fresh_grad_ok`"),
    nbf.v4.new_code_cell(
        "ct2 = pd.crosstab(lv.peran_analyst, lv.fresh_grad_ok)\n"
        "chi2, p, dof, _ = stats.chi2_contingency(ct2)\n"
        "rate = lv.groupby('peran_analyst').fresh_grad_ok.mean()\n"
        "print(ct2, '\\n', rate.round(3))\n"
        "print(f'chi2={chi2:.2f}, p={p:.4f}')"),

    nbf.v4.new_markdown_cell(
        "## 3. Gaji: Junior vs Senior\n"
        "⚠️ Hanya ~48 lowongan menampilkan gaji (~3%) → power rendah. "
        "Hasil bersifat indikatif, BUKAN estimasi pasar."),
    nbf.v4.new_code_cell(
        "bg = lv.dropna(subset=['gaji_max_jt'])\n"
        "print(bg.groupby('senioritas').gaji_max_jt\n"
        "        .agg(['count','median','mean']).round(1))\n"
        "jun = bg[bg.senioritas=='Junior / Entry'].gaji_max_jt\n"
        "sen = bg[bg.senioritas=='Senior / Lead'].gaji_max_jt\n"
        "if len(jun) >= 3 and len(sen) >= 3:\n"
        "    u, p = stats.mannwhitneyu(jun, sen, alternative='less')\n"
        "    print(f'Mann-Whitney (junior < senior): U={u:.0f}, p={p:.4f}')\n"
        "else:\n"
        "    print('n per grup terlalu kecil untuk uji — dilaporkan deskriptif saja')"),

    nbf.v4.new_markdown_cell(
        "## 4. Apakah domain menentukan peluang fresh-grad?\n"
        "Chi-square: `domain` × `fresh_grad_ok` — domain dengan expected "
        "count <5 digabung 'Lainnya'."),
    nbf.v4.new_code_cell(
        "dom = lv.domain.value_counts()\n"
        "lv3 = lv.copy()\n"
        "lv3['dom'] = np.where(lv3.domain.isin(dom[dom>=50].index),\n"
        "                      lv3.domain, 'Lainnya')\n"
        "ctd = pd.crosstab(lv3.dom, lv3.fresh_grad_ok)\n"
        "chi2, p, dof, exp = stats.chi2_contingency(ctd)\n"
        "print(ctd, '\\n')\n"
        "print((ctd.div(ctd.sum(1), axis=0)[True]*100)\n"
        "      .round(1).rename('fresh-grad %'))\n"
        "print(f'chi2={chi2:.1f}, p={p:.4g}, dof={dof}')"),

    nbf.v4.new_markdown_cell(
        "## 5. Platform × domain — dua platform, dua pasar\n"
        "Apakah komposisi domain berbeda antara Kalibrr dan LinkedIn?"),
    nbf.v4.new_code_cell(
        "ctp = pd.crosstab(lv3.dom, lv3.sumber)\n"
        "chi2, p, dof, _ = stats.chi2_contingency(ctp)\n"
        "n_ = ctp.values.sum()\n"
        "v = np.sqrt(chi2 / (n_ * (min(ctp.shape) - 1)))\n"
        "print(ctp)\n"
        "print(f'chi2={chi2:.1f}, p={p:.4g}, CramérV={v:.3f}')\n"
        "print('CramérV > 0.3 = asosiasi kuat antar platform dan domain')"),

    nbf.v4.new_markdown_cell(
        "## 6. Skill × keluarga peran — mana yang membedakan?\n"
        "Untuk tiap skill top-8: chi-square hadir/tidak × role_family "
        "(family kecil digabung 'Lainnya')."),
    nbf.v4.new_code_cell(
        "lv2 = lv.copy()\n"
        "top_fam = lv2.role_family.value_counts()\n"
        "lv2['fam'] = np.where(lv2.role_family.isin(top_fam[top_fam>=20].index),\n"
        "                      lv2.role_family, 'Lainnya')\n"
        "hasil = []\n"
        "for s in sk.skill.value_counts().head(8).index:\n"
        "    ids = set(sk[sk.skill == s].id_lowongan)\n"
        "    lv2['ada'] = lv2.id_lowongan.isin(ids)\n"
        "    ct = pd.crosstab(lv2.fam, lv2.ada)\n"
        "    if ct.shape == (len(lv2.fam.unique()), 2):\n"
        "        chi2, p, dof, _ = stats.chi2_contingency(ct)\n"
        "        hasil.append((s, round(chi2,1), round(p,4)))\n"
        "pd.DataFrame(hasil, columns=['skill','chi2','p']).sort_values('p')"),

    nbf.v4.new_markdown_cell(
        "## Kesimpulan\n"
        "- Uji signifikan → laporkan; tidak signifikan → katakan jujur.\n"
        "- Dataset riil ~1.500 lowongan: uji bermakna untuk efek "
        "sedang-besar; efek sangat kecil tetap sulit dideteksi.\n"
        "- Analisis gaji dibatasi ~3% coverage: kesimpulan gaji bersifat "
        "hipotesis, bukan estimasi pasar.\n"
        "- Hasil non-signifikan dilaporkan apa adanya — bukan "
        "dirapikan demi narasi."),
]
nbf.write(nb, "notebooks/02_statistik_job_market.ipynb")
print("notebook 2 dibuat")
