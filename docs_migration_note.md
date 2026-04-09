# Migration note

Removed/changed legacy behavior:
- Paragraph-spread expansion for missing page boundaries in chunk outputs has been removed.
- Donor-family detection no longer classifies by InDesign metadata alone.
- Queue checkpointing now runs during queue upserts for better crash durability.
