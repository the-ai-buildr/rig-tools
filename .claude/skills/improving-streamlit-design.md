# Skill: Improving Streamlit Design

<!--
Purpose: Visual design patterns — icons, badges, spacing, typography, status indicators.
Source: https://github.com/the-ai-buildr/st-agent-skills (improving-streamlit-design)
-->

## When to Use

Improving visual appearance, adding icons, badges, spacing, or polishing existing UI.

## Rules

1. Use **Material icons** (`:material/icon_name:`) everywhere — prefer over emojis for professional look.
   Find icon names at [Google Fonts Icons](https://fonts.google.com/icons). Works in callouts,
   expanders, buttons, and tabs.
2. `st.badge()` standalone; `:green-badge[Active]` inline in markdown for status indicators.
3. **Sentence case** for all labels, titles, buttons — avoid Title Case ("Feels Shouty").
4. `st.caption()` for lightweight metadata; `st.info()` for important instructions;
   `st.toast()` for auto-dismissing confirmations (not `st.success()`).
5. Use `st.space()` with `"small"`, `"medium"`, `"large"`, or pixel value for vertical spacing.
6. `text_alignment` parameter on text elements: `"left"`, `"center"`, `"right"`, `"justify"`.
7. `st.set_page_config()` is called **once** in `app.py` — never repeat in pages or components.

## Patterns

```python
# Material icons in buttons
st.button(":material/calculate: Calculate", type="primary")
st.button(":material/restart_alt: Reset")
st.button(":material/download: Export report")

# Status badges
st.badge("Active", color="green")
st.badge("Offline", color="red")
# Inline in markdown
st.markdown(":green-badge[Active]  :red-badge[Offline]  :blue-badge[Pending]")

# Feedback patterns
st.caption("Last updated: 14:32 UTC")                           # lightweight info
st.info(":material/info: Fill in all fields before submitting.") # instruction
st.toast("Calculation saved!")                                   # transient confirmation

# Spacing
st.space("medium")
st.space(32)  # custom px

# Centered title
st.markdown("## Kill Sheet", unsafe_allow_html=False)  # text_alignment param on st.markdown
st.markdown("All results in US units.", text_alignment="center")
```
