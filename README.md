![anaplan-diff](docs/banner.png)

# anaplan-diff

Diff two Anaplan models. See which modules and line items were added, removed, or had their formula changed between two builds.

![Two line item exports uploaded, diff output listing created, deleted and changed line items](docs/screenshot.png)

## Why I built it

Anaplan can't answer "what changed between dev and prod?" or "what did the last sprint touch?". ALM tells you a revision was synced, not what was in it. Before a release I wanted a list I could paste into a change note and hand to a model owner or an auditor. I didn't want to get it by clicking through modules side by side.

So this takes the standard line item export from each model and prints the difference.

## What it reports

- Modules deleted from the first model and created in the second
- Line items created (with their formula) and deleted
- Formula changes on line items present in both, shown as FROM and TO

Line items without a formula are ignored, so you get the calculation logic only. That's usually what a reviewer wants.

## How to use it

1. In each model go to Modules > Line Items and export the grid to CSV. You don't need API access.
2. Run the app locally:

```bash
git clone https://github.com/klameer/anaplan-diff.git
cd anaplan-diff
pip install -r requirements.txt
python main.py
```

3. Open http://127.0.0.1:5000, upload the two exports, press Compare.

No model to hand? `docs/sample_before.csv` and `docs/sample_after.csv` are a small fictional export pair. That's what the screenshot shows.

The comparison runs on your machine. The tool doesn't send the files anywhere.

## Reading the output

```
MODULES
  DELETE Modules
  - OLD Revenue Calc
  CREATE Modules
  + REV01 Revenue Calc

LINE ITEMS
  CREATE Line Items
  + NAME: REV01 Revenue Calc.Net Revenue | FORMULA: Gross Revenue - Discounts
  DELETE Line Items
  - OLD Revenue Calc.Net Revenue
  CHANGE Line Items
  COST01 Opex.Total Cost | FROM: Salaries + Bonus | TO: Salaries + Bonus + NI
```

A rename shows up as a delete plus a create, because the export carries no stable ID. Read the two sections together.

## Limits

- It compares module names and formulas only. Dimensionality, formats, summary methods and applies-to changes aren't diffed yet.
- It expects the classic line item export layout (a `Module Name` column, an unnamed line item column, a `Formula` column). If Anaplan changes the export, the parser needs a tweak.

## Related

- [anaplan-impact-analysis](https://github.com/klameer/anaplan-impact-analysis): from the same export, see what depends on a line item before you change it.
- [anaplan-api-starter](https://github.com/klameer/anaplan-api-starter): pull the exports by API instead of by hand.

MIT licensed. I'm [Karim Lameer](https://www.linkedin.com/in/karimlameer), Master Anaplanner and CIMA-qualified accountant. I write about this at [codelessops.com](https://codelessops.com).
