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

    def fulfill_offer(self, offer_id: str, buyer) -> bool:
        if offer_id not in self.offers:
            return False
        offer = self.offers[offer_id]
        if buyer.state.wallet >= offer.price:
            buyer.state.wallet -= offer.price
            buyer.state.inventory[offer.item] = buyer.state.inventory.get(offer.item, 0) + offer.quantity
            # In a real impl, we'd credit the seller too here
            del self.offers[offer_id]
            return True
        return False