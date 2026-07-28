from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from fraud_detection.config import FraudRuleConfig
from fraud_detection.domain.models import RuleEvidence, Transaction


class FraudRule(ABC):
    rule_id: str
    description: str
    weight: int

    @abstractmethod
    def evaluate(self, transaction: Transaction, history: Sequence[Transaction]) -> RuleEvidence | None:
        raise NotImplementedError


class HighAmountRule(FraudRule):
    rule_id = "high_amount"
    description = "Valor da transação acima do limite configurado para alto valor."
    weight = 35

    def __init__(self, threshold: float) -> None:
        self.threshold = threshold

    def evaluate(self, transaction: Transaction, history: Sequence[Transaction]) -> RuleEvidence | None:
        if transaction.amount <= self.threshold:
            return None
        return RuleEvidence(self.rule_id, self.description, self.weight, {"threshold": self.threshold})


class ProfileMismatchRule(FraudRule):
    rule_id = "profile_amount_mismatch"
    description = "Valor incompatível com o perfil usual do cliente sintético."
    weight = 25

    def __init__(self, multiplier: float) -> None:
        self.multiplier = multiplier

    def evaluate(self, transaction: Transaction, history: Sequence[Transaction]) -> RuleEvidence | None:
        limit = transaction.customer_profile_amount * self.multiplier
        if transaction.amount <= limit:
            return None
        return RuleEvidence(self.rule_id, self.description, self.weight, {"profile_limit": round(limit, 2)})


class RiskyLocationRule(FraudRule):
    rule_id = "risky_location"
    description = "UF da transação presente na lista educacional de risco configurada."
    weight = 20

    def __init__(self, risky_states: frozenset[str]) -> None:
        self.risky_states = risky_states

    def evaluate(self, transaction: Transaction, history: Sequence[Transaction]) -> RuleEvidence | None:
        if transaction.state not in self.risky_states:
            return None
        return RuleEvidence(self.rule_id, self.description, self.weight, {"state": transaction.state})


class BurstTransactionRule(FraudRule):
    rule_id = "burst_transactions"
    description = "Múltiplas transações do mesmo cliente sintético ocorreram em intervalo curto."
    weight = 30

    def __init__(self, window_seconds: int, min_transactions: int) -> None:
        self.window_seconds = window_seconds
        self.min_transactions = min_transactions

    def evaluate(self, transaction: Transaction, history: Sequence[Transaction]) -> RuleEvidence | None:
        lower_bound = transaction.event_timestamp.timestamp() - self.window_seconds
        count = sum(
            1
            for item in history
            if item.customer_id == transaction.customer_id and item.event_timestamp.timestamp() >= lower_bound
        )
        if count + 1 < self.min_transactions:
            return None
        return RuleEvidence(
            self.rule_id,
            self.description,
            self.weight,
            {"window_seconds": self.window_seconds, "transactions_in_window": count + 1},
        )


class DeviceChangeRule(FraudRule):
    rule_id = "device_change"
    description = "Tipo de dispositivo diferente do dispositivo usual do cliente sintético."
    weight = 15

    def evaluate(self, transaction: Transaction, history: Sequence[Transaction]) -> RuleEvidence | None:
        if transaction.device_type != transaction.customer_usual_device_type:
            return RuleEvidence(
                self.rule_id,
                self.description,
                self.weight,
                {
                    "device_type": transaction.device_type,
                    "usual_device_type": transaction.customer_usual_device_type,
                },
            )
        return None


class UnusualHourRule(FraudRule):
    rule_id = "unusual_hour"
    description = "Transação ocorreu em uma janela de horário incomum."
    weight = 10

    def __init__(self, unusual_hours: frozenset[int]) -> None:
        self.unusual_hours = unusual_hours

    def evaluate(self, transaction: Transaction, history: Sequence[Transaction]) -> RuleEvidence | None:
        hour = transaction.event_timestamp.hour
        if hour not in self.unusual_hours:
            return None
        return RuleEvidence(self.rule_id, self.description, self.weight, {"hour": hour})


class CombinedSignalsRule(FraudRule):
    rule_id = "combined_risk_signals"
    description = "Sinais de valor, localização e dispositivo se combinam em um alerta mais forte."
    weight = 20

    def __init__(self, high_amount_threshold: float, risky_states: frozenset[str]) -> None:
        self.high_amount_threshold = high_amount_threshold
        self.risky_states = risky_states

    def evaluate(self, transaction: Transaction, history: Sequence[Transaction]) -> RuleEvidence | None:
        high_amount = transaction.amount > self.high_amount_threshold * 0.75
        risky_location = transaction.state in self.risky_states
        changed_state = transaction.state != transaction.customer_home_state
        if high_amount and risky_location and changed_state:
            return RuleEvidence(
                self.rule_id,
                self.description,
                self.weight,
                {"state": transaction.state, "home_state": transaction.customer_home_state},
            )
        return None


def build_default_rules(config: FraudRuleConfig) -> list[FraudRule]:
    return [
        HighAmountRule(config.high_amount_threshold),
        ProfileMismatchRule(config.profile_amount_multiplier),
        RiskyLocationRule(config.risky_states),
        BurstTransactionRule(config.burst_window_seconds, config.burst_min_transactions),
        DeviceChangeRule(),
        UnusualHourRule(config.unusual_hours),
        CombinedSignalsRule(config.high_amount_threshold, config.risky_states),
    ]
