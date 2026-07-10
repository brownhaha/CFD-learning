from __future__ import annotations

import argparse
from pathlib import Path
import sys

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "solvers"))

from advection_1d import AdvectionConfig, initial_condition, step_upwind_periodic  # noqa: E402


def run_history(
    config: AdvectionConfig,
    nframes: int = 120,
    perturb_high_frequency: bool = False,
) -> tuple[np.ndarray, list[np.ndarray], list[float]]:
    dx = config.length / config.nx
    x = (np.arange(config.nx) + 0.5) * dx
    u = initial_condition(x)
    if perturb_high_frequency:
        checkerboard = np.where(np.arange(config.nx) % 2 == 0, 1.0, -1.0)
        u = u + 1.0e-6 * checkerboard

    dt = config.cfl * dx / abs(config.speed)
    frame_interval = max(1, int(np.ceil(config.final_time / dt / nframes)))
    history = [u.copy()]
    times = [0.0]

    t = 0.0
    step = 0
    while t < config.final_time - 1e-14:
        dt_step = min(dt, config.final_time - t)
        u = step_upwind_periodic(u, config, dt_step, dx)
        t += dt_step
        step += 1
        if step % frame_interval == 0 or t >= config.final_time - 1e-14:
            history.append(u.copy())
            times.append(t)

    return x, history, times


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Animate CFL effects for 1D upwind advection.")
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save the animation as a GIF instead of opening an interactive window.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    figure_dir = ROOT / "figures"
    figure_dir.mkdir(exist_ok=True)

    configs = [
        AdvectionConfig(nx=200, cfl=0.8, final_time=1.0),
        AdvectionConfig(nx=200, cfl=1.2, final_time=0.55),
    ]
    labels = [
        "CFL = 0.8: stable but diffusive",
        "CFL = 1.2: unstable high-frequency mode",
    ]
    histories = [
        run_history(configs[0]),
        run_history(configs[1], perturb_high_frequency=True),
    ]
    nframes = min(len(item[1]) for item in histories)

    fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    lines = []
    time_texts = []

    for ax, (x, history, _times), label in zip(axes, histories, labels):
        u0 = history[0]
        ax.plot(x, u0, color="#111827", linewidth=1.6, linestyle="--", label="initial")
        (line,) = ax.plot(x, history[0], color="#2563eb", linewidth=2.0, label="current")
        lines.append(line)
        ax.set_title(label)
        ax.set_ylabel("u")
        ax.grid(True, alpha=0.25)
        ax.legend(frameon=False, loc="upper right")
        time_texts.append(ax.text(0.02, 0.88, "", transform=ax.transAxes))

    axes[-1].set_xlabel("x")
    axes[0].set_ylim(-0.1, 1.1)
    axes[1].set_ylim(-2.5, 2.5)

    def update(frame: int) -> list[object]:
        artists: list[object] = []
        for line, text, (_x, history, times) in zip(lines, time_texts, histories):
            idx = min(frame, len(history) - 1)
            line.set_ydata(history[idx])
            text.set_text(f"t = {times[idx]:.3f}")
            artists.extend([line, text])
        return artists

    ani = animation.FuncAnimation(fig, update, frames=nframes, interval=60, blit=True)
    fig.suptitle("Dynamic CFL effect in first-order upwind advection")
    fig.tight_layout()

    if args.save:
        output = figure_dir / "cfl_advection_animation.gif"
        ani.save(output, writer=animation.PillowWriter(fps=16))
        plt.close(fig)
        print(f"Wrote {output}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
