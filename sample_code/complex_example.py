"""
Sample Python Code: High cyclomatic complexity and large parameter lists.
Contains multiple execution paths, branching loops, and high risk indicators.
"""

from typing import List, Dict, Any, Optional


def process_complex_transactions(
    transactions: List[Dict[str, Any]],
    user_tier: str,
    exchange_rate: float,
    discount_rate: float,
    apply_tax: bool,
    tax_rate: float,
    currency_symbol: str,
    max_limit: float,
    audit_log: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Complex transaction processing function with elevated cyclomatic complexity,
    excessive parameters, and multiple conditional branches.
    """
    total_processed = 0.0
    discounted_total = 0.0
    taxed_total = 0.0
    rejected_count = 0
    accepted_count = 0

    for tx in transactions:
        amount = tx.get("amount", 0.0)
        status = tx.get("status", "pending")
        tx_type = tx.get("type", "debit")

        if amount > 0:
            if status == "verified" or status == "authorized":
                if tx_type == "credit":
                    converted = amount * exchange_rate
                    if user_tier == "platinum":
                        fee = converted * 0.01
                    elif user_tier == "gold":
                        fee = converted * 0.02
                    elif user_tier == "silver":
                        fee = converted * 0.03
                    else:
                        fee = converted * 0.05

                    final_amount = converted - fee
                    if final_amount <= max_limit:
                        total_processed += final_amount
                        accepted_count += 1
                    else:
                        rejected_count += 1
                elif tx_type == "debit":
                    converted = amount * exchange_rate
                    if discount_rate > 0:
                        discounted = converted * (1.0 - discount_rate)
                    else:
                        discounted = converted
                    discounted_total += discounted

                    if apply_tax:
                        if tax_rate > 0.20:
                            taxed = discounted * (1.0 + 0.20)
                        elif tax_rate > 0.10:
                            taxed = discounted * (1.0 + 0.10)
                        else:
                            taxed = discounted * (1.0 + tax_rate)
                        taxed_total += taxed
                    else:
                        taxed_total += discounted

                    if taxed_total <= max_limit:
                        total_processed += taxed_total
                        accepted_count += 1
                    else:
                        rejected_count += 1
                else:
                    rejected_count += 1
            else:
                rejected_count += 1
        else:
            rejected_count += 1

    return {
        "accepted": accepted_count,
        "rejected": rejected_count,
        "total_amount": round(total_processed, 2),
        "currency": currency_symbol,
    }
