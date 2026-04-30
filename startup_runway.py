#!/usr/bin/env python3
"""
STARTUP RUNWAY — A Terminal Strategy Game

Manage your startup's cash runway through fundraising droughts,
surprise AWS bills, customer churn, and the chaos of startup life.
Survive 24 months to reach profitability... or die trying.
"""

import random
import sys
import os
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Outcome(Enum):
    CONTINUE = "continue"
    GAME_OVER = "game_over"
    VICTORY = "victory"


@dataclass
class Startup:
    name: str
    cash: float = 500_000
    mrr: float = 5_000
    burn_rate: float = 45_000
    team_size: int = 5
    morale: int = 75
    month: int = 0
    product_quality: int = 50
    brand_reputation: int = 30
    fundraising_active: bool = False
    fundraising_months: int = 0
    pivot_count: int = 0

    @property
    def runway_months(self) -> float:
        net_burn = self.burn_rate - self.mrr
        if net_burn <= 0:
            return float("inf")
        return self.cash / net_burn

    @property
    def is_profitable(self) -> bool:
        return self.mrr >= self.burn_rate

    def clamp_stats(self):
        self.morale = max(0, min(100, self.morale))
        self.product_quality = max(0, min(100, self.product_quality))
        self.brand_reputation = max(0, min(100, self.brand_reputation))
        self.team_size = max(1, self.team_size)
        self.mrr = max(0, self.mrr)
        self.burn_rate = max(5_000, self.burn_rate)
        self.cash = max(0, self.cash)


@dataclass
class Event:
    title: str
    description: str
    effect: str
    apply: object  # callable(startup) -> None


