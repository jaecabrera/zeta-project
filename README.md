# Goblin-Zeta 

This project uses reinforcement learning to train the AI agent. The goal of the AI is to navigate through the puzzle and reach the flag to complete the game.

Collateral to dangerous objects (spikes) or static objects (wall boxes) will punish the agent, on the flip side if the agent picks up any colored key (mushroom) or unlocks the 
appropriate colored door then the agent is rewarded. 

**Other +-Reward conditions are:**

* If agent unlocks wrong door with wrong key then (- reward)
* If agent did not get a reward within the time frame of 10 seconds then agent dies. (-reward)
* If agent tries to unlock a blue door with a red key then (-reward)
* If agent steps on spike then dies (-reward)
  
* If agent picks up a key (mushroom) then (+ reward)
* If agent unlocks door with right key then (+ reward)


A demo of the learning can be watched here (https://www.youtube.com/watch?v=qibslZMAvGM)

**Issues**:
* Long training time.
* Agent is glitching/training outside of the map.
