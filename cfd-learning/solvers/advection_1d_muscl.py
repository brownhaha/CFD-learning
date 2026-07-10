from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from advection_1d import initial_condition


@dataclass(frozen=True)
class MusclConfig:
    nx: int = 200
    length: float = 1.0
    speed: float = 1.0
    cfl: float = 0.8
    final_time: float = 1.0


def minmod(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    same_sign = a * b > 0.0
    limited = np.sign(a) * np.minimum(np.abs(a), np.abs(b))
    return np.where(same_sign, limited, 0.0)


def compute_limited_slope(u: np.ndarray, dx: float) -> np.ndarray:
    backward = (u - np.roll(u, 1)) / dx
    forward = (np.roll(u, -1) - u) / dx
    return minmod(backward, forward)


def spatial_operator_muscl_periodic(u: np.ndarray, config: MusclConfig, dx: float) -> np.ndarray:
    a = config.speed
    if a <= 0.0:
        raise ValueError("This MUSCL lesson implements only positive advection speed.")

    slope = compute_limited_slope(u, dx)
    left_state_at_right_face = u + 0.5 * dx * slope
    flux_right = a * left_state_at_right_face
    flux_left = np.roll(flux_right, 1)
    return -(flux_right - flux_left) / dx


def step_muscl_periodic(u: np.ndarray, config: MusclConfig, dt: float, dx: float) -> np.ndarray:
    """Advance one step with TVD RK2 time integration."""
    k1 = spatial_operator_muscl_periodic(u, config, dx)
    u_stage = u + dt * k1
    k2 = spatial_operator_muscl_periodic(u_stage, config, dx)
    return 0.5 * u + 0.5 * (u_stage + dt * k2)


def solve(config: MusclConfig) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    dx = config.length / config.nx
    x = (np.arange(config.nx) + 0.5) * dx
    u0 = initial_condition(x)
    u = u0.copy()

    dt = config.cfl * dx / abs(config.speed)
    t = 0.0
    while t < config.final_time - 1e-14:
        dt_step = min(dt, config.final_time - t)
        u = step_muscl_periodic(u, config, dt_step, dx)
        t += dt_step

    return x, u0, u


def main() -> None:
    config = MusclConfig()
    x, u0, u = solve(config)

    l1_error = np.mean(np.abs(u - u0))
    linf_error = np.max(np.abs(u - u0))
    print(f"scheme      = MUSCL + minmod + TVD RK2")
    print(f"nx          = {config.nx}")
    print(f"CFL         = {config.cfl}")
    print(f"final_time  = {config.final_time}")
    print(f"L1 error    = {l1_error:.6e}")
    print(f"Linf error  = {linf_error:.6e}")

    output_dir = Path(__file__).resolve().parents[1] / "outputs"
    output_dir.mkdir(exist_ok=True)
    np.savez(output_dir / "advection_1d_muscl.npz", x=x, initial=u0, final=u)


if __name__ == "__main__":
    main()
