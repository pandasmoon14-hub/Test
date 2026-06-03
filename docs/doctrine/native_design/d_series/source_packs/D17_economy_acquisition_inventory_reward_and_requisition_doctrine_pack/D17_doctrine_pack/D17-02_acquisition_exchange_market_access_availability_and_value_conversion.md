# D17-02 — Acquisition, Exchange, Market Access, Availability, and Value Conversion

> Doctrine status: D17 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied economy/acquisition/inventory/reward/requisition analysis is used as non-final research pressure and guardrail material, not canon terminology by default.


## Core question
How does Astra determine whether a character, faction, group, or platform can obtain, exchange, sell, trade, request, loot, salvage, requisition, borrow, or access value without turning shops, loot tables, coin prices, auction houses, black markets, faction stores, contribution systems, or post-scarcity access into universal Astra law?

## Eight-checkpoint acquisition and exchange procedure
```text
1. Value request checkpoint
2. Value-state classification checkpoint
3. Access channel checkpoint
4. Availability and scarcity checkpoint
5. Permission, legality, and custody checkpoint
6. Exchange / conversion checkpoint
7. Cost, burden, and sink checkpoint
8. Outcome and owner-file handoff checkpoint
```

## Value request checkpoint
A value question begins when someone tries to obtain, exchange, claim, store, access, move, sell, spend, requisition, or convert value: buying gear, selling salvage, requesting ammunition, bartering for fuel, looting opposition, opening market access, trading a favor for a license, auctioning a relic fragment, storing a dangerous object, converting contribution points into supplies, using post-scarcity fabrication access, or claiming wreck salvage.

## Access channel checkpoint
Access channel changes procedure and risk:
```text
purchase — requires market, seller, price, permission, availability
barter — requires acceptable exchange value and mutual recognition
trade — requires transfer rights and custody/ownership clarity
reward — requires lawful reward trigger and ownership handoff
loot — requires source, custody, legality, and D16/D17/D10/D15 review
salvage — requires salvage state, claim review, and D09/D15/D17 handoff
requisition — requires authority, eligibility, supply, and institutional approval
black_market — requires access, risk, legality pressure, and trace
auction — requires venue, time, competition, custody
faction_store — requires standing, access, contribution, permission, stock
post_scarcity_access — requires infrastructure, permission, identity, energy, pattern, license, or policy
source_local_channel — requires explicit boundary
```

## Availability and scarcity outcomes
```text
available_now
available_with_delay
available_with_requirement
available_at_cost
available_with_risk
available_only_through_project
available_only_through_faction
available_only_through_travel
available_only_through_black_market
available_only_through_source_local_procedure
unavailable
unknown
protected_hidden
quarantined
escalated
```
Scarcity may create price, but may also create time, route, faction, license, Project, black-market, or claim pressure.

## Permission, legality, and custody questions
```text
Who owns it?
Who possesses it?
Who claims it?
Who can legally transfer it?
Is use allowed but sale forbidden?
Is transport restricted?
Is it contraband, faction-controlled, licensed, bound, stolen, salvage_pending, unknown, or protected hidden?
```
D17 owns value/access procedure. D10 owns law/world-state. D15 owns enforcement, claims, and obligations. D11 owns presentation.

## Exchange and conversion
Conversions may include currency to item, item to currency, material to crafted output, salvage to component, favor to access, standing to license, contribution point to faction supply, debt to obligation, loot to sale value, reward claim to item/access, requisition authority to supply, service to payment, information to market advantage, post-scarcity pattern to fabricated object, or source-local currency to source-local benefit.

Conversion requires valid channel, permission, availability, and owner-file support. Friction may include transaction cost, tax, tariff, delay, spoilage, loss rate, exchange rate, standing requirement, broker requirement, black-market risk, requisition approval, material waste, custody dispute, or source-local rules.

## Cost, burden, and sink checkpoint
Before completion, identify what leaves, is reserved, is consumed, or becomes burden: currency payment, barter transfer, favor spent, debt incurred, standing risked, tax, tariff, fee, dues, bribe, storage cost, transport cost, license fee, maintenance, decay, spoilage, repair requirement, fuel, ammo, time, opportunity cost, legal trace, faction scrutiny, or source-local sink.

## Outcome states
```text
acquired, acquired_with_cost, acquired_with_burden, acquired_with_dispute, acquired_with_trace, access_granted, access_limited, access_denied, exchange_completed, exchange_partial, exchange_delayed, exchange_failed, custody_changed, ownership_changed, claim_created, claim_contested, requisition_approved, requisition_denied, reward_delivered, loot_pending_review, salvage_pending_claim, black_market_trace_created, unavailable, quarantined, escalated, source_local_result
```

## Principles
```text
Payment is not access.
Possession is not ownership.
Rarity is not price.
Market listing is not world truth.
Loot is not automatically lawful property.
Salvage is not automatically owned.
Requisition is not free supply.
Post-scarcity is not no-scarcity.
Faction access is not advancement permission.
Contribution points are not universal currency.
Black markets are not guaranteed shops.
```
