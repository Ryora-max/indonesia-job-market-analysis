"""Bangun notebooks/01_job_market_eda.ipynb — EDA data riil."""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = [
    nbf.v4.new_markdown_cell(
        "# EDA — Indonesia Analytics Job Market\n"
        "Data riil: lowongan relevan (Kalibrr + LinkedIn guest API).\n"
        "**Catatan:** data ini bukan sintetis — noise dan missingness "
        "adalah bagian dari kenyataan data riil."),
    nbf.v4.new_code_cell(
        "import pandas as pd\nimport matplotlib.pyplot as plt\n"
        "import seaborn as sns\nsns.set_theme(style='whitegrid')\n"
        "lv = pd.read_csv('../data/processed/lowongan.csv')\n"
        "sk = pd.read_csv('../data/processed/job_skill.csv')\n"
        "print(lv.shape, sk.shape)\nlv.head()"),
    nbf.v4.new_markdown_cell("## Komposisi peran & sumber"),
    nbf.v4.new_code_cell(
        "fig, ax = plt.subplots(1, 2, figsize=(13, 4))\n"
        "lv.role_family.value_counts().plot.barh(ax=ax[0], color='#7C3AED')\n"
        "ax[0].set_title('Keluarga peran')\n"
        "lv.sumber.value_counts().plot.pie(ax=ax[1], autopct='%.0f%%')\n"
        "ax[1].set_ylabel(''); ax[1].set_title('Sumber data')\n"
        "plt.tight_layout()"),
    nbf.v4.new_markdown_cell(
        "## Skill demand — apa yang benar-benar diminta pasar?"),
    nbf.v4.new_code_cell(
        "n = len(lv)\n"
        "top = sk.skill.value_counts().head(15)\n"
        "(top / n * 100).plot.barh(color='#7C3AED', figsize=(9, 5))\n"
        "plt.xlabel('% lowongan'); plt.title('Share skill demand')\n"
        "plt.show()\nprint(top)"),
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
        "Hanya ~6% lowongan menampilkan gaji (Kalibrr saja)."),
    nbf.v4.new_code_cell(
        "bg = lv.dropna(subset=['gaji_max_jt'])\n"
        "print(f'{len(bg)}/{len(lv)} lowongan bergaji')\n"
        "(bg.groupby('role_family').gaji_max_jt.median().sort_values()\n"
        "   .plot.barh(figsize=(8,4), color='#16A34A'))\n"
        "plt.xlabel('Median gaji max (Rp jt/bln)'); plt.show()"),
    nbf.v4.new_markdown_cell(
        "## Insight utama\n"
        "1. Pasar analitik RI terkonsentrasi ekstrem di DKI Jakarta.\n"
        "2. Excel & SQL > Python: skill fundamental mengalahkan tools hype.\n"
        "3. Remote murni langka — hybrid mulai muncul tapi minoritas.\n"
        "4. Transparansi gaji sangat rendah: analisis gaji bias.\n"
        "5. Search job board noisy: ~8-17% hasil benar-benar relevan."),
]
nb.cells = cells
nbf.write(nb, "notebooks/01_job_market_eda.ipynb")
print("notebook dibuat")
