import uuid
import random
import logging
from .market import Market
from .agent import Citizen

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class CityWorld:
    def __init__(self, width: int = 20, height: int = 20):
        self.width = width
        self.height = height
        self.ticks = 0
        self.market = Market()
        self.agents = {}
        self.market.on_trade_executed.append(self._settle_trade)

    def spawn_agent(self):
        agent_id = f"agent_{self.uuid_id()}"
        agent = Citizen(
            agent_id=agent_id,
            x=random.randint(0, self.width-1),
            y=random.randint(0, self.height-1)
        )
        self.agents[agent_id] = agent
        logger.info(f"Citizen {agent_id} moved into the city as a {agent.state.profession.value}.")

    def _settle_trade(self, tx):
        buyer = self.agents.get(tx['buyer_id'])
        seller = self.agents.get(tx['seller_id'])
        
        # Atomic trade: only update if both parties still exist
        if buyer and seller:
            buyer.handle_trade_event(tx)
            seller.handle_trade_event(tx)

    def tick(self):
        self.ticks += 1
        
        # Sustain population
        if len(self.agents) < 15:
            self.spawn_agent()

        agent_ids = list(self.agents.keys())
        for a_id in agent_ids:
            if a_id not in self.agents: continue
            agent = self.agents[a_id]
            
            try:
                agent.step(self)
            except Exception as e:
                logger.error(f"Error in agent {a_id} step: {e}")
            
            if agent.state.energy <= 0:
                logger.info(f"Citizen {a_id} has left the city (energy depletion).")
                self._cleanup_agent_orders(a_id)
                del self.agents[a_id]
        
        return {
            "tick": self.ticks,
            "transactions": len(self.market.transaction_history),
            "population": len(self.agents)
        }

    def _cleanup_agent_orders(self, agent_id: str):
        for res in self.market.order_book:
            self.market.order_book[res] = [
                o for o in self.market.order_book[res] if o.agent_id != agent_id
            ]

    @staticmethod
    def uuid_id():
        return str(uuid.uuid4())[:8]