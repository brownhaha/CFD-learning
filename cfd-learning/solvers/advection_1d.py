from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class AdvectionConfig:
    nx: int = 200
    length: float = 1.0
    speed: float = 1.0
    cfl: float = 0.8
    final_time: float = 1.0
    initial: str = "gaussian"


def initial_condition(x: np.ndarray) -> np.ndarray:
    """A smooth pulse on a periodic domain."""
    return np.exp(-200.0 * (x - 0.3) ** 2)


def square_wave_initial_condition(x: np.ndarray) -> np.ndarray:
    """A discontinuous square pulse on a periodic domain."""
    return np.where((x >= 0.2) & (x <= 0.4), 1.0, 0.0)


def make_initial_condition(x: np.ndarray, name: str) -> np.ndarray:
    if name == "gaussian":
        return initial_condition(x)
    if name == "square":
        return square_wave_initial_condition(x)
    raise ValueError(f"Unknown initial condition: {name}")


def step_upwind_periodic(u: np.ndarray, config: AdvectionConfig, dt: float, dx: float) -> np.ndarray:
    """Advance one finite-volume step for positive advection speed."""
    a = config.speed
    if a <= 0.0:
        raise ValueError("This first lesson implements only positive advection speed.")

    flux_right = a * u
    flux_left = a * np.roll(u, 1)
    return u - dt / dx * (flux_right - flux_left)


def solve(config: AdvectionConfig) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    dx = config.length / config.nx
    x = (np.arange(config.nx) + 0.5) * dx
    u0 = make_initial_condition(x, config.initial)
    u = u0.copy()

    dt = config.cfl * dx / abs(config.speed)
    t = 0.0
    while t < config.final_time - 1e-14:
        dt_step = min(dt, config.final_time - t)
        u = step_upwind_periodic(u, config, dt_step, dx)
        t += dt_step

    return x, u0, u


def main() -> None:
    config = AdvectionConfig()
    x, u0, u = solve(config)

    l1_error = np.mean(np.abs(u - u0))
    linf_error = np.max(np.abs(u - u0))
    print(f"nx          = {config.nx}")
    print(f"CFL         = {config.cfl}")
    print(f"final_time  = {config.final_time}")
    print(f"L1 error    = {l1_error:.6e}")
    print(f"Linf error  = {linf_error:.6e}")

    output_dir = Path(__file__).resolve().parents[1] / "outputs"
    output_dir.mkdir(exist_ok=True)
    np.savez(output_dir / "advection_1d.npz", x=x, initial=u0, final=u)


if __name__ == "__main__":
    main()
