from extended_choices import Choices

EVENT_STATUS = Choices(
    ('RECEIVED', 1, 'received'),
    ('PARSED', 2, 'parsed'),
)

SLACK_COLORS = Choices(
    ('PRIMARY', 1, "#2980b9"),
    ('SUCCESS', 2, "#2ecc71"),
    ('INFO', 3, "#16a085"),
    ('WARNING', 4, "#f4a62a"),
    ('DANGER', 5, "#c0392b"),
)
