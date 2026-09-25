
import random

# Idadi ya bits za seed — inatosha kutoa nafasi kubwa ya seed
# zisizogongana (collision) bila kuzidisha ukubwa wa namba bure
_SEED_BITS = 32
_SEED_MAX = (2 ** _SEED_BITS) - 1


def generate_seed() -> int:
    """
    Huzalisha seed mpya, isiyotabirika, kwa ajili ya kuzalisha swali
    JIPYA (si kurudia lililopo). Hutumia `random.SystemRandom`, ambayo
    inachota nasibu kutoka kwa mfumo wa uendeshaji (OS-level entropy),
    hivyo haitabiriki — tofauti na RNG ya kawaida ya `random.Random`.
    """
    return random.SystemRandom().randint(0, _SEED_MAX)



def get_rng(seed: int) -> random.Random:
    """
    Hurudisha RNG (random.Random) iliyowekwa seed maalum.

    Kutumia seed ile ile hapa daima kutatoa mfuatano ule ule wa
    namba za nasibu — ndiyo msingi wa "deterministic when using the
    same seed" iliyotajwa kwenye Technical Notes za ticket.
    """
    if not isinstance(seed, int):
        raise TypeError(f"seed must be an int, got: {type(seed).__name__}")
    return random.Random(seed)