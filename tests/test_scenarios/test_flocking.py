#  Copyright (c) 2022-2024.
#  ProrokLab (https://www.proroklab.org/)
#  All rights reserved.

import pytest

from vmas import make_env
from vmas.scenarios import flocking


class TestFlocking:
    def setup_env(
        self,
        n_envs,
        **kwargs,
    ) -> None:
        self.env = make_env(
            scenario="flocking",
            num_envs=n_envs,
            device="cpu",
            # Environment specific variables
            **kwargs,
        )
        self.env.seed(0)

    @pytest.mark.parametrize("n_agents", [1, 5])
    def test_heuristic(self, n_agents, n_steps=50, n_envs=4):
        self.setup_env(n_agents=n_agents, n_envs=n_envs)
        policy = flocking.HeuristicPolicy(True)

        obs = self.env.reset()

        for _ in range(n_steps):
            actions = []
            for i in range(n_agents):
                obs_agent = obs[i]

                action_agent = policy.compute_action(
                    obs_agent, self.env.agents[i].u_range
                )

                actions.append(action_agent)

            obs, new_rews, dones, _ = self.env.step(actions)
