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
    parser = argparse.ArgumentParser(description="Compare first-order upwind and MUSCL advection.")
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save the figure instead of opening an interactive window.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    figure_dir = ROOT / "figures"
    figure_dir.mkdir(exist_ok=True)

    upwind_config = AdvectionConfig(nx=200, cfl=0.8, final_time=1.0)
    muscl_config = MusclConfig(nx=200, cfl=0.8, final_time=1.0)

    x, u0, u_upwind = solve_upwind(upwind_config)
    _, _, u_muscl = solve_muscl(muscl_config)

    upwind_l1 = np.mean(np.abs(u_upwind - u0))
    muscl_l1 = np.mean(np.abs(u_muscl - u0))

    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.plot(x, u0, color="#111827", linewidth=2.2, label="initial")
    ax.plot(x, u_upwind, color="#2563eb", linewidth=2.0, label=f"first-order upwind, L1={upwind_l1:.3e}")
    ax.plot(x, u_muscl, color="#dc2626", linewidth=2.0, label=f"MUSCL + minmod, L1={muscl_l1:.3e}")
    ax.set_title("1D advection: first-order upwind vs MUSCL + minmod")
    ax.set_xlabel("x")
    ax.set_ylabel("u")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()

    if args.save:
        output = figure_dir / "upwind_vs_muscl.png"
        fig.savefig(output, dpi=180)
        plt.close(fig)
        print(f"Wrote {output}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
