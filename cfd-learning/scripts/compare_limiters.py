from __future__ import annotations

import argparse
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "solvers"))

from advection_1d import AdvectionConfig, solve as solve_upwind  # noqa: E402
from advection_1d_muscl import LimiterName, MusclConfig, solve as solve_muscl  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare MUSCL slope limiters.")
    parser.add_argument(
        "--ic",
        choices=["gaussian", "square"],
        default="gaussian",
        help="Initial condition to compare.",
    )
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

    limiters: list[LimiterName] = ["minmod", "mc", "vanleer", "superbee"]
    colors = {
        "initial": "#111827",
        "upwind": "#2563eb",
        "minmod": "#dc2626",
        "mc": "#16a34a",
        "vanleer": "#9333ea",
        "superbee": "#ea580c",
    }

    x, u0, u_upwind = solve_upwind(AdvectionConfig(nx=200, cfl=0.8, final_time=1.0, initial=args.ic))
    exact_peak_x, exact_peak_u = peak_info(x, u0)

    results: list[tuple[str, np.ndarray, str]] = [
        ("first-order upwind", u_upwind, colors["upwind"]),
    ]
    for limiter in limiters:
        _, _, u = solve_muscl(MusclConfig(nx=200, cfl=0.8, final_time=1.0, limiter=limiter, initial=args.ic))
        results.append((f"MUSCL + {limiter}", u, colors[limiter]))

    fig, (ax, table_ax) = plt.subplots(
        2,
        1,
        figsize=(9.2, 7.0),
        gridspec_kw={"height_ratios": [4.6, 1.5]},
    )

    line_styles = {
        "initial": {"linestyle": "-", "marker": None, "markevery": None, "linewidth": 2.8},
        "first-order upwind": {"linestyle": "--", "marker": "o", "markevery": 18, "linewidth": 1.8},
        "MUSCL + minmod": {"linestyle": "-.", "marker": "s", "markevery": 19, "linewidth": 1.8},
        "MUSCL + mc": {"linestyle": ":", "marker": "^", "markevery": 20, "linewidth": 2.2},
        "MUSCL + vanleer": {"linestyle": (0, (5, 1, 1, 1)), "marker": "D", "markevery": 21, "linewidth": 1.8},
        "MUSCL + superbee": {"linestyle": (0, (7, 2)), "marker": "v", "markevery": 22, "linewidth": 1.9},
    }

    ax.plot(x, u0, color=colors["initial"], label="initial", **line_styles["initial"])
    table_rows = []
    for label, u, color in results:
        l1_error = float(np.mean(np.abs(u - u0)))
        peak_x, peak_u = peak_info(x, u)
        phase_dx = peak_x - exact_peak_x
        amp_du = peak_u - exact_peak_u
        table_rows.append([label, f"{l1_error:.3e}", f"{peak_u:.6f}", f"{amp_du:+.6f}", f"{phase_dx:+.6f}"])
        ax.plot(
            x,
            u,
            color=color,
            label=label,
            markerfacecolor="white",
            markeredgewidth=0.8,
            markersize=4.5,
            **line_styles[label],
        )
        ax.scatter([peak_x], [peak_u], color=color, s=28, zorder=5)

    ax.set_title(f"Limiter comparison for 1D MUSCL advection ({args.ic})")
    ax.set_xlabel("x")
    ax.set_ylabel("u")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False, ncols=2)

    table_ax.axis("off")
    table = table_ax.table(
        cellText=table_rows,
        colLabels=["scheme", "L1", "u_peak", "amp_du", "phase_dx"],
        loc="center",
        cellLoc="center",
        colLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.0, 1.35)
    fig.tight_layout()

    print("Limiter diagnostics")
    print(f"{'scheme':<24} {'L1':>12} {'u_peak':>10} {'amp_du':>10} {'phase_dx':>10}")
    for row in table_rows:
        print(f"{row[0]:<24} {row[1]:>12} {row[2]:>10} {row[3]:>10} {row[4]:>10}")

    if args.save:
        output = figure_dir / f"limiter_comparison_{args.ic}.png"
        fig.savefig(output, dpi=180)
        plt.close(fig)
        print(f"Wrote {output}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
