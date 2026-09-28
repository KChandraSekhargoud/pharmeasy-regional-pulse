def draft_report_v1(flagged_regions, metrics_dict):
    report_blocks = []
    for region, change in flagged_regions.items():
        block = f"""Context: The region {region} was evaluated against the 8% MoM deviation threshold.
Insight: {region} experienced a significant shift, recording a {change:+.2f}% Month-on-Month movement.
Implication: Operational and supply chain leads should review {region}'s inventory allocation to accommodate this structural shift."""
        report_blocks.append(block)
    return "\n\n".join(report_blocks)