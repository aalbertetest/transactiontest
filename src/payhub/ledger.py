"""Double-entry journal posting."""

from __future__ import annotations

from sqlalchemy.orm import Session

from payhub.models import (
    Account,
    AccountType,
    LedgerEntry,
    LedgerSide,
    PaymentTransaction,
    User,
)


def ensure_wallet(db: Session, user: User, currency: str = "USD") -> Account:
    acc = (
        db.query(Account)
        .filter(
            Account.user_id == user.id,
            Account.type == AccountType.user_wallet,
            Account.currency == currency,
        )
        .first()
    )
    if acc:
        return acc
    acc = Account(
        user_id=user.id,
        type=AccountType.user_wallet,
        currency=currency,
        name=f"Wallet {user.email}",
    )
    db.add(acc)
    db.flush()
    return acc


def get_fee_revenue_account(db: Session, currency: str = "USD") -> Account:
    fees = (
        db.query(Account)
        .filter(Account.type == AccountType.fee_revenue, Account.currency == currency)
        .first()
    )
    if not fees:
        fees = Account(
            user_id=None,
            type=AccountType.fee_revenue,
            currency=currency,
            name="Fee revenue",
        )
        db.add(fees)
        db.flush()
    return fees


def compute_fee(amount_cents: int, bps: int = 29, min_fee: int = 30) -> int:
    raw = (amount_cents * bps + 9999) // 10000
    return max(raw, min_fee)


def post_p2p_payment(
    db: Session,
    payer: User,
    payee: User,
    amount_cents: int,
    fee_cents: int,
    idempotency_key: str | None,
    fraud_flags: str | None,
) -> PaymentTransaction:
    """Post a P2P transfer with balanced double-entry.

    User wallets are modeled as liability accounts: debiting the payer wallet
    reduces the platform's obligation to the payer; crediting the payee wallet
    increases the obligation to the payee. Fee revenue is credited separately.
    """
    payer_wallet = ensure_wallet(db, payer)
    payee_wallet = ensure_wallet(db, payee)
    fee_revenue = get_fee_revenue_account(db)

    payment = PaymentTransaction(
        payer_user_id=payer.id,
        payee_user_id=payee.id,
        amount_cents=amount_cents,
        fee_cents=fee_cents,
        status="posted",
        idempotency_key=idempotency_key,
        fraud_flags=fraud_flags,
    )
    db.add(payment)
    db.flush()

    total_from_payer = amount_cents + fee_cents

    db.add(
        LedgerEntry(
            payment_id=payment.id,
            account_id=payer_wallet.id,
            side=LedgerSide.debit,
            amount_cents=total_from_payer,
        )
    )
    db.add(
        LedgerEntry(
            payment_id=payment.id,
            account_id=payee_wallet.id,
            side=LedgerSide.credit,
            amount_cents=amount_cents,
        )
    )
    if fee_cents:
        db.add(
            LedgerEntry(
                payment_id=payment.id,
                account_id=fee_revenue.id,
                side=LedgerSide.credit,
                amount_cents=fee_cents,
            )
        )

    return payment


def journal_balances(db: Session, payment_id: str) -> tuple[int, int]:
    rows = db.query(LedgerEntry).filter(LedgerEntry.payment_id == payment_id).all()
    deb = sum(r.amount_cents for r in rows if r.side == LedgerSide.debit)
    cred = sum(r.amount_cents for r in rows if r.side == LedgerSide.credit)
    return deb, cred
