# 📖 Sales Dataset — Data Dictionary

**Source:** `data/raw/Sample - Superstore.csv`
**Cleaned Version:** `data/processed/cleaned_sales.csv`
**Produced By:** `notebooks/01_data_cleaning.ipynb`

---

## Original Columns (21)

### Identifiers

| Column | Type | Description |
|---|---|---|
| `row_id` | `int64` | Unique row identifier (1-indexed). |
| `order_id` | `object` | Unique order identifier (e.g., `CA-2016-152156`). A single order can contain multiple line items (products). |
| `customer_id` | `object` | Unique customer identifier (e.g., `CG-12520`). |
| `product_id` | `object` | Unique product identifier (e.g., `FUR-BO-10001798`). Encodes category prefix. |

### Dates

| Column | Type | Description |
|---|---|---|
| `order_date` | `datetime64` | Date the order was placed. **Note:** Exported as ISO string (`YYYY-MM-DD`) in CSV. Load with `parse_dates=["order_date", "ship_date"]`. |
| `ship_date` | `datetime64` | Date the order was shipped. Always ≥ `order_date`. |

### Shipping

| Column | Type | Description |
|---|---|---|
| `ship_mode` | `object` | Shipping method. Values: `Standard Class`, `Second Class`, `First Class`, `Same Day`. |

### Customer

| Column | Type | Description |
|---|---|---|
| `customer_name` | `object` | Full name of the customer. |
| `segment` | `object` | Customer segment. Values: `Consumer`, `Corporate`, `Home Office`. |

### Geography

| Column | Type | Description |
|---|---|---|
| `country` | `object` | Country of the transaction. All values: `United States`. |
| `city` | `object` | City of the customer. |
| `state` | `object` | US state of the customer. |
| `postal_code` | `int64` | 5-digit US postal (ZIP) code. |
| `region` | `object` | US sales region. Values: `Central`, `East`, `South`, `West`. |

### Product

| Column | Type | Description |
|---|---|---|
| `category` | `object` | Top-level product category. Values: `Furniture`, `Office Supplies`, `Technology`. |
| `sub_category` | `object` | Product sub-category (17 unique). Examples: `Chairs`, `Phones`, `Binders`, `Tables`. |
| `product_name` | `object` | Full product name / description. |

### Financials

| Column | Type | Description |
|---|---|---|
| `sales` | `float64` | Revenue generated from the transaction (USD). Always ≥ 0. |
| `quantity` | `int64` | Number of units sold. Always ≥ 1. |
| `discount` | `float64` | Discount percentage applied (0.0 = no discount, 0.45 = 45% off). |
| `profit` | `float64` | Net profit after discount (USD). **Can be negative** — indicates a loss-making transaction. |

---

## Engineered Features (6)

Created in `notebooks/01_data_cleaning.ipynb`.

| Column | Type | Formula / Rule | Description |
|---|---|---|---|
| `profit_margin` | `float64` | `profit / sales` (0.0 if `sales == 0`) | Profitability ratio. A value of 0.30 means 30% profit margin. **⚠️ Contains outliers:** values range from approximately −2.75 to +0.50. Extreme negatives represent transactions where the loss far exceeded the revenue (e.g., heavy discounts on returned/low-margin items). These are valid business data — do not remove automatically, but account for them in visualizations and ML models (see note below). |
| `order_year` | `int64` | `order_date.dt.year` | Year the order was placed. Used for year-over-year analysis. |
| `order_month` | `int64` | `order_date.dt.month` | Month (1–12) the order was placed. Used for seasonality analysis. |
| `order_quarter` | `object` | `"Q" + order_date.dt.quarter` | Fiscal quarter label: `Q1`, `Q2`, `Q3`, `Q4`. |
| `shipping_days` | `int64` | `ship_date - order_date` (days) | Number of days between order placement and shipment. 0 = same-day ship. |
| `is_loss` | `bool` | `True` if `profit < 0` | Boolean flag for loss-making transactions. ~18.7% of rows are losses. |

---

## ⚠️ Notes on `profit_margin` Outliers

The `profit_margin` feature has extreme values at both tails:

```
count    9994.00
mean        0.12
std         0.24
min        -2.75    ← loss of 275% of revenue
25%         0.05
50%         0.14
75%         0.24
max         0.50
```

**Why this happens:**
- High discounts applied to low-revenue items can produce losses that exceed the sale price.
- Example: an item sold for $10 with a $27.50 loss yields `profit_margin = -2.75`.

**Guidance for downstream use:**
- **EDA:** Use `df["profit_margin"].describe()` and box plots to inspect the distribution. Discuss outliers explicitly.
- **ML Models:** Consider winsorizing or capping extreme values (e.g., clip to `[-1.0, 0.5]`) as a preprocessing step. Document any transformation applied.
- **Dashboards:** Use conditional formatting to highlight extreme margins.
- **Do NOT remove** these rows automatically — they represent real business events.

---

## Loading the Cleaned Dataset

```python
import pandas as pd

df = pd.read_csv(
    "data/processed/cleaned_sales.csv",
    parse_dates=["order_date", "ship_date"]
)
```

> **Important:** Always use `parse_dates` when loading the CSV. Without it, `order_date` and `ship_date` will be loaded as strings (`object` type) instead of `datetime64`.
