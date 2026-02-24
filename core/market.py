import uuid
from typing import List, Dict
from .models import Offer

class Market:
    def __init__(self):
        self.offers: Dict[str, Offer] = {}

    def post_offer(self, agent_id: str, item: str, price: float, quantity: int) -> str:
        offer_id = str(uuid.uuid4())
        offer = Offer(id=offer_id, creator_id=agent_id, item=item, price=price, quantity=quantity)
        self.offers[offer_id] = offer
        return offer_id

    def fulfill_offer(self, offer_id: str, buyer, world_agents: list, tick: int, economy) -> bool:
        if offer_id not in self.offers:
            return False
        
        offer = self.offers[offer_id]
        seller = next((a for a in world_agents if a.id == offer.creator_id), None)
        
        if not seller or seller.state.inventory.get(offer.item, 0) < offer.quantity:
            # Seller either disappeared or no longer has the goods
            if offer_id in self.offers: del self.offers[offer_id]
            return False

        if buyer.state.wallet >= offer.price:
            # Execute transaction through economy manager for record keeping
            if economy.transfer(buyer, seller, offer.price, f"purchase_{offer.item}", tick):
                # Update Inventories
                seller.state.inventory[offer.item] -= offer.quantity
                buyer.state.inventory[offer.item] = buyer.state.inventory.get(offer.item, 0) + offer.quantity
                
                del self.offers[offer_id]
                return True
        return False