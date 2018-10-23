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
from typing import Tuple

from rl_coach.core_types import Episode
from rl_coach.memories.memory import Memory, MemoryGranularity


class EpisodicMemory(Memory):
    def __init__(self, max_size: Tuple[MemoryGranularity, int]):
        """
        :param max_size: the maximum number of objects to hold in the memory
        """
        super().__init__(max_size)

    def store_episode(self, episode: Episode) -> None:
        """
        Store a new episode in the memory.
        :param episode: the new episode to store
        :return: None
        """
        pass
