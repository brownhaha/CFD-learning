from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "solvers"))

from advection_1d import AdvectionConfig, solve  # noqa: E402


def save_finite_volume_cell(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 2.8))
    ax.set_xlim(-0.2, 3.2)
    ax.set_ylim(-0.7, 1.2)
    ax.axis("off")

    faces = [0.0, 1.0, 2.0, 3.0]
    for face in faces:
        ax.plot([face, face], [-0.25, 0.45], color="black", linewidth=1.4)
    ax.plot([0.0, 3.0], [0.1, 0.1], color="black", linewidth=1.2)

    ax.fill_between([1.0, 2.0], -0.22, 0.42, color="#dbeafe", alpha=0.9)
    ax.text(1.5, 0.62, "cell i", ha="center", va="center", fontsize=14)
    ax.text(1.0, -0.45, r"$x_{i-\frac{1}{2}}$", ha="center", fontsize=12)
    ax.text(2.0, -0.45, r"$x_{i+\frac{1}{2}}$", ha="center", fontsize=12)

    ax.annotate(
        r"$F_{i-\frac{1}{2}}$",
        xy=(1.0, 0.15),
        xytext=(0.42, 0.82),
        arrowprops=dict(arrowstyle="->", linewidth=1.4),
        fontsize=13,
        ha="center",
    )
    ax.annotate(
        r"$F_{i+\frac{1}{2}}$",
        xy=(2.0, 0.15),
        xytext=(2.58, 0.82),
        arrowprops=dict(arrowstyle="->", linewidth=1.4),
        fontsize=13,
        ha="center",
    )

    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_advection_result(path: Path) -> None:
    config = AdvectionConfig()
    x, u0, u = solve(config)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(x, u0, color="#111827", linewidth=2.0, label="initial")
    ax.plot(x, u, color="#2563eb", linewidth=2.0, label="after one period")
    ax.set_xlabel("x")
    ax.set_ylabel("u")
    ax.set_title("1D linear advection: first-order upwind")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def main() -> None:
    figure_dir = ROOT / "figures"
    figure_dir.mkdir(exist_ok=True)
    save_finite_volume_cell(figure_dir / "finite_volume_cell.png")
    save_advection_result(figure_dir / "advection_result.png")
    print(f"Wrote figures to {figure_dir}")


if __name__ == "__main__":
    main()

