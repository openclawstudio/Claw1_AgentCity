# Claw1_AgentCity

AgentCity is an autonomous metropolis where AI agents interact, trade, and build a digital society.

## Current Features (MVP Phase 1)
- **World Engine**: A grid-based environment with a heartbeat simulation loop.
- **Entity System**: Base classes for agents and physical assets.
- **Citizen Agents**: Self-governing agents with basic state management (energy, movement, goals).

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the simulation:
   ```bash
   python main.py
   ```

## Architecture
- `core/world.py`: Manages the spatial grid and simulation ticks.
- `core/agent.py`: Contains AI logic and citizen behaviors.
- `core/models.py`: Pydantic data models for serialization and state management.