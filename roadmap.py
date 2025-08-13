import pandas as pd
import graphviz
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

# --- Common Data and Configuration ---

# FONT_NAME 保持不变
FONT_NAME = "Inter"

# 网页设计风格的颜色体系
# Sourced from your student_dashboard.html CSS
THEME_COLORS = {
    'primary_light': '#E6FFFA', # Mastered
    'proficient_yellow': '#FEFCE8', # A softer yellow for Proficient
    'review_red': '#FEE2E2',      # A softer red for Needs Review
    'not_started_grey': '#F7FAFC', # Not Started (same as cluster bg)
    'border': '#E2E8F0',
    'text_dark': '#2D3748',
    'text_light': '#5A6A85',
    'cluster_bg': '#FFFFFF'
}

# 更新后的状态映射和颜色
status_map = {
    4: 'Mastered', 3: 'Proficient', 2: 'Needs Review', 1: 'Not Started'
}
colors = {
    4: THEME_COLORS['primary_light'],
    3: THEME_COLORS['proficient_yellow'],
    2: THEME_COLORS['review_red'],
    1: THEME_COLORS['not_started_grey']
}

# Student's initial status
initial_status = {
    'misa': 3, 'complex': 2, 'trig': 2, 'function': 2, 'log': 4, 'exp': 4,
    'equation': 3, 'poly': 2, 'seq': 2, 'stats': 2, 'circle': 2, 'angle': 3,
    'coor': 2, 'length': 2, '3d': 1, 'area': 2, 'sim': 2, 'base': 1,
    'mod': 1, 'factor': 2, 'div': 2, 'lcm': 2, 'digit': 1, 'Markov': 1,
    'Recursion': 1, 'logic': 3, 'uniform': 2, 'geom': 1, 'game': 1,
    'Expectation': 1, 'count': 2, 'prob': 2
}

# Knowledge map data
data = {
    'topic_code': list(initial_status.keys()),
    'Topic': ['Miscellaneous Algebra', 'Complex Numbers', 'Trigonometry', 'Functions', 'Logarithms', 'Exponents', 'Equations', 'Polynomials', 'Sequences', 'Statistics', 'Circles', 'Angles', 'Coordinate Geometry', 'Length', '3D Geometry', 'Area', 'Similarity', 'Number Bases', 'Modular Arithmetic', 'Factoring', 'Divisibility', 'LCM/GCF', 'Digits', 'Markov Chains', 'Recursion', 'Logic', 'Uniform Probability', 'Geometric Probability', 'Game Theory', 'Expected Value', 'Counting', 'Probability'],
    'Division': ['Algebra', 'Algebra', 'Algebra', 'Algebra', 'Algebra', 'Algebra', 'Algebra', 'Algebra', 'Algebra', 'Combinatorics', 'Geometry', 'Geometry', 'Geometry', 'Geometry', 'Geometry', 'Geometry', 'Geometry', 'Number Theory', 'Number Theory', 'Number Theory', 'Number Theory', 'Number Theory', 'Number Theory', 'Combinatorics', 'Combinatorics', 'Combinatorics', 'Combinatorics', 'Combinatorics', 'Combinatorics', 'Combinatorics', 'Combinatorics', 'Combinatorics']
}
df = pd.DataFrame(data)
df['status_code'] = df['topic_code'].map(initial_status)
df['status_label'] = df['status_code'].map(status_map)

# Edge definitions
edges = [
    # --- Algebra Core ---
    ('function', 'poly'),
    ('function', 'trig'),
    ('function', 'seq'),
    ('function', 'equation'),
    ('equation', 'poly'),
    ('complex', 'poly'),
    ('complex', 'trig'),
    ('exp', 'log'),
    ('log', 'equation'),
    ('misa', 'equation'),

    # --- Number Theory Core ---
    ('div', 'factor'),
    ('factor', 'lcm'),
    ('div', 'mod'),
    ('mod', 'base'),
    ('base', 'digit'),

    # --- Geometry Core ---
    ('angle', 'trig'),
    ('angle', 'circle'),
    ('length', 'area'),
    ('length', 'sim'),
    ('area', '3d'),
    ('coor', 'area'),
    ('coor', 'sim'),
    ('coor', 'circle'),

    # --- Counting & Probability Core ---
    ('logic', 'count'),
    ('count', 'prob'),
    ('count', 'Recursion'),
    ('count', 'geom'),
    ('prob', 'stats'),
    ('prob', 'Expectation'),
    ('prob', 'uniform'),
    ('prob', 'game'),
    ('prob', 'Markov'),

    # --- Inter-Component Bridges ---
    # Number Theory -> Algebra
    ('mod', 'poly'),
    # Geometry -> Counting
    ('coor', 'geom'),
    # Algebra -> Counting
    ('seq', 'prob'),
]

# --- Step 1: Generate the main knowledge graph image ---

