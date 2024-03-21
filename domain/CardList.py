from domain.Card import Card
from uuid import uuid4
class CardList:
    def __init__(self, name: str, cards: list[Card] = []) -> None:
        self.id = str("list-" + str(uuid4()))
        self.name = name
        self.cards = cards

    def get_id(self) -> str:
        return self.id
    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def set_name(self, name: str) -> None:
        self.name = name

    def get_name(self) -> str:
        return self.name

    def set_cards(self, cards: list[Card]) -> None:
        self.cards = cards

    def get_cards(self) -> list[Card]:
        return self.cards

    def reorderCardsByIdList(self, id_list: list[str]) -> None:
        cards = self.get_cards()
        card_to_id = {card.id: card for card in cards}
        ordered_cards = [card_to_id[id] for id in id_list if id in card_to_id]
        for card in cards:
            if card.id not in id_list:
                ordered_cards.append(card)
        self.set_cards(ordered_cards)