def _make_events() -> list[Event]:
    """All possible random events that can strike your startup."""
    return [
        Event(
            "VC Ghosting",
            "The partner who said 'we're definitely leading your round'\n"
            "  hasn't replied to your last 7 emails. Their assistant says\n"
            "  they're 'traveling'. It's been 3 weeks.",
            "Morale -10. If fundraising, progress resets.",
            lambda s: _vc_ghosting(s),
        ),
        Event(
            "Surprise AWS Bill",
            "Someone left a p3.16xlarge running for the entire month.\n"
            "  The bill is... significant. Your CTO blames 'a dev environment'.",
            "Cash -$25,000 to -$80,000.",
            lambda s: _aws_bill(s),
        ),
        Event(
            "Customer Churn Wave",
            "Three of your biggest customers cancelled this week.\n"
            "  One said they're 'going in a different direction'.\n"
            "  Another built it in-house. The third just vanished.",
            "MRR drops 15-30%.",
            lambda s: _customer_churn(s),
        ),
        Event(
            "Key Engineer Poached",
            "Your senior engineer just got a LinkedIn message from FAANG.\n"
            "  They want 2x the salary and actual work-life balance.\n"
            "  They're 'thinking about it'.",
            "Team -1, product quality -10, morale -5.",
            lambda s: _engineer_poached(s),
        ),
        Event(
            "Competitor Launches",
            "TechCrunch just covered a well-funded competitor launching\n"
            "  an almost identical product. They raised $20M. Your investor\n"
            "  forwards you the article with a single '?'.",
            "Brand reputation -15, morale -10.",
            lambda s: _competitor_launches(s),
        ),
        Event(
            "Viral Hacker News Post",
            "Someone posted your product on Hacker News and it hit #1.\n"
            "  The comments are... actually positive? Your site is\n"
            "  struggling under the traffic.",
            "MRR +20-40%, brand reputation +15.",
            lambda s: _viral_hn(s),
        ),
        Event(
            "Enterprise Lead",
            "A Fortune 500 company wants a demo. They have 'budget'.\n"
            "  But they also want SOC2 compliance, SSO, and a 47-page\n"
            "  security questionnaire filled out by Friday.",
            "Potential MRR +$5K-15K, but product quality -5.",
            lambda s: _enterprise_lead(s),
        ),
        Event(
            "Compliance Surprise",
            "You just discovered your product needs GDPR compliance.\n"
            "  Your lawyer says it'll take 'a few weeks'. Your lawyer\n"
            "  has a very different definition of 'a few'.",
            "Cash -$15,000 to -$30,000, burn +$2K/mo.",
            lambda s: _compliance_surprise(s),
        ),
        Event(
            "Founding Team Drama",
            "Your co-founder wants to 'have a talk about the vision'.\n"
            "  They've been having coffee with other founders.\n"
            "  The vesting cliff is next month.",
            "Morale -15.",
            lambda s: _founder_drama(s),
        ),
        Event(
            "Product Hunt Launch",
            "Your Product Hunt launch day is here! The community votes\n"
            "  are rolling in. The kitty emoji hunter left a comment.\n"
            "  You might actually get Product of the Day.",
            "MRR +10-25%, brand reputation +10.",
            lambda s: _product_hunt(s),
        ),
        Event(
            "Investor FOMO",
            "An angel investor saw your latest tweet thread about growth\n"
            "  metrics and slid into your DMs. They want to write a check\n"
            "  'before your round fills up'.",
            "Cash +$25K-75K.",
            lambda s: _investor_fomo(s),
        ),
        Event(
            "Critical Bug in Production",
            "Your monitoring dashboard just lit up like a Christmas tree.\n"
            "  Customers are reporting data loss. Twitter is not happy.\n"
            "  Your on-call engineer is at a music festival.",
            "MRR -10%, brand reputation -10, morale -10.",
            lambda s: _prod_bug(s),
        ),
        Event(
            "Acqui-hire Offer",
            "A mid-stage startup wants to acquire your team. The offer\n"
            "  is... underwhelming, but it comes with salary and stability.\n"
            "  Your team is curious.",
            "Morale -5 (uncertainty).",
            lambda s: _acquihire(s),
        ),
        Event(
            "Stripe Holds Your Funds",
            "Stripe flagged your account for 'unusual activity' and is\n"
            "  holding $20K-$50K in reserves. Their support says they'll\n"
            "  'review it within 5-7 business days'. Sure, Stripe.",
            "Cash temporarily reduced.",
            lambda s: _stripe_hold(s),
        ),
        Event(
            "Intern Ships a Feature",
            "Your summer intern just shipped a feature that customers\n"
            "  have been requesting for months. It actually works.\n"
            "  Your senior devs are quietly impressed (and nervous).",
            "Product quality +10, morale +5, MRR +5%.",
            lambda s: _intern_ships(s),
        ),
        Event(
            "Office Lease Expires",
            "Your WeWork hot desk subscription just doubled in price.\n"
            "  You could go fully remote, but the team 'values the\n"
            "  in-person collaboration'. Do they though?",
            "Burn rate +$3K or go remote (morale gamble).",
            lambda s: _office_lease(s),
        ),
        Event(
            "Customer Referral Boom",
            "Your NPS score is through the roof. Customers are actively\n"
            "  referring friends. Your CAC just dropped to nearly zero\n"
            "  for this batch of signups.",
            "MRR +15-30%, brand reputation +10.",
            lambda s: _referral_boom(s),
        ),
        Event(
            "Domain Squatter",
            "The perfect .com domain for your startup is being held\n"
            "  by a squatter who wants $15,000. Your current domain\n"
            "  has a hyphen in it. Investors keep misspelling it.",
            "Cash -$15K (if you buy it), brand reputation +5.",
            lambda s: _domain_squatter(s),
        ),
    ]


def _vc_ghosting(s: Startup):
    s.morale -= 10
    if s.fundraising_active:
        s.fundraising_months = 0
        s.fundraising_active = False


def _aws_bill(s: Startup):
    bill = random.randint(25_000, 80_000)
    s.cash -= bill
    _print_impact(f"  Surprise bill: ${bill:,}")


def _customer_churn(s: Startup):
    pct = random.uniform(0.15, 0.30)
    lost = s.mrr * pct
    s.mrr -= lost
    _print_impact(f"  MRR lost: ${lost:,.0f} ({pct*100:.0f}% churn)")