try:
    dot_map = graphviz.Digraph('Knowledge_Map_Part')
    # Global graph attributes
    dot_map.attr(
        rankdir='TB',
        # label='AMC10 Personalized Knowledge Map - Alex',
        labelloc='t',
        fontsize='24',
        fontname=FONT_NAME,
        fontcolor=THEME_COLORS['text_dark'],
        bgcolor=THEME_COLORS['cluster_bg']
    )
    # Global node attributes
    dot_map.attr(
        'node',
        shape='box',
        style='rounded,filled',
        fontname=FONT_NAME,
        fontcolor=THEME_COLORS['text_dark'],
        color=THEME_COLORS['border']
    )
    # Global edge attributes
    dot_map.attr(
        'edge',
        color=THEME_COLORS['text_light']
    )

    for division in df['Division'].unique():
        with dot_map.subgraph(name=f'cluster_{division}') as c:
            # Cluster styling to simulate a card with a transparent background
            c.attr(
                label=division,
                style='rounded',
                bgcolor='transparent',
                color=THEME_COLORS['border'],
                fontname=FONT_NAME,
                fontcolor=THEME_COLORS['text_dark']
            )
            nodes = df[df['Division'] == division]
            for _, row in nodes.iterrows():
                # Dynamically highlight border for mastered topics
                node_border_color = THEME_COLORS['primary_light'] if row['status_code'] == 4 else THEME_COLORS['border']
                c.node(
                    row['topic_code'],
                    label=row['Topic'],
                    fillcolor=colors[row['status_code']],
                    color=node_border_color
                )
    
    dot_map.edges(edges)
    graph_filename_base = 'knowledge_graph_part'
    dot_map.render(graph_filename_base, format='png', cleanup=True)
    graph_filename_png = f'{graph_filename_base}.png'
    print(f"Successfully generated '{graph_filename_png}'")
except Exception as e:
    print(f"Failed to generate the knowledge graph part. Error: {e}")
    graph_filename_png = None

# --- Step 2: Generate the aligned footer image ---

try:
    dot_footer = graphviz.Digraph('Footer_Part_Aligned')
    dot_footer.attr(rankdir='TB', ranksep='0.3', nodesep='0.2')

    # Row 1: Explanation
    with dot_footer.subgraph(name='explanation_row') as s:
        s.attr(rank='same')
        s.node('node_A', 'Topic A', shape='box', style='rounded,filled', fillcolor='#E0E0E0', fontname=FONT_NAME)
        s.node('node_B', 'Topic B', shape='box', style='rounded,filled', fillcolor='#E0E0E0', fontname=FONT_NAME)
        s.node('explanation_text', '  Means: "Topic A" is a prerequisite for "Topic B"', shape='plaintext', fontsize='12', fontname=FONT_NAME)
        s.edge('node_A', 'node_B')
        s.edge('node_B', 'explanation_text', style='invis', constraint='false')

    # Row 2: Legend
    with dot_footer.subgraph(name='legend_row') as s:
        s.attr(rank='same')
        s.attr('node', shape='box', style='filled', fontsize='12', fontname=FONT_NAME)
        s.node('legend_mastered', 'Mastered', fillcolor=colors[4])
        s.node('legend_proficient', 'Proficient', fillcolor=colors[3])
        s.node('legend_review', 'Needs Review', fillcolor=colors[2])
        s.node('legend_not_started', 'Not Started', fillcolor=colors[1])
        s.edge('legend_mastered', 'legend_proficient', style='invis')
        s.edge('legend_proficient', 'legend_review', style='invis')
        s.edge('legend_review', 'legend_not_started', style='invis')

    dot_footer.edge('node_A', 'legend_mastered', style='invis')

    footer_filename_base = 'footer_part_aligned'
    dot_footer.render(footer_filename_base, format='png', cleanup=True)
    footer_filename_png = f'{footer_filename_base}.png'
    print(f"Successfully generated '{footer_filename_png}'")

except Exception as e:
    print(f"Failed to generate the footer part. Error: {e}")
    footer_filename_png = None



# --- Step 3: Stitch the two images together ---

if graph_filename_png and footer_filename_png:
    try:
        img_graph = mpimg.imread(graph_filename_png)
        img_footer = mpimg.imread(footer_filename_png)
        h_graph, w_graph, _ = img_graph.shape
        h_footer, w_footer, _ = img_footer.shape
        
        vertical_margin_pixels = 40

        new_width = max(w_graph, w_footer)
        new_height = h_graph + h_footer + vertical_margin_pixels

        fig = plt.figure(figsize=(new_width / 100, new_height / 100), dpi=100)

        graph_height_prop = h_graph / new_height
        footer_height_prop = h_footer / new_height
        margin_height_prop = vertical_margin_pixels / new_height

        footer_bottom_prop = 0
        graph_bottom_prop = footer_height_prop + margin_height_prop

        graph_x_pos = (new_width - w_graph) / 2 / new_width
        footer_x_pos = (new_width - w_footer) / 2 / new_width
        
        ax_graph = fig.add_axes([graph_x_pos, graph_bottom_prop, w_graph/new_width, graph_height_prop])
        ax_graph.imshow(img_graph)
        ax_graph.axis('off')

        ax_footer = fig.add_axes([footer_x_pos, footer_bottom_prop, w_footer/new_width, footer_height_prop])
        ax_footer.imshow(img_footer)
        ax_footer.axis('off')

        final_filename = 'student_knowledge_map_alex.png'
        plt.savefig(final_filename, dpi=100, bbox_inches='tight', pad_inches=0.05, facecolor='white')
        print(f"\nSuccessfully stitched images into '{final_filename}'")
        os.remove(graph_filename_png)
        os.remove(footer_filename_png)

    except Exception as e:
        print(f"\nFailed to stitch images. Error: {e}")

