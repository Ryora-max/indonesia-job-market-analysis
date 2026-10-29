"""Bangun notebooks/01_job_market_eda.ipynb — EDA data riil."""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = [
    nbf.v4.new_markdown_cell(
        "# EDA — Indonesia IT & Analytics Job Market\n"
        "Data riil: lowongan IT/data dari Kalibrr + LinkedIn guest API — "
        "mencakup data/analytics, software engineering, infra, security, "
        "QA, IT support, UI/UX, dan ERP/konsultasi.\n"
        "**Catatan:** data ini bukan sintetis — noise dan missingness "
        "adalah bagian dari kenyataan data riil."),
    nbf.v4.new_code_cell(
        "import pandas as pd\nimport matplotlib.pyplot as plt\n"
        "import seaborn as sns\nsns.set_theme(style='whitegrid')\n"
        "lv = pd.read_csv('../data/processed/lowongan.csv')\n"
        "sk = pd.read_csv('../data/processed/job_skill.csv')\n"
        "print(lv.shape, sk.shape)\nlv.head()"),
    nbf.v4.new_markdown_cell("## Komposisi domain, peran & sumber"),
    nbf.v4.new_code_cell(
        "fig, ax = plt.subplots(1, 3, figsize=(17, 4.5))\n"
        "lv.domain.value_counts().plot.barh(ax=ax[0], color='#7C3AED')\n"
        "ax[0].set_title('Domain pekerjaan')\n"
        "lv.role_family.value_counts().head(10).plot.barh(ax=ax[1], "
        "color='#0EA5E9')\n"
        "ax[1].set_title('Top-10 keluarga peran')\n"
        "lv.sumber.value_counts().plot.pie(ax=ax[2], autopct='%.0f%%')\n"
        "ax[2].set_ylabel(''); ax[2].set_title('Sumber data')\n"
        "plt.tight_layout()"),
    nbf.v4.new_markdown_cell(
        "## Skill demand — apa yang benar-benar diminta pasar?"),
    nbf.v4.new_code_cell(
        "n = len(lv)\n"
        "top = sk.skill.value_counts().head(15)\n"
        "(top / n * 100).plot.barh(color='#7C3AED', figsize=(9, 5))\n"
        "plt.xlabel('% lowongan'); plt.title('Share skill demand')\n"
        "plt.show()\nprint(top)"),
    nbf.v4.new_markdown_cell(
        "## Skill signature per domain\n"
        "Top-3 skill per domain — menunjukkan bedanya tuntutan tiap segmen IT."),
    nbf.v4.new_code_cell(
        "sig = (sk.merge(lv[['id_lowongan','domain']], on='id_lowongan')\n"
        "         .groupby(['domain','skill']).size().rename('n')\n"
        "         .reset_index()\n"
        "         .sort_values(['domain','n'], ascending=[True,False])\n"
        "         .groupby('domain').head(3))\n"
        "print(sig.to_string(index=False))"),
    nbf.v4.new_markdown_cell("## Geografi & cara kerja"),
    nbf.v4.new_code_cell(
        "fig, ax = plt.subplots(1, 2, figsize=(13, 4))\n"
        "lv.provinsi.value_counts().head(10).plot.barh(ax=ax[0])\n"
        "ax[0].set_title('Top provinsi')\n"
        "ax[1].bar(['remote', 'hybrid', 'fresh_grad'],\n"
        "          [lv.remote.mean(), lv.hybrid.mean(), lv.fresh_grad_ok.mean()])\n"
        "ax[1].set_title('Share lowongan'); plt.tight_layout()"),
    nbf.v4.new_markdown_cell(
        "## Gaji — analisis terbatas pada lowongan transparan\n"
        "Hanya ~3% lowongan menampilkan gaji — coverage sangat bias."),
    nbf.v4.new_code_cell(
        "bg = lv.dropna(subset=['gaji_max_jt'])\n"
        "print(f'{len(bg)}/{len(lv)} lowongan bergaji')\n"
        "(bg.groupby('role_family').gaji_max_jt.median().sort_values()\n"
        "   .plot.barh(figsize=(8,4), color='#16A34A'))\n"
        "plt.xlabel('Median gaji max (Rp jt/bln)'); plt.show()"),
    nbf.v4.new_markdown_cell(
        "## Insight utama\n"
        "1. Pasar IT/data RI terkonsentrasi ekstrem di DKI Jakarta.\n"
        "2. Software Engineering = segmen terbesar; Data & Analytics "
        "masih terbesar kedua — dua dunia dengan skill signature beda.\n"
        "3. Dua platform, dua pasar: Kalibrr=UKM/lokal, "
        "LinkedIn=enterprise/multinasional.\n"
        "4. Remote murni langka — hybrid mulai muncul tapi minoritas.\n"
        "5. Transparansi gaji sangat rendah: analisis gaji bias.\n"
        "6. Search job board noisy: hanya sebagian hasil benar-benar "
        "relevan — filtering adalah bagian inti pipeline."),
]
nb.cells = cells
nbf.write(nb, "notebooks/01_job_market_eda.ipynb")
print("notebook dibuat")
