from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import numpy as np

from advection_1d import make_initial_condition

LimiterName = Literal["minmod", "mc", "vanleer", "superbee"]


@dataclass(frozen=True)
class MusclConfig:
    nx: int = 200
    length: float = 1.0
    speed: float = 1.0
    cfl: float = 0.8
    final_time: float = 1.0
    limiter: LimiterName = "minmod"
    initial: str = "gaussian"


def minmod(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    same_sign = a * b > 0.0
    limited = np.sign(a) * np.minimum(np.abs(a), np.abs(b))
    return np.where(same_sign, limited, 0.0)


def minmod_three(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return minmod(a, minmod(b, c))


def flux_limiter(r: np.ndarray, limiter: LimiterName) -> np.ndarray:
    if limiter == "minmod":
        return np.maximum(0.0, np.minimum(1.0, r))
    if limiter == "mc":
        return np.maximum(0.0, np.minimum(np.minimum(2.0 * r, 0.5 * (1.0 + r)), 2.0))
    if limiter == "vanleer":
        return (r + np.abs(r)) / (1.0 + np.abs(r))
    if limiter == "superbee":
        return np.maximum(0.0, np.maximum(np.minimum(2.0 * r, 1.0), np.minimum(r, 2.0)))
    raise ValueError(f"Unknown limiter: {limiter}")


def compute_limited_slope(u: np.ndarray, dx: float, limiter: LimiterName) -> np.ndarray:
    backward = (u - np.roll(u, 1)) / dx
    forward = (np.roll(u, -1) - u) / dx
    if limiter == "minmod":
        return minmod(backward, forward)
    if limiter == "mc":
        centered = 0.5 * (np.roll(u, -1) - np.roll(u, 1)) / dx
        return minmod_three(centered, 2.0 * backward, 2.0 * forward)

    eps = 1.0e-14
    denominator = np.where(np.abs(forward) > eps, forward, np.where(forward >= 0.0, eps, -eps))
    r = backward / denominator
    return flux_limiter(r, limiter) * forward


def spatial_operator_muscl_periodic(u: np.ndarray, config: MusclConfig, dx: float) -> np.ndarray:
    a = config.speed
    if a <= 0.0:
        raise ValueError("This MUSCL lesson implements only positive advection speed.")

    slope = compute_limited_slope(u, dx, config.limiter)
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
    u0 = make_initial_condition(x, config.initial)
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
    print(f"scheme      = MUSCL + {config.limiter} + TVD RK2")
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
