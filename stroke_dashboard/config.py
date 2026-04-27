APP_TITLE = "Kentucky Stroke Metrics for SEQIP"
HEADER_EYEBROW = "SEQIP statewide system of care group"
HEADER_DESCRIPTION = (
    "A dark, high-contrast operating view for statewide stroke access, "
    "throughput, and documentation performance across Kentucky regions."
)
HEADER_BADGE_LABEL = "Dummy data"
FOOTER_NOTE = (
    "Data are fabricated for product demonstration. Do not use for clinical, "
    "regulatory, or performance reporting."
)

REGIONS = {
    "Appalachian": ["Eastern Kentucky Stroke Center", "Bluegrass Mountain Health"],
    "Bluegrass": ["Lexington Comprehensive Stroke", "Frankfort Regional"],
    "Louisville": ["River City Medical Center", "Jefferson Stroke Institute"],
    "Northern Kentucky": ["Covington Medical", "Ohio River Health"],
    "Purchase/Pennyrile": ["Paducah Regional", "Pennyrile Community Hospital"],
}

METRIC_LABELS = {
    "door_to_needle": "Median door-to-needle time",
    "door_to_imaging": "Median door-to-imaging time",
    "discharge_antithrombotic": "Antithrombotic at discharge",
    "dysphagia_screen": "Dysphagia screen documented",
    "nihss_documented": "NIHSS documented",
    "transfer_acceptance": "Transfer acceptance under 20 min",
}

TARGETS = {
    "door_to_needle": 45,
    "door_to_imaging": 25,
    "discharge_antithrombotic": 95,
    "dysphagia_screen": 90,
    "nihss_documented": 92,
    "transfer_acceptance": 85,
}