def _engineer_poached(s: Startup):
    if s.team_size > 1:
        s.team_size -= 1
        s.burn_rate -= random.randint(8_000, 12_000)
    s.product_quality -= 10
    s.morale -= 5


def _competitor_launches(s: Startup):
    s.brand_reputation -= 15
    s.morale -= 10


def _viral_hn(s: Startup):
    pct = random.uniform(0.20, 0.40)
    gained = s.mrr * pct
    s.mrr += gained
    s.brand_reputation += 15
    _print_impact(f"  MRR gained: ${gained:,.0f}")


def _enterprise_lead(s: Startup):
    deal = random.randint(5_000, 15_000)
    s.mrr += deal
    s.product_quality -= 5
    _print_impact(f"  Enterprise contract: +${deal:,}/mo MRR")


def _compliance_surprise(s: Startup):
    cost = random.randint(15_000, 30_000)
    s.cash -= cost
    s.burn_rate += 2_000
    _print_impact(f"  Legal/compliance costs: ${cost:,}")


def _founder_drama(s: Startup):
    s.morale -= 15


def _product_hunt(s: Startup):
    pct = random.uniform(0.10, 0.25)
    gained = s.mrr * pct
    s.mrr += gained
    s.brand_reputation += 10
    _print_impact(f"  New signups added: +${gained:,.0f}/mo MRR")


def _investor_fomo(s: Startup):
    check = random.randint(25_000, 75_000)
    s.cash += check
    _print_impact(f"  Angel check received: ${check:,}")


def _prod_bug(s: Startup):
    s.mrr *= 0.90
    s.brand_reputation -= 10
    s.morale -= 10


def _acquihire(s: Startup):
    s.morale -= 5


def _stripe_hold(s: Startup):
    hold = random.randint(20_000, 50_000)
    s.cash -= hold
    _print_impact(f"  Funds held: ${hold:,} (may be released next month)")


def _intern_ships(s: Startup):
    s.product_quality += 10
    s.morale += 5
    s.mrr *= 1.05


def _office_lease(s: Startup):
    s.burn_rate += 3_000
    s.morale -= 3


def _referral_boom(s: Startup):
    pct = random.uniform(0.15, 0.30)
    gained = s.mrr * pct
    s.mrr += gained
    s.brand_reputation += 10
    _print_impact(f"  Referral MRR: +${gained:,.0f}/mo")


def _domain_squatter(s: Startup):
    s.cash -= 15_000
    s.brand_reputation += 5
    _print_impact("  Bought the domain for $15,000. Worth it? Maybe.")


ACTIONS = [
    ("Hire an engineer", "hire"),
    ("Lay off a team member", "layoff"),
    ("Launch a marketing campaign", "marketing"),
    ("Raise prices 20%", "raise_prices"),
    ("Cut infrastructure costs", "cut_costs"),
    ("Start fundraising", "fundraise"),
    ("Pivot the product", "pivot"),
    ("Focus on product quality", "build"),
    ("Do nothing (save cash)", "nothing"),
]


def _print_impact(msg: str):
    print(f"\033[33m{msg}\033[0m")


def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")


def print_banner():
    banner = r"""
   _____ _             _                  ____                               
  / ____| |           | |                |  _ \                              
 | (___ | |_ __ _ _ __| |_ _   _ _ __   | |_) |_   _ _ __ _ __             
  \___ \| __/ _` | '__| __| | | | '_ \  |  _ <| | | | '__| '_ \            
  ____) | || (_| | |  | |_| |_| | |_) | | |_) | |_| | |  | | | |           
 |_____/ \__\__,_|_|   \__|\__,_| .__/  |____/ \__,_|_|  |_| |_|           
                                 | |                                         
    R U N W A Y               |_|       M A N A G E R                   
    """
    print(f"\033[36m{banner}\033[0m")


