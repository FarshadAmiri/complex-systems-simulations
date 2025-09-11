import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import random
from collections import defaultdict

"""
Social Learning Network Simulation

This simulation models how knowledge spreads through social networks of learning agents:
- Individual agents with personality traits and domain expertise
- Dynamic network formation based on compatibility and mutual benefit
- Multiple learning mechanisms (observation, teaching, experimentation)
- Environmental challenges requiring different skills and collaboration
- Emergence of expertise clusters, knowledge flow, and social hierarchies

Key Concepts:
- Agents have personality traits (curiosity, sociability, teaching) and skill levels
- Social connections form based on personality compatibility and skill complementarity
- Knowledge spreads through the network via teaching and observation
- Environmental tasks require different skill combinations
- Successful collaboration leads to stronger social bonds
"""

# ==== Parameters ====
num_agents = 50                    # Number of agents in the simulation
num_skills = 4                     # Number of different skill domains
max_connections = 5                # Maximum social connections per agent
max_iterations = 300               # Maximum simulation steps

# Personality trait parameters (each trait ranges from 0.0 to 1.0)
curiosity_influence = 0.4          # How much curiosity affects learning
sociability_influence = 0.3        # How much sociability affects network formation
teaching_influence = 0.3           # How much teaching affects knowledge transfer

# Learning parameters
self_learning_rate = 0.02          # Rate of independent skill improvement
social_learning_rate = 0.05        # Rate of learning from others
teaching_efficiency = 0.8          # How effectively teachers transfer knowledge
connection_threshold = 0.6         # Minimum compatibility for forming connections
task_difficulty = 0.7              # Difficulty level of environmental tasks

# Network dynamics
connection_decay = 0.01            # Rate at which unused connections weaken
collaboration_bonus = 0.1          # Bonus for successful collaboration
network_update_frequency = 5       # Steps between network updates

# Visualization parameters
update_interval = 300              # Milliseconds between animation frames

# Skill domains
SKILL_NAMES = ['Technical', 'Creative', 'Social', 'Analytical']
SKILL_COLORS = ['red', 'orange', 'blue', 'green']

