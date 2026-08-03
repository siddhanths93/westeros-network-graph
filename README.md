# ⚔️ The Data Science of Westeros — Character Network Graph

An interactive network graph analysing character relationships, power, and influence across all 8 seasons of Game of Thrones.

## Features
- **Interactive network** — drag, zoom, hover for character details
- **Season filter** — watch the network evolve across seasons
- **House colouring** — see alliances visually
- **Power rankings** — betweenness centrality reveals the true power brokers
- **Strongest bonds** — which character pairs interacted most

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Download the data
```bash
mkdir data
for i in 1 2 3 4 5 6 7 8; do
  curl -o data/got-s${i}-edges.csv \
    https://raw.githubusercontent.com/mathbeveridge/gameofthrones/master/data/got-s${i}-edges.csv
done
```

### 3. Run the app
```bash
streamlit run app.py
```

## Data Source
Andrew Beveridge's "Network of Thrones"  
https://github.com/mathbeveridge/gameofthrones

Characters are connected when they speak to or about each other, appear in the same scene, or are mentioned together. Edge weight = number of such interactions.

## Key Concepts Used
- **Betweenness Centrality** — measures how often a character sits on the shortest path between two others. High score = political broker / power bridge.
- **Degree Centrality** — how many unique characters someone interacts with.
- **Interaction Strength** — total weighted interactions across selected seasons.

## Tech Stack
- Python · NetworkX · PyVis · Pandas · Streamlit
