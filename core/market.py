import uuid
from typing import List, Dict, Optional
from .models import Offer

class Market:
    def __init__(self):
        self.offers: Dict[str, Offer] = {}

    def post_offer(self, agent_id: str, item: str, price: float, quantity: int, seller_inventory: Dict[str, int]) -> Optional[str]:
        # Validation: Ensure agent actually has the items before posting
        if seller_inventory.get(item, 0) < quantity:
            return None
            
        offer_id = str(uuid.uuid4())
        offer = Offer(id=offer_id, creator_id=agent_id, item=item, price=price, quantity=quantity)
        self.offers[offer_id] = offer
        return offer_id

    def cleanup_stale_offers(self, world_agents_map: dict):
        """Remove offers from agents who are no longer alive or present."""
        stale_ids = [
            oid for oid, offer in self.offers.items()
            if offer.creator_id not in world_agents_map or not world_agents_map[offer.creator_id].alive
        ]
        for oid in stale_ids:
            del self.offers[oid]

    def fulfill_offer(self, offer_id: str, buyer, world_agents_map: dict, tick: int, economy) -> bool:
        if offer_id not in self.offers:
            return False
        
        offer = self.offers[offer_id]
        seller = world_agents_map.get(offer.creator_id)
        
        # Prevent self-trading and validate seller existence
        if not seller or not seller.alive or seller.id == buyer.id:
            self.offers.pop(offer_id, None)
            return False

        # Double check seller still has inventory
        if seller.state.inventory.get(offer.item, 0) < offer.quantity:
            self.offers.pop(offer_id, None)
            return False

        if buyer.state.wallet >= offer.price:
            if economy.transfer(buyer, seller, offer.price, f"purchase_{offer.item}", tick):
                seller.state.inventory[offer.item] -= offer.quantity
                buyer.state.inventory[offer.item] = buyer.state.inventory.get(offer.item, 0) + offer.quantity
                self.offers.pop(offer_id, None)
                return True
        return False