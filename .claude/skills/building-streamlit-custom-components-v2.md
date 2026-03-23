# Skill: Building Streamlit Custom Components v2

<!--
Purpose: Bidirectional custom components using st.components.v2 (CCv2).
Source: https://github.com/the-ai-buildr/st-agent-skills (building-streamlit-custom-components-v2)
-->

## When to Use

Building bidirectional custom UI components that need JavaScript/HTML not available in core Streamlit.

## Critical Rules

- **Never use v1 APIs:** no `st.components.v1`, no `components.declare_component()`,
  no `Streamlit.setComponentValue()`, no `window.Streamlit`, no `streamlit-component-lib` npm package.
- `st.components.v1` is deprecated — always use v2.
- Start inline; graduate to a packaged component only when the codebase outgrows a single file.
- Never hand-scaffold packaging/manifest/build wiring — always start from Streamlit's official
  `component-template v2`.

## Structure

```python
# Python side — wrap the callable
import streamlit.components.v2 as components

_my_component = components.component(
    name="my_component",
    script="""
    export default function(component) {
        const { setStateValue, setTriggerValue, parentElement, data } = component;
        // ... render UI, call setStateValue on user interaction
    }
    """,
)

def my_component(label: str, default: str = "") -> str:
    """My custom input component."""
    return _my_component(label=label, default=default, default_return=default)
```

## Frontend API

```javascript
export default function(component) {
    const { setStateValue, setTriggerValue, parentElement, data } = component;

    // Render into parentElement
    parentElement.innerHTML = `<input type="text" value="${data.default}">`;

    // Send value back to Python
    parentElement.querySelector("input").addEventListener("input", (e) => {
        setStateValue(e.target.value);
    });
}
```

## Styling

- Default `isolate_styles=True` runs in shadow DOM — styles don't leak in or out.
- Use `--st-*` CSS variables for theme adaptation:
  ```css
  color: var(--st-text-color);
  background: var(--st-background-color);
  border-color: var(--st-border-color);
  ```
