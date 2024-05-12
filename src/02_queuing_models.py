import marimo

__generated_with = "0.5.2"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    return mo,


@app.cell
def __(mo):
    mo.md("# Queuing Models")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        """
        ## Infinite Queue Models

        Models of queues with infinite length need to take account of two characteristic properties:

        - The arrival rate, $\\lambda$
        - The departure rate, $\\mu$
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## The relationship between $\\lambda$ and $\mu$

            In Queuing theory $\\lambda$ represents the __arrival rate__, the number of people entering the system per time and $\\mu$ represents the __departure rate__, number of people leaving the system per time.

        ### $\\rho$ ($\\frac{\\lambda}{\\mu}$)
        $\\rho$ is the ratio of arrivals to departures given by: 

        $$\\rho = \\frac{\\lambda}{\\mu}$$

        or in Python:

        ```python
        def rho(arrival_rate: int, departure_rate: int) -> float:
                return arrival_rate / departure_rate
        ```

        ### Probability of $n$ elements being on queue ($p(n)$)

        $p(n) = \\rho^{n} \\times (1 - \\rho)$

        Or in Python:

        ```python
        def prob_of_n_on_queue(n: int, rho: float) -> float:
            return rho**n * (1 - rho)
        ```

        ### Probability of at most $n$ elements being on queue ($p(0..n)$)
        $p(0..n) = \sum_{x=0}^{n}{p(x)}$

        Or in Python: 

        ```python
        def prob_of_at_most_n_on_queue(n: int, rho: float) -> float:
            return sum(map(
                lambda n: prob_of_n_on_queue(n, rho),
                range(0, n+1)
            ))
        ```

        ### Probability of at more than $n$ elements being on queue ($p(n+1..)$)
        $p(n+1..) = 1 - p(0..n)$

        ```python
        def prob_of_more_than_n_on_queue(n: int, rho: float) -> float:
            return 1.0 - prob_of_at_most_n_on_queue(n)
        ```
        """
    )
    return


@app.cell
def __():
    # 8/9

    def rho(arrival_rate: int, departure_rate: int) -> float:
        return arrival_rate / departure_rate


    def prob_of_n_on_queue(n: int, rho: float) -> float:
        return rho**n * (1 - rho)

    def prob_of_at_most_n_on_queue(n: int, rho: float) -> float:
        return sum(map(
            lambda n: prob_of_n_on_queue(n, rho),
            range(0, n+1)
        ))

    def prob_of_more_than_n_on_queue(n: int, rho: float) -> float:
        return 1.0 - prob_of_at_most_n_on_queue(n)
        
    return (
        prob_of_at_most_n_on_queue,
        prob_of_more_than_n_on_queue,
        prob_of_n_on_queue,
        rho,
    )


@app.cell
def __(mo, prob_of_n_on_queue, rho):
    get_arrival, set_arrival = mo.state(1)
    get_departure, set_departure = mo.state(1)
    get_n, set_n = mo.state(1)

    get_rho, set_rho = mo.state(
        rho(arrival_rate=get_arrival(), departure_rate=get_departure())
    )

    p_of_n = prob_of_n_on_queue(
        n=get_arrival(),
        rho=float(get_rho())
    )

    arrival_slider = mo.ui.number(
        0, 12, 
        value=get_arrival(), 
        on_change=set_arrival,
        label="$Arrival \: time:$"
    )
    departure_slider = mo.ui.number(
        0, 12, 
        value=get_departure(), 
        on_change=set_departure,
        label="$Departure \: time:$"
    )
    n_slider = mo.ui.number(
        0, 12, 
        value=get_n(), 
        on_change=set_n,
        label="$Number \: of \: people \: in \: the \: queue:$"
    )
    return (
        arrival_slider,
        departure_slider,
        get_arrival,
        get_departure,
        get_n,
        get_rho,
        n_slider,
        p_of_n,
        set_arrival,
        set_departure,
        set_n,
        set_rho,
    )


@app.cell
def __(arrival_slider, departure_slider, n_slider):
    [arrival_slider, departure_slider, n_slider]
    return


@app.cell
def __(
    get_arrival,
    get_departure,
    get_n,
    mo,
    prob_of_at_most_n_on_queue,
    prob_of_n_on_queue,
    rho,
):
    mo.md(
        f"""
        ## Results

        $\\lambda =$ {get_arrival()}


        $\\mu =$ {get_departure()}

        $n =$ {get_n()}


        $\\rho =$ {rho(get_arrival(), get_departure())}

        $p_n$ {prob_of_n_on_queue(get_n(), rho(get_arrival(), get_departure()))}

        $p \: at \: least$ = {prob_of_at_most_n_on_queue(get_n(), rho(get_arrival(), get_departure()))}
        """
    )
    return


if __name__ == "__main__":
    app.run()
