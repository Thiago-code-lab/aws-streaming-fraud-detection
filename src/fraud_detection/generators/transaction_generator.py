from __future__ import annotations

import random
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from typing import Iterator

from fraud_detection.domain.models import CustomerProfile, Transaction

STATES = ("SP", "RJ", "MG", "PR", "SC", "RS", "BA", "PE", "GO", "DF", "AC", "RR", "RO")
DEVICES = ("mobile", "desktop", "pos")
CATEGORIES = ("grocery", "fuel", "electronics", "travel", "restaurant", "marketplace")


@dataclass(frozen=True)
class TransactionGenerator:
    seed: int | None = None
    profile_count: int = 50

    def generate(self, count: int) -> list[Transaction]:
        if count < 0:
            raise ValueError("count deve ser não negativo")
        rng = random.Random(self.seed)
        profiles = self._build_profiles(rng)
        start = datetime(2026, 1, 1, tzinfo=UTC)
        transactions: list[Transaction] = []
        for index in range(count):
            profile = rng.choice(profiles)
            timestamp = start + timedelta(seconds=index * rng.randint(20, 180))
            transaction = self._build_transaction(rng, profile, timestamp, index)
            transactions.append(transaction)
        return transactions

    def iter_generate(self, count: int) -> Iterator[Transaction]:
        yield from self.generate(count)

    def _build_profiles(self, rng: random.Random) -> list[CustomerProfile]:
        return [
            CustomerProfile(
                customer_id=f"cust_{index:04d}",
                home_state=rng.choice(STATES[:10]),
                usual_device_type=rng.choice(DEVICES),
                typical_amount=round(rng.uniform(35.0, 1_200.0), 2),
            )
            for index in range(self.profile_count)
        ]

    def _build_transaction(
        self,
        rng: random.Random,
        profile: CustomerProfile,
        timestamp: datetime,
        index: int,
    ) -> Transaction:
        suspicious = rng.random() < 0.12
        amount = self._amount_for(rng, profile, suspicious)
        state = rng.choice(("AC", "RR", "RO")) if suspicious and rng.random() < 0.65 else profile.home_state
        device = (
            rng.choice([item for item in DEVICES if item != profile.usual_device_type])
            if suspicious and rng.random() < 0.5
            else profile.usual_device_type
        )
        card_token = sha256(f"{self.seed}:{profile.customer_id}:{index}".encode()).hexdigest()[:10]
        return Transaction(
            transaction_id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"{self.seed}:{index}:{profile.customer_id}")),
            event_timestamp=timestamp,
            amount=amount,
            state=state,
            device_type=device,
            customer_id=profile.customer_id,
            customer_profile_amount=profile.typical_amount,
            customer_home_state=profile.home_state,
            customer_usual_device_type=profile.usual_device_type,
            masked_card=f"card_****_{card_token}",
            merchant_category=rng.choice(CATEGORIES),
        )

    @staticmethod
    def _amount_for(rng: random.Random, profile: CustomerProfile, suspicious: bool) -> float:
        if suspicious:
            return round(profile.typical_amount * rng.uniform(3.5, 9.0), 2)
        return round(max(1.0, rng.gauss(profile.typical_amount, profile.typical_amount * 0.25)), 2)
