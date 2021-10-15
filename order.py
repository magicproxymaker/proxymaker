from xml.etree.ElementTree import Element, SubElement, tostring

#############
# Constants #
#############
BRACKETS = (18, 36, 55, 72, 90, 108, 126, 144, 162, 180, 198, 216, 234, 396, 504, 612)
STOCK = ("(S27) Smooth", "(S30) Standard Smooth", "(S33) Superior Smooth", "(M31) Linen",
         "(A35) Thick Standard", "(P10) Plastic")

class OrderDetails(object):
    def __init__(self, cards, stock, back):
        # Total number of cards in the order
        self.quantity = len(cards)

        # The mpc "bracket" the order falls in
        self.bracket = self.min_bracket(cards)

        # The mpc card stock for the order
        self.stock = stock

        # Whether the cards should be foiled (is this an option?)
        self.foil = "false"

        # The list of cards
        self.cards = cards

        # The default card back, certain cards can override their back
        # TODO: Figure out what the cardback should be, probably will need to be
        # the location of the image going forward
        self.card_back = back

    def min_bracket(self, cards):
        """
        Determine the minimum bracket the order will fit in.
        """
        return str(min([i for i in BRACKETS if i > len(cards)]))

    def generate_xml(self):
        """
        Generates an xml file that the autofill script can use to automate
        MPC order generation.
        """
        root = Element("order")
        details = SubElement(root, "details")

        quantity = SubElement(details, "quantity")
        quantity.text = str(self.quantity)

        bracket = SubElement(details, "bracket")
        bracket.text = self.bracket

        stock = SubElement(details, "stock")
        stock.text = self.stock

        foil = SubElement(details, "foil")
        foil.text = str(self.foil)

        fronts = SubElement(root, "fronts")
        self.create_cards_xml(fronts, True)

        backs = SubElement(root, "backs")
        self.create_cards_xml(backs, False)

        cardback = SubElement(root, "cardback")
        cardback.text = self.card_back

        return tostring(root)

    def create_cards_xml(self, root, front):
        """
        Create the xml for the card section of the order

            root - The parent element in the element tree
            front - A bool indicating whether these cards are fronts or backs
        """
        for card in self.cards:
            if card.front is front:
                self.create_card_xml(card, root)

    def create_card_xml(self, card, root):
        """
        Create the xml for an individual card.

            root - The parent element in the element tree
            front - A bool indicating whether these cards are fronts or backs
        """
        card_elem = SubElement(root, "card")
        card_id = SubElement(card_elem, "id")
        card_id.text = card.id
        slots = SubElement(card_elem, "slots")
        slots.text = ",".join(card.slots)
        name = SubElement(card_elem, "name")
        name.text = card.name
        query = SubElement(card_elem, "query")
        query.text = card.query
        card_dir = SubElement(card_elem, "dir")
        card_dir.text = card.dir

class Card(object):
    def __init__(self, card_id, slots, name, query, dir, front):
        self.id = str(card_id)
        self.slots = [str(i) for i in slots]
        self.name = name
        self.query = query
        self.dir = dir
        self.front = front

if __name__ == "__main__":
    cards = []
    cards.append(Card(1, [1], "card1", "q1", "dir1", True))
    cards.append(Card(2, [2], "card2", "q2", "dir2", True))
    cards.append(Card(3, [3], "card3", "q3", "dir3", True))
    cards.append(Card(4, [4], "card4", "q4", "dir4", True))
    cards.append(Card(5, [4], "card5", "q5", "dir5", False))

    o = OrderDetails(cards, STOCK[1], "CARDBACK")

    print(o.generate_xml())