class LearningAgent:
    """Represents an individual agent with personality traits and skills"""
    
    def __init__(self, agent_id):
        self.id = agent_id
        
        # Personality traits (0.0 to 1.0)
        self.curiosity = random.random()        # Willingness to learn and explore
        self.sociability = random.random()      # Tendency to form social connections
        self.teaching = random.random()         # Willingness to teach others
        
        # Skill levels (0.0 to 1.0) for each domain
        self.skills = np.array([random.random() for _ in range(num_skills)])
        
        # Social network
        self.connections = {}  # agent_id -> connection_strength
        self.connection_history = defaultdict(list)  # Track interaction quality
        
        # Learning history
        self.learning_events = []
        self.teaching_events = []
        
        # Task performance
        self.task_success_rate = 0.0
        self.collaboration_count = 0
        
    def get_personality_vector(self):
        """Get personality as a vector for compatibility calculation"""
        return np.array([self.curiosity, self.sociability, self.teaching])
    
    def calculate_compatibility(self, other_agent):
        """Calculate compatibility with another agent based on personality"""
        self_personality = self.get_personality_vector()
        other_personality = other_agent.get_personality_vector()
        
        # Euclidean distance in personality space (inverted for compatibility)
        distance = np.linalg.norm(self_personality - other_personality)
        compatibility = 1.0 - (distance / np.sqrt(3))  # Normalize to [0,1]
        
        # Bonus for complementary skills
        skill_complement = np.mean(np.abs(self.skills - other_agent.skills))
        compatibility += skill_complement * 0.3
        
        return min(1.0, max(0.0, compatibility))
    
    def can_form_connection(self, other_agent):
        """Check if agent can form a new connection"""
        if len(self.connections) >= max_connections:
            return False
        if other_agent.id in self.connections:
            return False
        
        compatibility = self.calculate_compatibility(other_agent)
        return compatibility > connection_threshold
    
    def form_connection(self, other_agent, initial_strength=0.5):
        """Form a bidirectional connection with another agent"""
        if self.can_form_connection(other_agent) and other_agent.can_form_connection(self):
            self.connections[other_agent.id] = initial_strength
            other_agent.connections[self.id] = initial_strength
            return True
        return False
    
    def strengthen_connection(self, other_agent_id, amount):
        """Strengthen connection based on positive interaction"""
        if other_agent_id in self.connections:
            self.connections[other_agent_id] = min(1.0, 
                self.connections[other_agent_id] + amount)
    
    def weaken_connections(self):
        """Gradually weaken unused connections"""
        to_remove = []
        for agent_id in self.connections:
            self.connections[agent_id] -= connection_decay
            if self.connections[agent_id] <= 0:
                to_remove.append(agent_id)
        
        for agent_id in to_remove:
            del self.connections[agent_id]
    
    def learn_independently(self):
        """Independent learning based on curiosity"""
        learning_boost = self.curiosity * self_learning_rate
        
        # Focus learning on weakest skills (exploration) or strongest skills (exploitation)
        if random.random() < self.curiosity:
            # Exploration: improve weakest skill
            weakest_skill = np.argmin(self.skills)
            self.skills[weakest_skill] += learning_boost * 2
        else:
            # Exploitation: improve random skill
            skill_to_improve = random.randint(0, num_skills - 1)
            self.skills[skill_to_improve] += learning_boost
        
        # Keep skills in valid range
        self.skills = np.clip(self.skills, 0, 1)
    
    def learn_from_agent(self, teacher_agent, teacher_skill_domain):
        """Learn a specific skill from another agent"""
        if teacher_skill_domain >= len(self.skills):
            return False
        
        # Learning effectiveness based on teacher's skill and teaching ability
        teacher_skill_level = teacher_agent.skills[teacher_skill_domain]
        teaching_effectiveness = teacher_agent.teaching * teaching_efficiency
        
        # Student's learning ability
        learning_ability = self.curiosity * social_learning_rate
        
        # Calculate learning gain
        skill_gap = max(0, teacher_skill_level - self.skills[teacher_skill_domain])
        learning_gain = skill_gap * learning_ability * teaching_effectiveness
        
        if learning_gain > 0.01:  # Minimum threshold for meaningful learning
            self.skills[teacher_skill_domain] += learning_gain
            self.skills[teacher_skill_domain] = min(1.0, self.skills[teacher_skill_domain])
            
            # Record learning event
            self.learning_events.append({
                'teacher': teacher_agent.id,
                'skill': teacher_skill_domain,
                'gain': learning_gain
            })
            
            return True
        return False
    
    def teach_agent(self, student_agent):
        """Teach best skill to another agent"""
        if self.teaching < 0.3:  # Must be willing to teach
            return False
        
        # Find skill domain where teacher has significant advantage
        skill_advantages = self.skills - student_agent.skills
        best_teaching_skill = np.argmax(skill_advantages)
        
        if skill_advantages[best_teaching_skill] > 0.2:  # Significant skill gap
            success = student_agent.learn_from_agent(self, best_teaching_skill)
            if success:
                self.teaching_events.append({
                    'student': student_agent.id,
                    'skill': best_teaching_skill
                })
                return True
        return False
    
    def attempt_task(self, required_skills):
        """Attempt a task requiring specific skill levels"""
        # Task success probability based on skill match
        skill_match = np.mean([min(self.skills[i], required_skills[i]) 
                              for i in range(len(required_skills))])
        
        success_probability = skill_match / task_difficulty
        success = random.random() < success_probability
        
        # Update success rate
        self.task_success_rate = (self.task_success_rate * 0.9 + 
                                 (1.0 if success else 0.0) * 0.1)
        
        return success
    
    def collaborate_on_task(self, partners, required_skills):
        """Collaborate with other agents on a complex task"""
        # Combine skills of all collaborators
        combined_skills = np.copy(self.skills)
        for partner in partners:
            combined_skills = np.maximum(combined_skills, partner.skills)
        
        # Collaboration bonus
        collaboration_effectiveness = 1.0 + len(partners) * collaboration_bonus
        effective_skills = combined_skills * collaboration_effectiveness
        
        # Calculate success probability
        skill_match = np.mean([min(effective_skills[i], required_skills[i]) 
                              for i in range(len(required_skills))])
        
        success_probability = skill_match / task_difficulty
        success = random.random() < success_probability
        
        # Update collaboration count for all participants
        if success:
            self.collaboration_count += 1
            for partner in partners:
                partner.collaboration_count += 1
                # Strengthen connections
                if partner.id in self.connections:
                    self.strengthen_connection(partner.id, 0.1)
                if self.id in partner.connections:
                    partner.strengthen_connection(self.id, 0.1)
        
        return success
    
    def get_dominant_skill(self):
        """Return the skill domain where agent is strongest"""
        return np.argmax(self.skills)

