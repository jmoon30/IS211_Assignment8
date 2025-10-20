
"""
IS211 Assignment 8: Pig with Factory + Proxy (Timed) + optional --delay
- Human/Computer players via Factory
- Optional timed game via Proxy
- Optional per-decision delay so the timer is easy to observe
"""
import argparse
import random
import time
from dataclasses import dataclass
from typing import List

random.seed(0)  # comment out for true randomness

class Die:
    def roll(self) -> int:
        return random.randint(1, 6)

@dataclass
class Player:
    name: str
    score: int = 0
    def decide(self, last_roll: int, turn_total: int) -> str:
        raise NotImplementedError

class HumanPlayer(Player):
    def decide(self, last_roll: int, turn_total: int) -> str:
        decision = input("(r)oll or (h)old? ").strip().lower()
        while decision not in {"r", "h"}:
            decision = input("Please enter 'r' to roll or 'h' to hold: ").strip().lower()
        return decision

class ComputerPlayer(Player):
    def decide(self, last_roll: int, turn_total: int) -> str:
        threshold = min(25, PigGame.TARGET_SCORE - self.score)
        if turn_total >= threshold:
            print(f"{self.name} decides to HOLD at {turn_total} (threshold {threshold}).")
            return 'h'
        print(f"{self.name} decides to ROLL (turn total {turn_total} < threshold {threshold}).")
        return 'r'

class PlayerFactory:
    @staticmethod
    def create(kind: str, name: str) -> Player:
        k = (kind or "human").lower().strip()
        if k == "human":
            return HumanPlayer(name=name)
        if k == "computer":
            return ComputerPlayer(name=name)
        raise ValueError(f"Unknown player type: {kind}")

class PigGame:
    TARGET_SCORE = 100
    def __init__(self, players: List[Player], die: Die | None = None, delay: float = 0.0):
        if len(players) != 2:
            raise ValueError("Exactly two players are required.")
        self.players = players
        self.die = die or Die()
        self.current_index = 0
        self.delay = delay  # seconds between computer decisions

    def banner(self):
        p0, p1 = self.players
        print("Welcome to Pig! First to 100 wins.")
        print(f"Players: {p0.name} ({p0.__class__.__name__}) vs {p1.name} ({p1.__class__.__name__})")

    def current_player(self) -> Player:
        return self.players[self.current_index]

    def next_player(self):
        self.current_index = (self.current_index + 1) % len(self.players)

    def play_turn(self) -> bool:
        player = self.current_player()
        turn_total = 0

        roll = self.die.roll()
        if roll == 1:
            print(f"{player.name} rolled a 1. Turn over. No points added.\n")
            self.next_player()
            return False
        else:
            turn_total += roll
            while True:
                print(f"{player.name} rolled: {roll}")
                print(f"Turn total: {turn_total}")
                print(f"{player.name}'s game score: {player.score}")

                # Optional pacing to make timed mode observable
                if isinstance(player, ComputerPlayer) and self.delay > 0:
                    time.sleep(self.delay)

                decision = player.decide(last_roll=roll, turn_total=turn_total)
                if decision == 'h':
                    player.score += turn_total
                    print(f"{player.name} holds. Added {turn_total}. TOTAL = {player.score}.\n")
                    if player.score >= self.TARGET_SCORE:
                        print(f"{player.name} wins with {player.score} points!\n")
                        return True
                    self.next_player()
                    return False
                else:  # roll again
                    roll = self.die.roll()
                    if roll == 1:
                        print(f"{player.name} rolled a 1. Turn over. No points added.\n")
                        self.next_player()
                        return False
                    turn_total += roll

    def play(self):
        print("Mode: UNTIMED")
        self.banner()
        while True:
            if self.play_turn():
                break

class TimedGameProxy:
    def __init__(self, game: PigGame, seconds: int = 60):
        self._game = game
        self.seconds = seconds

    def play(self):
        print(f"Mode: TIMED ({self.seconds} seconds)")
        self._game.banner()
        start = time.time()
        while True:
            if time.time() - start >= self.seconds:
                self._declare_time_winner(time.time() - start)
                break
            if self._game.play_turn():
                break
            if time.time() - start >= self.seconds:
                self._declare_time_winner(time.time() - start)
                break

    def _declare_time_winner(self, elapsed: float):
        p0, p1 = self._game.players
        print(f"\nTime's up at {elapsed:.1f} seconds!")
        print(f"Final scores -> {p0.name}: {p0.score}, {p1.name}: {p1.score}")
        if p0.score > p1.score:
            print(f"{p0.name} wins by score!")
        elif p1.score > p0.score:
            print(f"{p1.name} wins by score!")
        else:
            print("It's a tie!")

def parse_args():
    parser = argparse.ArgumentParser(description="Pig game with Factory and Proxy patterns.")
    parser.add_argument("--player1", choices=["human", "computer"], default="human")
    parser.add_argument("--player2", choices=["human", "computer"], default="human")
    parser.add_argument("--name1", default="Player 1")
    parser.add_argument("--name2", default="Player 2")
    parser.add_argument("--timed", action="store_true", help="Enable timed mode")
    parser.add_argument("--seconds", type=int, default=60, help="Duration for timed mode (default 60)")
    parser.add_argument("--delay", type=float, default=0.0, help="Sleep this many seconds between computer decisions")
    return parser.parse_args()

def main():
    args = parse_args()
    p1 = PlayerFactory.create(args.player1, args.name1)
    p2 = PlayerFactory.create(args.player2, args.name2)
    game = PigGame([p1, p2], delay=args.delay)
    if args.timed:
        TimedGameProxy(game, seconds=args.seconds).play()
    else:
        game.play()

if __name__ == "__main__":
    main()
