"""Graphs styles"""

import matplotlib.pyplot as plt
import seaborn as sns

def set_publication_style() -> None:
    """Tema limpio y elegante, apto para artículo científico."""
    plt.rcdefaults()  # reinicia a valores por defecto
    sns.set_theme(context="paper", style="ticks", palette="colorblind")

    plt.rcParams.update(
        {
            "figure.figsize": (6, 3),
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.labelsize": 10,
            "axes.titlesize": 11,
            "axes.grid": True,
            "grid.alpha": 0.3,
            "grid.linestyle": ":",
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.fontsize": 8,
            "figure.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.05,
        }
    )

