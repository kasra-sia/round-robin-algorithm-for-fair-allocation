# Round-robin allocation and envy-freeness

Three people have to split nine indivisible items. They take turns picking, and afterwards the script checks whether anyone would rather have someone else's share. It does this under three different assumptions about how people value a bundle of items.

I wrote this for the Game Theory course at Sharif University of Technology (Spring 2024). It is deliberately tiny: one instance that you can work through by hand, so every number in the output can be checked.

## The question

When goods can't be split, it is not obvious what a fair outcome is. A common test is *envy-freeness*: nobody values another person's bundle more than their own. Exact envy-freeness is not always possible. With one item and two people, someone gets nothing and envies the other. So the literature often settles for *envy-freeness up to one item* (EF1): if anyone envies someone else, the envy goes away once a single item is removed from the other person's bundle.

Round robin is about the simplest rule there is. People take turns in a fixed order, and on each turn the current person takes the item they like most among those still left. When each person values a bundle as the plain sum of its items (additive valuations), round robin is known to always produce an EF1 allocation. This project looks at one concrete instance: does round robin do better than EF1 here, and what changes when bundles are worth more than the sum of their parts?

## The instance

Three agents (1, 2, 3) and nine items (A to I). Each agent gives each item a value:

| Agent | A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 8 | 9 |
| 2 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| 3 | 8 | 3 | 8 | 7 | 6 | 5 | 1 | 2 | 3 |

Agents 1 and 2 both rank I and H at the top, so they compete for the same items early on. Agent 3 wants something else: A and C first, then D and E. Agent 3 values A and C equally, which matters later (see [A note on ties](#a-note-on-ties)).

## Three ways to value a bundle

The script judges the final bundles under three preference types, named as in the code:

- `Additive`: a bundle is worth the sum of its items.
- `Semi-Additive`: the same, plus a small bonus of 0.5 if the bundle contains both A and B, so A and B are slightly better together.
- `Non-Additive`: the same, plus a bonus of 7 for A and B together. Here they are strong complements, and having both is worth almost as much as a third item.

The picking itself never looks at these bonuses. On every turn an agent picks by single-item value, so the allocation is the same under all three preference types. The preference type only changes how the finished bundles are compared in the envy check. That is why the three allocation columns in the output are identical.

## How the picks go

The turn order is 1, 2, 3, repeated until the items run out, so with nine items everyone picks three times. In most runs it goes like this:

| Round | Agent 1 | Agent 2 | Agent 3 |
|---|---|---|---|
| 1 | I (9) | H (8) | C (8), tied with A |
| 2 | A (7) | G (7) | D (7) |
| 3 | B (6) | F (6) | E (6) |

Agent 1 gets {I, A, B}, agent 2 gets {H, G, F} and agent 3 gets {C, D, E}.

## Checking envy

For every pair of agents, the script values the other agent's bundle with the first agent's own valuation. Agent *i* envies agent *j* if *j*'s bundle is worth strictly more to *i* than *i*'s own bundle.

Here is how each agent values every bundle in the run above with additive valuations. Each row is the agent doing the valuing:

| Valued by | {I, A, B} | {H, G, F} | {C, D, E} |
|---|---|---|---|
| Agent 1 | **22** | 11 | 12 |
| Agent 2 | 12 | **21** | 12 |
| Agent 3 | 14 | 8 | **21** |

Everyone values their own bundle (in bold) the most, so nobody envies anyone.

With the semi-additive valuation, only {I, A, B} contains both A and B, so only it gets the 0.5 bonus: agent 1 values it at 22.5, agent 2 at 12.5 and agent 3 at 14.5. Nothing else changes, and there is still no envy.

With the non-additive valuation the bonus is 7, so {I, A, B} is worth 29 to agent 1, 19 to agent 2 and 21 to agent 3. Agent 3's own bundle is also worth 21, so agent 3 values agent 1's bundle exactly as much as their own. The check only counts a strictly greater value as envy, so the result is still envy-free, but only just: with a bonus of 8 instead of 7, agent 3 would envy agent 1.

So in this instance round robin does better than its EF1 guarantee: the allocation is fully envy-free under all three preference types. The guarantee itself only covers additive valuations, and the non-additive case shows the reason. The picking rule can't see that A and B are worth more together, so whoever happens to collect both gets a bonus that nobody accounted for when picking.

## Running it

You need Python 3 and pandas:

```bash
pip install pandas
python main.py
```

The output:

```
Allocations:
    Additive Semi-Additive Non-Additive
1  [I, A, B]     [I, A, B]    [I, A, B]
2  [H, G, F]     [H, G, F]    [H, G, F]
3  [C, D, E]     [C, D, E]    [C, D, E]

Envy Checks:
   Additive  Semi-Additive  Non-Additive
1     False          False         False
2     False          False         False
3     False          False         False
```

`False` means the agent envies nobody.

## A note on ties

In the first round agent 3 values A and C both at 8. The script picks the best item with `max()` over a Python `set`, and when two items tie, `max()` returns whichever it meets first. The order of a set of strings depends on Python's hash seed, which changes between runs. So some runs give agent 3 item A in the first round instead of C, and the allocation comes out differently:

```
1  [I, B, D]
2  [H, G, F]
3  [A, C, E]
```

This allocation is envy-free too. No bundle contains both A and B, so the bonuses never apply and the three preference types agree. To get the same result on every run, fix the hash seed (`PYTHONHASHSEED=0 python main.py`) or pick from a sorted list instead of a set.

## What's in the repository

- `main.py` holds the item values, the round-robin allocation, the bundle valuation for each preference type and the envy check, and prints the results as two pandas tables.
- `LICENSE` is the MIT license.

## Limitations and ideas

This is a single hand-made instance, not a study, and the code is written for exactly three agents and nine items. Some things I'd like to try next:

- Check EF1 as well as exact envy-freeness, and run both on many random instances to see how often round robin is exactly envy-free.
- Make ties explicit, either by breaking them with a fixed rule or by reporting every allocation the ties allow.
- Let the picking rule see complementarities, for example by valuing an item by how much it adds to the bundle so far. Then compare that with plain round robin under the non-additive preferences.
- Compare round robin with other rules such as envy-cycle elimination or maximum Nash welfare on the same instances.

## License

[MIT](LICENSE)