class SocialLearningSimulation:
    """Main simulation class managing agents and their interactions"""
    
    def __init__(self):
        self.agents = [LearningAgent(i) for i in range(num_agents)]
        self.iteration = 0
        self.network_graph = nx.Graph()
        self.task_history = []
        self.network_metrics = []
        
        # Initialize network graph
        self.update_network_graph()
    
    def update_network_graph(self):
        """Update NetworkX graph representation of social network"""
        self.network_graph.clear()
        
        # Add all agents as nodes
        for agent in self.agents:
            self.network_graph.add_node(agent.id)
        
        # Add connections as edges
        for agent in self.agents:
            for connected_id, strength in agent.connections.items():
                if not self.network_graph.has_edge(agent.id, connected_id):
                    self.network_graph.add_edge(agent.id, connected_id, weight=strength)
    
    def form_new_connections(self):
        """Allow agents to form new social connections"""
        # Randomly pair agents to check for potential connections
        potential_pairs = [(i, j) for i in range(num_agents) 
                          for j in range(i+1, num_agents)]
        random.shuffle(potential_pairs)
        
        connections_formed = 0
        for i, j in potential_pairs[:num_agents//2]:  # Limit attempts per iteration
            agent_i, agent_j = self.agents[i], self.agents[j]
            
            if agent_i.form_connection(agent_j):
                connections_formed += 1
        
        return connections_formed
    
    def social_learning_phase(self):
        """Agents learn from their social connections"""
        learning_events = 0
        
        for agent in self.agents:
            # Find connected agents who could be teachers
            potential_teachers = [self.agents[conn_id] for conn_id in agent.connections
                                 if agent.connections[conn_id] > 0.3]
            
            if potential_teachers:
                # Choose teacher based on connection strength and teaching ability
                teacher_weights = [agent.connections[t.id] * t.teaching 
                                 for t in potential_teachers]
                
                if max(teacher_weights) > 0:
                    teacher = potential_teachers[np.argmax(teacher_weights)]
                    if teacher.teach_agent(agent):
                        learning_events += 1
                        # Strengthen connection on successful learning
                        agent.strengthen_connection(teacher.id, 0.05)
        
        return learning_events
    
    def generate_task(self):
        """Generate a random task requiring specific skills"""
        # Create task with random skill requirements
        required_skills = np.random.rand(num_skills) * 0.8 + 0.2  # Between 0.2 and 1.0
        return required_skills
    
    def task_assignment_phase(self):
        """Assign tasks to agents and track performance"""
        # Generate multiple tasks
        num_tasks = max(1, num_agents // 10)
        successful_tasks = 0
        
        for _ in range(num_tasks):
            task_skills = self.generate_task()
            
            # Randomly choose between individual and collaborative tasks
            if random.random() < 0.7:  # Individual task
                agent = random.choice(self.agents)
                if agent.attempt_task(task_skills):
                    successful_tasks += 1
            else:  # Collaborative task
                # Select agents with strong connections
                connected_agents = [agent for agent in self.agents 
                                  if len(agent.connections) > 0]
                if connected_agents:
                    leader = random.choice(connected_agents)
                    partners = [self.agents[conn_id] for conn_id in leader.connections
                              if leader.connections[conn_id] > 0.5][:3]  # Max 3 partners
                    
                    if leader.collaborate_on_task(partners, task_skills):
                        successful_tasks += 1
            
            self.task_history.append({
                'iteration': self.iteration,
                'required_skills': task_skills,
                'success': successful_tasks > 0
            })
        
        return successful_tasks
    
    def calculate_network_metrics(self):
        """Calculate network analysis metrics"""
        if len(self.network_graph.edges()) == 0:
            return {
                'avg_clustering': 0,
                'avg_path_length': 0,
                'network_density': 0,
                'num_components': len(self.network_graph.nodes())
            }
        
        # Basic network metrics
        clustering = nx.average_clustering(self.network_graph)
        
        # Path length (only for connected components)
        components = list(nx.connected_components(self.network_graph))
        avg_path_lengths = []
        for component in components:
            if len(component) > 1:
                subgraph = self.network_graph.subgraph(component)
                avg_path_lengths.append(nx.average_shortest_path_length(subgraph))
        
        avg_path_length = np.mean(avg_path_lengths) if avg_path_lengths else 0
        density = nx.density(self.network_graph)
        
        return {
            'avg_clustering': clustering,
            'avg_path_length': avg_path_length,
            'network_density': density,
            'num_components': len(components)
        }
    
    def update_simulation(self):
        """Run one iteration of the simulation"""
        self.iteration += 1
        
        # Phase 1: Independent learning
        for agent in self.agents:
            agent.learn_independently()
        
        # Phase 2: Social learning
        learning_events = self.social_learning_phase()
        
        # Phase 3: Task assignment and performance
        successful_tasks = self.task_assignment_phase()
        
        # Phase 4: Network evolution
        if self.iteration % network_update_frequency == 0:
            # Form new connections
            new_connections = self.form_new_connections()
            
            # Weaken unused connections
            for agent in self.agents:
                agent.weaken_connections()
            
            # Update network graph
            self.update_network_graph()
        
        # Calculate metrics
        network_metrics = self.calculate_network_metrics()
        network_metrics['iteration'] = self.iteration
        network_metrics['learning_events'] = learning_events
        network_metrics['successful_tasks'] = successful_tasks
        self.network_metrics.append(network_metrics)
        
        return network_metrics

# Global simulation instance
sim = None

def create_network_visualization(agents, network_graph):
    """Create a visualization of the social network"""
    if len(network_graph.nodes()) == 0:
        return plt.subplots(1, 1, figsize=(6, 6))
    
    # Create layout
    try:
        pos = nx.spring_layout(network_graph, k=1, iterations=50)
    except:
        pos = {i: (random.random(), random.random()) for i in network_graph.nodes()}
    
    # Node colors based on dominant skill
    node_colors = [SKILL_COLORS[agents[node_id].get_dominant_skill()] 
                   for node_id in network_graph.nodes()]
    
    # Node sizes based on overall skill level
    node_sizes = [np.sum(agents[node_id].skills) * 200 + 100 
                  for node_id in network_graph.nodes()]
    
    # Edge weights
    edge_weights = [network_graph[u][v]['weight'] * 3 
                    for u, v in network_graph.edges()]
    
    return pos, node_colors, node_sizes, edge_weights

def update_visualization(frame):
    """Update function for animation"""
    global sim
    
    # Update simulation
    metrics = sim.update_simulation()
    
    # Clear previous plots
    ax1.clear()
    ax2.clear()
    
    # Network visualization
    ax1.set_title(f'Social Learning Network - Iteration {sim.iteration}\n'
                  f'Connections: {len(sim.network_graph.edges())}, '
                  f'Learning Events: {metrics["learning_events"]}')
    
    if len(sim.network_graph.nodes()) > 0:
        pos, node_colors, node_sizes, edge_weights = create_network_visualization(
            sim.agents, sim.network_graph)
        
        # Draw network
        nx.draw_networkx_edges(sim.network_graph, pos, ax=ax1, 
                              width=edge_weights, alpha=0.6, edge_color='gray')
        nx.draw_networkx_nodes(sim.network_graph, pos, ax=ax1,
                              node_color=node_colors, node_size=node_sizes, alpha=0.8)
        
        # Add legend
        legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                                     markerfacecolor=color, markersize=10, label=skill)
                          for skill, color in zip(SKILL_NAMES, SKILL_COLORS)]
        ax1.legend(handles=legend_elements, loc='upper right')
    
    ax1.set_aspect('equal')
    ax1.axis('off')
    
    # Metrics visualization
    if len(sim.network_metrics) > 1:
        iterations = [m['iteration'] for m in sim.network_metrics]
        clustering = [m['avg_clustering'] for m in sim.network_metrics]
        density = [m['network_density'] for m in sim.network_metrics]
        learning = [m['learning_events'] for m in sim.network_metrics]
        
        ax2.plot(iterations, clustering, 'b-', label='Avg Clustering', linewidth=2)
        ax2.plot(iterations, density, 'r-', label='Network Density', linewidth=2)
        
        # Scale learning events to [0,1] range for visualization
        max_learning = max(learning) if max(learning) > 0 else 1
        scaled_learning = [l / max_learning for l in learning]
        ax2.plot(iterations, scaled_learning, 'g-', label='Learning Events (scaled)', linewidth=2)
        
        ax2.set_xlabel('Iteration')
        ax2.set_ylabel('Metric Value')
        ax2.set_title('Network Evolution Metrics')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 1)
    
    return []

def main():
    """Main simulation function"""
    global sim, ax1, ax2
    
    # Initialize simulation
    sim = SocialLearningSimulation()
    
    # Create figure with subplots
    fig = plt.figure(figsize=(15, 6))
    
    # Network plot
    ax1 = plt.subplot(1, 2, 1)
    
    # Metrics plot
    ax2 = plt.subplot(1, 2, 2)
    
    # Create animation
    ani = animation.FuncAnimation(fig, update_visualization, frames=max_iterations,
                                  interval=update_interval, repeat=False, blit=False)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()