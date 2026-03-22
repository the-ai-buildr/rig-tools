# Skill: Using Streamlit Markdown

<!--
Purpose: Markdown, colored text, badges, icons, LaTeX, and all inline formatting in Streamlit.
Source: https://github.com/the-ai-buildr/st-agent-skills (using-streamlit-markdown)
-->

## When to Use

Using colored text, badges, icons, LaTeX, small text, or any Markdown formatting in Streamlit.

## Quick Reference

| Syntax | Result |
|---|---|
| `:red[text]` | Red colored text |
| `:blue-background[text]` | Blue background highlight |
| `:green-badge[text]` | Green badge (inline) |
| `:material/icon_name:` | Material icon |
| `$formula$` | Inline LaTeX |
| `$$formula$$` | Block LaTeX |
| `:small[text]` | Smaller text |
| `:large[text]` | Larger text |

**Available colors:** `red`, `orange`, `yellow`, `green`, `blue`, `violet`, `gray`/`grey`, `rainbow`, `primary`

Each color supports: `:color[text]`, `:color-background[text]`, `:color-badge[text]`

## Markdown Support Levels

**Full Markdown** (all syntax supported):
`st.markdown()`, `st.write()`, `st.caption()`, callout functions (`st.info`, `st.warning`, etc.),
`st.table` cells/headers, `help` tooltips

**Label subset** (inline formatting only — no headings/lists):
Widget labels, `st.tabs` names, `st.metric`, `st.title/header/subheader`, `st.button`, etc.

**No Markdown**:
`st.text()`, `st.json()`, dataframe cells, selectbox options, input placeholders, `st.Page` titles

## st.markdown() Parameters

```python
st.markdown("## Section title", text_alignment="center")  # "left"|"center"|"right"|"justify"
st.markdown("Wide content", width="stretch")               # "stretch"|"content"|pixels
```

## Patterns

```python
# Colored text and badges
st.markdown(":green[Well status: OK]  :red-badge[Kick alert]")

# Icon in markdown
st.markdown(":material/oil_barrel: **Mud weight:** 12.5 ppg")

# LaTeX formula
st.markdown("Hydrostatic pressure: $P_h = 0.052 \\times MW \\times TVD$")

# Status line with mixed formatting
st.markdown(
    ":blue-background[Active well]  "
    ":green-badge[Connected]  "
    ":material/schedule: Last sync: 14:32 UTC"
)

# Small caption-like text
st.markdown(":small[Data as of 2024-01-15. Refresh to update.]")
```
