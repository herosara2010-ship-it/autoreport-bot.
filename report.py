
import csv
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
from datetime import date

INPUT_FILE = Path("sales.csv")
OUTPUT_FILE = Path("report.md")


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError("Please add sales.csv first.")

    total_revenue = Decimal("0")
    total_units = 0
    orders = 0
    product_totals = defaultdict(Decimal)

    with INPUT_FILE.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)

        required = {"date", "product", "quantity", "unit_price"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError(
                "CSV must contain: date, product, quantity, unit_price"
            )

        for row in reader:
            product = row["product"].strip()
            if not product:
                raise ValueError("Product names cannot be empty.")

            quantity = int(row["quantity"])
            price = Decimal(row["unit_price"])

            if quantity < 0 or price < 0:
                raise ValueError("Quantity and price must be non-negative.")

            revenue = quantity * price
            total_revenue += revenue
            total_units += quantity
            orders += 1
            product_totals[product] += revenue

    lines = [
        "# Automated Sales Report",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        f"- Rows processed: {orders}",
        f"- Units sold: {total_units}",
        f"- Total sales: {total_revenue:.2f}",
        "",
        "## Sales by product",
        "",
        "| Product | Sales |",
        "|---|---:|",
    ]

    for product, revenue in sorted(
        product_totals.items(),
        key=lambda item: item[1],
        reverse=True,
    ):
        lines.append(f"| {product} | {revenue:.2f} |")

    OUTPUT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Report created: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
