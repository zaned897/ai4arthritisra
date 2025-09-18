from pathlib import Path
import pandas as pd


def read_scope_csv(path: Path) -> pd.DataFrame:
    """
    Lee un CSV de osciloscopio con cabecera de dos filas:

        x-axis,1,2
        second,Volt,Volt

    Devuelve un DataFrame ordenado con columnas:
        time_s, 1_volt, 2_volt, ...
    """
    df = pd.read_csv(path, header=[0, 1], engine="python", comment="#")

    # Aplana el MultiIndex: ("1","Volt") → "1_volt"
    df.columns = [
        f"{name}_{unit}".strip().lower().replace(" ", "_")
        for name, unit in df.columns
    ]

    # Renombra la columna temporal a time_s
    time_col = next(c for c in df.columns if c.startswith("x-axis"))
    df = df.rename(columns={time_col: "time_s"})

    df = df.apply(pd.to_numeric, errors="coerce")     \
        .sort_values("time_s")                    \
        .reset_index(drop=True)

    df["time_us"] = df["time_s"] * 1e6               # <── multiplicar, no asignar escalar
    return df

