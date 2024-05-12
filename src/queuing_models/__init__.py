class QueueModel:
    arrival_rate: int
    departure_rate: int

    def __init__(arrival_rate: int, departure_rate: int) -> QueueModel:
        self.arrival_rate = arrival_rate
        self.departure_rate = departure_rate 

    def rho(self) -> float:
        """ρ = λ / μ"""
        return self.arrival_rate / self.departure_rate

    def probability_of_n_on_queue(n: int) -> float:
        return 

    def probability_of_n_on_queue