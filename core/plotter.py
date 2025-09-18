# core/plotter.py
from pathlib import Path
from typing import Mapping, Sequence, Optional
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils.style import set_publication_style


def _annotate_point(ax, x, y, text, color):
    """Coloca una flecha y etiqueta en (x, y)."""
    ax.annotate(
        text,
        xy=(x, y),
        xytext=(5, 5),
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->", lw=0.6, color=color),
        fontsize=8,
        color=color,
    )


def plot_trace(
    df: pd.DataFrame,
    channels: Sequence[str] = ("1_volt", "2_volt"),
    *,
    channel_labels: Mapping[str, str] | None = None,
    show_title: bool = True,
    outfile: Optional[Path] = None,
    time_column: str = "time_us",
    time_label: str = "Time (µs)",
    y_label: str = "Voltage (V)",
    file_format: str = "pdf"  # <── nuevo parámetro
) -> None:
    set_publication_style()

    fig, ax = plt.subplots()

    for ch in channels:
        if ch not in df.columns:
            print(f"[WARN] {ch} no existe en DataFrame")
            continue

        color = ax._get_lines.get_next_color()
        label = channel_labels.get(ch, ch) if channel_labels else ch
        ax.plot(df[time_column], df[ch], lw=0.8, label=label, color=color)

        y = df[ch].to_numpy()
        t = df[time_column].to_numpy()
        unidad = y_label[y_label.find("(")+1 : y_label.find(")")] if "(" in y_label else "unidades"
        _annotate_point(ax, t[np.argmax(y)], y.max(), f"max {y.max():.2f} {unidad}", color)
        _annotate_point(ax, t[np.argmin(y)], y.min(), f"min {y.min():.2f} {unidad}", color)

    ax.set_xlabel(time_label)
    ax.set_ylabel(y_label)
    if show_title:
        ax.set_title("Scope trace")
    ax.legend(frameon=False)

    if outfile:
        # Asegura extensión correcta
        outfile = outfile.with_suffix(f".{file_format}")
        fig.savefig(outfile, dpi=300, bbox_inches="tight", format=file_format)
        print("Figura guardada en", outfile.resolve())
    else:
        plt.show()