def print_dashboard(s: Startup):
    runway = s.runway_months
    runway_str = f"{runway:.1f} months" if runway != float("inf") else "INFINITE (profitable!)"

    if runway == float("inf"):
        runway_color = "\033[32m"
    elif runway > 6:
        runway_color = "\033[32m"
    elif runway > 3:
        runway_color = "\033[33m"
    else:
        runway_color = "\033[31m"

    morale_bar = "█" * (s.morale // 5) + "░" * (20 - s.morale // 5)
    quality_bar = "█" * (s.product_quality // 5) + "░" * (20 - s.product_quality // 5)

    net_burn = s.burn_rate - s.mrr
    net_str = f"${net_burn:,.0f}" if net_burn > 0 else f"\033[32m+${abs(net_burn):,.0f}\033[0m"

    print(f"\033[1m{'═' * 60}\033[0m")
    print(f"\033[1m  {s.name} — Month {s.month}/24\033[0m")
    print(f"\033[1m{'═' * 60}\033[0m")
    print(f"  💰 Cash:         \033[1m${s.cash:,.0f}\033[0m")
    print(f"  📈 MRR:          \033[32m${s.mrr:,.0f}\033[0m /month")
    print(f"  🔥 Burn Rate:    \033[31m${s.burn_rate:,.0f}\033[0m /month")
    print(f"  📉 Net Burn:     {net_str} /month")
    print(f"  ⏳ Runway:       {runway_color}{runway_str}\033[0m")
    print(f"  👥 Team:         {s.team_size} people")
    print(f"  😊 Morale:       [{morale_bar}] {s.morale}%")
    print(f"  ⚙️  Quality:      [{quality_bar}] {s.product_quality}%")
    print(f"  🏷️  Reputation:   {s.brand_reputation}/100")
    if s.fundraising_active:
        print(f"  📋 Fundraising:  In progress ({s.fundraising_months}/3 months)")
    print(f"\033[1m{'═' * 60}\033[0m")


def get_action(s: Startup) -> str:
    print("\n  \033[1mWhat do you want to do this month?\033[0m\n")
    available = []
    for i, (label, action_id) in enumerate(ACTIONS):
        skip = False
        note = ""
        if action_id == "hire" and s.cash < 30_000:
            note = " (can't afford)"
            skip = True
        if action_id == "layoff" and s.team_size <= 1:
            note = " (no one to lay off)"
            skip = True
        if action_id == "fundraise" and s.fundraising_active:
            note = " (already in progress)"
            skip = True
        if action_id == "marketing" and s.cash < 20_000:
            note = " (can't afford)"
            skip = True

        color = "\033[90m" if skip else ""
        reset = "\033[0m" if skip else ""
        print(f"  {color}  [{i + 1}] {label}{note}{reset}")
        available.append((action_id, skip))

    while True:
        try:
            choice = input("\n  Enter choice (1-9): ").strip()
            if not choice:
                continue
            idx = int(choice) - 1
            if 0 <= idx < len(available):
                action_id, skip = available[idx]
                if skip:
                    print("  \033[31mYou can't do that right now.\033[0m")
                    continue
                return action_id
        except (ValueError, EOFError):
            pass
        print("  \033[31mInvalid choice. Pick 1-9.\033[0m")


def apply_action(s: Startup, action: str):
    print()
    if action == "hire":
        salary = random.randint(8_000, 14_000)
        s.team_size += 1
        s.burn_rate += salary
        s.cash -= 5_000  # recruiting costs
        s.product_quality += 5
        s.morale += 3
        _print_impact(f"  Hired engineer #{s.team_size}. Salary: ${salary:,}/mo. Recruiting cost: $5,000.")

    elif action == "layoff":
        savings = random.randint(8_000, 12_000)
        s.team_size -= 1
        s.burn_rate -= savings
        s.morale -= 15
        s.product_quality -= 5
        _print_impact(f"  Let someone go. Saving ${savings:,}/mo. Morale took a hit.")

    elif action == "marketing":
        cost = random.randint(15_000, 25_000)
        s.cash -= cost
        effectiveness = random.random()
        if effectiveness > 0.4:
            mrr_gain = s.mrr * random.uniform(0.10, 0.30)
            s.mrr += mrr_gain
            s.brand_reputation += 5
            _print_impact(f"  Spent ${cost:,} on marketing. MRR +${mrr_gain:,.0f}/mo. It worked!")
        else:
            s.brand_reputation += 2
            _print_impact(f"  Spent ${cost:,} on marketing. Results were... underwhelming.")

    elif action == "raise_prices":
        churn_pct = random.uniform(0.05, 0.15)
        lost = s.mrr * churn_pct
        s.mrr = (s.mrr - lost) * 1.20
        _print_impact(f"  Raised prices 20%. Lost {churn_pct*100:.0f}% of customers but revenue is up.")

    elif action == "cut_costs":
        savings = random.randint(3_000, 8_000)
        s.burn_rate -= savings
        s.morale -= 5
        s.product_quality -= 3
        _print_impact(f"  Cut costs by ${savings:,}/mo. Cancelled some subscriptions, downgraded infra.")

    elif action == "fundraise":
        s.fundraising_active = True
        s.fundraising_months = 0
        _print_impact("  Started fundraising. This will take ~3 months if all goes well.")
        _print_impact("  Your focus is divided — product quality will suffer slightly.")

    elif action == "pivot":
        s.pivot_count += 1
        s.mrr *= 0.5
        s.product_quality -= 15
        s.morale -= 10
        s.brand_reputation -= 5
        _print_impact("  PIVOT! New direction, new hope, half the revenue.")
        _print_impact(f"  This is pivot #{s.pivot_count}. Investors are {'concerned' if s.pivot_count > 1 else 'watching'}.")

    elif action == "build":
        s.product_quality += 10
        s.morale += 5
        if random.random() > 0.5:
            mrr_gain = s.mrr * random.uniform(0.05, 0.10)
            s.mrr += mrr_gain
            _print_impact(f"  Built great features. Quality up! Organic MRR +${mrr_gain:,.0f}.")
        else:
            _print_impact("  Focused on product quality. The improvements will compound.")

    elif action == "nothing":
        _print_impact("  You saved cash and kept the lights on. Sometimes that's enough.")


def apply_monthly_effects(s: Startup):
    s.cash -= s.burn_rate
    s.cash += s.mrr

    if s.fundraising_active:
        s.fundraising_months += 1
        s.product_quality -= 3
        if s.fundraising_months >= 3:
            success_chance = 0.3 + (s.brand_reputation / 200) + (s.mrr / 100_000)
            success_chance = min(0.85, success_chance)
            if random.random() < success_chance:
                amount = random.randint(500_000, 2_000_000)
                s.cash += amount
                s.burn_rate += 5_000  # increased expectations
                s.morale += 20
                s.fundraising_active = False
                print(f"\n  \033[32m🎉 FUNDING SECURED! Raised ${amount:,}!\033[0m")
                print(f"  \033[32m   Your burn rate increased slightly (investor expectations).\033[0m")
            else:
                s.fundraising_active = False
                s.morale -= 15
                print(f"\n  \033[31m💀 Fundraising failed. VCs passed. Back to bootstrapping.\033[0m")

    organic_growth = s.product_quality / 1000
    if s.brand_reputation > 50:
        organic_growth += 0.02
    s.mrr *= (1 + organic_growth)

    if s.morale < 30:
        s.product_quality -= 2
        if random.random() < 0.2 and s.team_size > 1:
            s.team_size -= 1
            s.burn_rate -= 10_000
            print(f"  \033[31m  An employee quit due to low morale.\033[0m")


def check_game_state(s: Startup) -> Outcome:
    if s.cash <= 0:
        return Outcome.GAME_OVER
    if s.month >= 24 and s.is_profitable:
        return Outcome.VICTORY
    if s.month >= 24:
        if s.runway_months > 6:
            return Outcome.VICTORY
        return Outcome.GAME_OVER
    return Outcome.CONTINUE


def show_game_over(s: Startup):
    print(f"\n\033[31m{'=' * 60}\033[0m")
    print(f"\033[31m{'GAME OVER':^60}\033[0m")
    print(f"\033[31m{'=' * 60}\033[0m")
    print(f"\n  {s.name} ran out of cash in month {s.month}.")
    print(f"  Final MRR: ${s.mrr:,.0f}")
    print(f"  Team size at shutdown: {s.team_size}")
    print(f"  Pivots attempted: {s.pivot_count}")
    print(f"\n  Your startup joins the 90% that don't make it.")
    print(f"  Time to update your LinkedIn to 'Open to Work'.\n")


def show_victory(s: Startup):
    print(f"\n\033[32m{'=' * 60}\033[0m")
    print(f"\033[32m{'🎉  YOU SURVIVED!  🎉':^60}\033[0m")
    print(f"\033[32m{'=' * 60}\033[0m")
    print(f"\n  {s.name} made it to 24 months!")
    print(f"  Final Cash:    ${s.cash:,.0f}")
    print(f"  Final MRR:     ${s.mrr:,.0f}/month")
    print(f"  Team Size:     {s.team_size}")
    print(f"  Pivots:        {s.pivot_count}")
    print(f"  Morale:        {s.morale}%")

    score = int(s.cash / 1000 + s.mrr * 10 + s.morale * 100 + s.brand_reputation * 50)
    print(f"\n  \033[1m  FOUNDER SCORE: {score:,}\033[0m")

    if s.is_profitable:
        print(f"\n  \033[32m  Your startup is PROFITABLE. VCs are calling YOU now.\033[0m")
    elif s.runway_months > 12:
        print(f"\n  \033[32m  You have {s.runway_months:.0f} months of runway. Plenty of time.\033[0m")
    else:
        print(f"\n  \033[33m  You barely made it. But you made it. That counts.\033[0m")
    print()


def get_startup_name() -> str:
    print_banner()
    print("  Welcome, founder. The startup grind awaits.\n")
    print("  You have $500K in seed funding, a small team, and a dream.")
    print("  Survive 24 months. Reach profitability. Don't run out of cash.\n")
    while True:
        name = input("  What's your startup called? > ").strip()
        if name:
            return name
        print("  \033[31m  Every startup needs a name (even the bad ones).\033[0m")


def press_enter():
    input("\n  \033[90mPress Enter to continue...\033[0m")


def main():
    clear_screen()
    try:
        name = get_startup_name()
    except (EOFError, KeyboardInterrupt):
        print("\n  Goodbye, founder.\n")
        return

    startup = Startup(name=name)
    events = _make_events()

    clear_screen()
    print(f"\n  \033[1m{startup.name}\033[0m is incorporated. Let's go.\n")
    press_enter()

    while True:
        startup.month += 1
        clear_screen()

        print_dashboard(startup)

        num_events = 1
        if random.random() < 0.25:
            num_events = 2
        if startup.month > 18 and random.random() < 0.3:
            num_events = 3

        month_events = random.sample(events, min(num_events, len(events)))

        for event in month_events:
            print(f"\n  \033[1;35m⚡ EVENT: {event.title}\033[0m")
            print(f"  {event.description}")
            print(f"  \033[90m[{event.effect}]\033[0m")
            event.apply(startup)

        startup.clamp_stats()

        outcome = check_game_state(startup)
        if outcome == Outcome.GAME_OVER:
            show_game_over(startup)
            break

        try:
            action = get_action(startup)
        except (EOFError, KeyboardInterrupt):
            print("\n\n  The founder walked away from the startup.\n")
            break

        apply_action(startup, action)
        apply_monthly_effects(startup)
        startup.clamp_stats()

        outcome = check_game_state(startup)
        if outcome == Outcome.GAME_OVER:
            show_game_over(startup)
            break
        elif outcome == Outcome.VICTORY:
            show_victory(startup)
            break

        press_enter()

    try:
        play_again = input("  Play again? (y/n): ").strip().lower()
        if play_again == "y":
            main()
    except (EOFError, KeyboardInterrupt):
        pass

    print("  Thanks for playing Startup Runway! 🚀\n")


if __name__ == "__main__":
    main()
