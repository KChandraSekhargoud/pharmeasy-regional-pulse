# Data Quality Report

This report maps the data cleaning steps applied in the pipeline to specific data-quality dimensions.

1. **Removing exact duplicates (59 rows):** Addresses **Uniqueness**. Ensures that no single transaction is counted multiple times in the reporting metrics, preventing revenue inflation.
2. **Normalizing region text (16 raw variants to 9 canonical):** Addresses **Consistency**. Fixes trailing spaces and varied capitalization (e.g., " hyderabad" vs "HYDERABAD ") so that aggregation functions group the data correctly.
3. **Imputing missing category via exact product lookup:** Addresses **Completeness** and **Accuracy**. Recovers 48 missing category fields using a deterministic 1:1 mapping from the product column, ensuring no data is dropped while maintaining 100% accuracy.
4. **Imputing missing profit_inr via category mean margin:** Addresses **Completeness** and **Validity**. Recovers 94 missing profit values by applying a statistically sound category-level margin to the existing valid sales figures.