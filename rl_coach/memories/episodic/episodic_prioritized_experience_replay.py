#
# Copyright (c) 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import operator
import random
from enum import Enum
from typing import List, Tuple, Any

import numpy as np

from rl_coach.core_types import Transition, Episode
from rl_coach.memories.episodic.episodic_memory import EpisodicMemory
from rl_coach.memories.memory import MemoryGranularity
from rl_coach.memories.non_episodic.experience_replay import ExperienceReplayParameters, ExperienceReplay
from rl_coach.memories.non_episodic.prioritized_experience_replay import PrioritizedExperienceReplay, \
    PrioritizedExperienceReplayParameters
from rl_coach.schedules import Schedule, ConstantSchedule


class EpisodicPrioritizedExperienceReplayParameters(PrioritizedExperienceReplayParameters):
    def __init__(self):
        super().__init__()

    @property
    def path(self):
        return 'rl_coach.memories.episodic.episodic_prioritized_experience_replay:EpisodicPrioritizedExperienceReplay'


class EpisodicPrioritizedExperienceReplay(PrioritizedExperienceReplay, EpisodicMemory):
    """
    This is the episodic proportional sampling variant of the prioritized experience replay as described
    in https://arxiv.org/pdf/1511.05952.pdf.
    """
    def __init__(self, max_size: Tuple[MemoryGranularity, int], alpha: float=0.6, beta: Schedule=ConstantSchedule(0.4),
                 epsilon: float=1e-6, allow_duplicates_in_batch_sampling: bool=True):
        """
        :param max_size: the maximum number of transitions or episodes to hold in the memory
        :param alpha: the alpha prioritization coefficient
        :param beta: the beta parameter used for importance sampling
        :param epsilon: a small value added to the priority of each transition
        :param allow_duplicates_in_batch_sampling: allow having the same transition multiple times in a batch
        """
        super().__init__(max_size=max_size, alpha=alpha, beta=beta, epsilon=epsilon,
                         allow_duplicates_in_batch_sampling=allow_duplicates_in_batch_sampling)

    def store_episode(self, episode: Episode, lock: bool=True) -> None:
        """
        Store a new episode in the memory.
        :param episode: the new episode to store
        :param lock: should we lock the mutex
        :return: None
        """
        if lock:
            self.reader_writer_lock.lock_writing_and_reading()

        for t in episode.transitions:
            self.store(t, False)

        if lock:
            self.reader_writer_lock.release_writing_and_reading()
