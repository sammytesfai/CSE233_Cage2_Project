<a name="readme-top"></a>
<br />
<div align="center">
<h3 align="center">CSE 233 Project</h3>

  <p align="center">
    Training Red Adversarial Agent to Comprise Cage 2 Network
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

The project involves training a reinforcement learning agent to act as an attacker in a simulated network environment. Using a modified version of the CybORG environment, groups develop a red agent to compromise an Operational Server while a blue agent defends it. Key tasks include modifying agent functions and training processes, with performance evaluated based on rewards gained in the simulation.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

There are two solution we provide of a Red Agent compromising the Cage 2 Network. The First Agent uses a PPO algorithm based on <a href=https://github.com/john-cardiff/-cyborg-cage-2>John Cardiff's</a> solution, which is based on a blue agent defending. This implementation required some minor changes to decoys and decoys states to work for a red agent. "Gavin insert quick description of Static Red agent"</a>

### PPO Red Agent Approach

Since the current state of CybORG did not support a Red Agent adversary changes needed to be made to CybORG for error checking and rewards. Due to this we have created a docker image that contains these CybORG changes as well as our red agent implementation. To download the docker image follow the below steps:
* Step 1:
  ```sh
  Instructions to downloading and running docker image
  ```

### Static Sleep/BlineAgent
 
To demonstrate this implementation we have added a new agent that performs the recommended initial sleep cycles at the start of an episode and then follows with performing the actions from a BlineAgent. The code for this can be found in red_evaluation_static.py and LateStartAgent.py. This Agent produces an average reward of 190 over 100 episodes. To demonstrate this run the below command in the top directory of the repository:
* Step 1:
   ```sh
   python3 /cse_233_project/CSE233_Cage2_Project# python3 red_evaluation_static.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Team Members

* Jimmy Franknedy
* Neel Apte
* Gavin Cooke
* Sammy Tesfai


<!-- ACKNOWLEDGMENTS -->
## References

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>