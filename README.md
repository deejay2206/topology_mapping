# Passive Topology Mapping Algorithm
This algorithm is a topology mapping framework designed to model topology from the perspective of a passive observer. It conducts observability analysis by determining what a passive observer "may see" versus what they "should see." The algorithm creates a logical network topology by using physical topology data as input. The first step involves selecting observation points in the network to act as passive observers. Next, the physical network topology is translated into an adjacency matrix, where each network interface is represented as a node and the connections between devices are depicted as edges. The algorithm then performs the observability analysis based on this model.

# Topology Mapping Observer Framework
This project implements a passive observer-based topology mapping framework for modeling network structures in Cyber-Physical Systems (CPS). The framework conducts **observability analysis** by identifying what an observer "may see" versus what they "should see" based on physical network data.

## 🚀 Features

- Parses physical topology into graph structure
- Selects passive observation points
- Converts physical topology into an adjacency matrix
- Performs observability analysis
- (Optional) Visualizes physical and logical topology

## 🛠 Technologies

- Python 3.10+
- NetworkX
- NumPy / SciPy
- Matplotlib (for visualization)
- PyTest (for testing)

## 📦 Installation

```bash
git clone https://github.com/deejay2206/topology-mapping-observer.git
cd topology-mapping-observer
pip install -r requirements.txt

