import plotly.graph_objects as go
import numpy as np

def test_data():
    sect_y1 = np.arange(0, 2000, 100)
    sect_y2 = np.arange(1900, 5000, 100)
    sect_y3 = np.arange(4900, 9000, 100)
    sect_y4 = np.arange(8900, 20500, 100)

    left_x1 = np.full_like(sect_y1, -12.25, dtype=float)
    right_x1 = np.full_like(sect_y1, 12.25, dtype=float)
    left_x2 = np.full_like(sect_y2, -8.5, dtype=float)
    right_x2 = np.full_like(sect_y2, 8.5, dtype=float)
    left_x3 = np.full_like(sect_y3, -6.5, dtype=float)
    right_x3 = np.full_like(sect_y3, 6.5, dtype=float)
    left_x4 = np.full_like(sect_y4, -5.5, dtype=float)
    right_x4 = np.full_like(sect_y4, 5.5, dtype=float)

    well_sections = {
        "left_x": np.concatenate([left_x1, left_x2, left_x3, left_x4]),
        "right_x": np.concatenate([right_x1, right_x2, right_x3, right_x4]),
        "y": np.concatenate([sect_y1, sect_y2, sect_y3, sect_y4]),
    }

    return well_sections

def get_schematic_figure(data=None):
    fig = go.Figure()

    if data is None:
        data = test_data()

    left_x = np.asarray(data["left_x"])
    right_x = np.asarray(data["right_x"])
    y = np.asarray(data["y"])

    # Use one closed polygon for fill so the body renders uniformly.
    fill_x = np.concatenate([left_x, right_x[::-1]])
    fill_y = np.concatenate([y, y[::-1]])
    wellbore_color = "rgba(181, 101, 29, 1)"
    wellbore_fill_color = "rgba(181, 101, 29, 0.1)"

    # Surface line
    fig.add_shape(
        type="line",
        x0=0, x1=1,         # span full width (paper coords)
        y0=0, y1=0,         # y = 0
        xref="paper",       # full width regardless of x range
        yref="y",
        line=dict(color="black", width=2)
    )

    fig.add_trace(
        go.Scatter(
            x=fill_x,
            y=fill_y,
            mode="lines",
            line=dict(color=wellbore_color, width=0),
            name="Wellbore fill",
            fill="toself",
            fillcolor=wellbore_fill_color,
            showlegend=False,
            hoverinfo="skip",
        )
    )

    # Left Wellbore
    fig.add_trace(
        go.Scatter(
            x=left_x,
            y=y,
            mode="lines",
            line=dict(color=wellbore_color, width=2),
            name="Left wellbore",
            showlegend=False,
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=right_x,
            y=y,
            mode="lines",
            line=dict(color=wellbore_color, width=2),
            name="Right wellbore",
            showlegend=False,
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[left_x[-1], right_x[-1]],
            y=[y[-1], y[-1]],
            mode="lines",
            line=dict(color=wellbore_color, width=3),
            name="Bottom wellbore",
            showlegend=False,
            hoverinfo="skip",
        )
    )
    
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(range=[-20, 20], fixedrange=True)

    # Set a compact layout for embedding inside card-like UI.
    fig.update_layout(
        xaxis=dict(visible=False, fixedrange=True),
        autosize=True,
        margin=dict(l=12, r=8, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig