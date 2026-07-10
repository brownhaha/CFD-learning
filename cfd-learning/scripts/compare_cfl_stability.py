from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "solvers"))

from advection_1d import AdvectionConfig, solve  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare CFL stability for 1D upwind advection.")
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

    cfl_values = [0.8, 1.0, 1.2]
    fig, axes = plt.subplots(len(cfl_values), 1, figsize=(8, 8), sharex=True, sharey=False)

    for ax, cfl in zip(axes, cfl_values):
        config = AdvectionConfig(nx=200, cfl=cfl, final_time=1.0)
        x, u0, u = solve(config)
        l1_error = np.mean(np.abs(u - u0))

        ax.plot(x, u0, color="#111827", linewidth=1.8, label="initial")
        ax.plot(x, u, color="#2563eb", linewidth=1.8, label="final")
        ax.set_title(f"CFL = {cfl:.1f}, L1 error = {l1_error:.3e}")
        ax.set_ylabel("u")
        ax.grid(True, alpha=0.25)
        ax.legend(frameon=False, loc="upper right")

    axes[-1].set_xlabel("x")
    fig.suptitle("CFL stability comparison for first-order upwind advection", y=0.995)
    fig.tight_layout()

    if args.save:
        output = figure_dir / "cfl_stability_comparison.png"
        fig.savefig(output, dpi=180)
        plt.close(fig)
        print(f"Wrote {output}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
