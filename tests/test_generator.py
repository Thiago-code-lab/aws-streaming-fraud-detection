from fraud_detection.generators.transaction_generator import TransactionGenerator


def test_generator_is_deterministic_with_seed() -> None:
    first = [item.to_dict() for item in TransactionGenerator(seed=42).generate(10)]
    second = [item.to_dict() for item in TransactionGenerator(seed=42).generate(10)]
    assert first == second


def test_generator_masks_card_tokens() -> None:
    transaction = TransactionGenerator(seed=42).generate(1)[0]
    assert transaction.masked_card.startswith("card_****_")
    assert len(transaction.masked_card) < 20
