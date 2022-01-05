class Turn:
    def __init__(self, turn_number) -> None:
        self.turn_number = turn_number

    def get_turn_number(self) -> None:
        return self.turn_number

    def increment_turn_number(self) -> None:
        self.turn_number = self.turn_number + 1