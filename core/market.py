import uuid
from typing import List, Dict, Optional
from .models import Offer

class Market:
    def __init__(self):
        self.offers: Dict[str, Offer] = {}

    def post_offer(self, agent_id: str, item: str, price: float, quantity: int) -> str:
        offer_id = str(uuid.uuid4())
        offer = Offer(id=offer_id, creator_id=agent_id, item=item, price=price, quantity=quantity)
        self.offers[offer_id] = offer
        return offer_id

    def fulfill_offer(self, offer_id: str, buyer, world_agents_map: dict, tick: int, economy) -> bool:
        """
        world_agents_map: Dict of agent_id -> agent object for O(1) lookup
        """
        if offer_id not in self.offers:
            return False
        
        offer = self.offers[offer_id]
        seller = world_agents_map.get(offer.creator_id)
        
        if not seller or not seller.alive or seller.state.inventory.get(offer.item, 0) < offer.quantity:
            # Seller either disappeared, died, or no longer has the goods
            self.offers.pop(offer_id, None)
            return False

        if buyer.state.wallet >= offer.price:
            # Execute transaction through economy manager
            if economy.transfer(buyer, seller, offer.price, f"purchase_{offer.item}", tick):
                # Update Inventories
                seller.state.inventory[offer.item] -= offer.quantity
                buyer.state.inventory[offer.item] = buyer.state.inventory.get(offer.item, 0) + offer.quantity
                
                # Remove offer after successful trade
                self.offers.pop(offer_id, None)
                return True
        return False