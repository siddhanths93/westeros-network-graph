import os
from pathlib import Path

import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components


# ──────────────────────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Westeros Network Graph",
    page_icon="⚔️",
    layout="wide",
)


# ──────────────────────────────────────────────────────────────
# Styling
# ──────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700;900&family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #080706;
    --panel: #11100d;
    --panel-2: #17130b;
    --panel-3: #1d170d;
    --gold: #d7b65d;
    --gold-soft: #b8943f;
    --gold-dim: #7e652b;
    --text: #f1ead8;
    --muted: #a79b82;
    --border: #3a2e15;
    --danger: #8b1e1e;
}

/* Main app */
.stApp {
    background:
        radial-gradient(circle at top center, rgba(215, 182, 93, 0.08), transparent 35%),
        radial-gradient(circle at 20% 15%, rgba(120, 23, 23, 0.14), transparent 30%),
        linear-gradient(180deg, #0b0907 0%, #050505 100%);
    color: var(--text);
}

.block-container {
    max-width: 1500px;
    padding-top: 1.6rem;
    padding-bottom: 3rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #0b0907 0%, #090807 100%);
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] * {
    font-family: Inter, sans-serif !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-family: Cinzel, serif !important;
    color: var(--gold) !important;
}

/* Text */
h1, h2, h3 {
    font-family: Cinzel, serif !important;
    color: var(--gold) !important;
    letter-spacing: 0.04em;
}

p, li, label, div, span {
    font-family: Inter, sans-serif;
}

hr {
    border-color: rgba(215, 182, 93, 0.16);
    margin-top: 1.1rem;
    margin-bottom: 1.1rem;
}

/* Header */
.main-title {
    font-family: Cinzel, serif;
    font-size: 2.45rem;
    font-weight: 900;
    color: var(--gold);
    text-align: center;
    letter-spacing: 0.09em;
    text-shadow: 0 0 24px rgba(215, 182, 93, 0.24);
    margin-bottom: 0.25rem;
}

.subtitle {
    font-family: Crimson Text, serif;
    font-size: 1.12rem;
    color: var(--muted);
    text-align: center;
    font-style: italic;
    margin-bottom: 1.7rem;
}

/* Cards */
.stat-box {
    background:
        linear-gradient(145deg, rgba(29, 23, 13, 0.92), rgba(10, 9, 7, 0.96));
    border: 1px solid rgba(215, 182, 93, 0.28);
    border-radius: 12px;
    padding: 1rem 0.8rem;
    text-align: center;
    min-height: 92px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.stat-number {
    font-family: Cinzel, serif;
    font-size: 1.65rem;
    font-weight: 800;
    color: var(--gold);
    line-height: 1.15;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.stat-label {
    font-size: 0.72rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.11em;
    margin-top: 0.35rem;
}

.insight-box {
    background:
        linear-gradient(90deg, rgba(54, 42, 18, 0.72), rgba(15, 13, 9, 0.9));
    border: 1px solid rgba(215, 182, 93, 0.22);
    border-left: 5px solid var(--gold);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 1.2rem 0 1.4rem 0;
    color: #e7dcc0;
    font-size: 0.95rem;
    line-height: 1.5;
}

.graph-shell {
    background:
        radial-gradient(circle at center, rgba(215, 182, 93, 0.05), transparent 42%),
        linear-gradient(180deg, #0d0c0a 0%, #070706 100%);
    border: 1px solid rgba(215, 182, 93, 0.24);
    border-radius: 16px;
    padding: 0.85rem;
    margin-top: 0.5rem;
}

.section-subtitle {
    color: var(--muted);
    font-size: 0.86rem;
    margin-top: -0.35rem;
    margin-bottom: 0.6rem;
}

/* Controls */
.stSelectbox label,
.stSlider label,
.stMultiSelect label {
    color: var(--gold) !important;
    font-size: 0.76rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.stMultiSelect div[data-baseweb="select"] > div,
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #17130b !important;
    border-color: rgba(215, 182, 93, 0.28) !important;
    color: var(--text) !important;
}

.stSlider [data-testid="stTickBar"] {
    display: none;
}

.stSlider div[role="slider"] {
    background-color: var(--gold) !important;
}

/* Ranking rows */
.rank-row {
    margin: 0.55rem 0 0.8rem 0;
}

.rank-line {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 0.28rem;
}

.rank-name {
    color: var(--text);
    font-size: 0.88rem;
    font-weight: 600;
}

.rank-value {
    color: var(--muted);
    font-size: 0.78rem;
}

.track {
    background: rgba(215, 182, 93, 0.11);
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
}

.fill {
    height: 8px;
    border-radius: 999px;
}

/* Footer */
.footer-note {
    text-align: center;
    color: rgba(167, 155, 130, 0.55);
    font-size: 0.78rem;
    margin-top: 1.4rem;
    font-style: italic;
}

/* Streamlit default cleanup */
div[data-testid="stToolbar"] {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}
</style>
""",
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────────────────────
# House colors
# ──────────────────────────────────────────────────────────────
HOUSE_COLORS = {
    "STARK": "#8fa3ad",
    "LANNISTER": "#d8b75d",
    "TARGARYEN": "#8b1e1e",
    "BARATHEON": "#c9a84c",
    "TYRELL": "#2f8f5b",
    "MARTELL": "#d9822b",
    "GREYJOY": "#6c7a7a",
    "TULLY": "#4169a8",
    "ARRYN": "#7db7d8",
    "BOLTON": "#7b1515",
    "FREY": "#8a5a2b",
    "NIGHT'S WATCH": "#2b2b2b",
    "WILDLING": "#8fbc8f",
    "OTHER": "#8f8f8f",
}

CHARACTER_HOUSE = {
    # Starks
    "NED": "STARK",
    "CATELYN": "STARK",
    "ROBB": "STARK",
    "SANSA": "STARK",
    "ARYA": "STARK",
    "BRAN": "STARK",
    "RICKON": "STARK",
    "BENJEN": "STARK",
    "LYANNA": "STARK",
    "HODOR": "STARK",

    # Lannisters
    "TYRION": "LANNISTER",
    "CERSEI": "LANNISTER",
    "JAIME": "LANNISTER",
    "TYWIN": "LANNISTER",
    "JOFFREY": "LANNISTER",
    "MYRCELLA": "LANNISTER",
    "TOMMEN": "LANNISTER",
    "LANCEL": "LANNISTER",
    "KEVAN": "LANNISTER",
    "MOUNTAIN": "LANNISTER",

    # Targaryens
    "DAENERYS": "TARGARYEN",
    "VISERYS": "TARGARYEN",
    "AEMON": "TARGARYEN",

    # Jon is intentionally mapped to Stark for the show-network view
    "JON": "STARK",

    # Night's Watch
    "SAM": "NIGHT'S WATCH",
    "MORMONT": "NIGHT'S WATCH",
    "THORNE": "NIGHT'S WATCH",
    "DOLOROUS": "NIGHT'S WATCH",
    "GRENN": "NIGHT'S WATCH",
    "PYPAR": "NIGHT'S WATCH",
    "ALLISER": "NIGHT'S WATCH",
    "JEOR": "NIGHT'S WATCH",

    # Baratheons
    "ROBERT": "BARATHEON",
    "STANNIS": "BARATHEON",
    "RENLY": "BARATHEON",
    "SHIREEN": "BARATHEON",
    "SELYSE": "BARATHEON",
    "DAVOS": "BARATHEON",
    "MELISANDRE": "BARATHEON",
    "GENDRY": "BARATHEON",

    # Tyrells
    "MARGAERY": "TYRELL",
    "LORAS": "TYRELL",
    "OLENNA": "TYRELL",
    "MACE": "TYRELL",

    # Greyjoys
    "THEON": "GREYJOY",
    "YARA": "GREYJOY",
    "ASHA": "GREYJOY",
    "BALON": "GREYJOY",
    "EURON": "GREYJOY",

    # Martells
    "OBERYN": "MARTELL",
    "ELLARIA": "MARTELL",
    "DORAN": "MARTELL",
    "TRYSTANE": "MARTELL",

    # Tully / Arryn / Bolton / Frey
    "EDMURE": "TULLY",
    "BLACKFISH": "TULLY",
    "BRYNDEN": "TULLY",
    "LYSA": "TULLY",
    "ROBIN": "ARRYN",
    "RAMSAY": "BOLTON",
    "ROOSE": "BOLTON",
    "WALDER": "FREY",

    # Free Folk
    "TORMUND": "WILDLING",
    "MANCE": "WILDLING",
    "YGRITTE": "WILDLING",
    "OSHA": "WILDLING",

    # Other
    "JORAH": "OTHER",
    "DAARIO": "OTHER",
    "MISSANDEI": "OTHER",
    "GREY WORM": "OTHER",
    "VARYS": "OTHER",
    "LITTLEFINGER": "OTHER",
    "PETYR": "OTHER",
    "BRONN": "OTHER",
    "PODRICK": "OTHER",
    "BRIENNE": "OTHER",
    "HOUND": "OTHER",
    "SANDOR": "OTHER",
    "BERIC": "OTHER",
    "GILLY": "OTHER",
    "SHAE": "OTHER",
}


def get_house(name: str) -> str:
    upper_name = name.upper()
    for key, house in CHARACTER_HOUSE.items():
        if key in upper_name:
            return house
    return "OTHER"


# ──────────────────────────────────────────────────────────────
# Data loading
# ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data() -> pd.DataFrame:
    dfs = []
    data_dir = Path(__file__).parent / "data"

    for season in range(1, 9):
        path = data_dir / f"got-s{season}-edges.csv"

        if path.exists():
            df = pd.read_csv(path)
            df["season"] = season
            dfs.append(df)

    if not dfs:
        return pd.DataFrame(columns=["Source", "Target", "Weight", "season"])

    return pd.concat(dfs, ignore_index=True)


@st.cache_data
def build_graph(seasons, min_weight: int, top_n: int):
    df = load_data()

    if df.empty:
        return nx.Graph(), pd.DataFrame(columns=["Source", "Target", "Weight"])

    df = df[df["season"].isin(seasons)]

    df_agg = (
        df.groupby(["Source", "Target"], as_index=False)["Weight"]
        .sum()
        .sort_values("Weight", ascending=False)
    )

    df_agg = df_agg[df_agg["Weight"] >= min_weight]

    G = nx.Graph()

    for _, row in df_agg.iterrows():
        G.add_edge(row["Source"], row["Target"], weight=float(row["Weight"]))

    if len(G.nodes) > top_n:
        strength = {
            node: sum(edge_data["weight"] for _, _, edge_data in G.edges(node, data=True))
            for node in G.nodes
        }
        top_chars = sorted(strength, key=strength.get, reverse=True)[:top_n]
        G = G.subgraph(top_chars).copy()

    return G, df_agg


def compute_metrics(G: nx.Graph) -> dict:
    if len(G.nodes) == 0:
        return {
            "betweenness": {},
            "degree": {},
            "strength": {},
        }

    for u, v, d in G.edges(data=True):
        d["distance"] = 1 / d["weight"]

    betweenness = nx.betweenness_centrality(G, weight="distance", normalized=True)

    degree = nx.degree_centrality(G)
    strength = {
        node: sum(edge_data["weight"] for _, _, edge_data in G.edges(node, data=True))
        for node in G.nodes
    }

    return {
        "betweenness": betweenness,
        "degree": degree,
        "strength": strength,
    }


def build_pyvis(G: nx.Graph, metrics: dict, color_by: str) -> Network:
    net = Network(
        height="720px",
        width="100%",
        bgcolor="#0b0907",
        font_color="#f1ead8",
    )

    net.barnes_hut(
        gravity=-14000,
        central_gravity=0.18,
        spring_length=230,
        spring_strength=0.025,
        damping=0.12,
    )

    betweenness = metrics.get("betweenness", {})
    strength = metrics.get("strength", {})

    max_strength = max(strength.values()) if strength else 1
    max_bc = max(betweenness.values()) if betweenness else 1

    for node in G.nodes():
        house = get_house(node)

        # if color_by == "House":
        #     color = HOUSE_COLORS.get(house, HOUSE_COLORS["OTHER"])
        # elif color_by == "Network Broker Score":
        #     value = betweenness.get(node, 0) / max_bc if max_bc else 0
        #     red = int(115 + 125 * value)
        #     green = int(75 + 80 * value)
        #     blue = int(20 + 25 * value)
        #     color = f"#{red:02x}{green:02x}{blue:02x}"
        # else:
        #     color = "#d7b65d"

        color = HOUSE_COLORS.get(house, HOUSE_COLORS["OTHER"])

        node_strength = strength.get(node, 0)
        size = 11 + 44 * (node_strength / max_strength if max_strength else 0)

        title = (
            f"{node}\n"
            f"House / faction: {house.title()}\n"
            f"Total interactions: {int(node_strength)}\n"
            f"Connections: {G.degree(node)}\n"
            f"Broker score: {betweenness.get(node, 0):.3f}"
        )

        net.add_node(
            node,
            label=node,
            color={
                "background": color,
                "border": "#0b0907",
                "highlight": {
                    "background": "#f0cf78",
                    "border": "#f1ead8",
                },
            },
            size=size,
            title=title,
            font={
                "color": "#f1ead8",
                "size": 15 if size > 32 else 12,
                "face": "Inter",
                "strokeWidth": 4,
                "strokeColor": "#080706",
            },
            borderWidth=2,
        )

    max_weight = max((edge_data["weight"] for _, _, edge_data in G.edges(data=True)), default=1)

    for source, target, edge_data in G.edges(data=True):
        weight = edge_data["weight"]
        width = 0.6 + 5.5 * (weight / max_weight if max_weight else 0)

        net.add_edge(
            source,
            target,
            value=weight,
            width=width,
            color={
                "color": "rgba(215, 182, 93, 0.24)",
                "highlight": "rgba(241, 234, 216, 0.65)",
            },
            title=f"{source} ↔ {target}: {int(weight)} interactions",
        )

    net.set_options(
        """
        {
          "interaction": {
            "hover": true,
            "tooltipDelay": 80,
            "navigationButtons": false,
            "keyboard": {
              "enabled": true
            }
          },
          "physics": {
            "enabled": true,
            "barnesHut": {
              "gravitationalConstant": -14000,
              "centralGravity": 0.18,
              "springLength": 230,
              "springConstant": 0.025,
              "damping": 0.12,
              "avoidOverlap": 0.35
            },
            "stabilization": {
              "enabled": true,
              "iterations": 220,
              "updateInterval": 20
            }
          },
          "nodes": {
            "shape": "dot",
            "shadow": {
              "enabled": true,
              "color": "rgba(215, 182, 93, 0.18)",
              "size": 8,
              "x": 0,
              "y": 0
            }
          },
          "edges": {
            "smooth": {
              "enabled": true,
              "type": "dynamic",
              "roundness": 0.35
            }
          }
        }
        """
    )

    return net


def render_rank_bar(name: str, value: float, max_value: float, color: str, label_value: str):
    width = int((value / max_value) * 100) if max_value else 0

    st.markdown(
        f"""
        <div class="rank-row">
            <div class="rank-line">
                <span class="rank-name">{name}</span>
                <span class="rank-value">{label_value}</span>
            </div>
            <div class="track">
                <div class="fill" style="width:{width}%; background:{color};"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────────────────────
# App
# ──────────────────────────────────────────────────────────────
st.markdown(
    '<div class="main-title"> WESTEROS NETWORK GRAPH</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">A character interaction map showing who connects the realm across Game of Thrones.</div>',
    unsafe_allow_html=True,
)

df_all = load_data()

if df_all.empty:
    st.error(
        "No data files found. Make sure the CSV files are inside a folder named `data` next to `app.py`."
    )
    st.code(
        """
westeros-network-graph/
  app.py
  data/
    got-s1-edges.csv
    got-s2-edges.csv
    ...
        """,
        language="text",
    )
    st.stop()


# Sidebar controls
with st.sidebar:
    st.markdown("### ⚔️ Controls")
    st.markdown("---")

    seasons = st.multiselect(
        "Seasons",
        options=list(range(1, 9)),
        default=[1],
        format_func=lambda x: f"Season {x}",
    )

    top_n = st.slider(
        "Top N characters",
        min_value=10,
        max_value=100,
        value=35,
        step=5,
    )

    min_weight = st.slider(
        "Minimum interactions",
        min_value=1,
        max_value=50,
        value=8,
        step=1,
    )

    # color_by = st.selectbox(
    #     "Color nodes by",
    #     ["House", "Network Broker Score", "None"],
    # )
    #
    color_by = "House"

    st.markdown("---")
    st.markdown("### 🏰 House Legend")

    legend_houses = [
        "STARK",
        "LANNISTER",
        "TARGARYEN",
        "BARATHEON",
        "TYRELL",
        "MARTELL",
        "GREYJOY",
        "NIGHT'S WATCH",
        "WILDLING",
        "OTHER",
    ]

    for house in legend_houses:
        color = HOUSE_COLORS.get(house, HOUSE_COLORS["OTHER"])
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:8px;margin:7px 0;">
                <div style="width:11px;height:11px;border-radius:50%;background:{color};border:1px solid rgba(241,234,216,0.25);"></div>
                <span style="font-size:0.83rem;color:#a79b82;">{house.title()}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # st.markdown("---")
    # st.caption("Data source: Andrew Beveridge's Network of Thrones dataset.")


if not seasons:
    st.warning("Select at least one season from the sidebar.")
    st.stop()


with st.spinner("Forging the network of Westeros..."):
    G, df_agg = build_graph(tuple(seasons), min_weight, top_n)
    metrics = compute_metrics(G)

betweenness = metrics.get("betweenness", {})
strength = metrics.get("strength", {})

top_broker = max(betweenness, key=betweenness.get) if betweenness else "—"
top_interactions = max(strength, key=strength.get) if strength else "—"

try:
    bridge_edges = list(nx.bridges(G))
    bridge_count = len(bridge_edges)
except Exception:
    bridge_count = 0

season_label = (
    f"Season {seasons[0]}"
    if len(seasons) == 1
    else f"Seasons {min(seasons)}–{max(seasons)}"
)


# KPI row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="stat-box">
            <div class="stat-number">{len(G.nodes)}</div>
            <div class="stat-label">Characters</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="stat-box">
            <div class="stat-number">{len(G.edges)}</div>
            <div class="stat-label">Connections</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="stat-box">
            <div class="stat-number">{top_broker}</div>
            <div class="stat-label">Network Broker</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f"""
        <div class="stat-box">
            <div class="stat-number">{top_interactions}</div>
            <div class="stat-label">Most Interactions</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Insight callout
if top_broker != "—":
    st.markdown(
        f"""
        <div class="insight-box">
            <b>{top_broker}</b> has the highest network broker score in {season_label}.
            That means this character sits between important groups and helps connect parts of the realm
            that would otherwise be less connected.
        </div>
        """,
        unsafe_allow_html=True,
    )


# Network visualization
st.markdown("### Character Network")
st.markdown(
    '<div class="section-subtitle">Node size = total interactions · Color = house/faction · Hover for details · Drag to explore</div>',
    unsafe_allow_html=True,
)

net = build_pyvis(G, metrics, color_by)

html_path = Path(__file__).parent / "got_network.html"
net.save_graph(str(html_path))

with open(html_path, "r", encoding="utf-8") as file:
    html = file.read()

html = html.replace(
    "<body>",
    '<body style="background-color:#0b0907;margin:0;padding:0;overflow:hidden;">',
)

st.markdown('<div class="graph-shell">', unsafe_allow_html=True)
components.html(html, height=740, scrolling=False)
st.markdown("</div>", unsafe_allow_html=True)


st.markdown("---")


# Bottom analysis
left_col, right_col = st.columns(2)

with left_col:
    st.markdown("### Network Brokers")
    st.markdown(
        """
        <div class="section-subtitle">
            Characters ranked by broker score, using betweenness centrality.
            A higher score means the character acts as a bridge between different groups in the network.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="insight-box" style="margin-top:0.6rem; margin-bottom:1rem;">
            <b>How to read this:</b><br>
            Broker score ranges from <b>0 to 1</b>. A score near 0 means the character is not a major bridge.
            A higher score means more character connections flow through them. In simple terms, these are the people
            who help connect separate houses, factions, or story clusters.
        </div>
        """,
        unsafe_allow_html=True,
    )

    rankings = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]
    max_rank_score = rankings[0][1] if rankings else 1

    if not rankings:
        st.info("No ranking available with the selected filters.")
    else:
        for index, (character, score) in enumerate(rankings, start=1):
            house = get_house(character)
            color = HOUSE_COLORS.get(house, HOUSE_COLORS["OTHER"])
            render_rank_bar(
                name=f"{index}. {character}",
                value=score,
                max_value=max_rank_score,
                color=color,
                label_value=f"{score:.3f}",
            )


with right_col:
    st.markdown("### Most Frequent Pairings")
    st.markdown(
        '<div class="section-subtitle">Character pairs with the highest interaction weight in the selected view.</div>',
        unsafe_allow_html=True,
    )

    if len(G.nodes) == 0:
        st.info("No pairings available with the selected filters.")
    else:
        top_edges = df_agg[
            (df_agg["Source"].isin(G.nodes)) & (df_agg["Target"].isin(G.nodes))
        ].sort_values("Weight", ascending=False).head(10)

        max_edge_weight = top_edges["Weight"].max() if not top_edges.empty else 1

        for _, row in top_edges.iterrows():
            render_rank_bar(
                name=f"{row['Source']} ↔ {row['Target']}",
                value=float(row["Weight"]),
                max_value=float(max_edge_weight),
                color="#d7b65d",
                label_value=str(int(row["Weight"])),
            )


st.markdown("---")

footer_cols = st.columns(3)

with footer_cols[0]:
    st.markdown(
        f"""
        <div class="stat-box">
            <div class="stat-number">{season_label}</div>
            <div class="stat-label">Selected View</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with footer_cols[1]:
    st.markdown(
        f"""
        <div class="stat-box">
            <div class="stat-number">{min_weight}+</div>
            <div class="stat-label">Min Interactions</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with footer_cols[2]:
    st.markdown(
        f"""
        <div class="stat-box">
            <div class="stat-number">{bridge_count}</div>
            <div class="stat-label">Critical Bridges</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="insight-box">
            <b>Critical Bridges:</b> These are fragile connections that hold parts of the network together.
            If one of these links is removed, a group of characters may become disconnected from the rest of the realm.
            A value of <b>0</b> means the selected network is not dependent on any single relationship link.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="footer-note">
        Data source: Andrew Beveridge's Network of Thrones dataset.
        This prototype uses character interaction edges to estimate centrality, influence, and connection strength.
    </div>
    """,
    unsafe_allow_html=True,
)