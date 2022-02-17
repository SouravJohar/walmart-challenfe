class Seat:

    def __init__(self, id, blocked=False, reserved=False, reservation_id=None):
        self.id = id
        self.blocked = blocked
        self.reserved = reserved
        self.reservation_id = reservation_id
