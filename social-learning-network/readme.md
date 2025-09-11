# Social Learning Network Simulation

## Overview

This repository contains a Python implementation of a **Social Learning Network Simulation**, demonstrating how knowledge spreads through dynamic social networks of learning agents. The model illustrates how individual personality traits, social connections, and collaborative learning shape the emergence of expertise, innovation, and social hierarchies in human communities.

Agents representing individuals with distinct personality profiles and skill sets form social networks, share knowledge through teaching and observation, and collaborate on complex tasks. Through iterative social learning and network evolution, specialized communities of practice, knowledge flow patterns, and collaborative structures naturally emerge.

## Key Concepts

### Social Learning Theory

- **Social Learning**: The process by which individuals acquire knowledge, skills, and behaviors through observation and interaction with others
- **Network Effects**: How the structure of social connections influences information flow and learning outcomes
- **Expertise Development**: The emergence of specialized knowledge domains through focused learning and practice
- **Collaborative Intelligence**: How groups achieve better outcomes through complementary skills and knowledge sharing

### The Social Learning Problem

- How do personality traits influence network formation and learning behaviors?
- What network structures are most effective for knowledge transfer and innovation?
- How does collaboration on challenging tasks strengthen social bonds and collective intelligence?
- What factors lead to the emergence of expertise clusters and knowledge hierarchies?

## Model Description

### Environment

- **Social Space**: A dynamic network where agents form and dissolve connections based on compatibility and mutual benefit
- **Skill Domains**: Multiple areas of expertise (Technical, Creative, Social, Analytical)
- **Tasks**: Environmental challenges requiring different skill combinations and collaboration levels

### Agents

- **Personality Traits**: Each agent has three key personality characteristics:
  - **Curiosity**: Willingness to learn and explore new ideas (affects independent learning)
  - **Sociability**: Tendency to form and maintain social connections (affects network formation)
  - **Teaching**: Willingness to share knowledge with others (affects knowledge transfer effectiveness)

- **Skills**: Agents develop expertise in multiple domains through learning and practice
- **Social Network**: Dynamic connections with other agents based on personality compatibility and mutual benefit
- **Learning Mechanisms**: Multiple ways to acquire knowledge:
  - Independent learning through curiosity-driven exploration
  - Social learning from more skilled network connections
  - Collaborative learning through joint task performance

### Dynamics

1. **Network Formation**: Agents form social connections based on personality compatibility and skill complementarity
2. **Independent Learning**: Agents improve skills through self-directed exploration based on curiosity levels
3. **Social Learning**: Agents learn from more skilled network partners through teaching and observation
4. **Task Performance**: Individual and collaborative tasks test agent skills and strengthen successful partnerships
5. **Network Evolution**: Connections strengthen through positive interactions or weaken through neglect

### Parameters

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `num_agents` | Number of agents in the simulation | 50 |
| `num_skills` | Number of different skill domains | 4 |
| `max_connections` | Maximum social connections per agent | 5 |
| `curiosity_influence` | How much curiosity affects learning | 0.4 |
| `sociability_influence` | How much sociability affects networking | 0.3 |
| `teaching_influence` | How much teaching affects knowledge transfer | 0.3 |
| `self_learning_rate` | Rate of independent skill improvement | 0.02 |
| `social_learning_rate` | Rate of learning from others | 0.05 |
| `connection_threshold` | Minimum compatibility for connections | 0.6 |
| `collaboration_bonus` | Bonus for successful collaboration | 0.1 |

## Visualization

The simulation provides real-time visualization with two main components:

### Social Network Map
- **Node Colors**: Represent each agent's dominant skill domain
  - **Red**: Technical expertise
  - **Orange**: Creative expertise  
  - **Blue**: Social expertise
  - **Green**: Analytical expertise
- **Node Sizes**: Represent overall skill level of agents
- **Edge Thickness**: Represent strength of social connections
- **Network Layout**: Shows the structure of social relationships

### Evolution Metrics
- **Average Clustering**: How tightly connected local communities are
- **Network Density**: Overall connectivity of the social network
- **Learning Events**: Rate of knowledge transfer between agents
- **Task Success**: Effectiveness of individual and collaborative performance

## Installation and Usage

### Prerequisites

- Python 3.7+
- Required packages: numpy, matplotlib, networkx

### Installation

1. Clone this repository:
```bash
git clone https://github.com/FarshadAmiri/complex-systems-simulations/
cd complex-systems-simulations/social-learning-network
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Simulation

Execute the main simulation:
```bash
python run.py
```

The simulation will open an interactive window showing:
- The dynamic social learning network on the left
- Network evolution metrics and learning statistics on the right

### Customization

You can modify simulation parameters by editing the variables at the top of `run.py`:

```python
# Adjust these parameters to explore different scenarios
num_agents = 50                    # Population size
num_skills = 4                     # Number of skill domains
max_connections = 5                # Social network capacity
curiosity_influence = 0.4          # Independent learning drive
sociability_influence = 0.3        # Network formation tendency
teaching_influence = 0.3           # Knowledge sharing willingness
social_learning_rate = 0.05        # Speed of social learning
collaboration_bonus = 0.1          # Benefits of teamwork
```

## Scientific Insights

This simulation demonstrates several important principles of social learning and network science:

1. **Small World Networks**: Efficient knowledge transfer through clustered communities with occasional long-range connections
2. **Expertise Clustering**: Agents with similar skills tend to form specialized communities of practice
3. **Network Effects on Learning**: Well-connected agents learn faster and develop more diverse skills
4. **Collaborative Advantage**: Teams with complementary skills outperform individuals on complex tasks
5. **Personality-Network Interactions**: Different personality types create different network structures and learning patterns

## Emergent Phenomena

- **Knowledge Hubs**: Highly connected agents who become central to information flow
- **Specialization vs. Generalization**: Balance between developing deep expertise and broad skills
- **Community Formation**: Natural clustering of agents with compatible personalities and complementary skills
- **Innovation Networks**: Structures that promote creative collaboration and knowledge synthesis

## Possible Extensions

- **Cultural Learning**: Add cultural norms and values that spread through networks
- **Hierarchical Skills**: Implement prerequisite relationships between different skills
- **Geographic Constraints**: Limit connections based on spatial proximity
- **Competitive Tasks**: Include zero-sum scenarios that create competitive dynamics
- **Knowledge Obsolescence**: Skills that decay over time without practice
- **Mentorship Networks**: Explicit teacher-student relationships with different dynamics

## References

This simulation is inspired by research in:
- Social Learning Theory (Bandura, 1977)
- Social Network Analysis (Wasserman & Faust, 1994)
- Communities of Practice (Wenger, 1998)
- Complex Networks and Learning (Barabási, 2016)