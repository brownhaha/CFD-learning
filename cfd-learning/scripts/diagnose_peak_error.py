from __future__ import annotations

import argparse
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "solvers"))

from advection_1d import AdvectionConfig, solve as solve_upwind  # noqa: E402
from advection_1d_muscl import MusclConfig, solve as solve_muscl  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnose peak amplitude and phase errors.")
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save the figure instead of opening an interactive window.",
    )
    return parser.parse_args()


def peak_info(x: np.ndarray, u: np.ndarray) -> tuple[float, float]:
    peak_index = int(np.argmax(u))
    return float(x[peak_index]), float(u[peak_index])


def main() -> None:
    args = parse_args()
    figure_dir = ROOT / "figures"
    figure_dir.mkdir(exist_ok=True)

    upwind_config = AdvectionConfig(nx=200, cfl=0.8, final_time=1.0)
    muscl_config = MusclConfig(nx=200, cfl=0.8, final_time=1.0)

    x, u0, u_upwind = solve_upwind(upwind_config)
    _, _, u_muscl = solve_muscl(muscl_config)

    curves = [
        ("initial", u0, "#111827"),
        ("first-order upwind", u_upwind, "#2563eb"),
        ("MUSCL + minmod", u_muscl, "#dc2626"),
    ]

    exact_peak_x, exact_peak_u = peak_info(x, u0)

    fig, (ax, table_ax) = plt.subplots(
        2,
        1,
        figsize=(8.5, 6.2),
        gridspec_kw={"height_ratios": [4.0, 1.2]},
    )
    table_rows = []
    for label, u, color in curves:
        px, pu = peak_info(x, u)
        phase_error = px - exact_peak_x
        amplitude_error = pu - exact_peak_u
        table_rows.append([label, f"{px:.6f}", f"{pu:.6f}", f"{phase_error:+.6f}", f"{amplitude_error:+.6f}"])
        ax.plot(x, u, color=color, linewidth=2.0, label=label)
        ax.scatter([px], [pu], color=color, s=42, zorder=5)

    ax.set_title("Peak diagnostics: amplitude error and phase error")
    ax.set_xlabel("x")
    ax.set_ylabel("u")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False)

    table_ax.axis("off")
    table = table_ax.table(
        cellText=table_rows,
        colLabels=["scheme", "x_peak", "u_peak", "phase_dx", "amp_du"],
        loc="center",
        cellLoc="center",
        colLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.0, 1.35)
    fig.tight_layout()

    if args.save:
        output = figure_dir / "peak_error_diagnostics.png"
        fig.savefig(output, dpi=180)
        plt.close(fig)
        print(f"Wrote {output}")
    else:
        plt.show()

    print("Peak diagnostics")
    print(f"{'scheme':<22} {'x_peak':>10} {'u_peak':>10} {'phase_dx':>10} {'amp_du':>10}")
    for label, u, _color in curves:
        px, pu = peak_info(x, u)
        print(f"{label:<22} {px:10.6f} {pu:10.6f} {px - exact_peak_x:10.6f} {pu - exact_peak_u:10.6f}")


if __name__ == "__main__":
    main()
