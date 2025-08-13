import pandas as pd
import graphviz
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

# --- Common Data and Configuration ---

# Status mapping and colors
status_map = {
    4: 'Mastered', 3: 'Proficient', 2: 'Needs Review', 1: 'Not Started'
}
colors = {
    4: '#C8E6C9', 3: '#FFF9C4', 2: '#FFCDD2', 1: '#F5F5F5'
}

# Student's initial status
initial_status = {
    'misa': 3, 'complex': 2, 'trig': 3, 'function': 2, 'log': 4, 'exp': 4,
    'equation': 3, 'poly': 3, 'seq': 2, 'stats': 3, 'circle': 2, 'angle': 3,
    'coor': 3, 'length': 2, '3d': 1, 'area': 2, 'sim': 2, 'base': 1,
    'mod': 1, 'factor': 2, 'div': 2, 'lcm': 3, 'digit': 1, 'Markov': 1,
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
    ('exp', 'log'), ('poly', 'function'), ('equation', 'poly'), ('trig', 'function'), ('complex', 'poly'), ('misa', 'equation'), ('seq', 'function'),
    ('div', 'factor'), ('factor', 'mod'), ('div', 'lcm'), ('base', 'digit'), ('lcm', 'factor'),
    ('angle', 'trig'), ('length', 'area'), ('area', '3d'), ('sim', 'coor'), ('circle', 'coor'), ('angle', 'circle'), ('length', 'sim'), ('coor', 'area'),
    ('logic', 'count'), ('count', 'prob'), ('prob', 'Expectation'), ('prob', 'uniform'), ('count', 'Recursion'), ('count', 'geom'), ('stats', 'prob'), ('prob', 'game'), ('uniform', 'Expectation'), ('geom', 'Expectation')
]

# --- Step 1: Generate the main knowledge graph image (No changes here) ---

try:
    dot_map = graphviz.Digraph('Knowledge_Map_Part')
    dot_map.attr(rankdir='TB', label='AMC10 Personalized Learning Path - Alex', labelloc='t', fontsize='24', fontname="Helvetica")
    dot_map.attr('node', shape='box', style='rounded,filled', fontname="Helvetica")
    for division in df['Division'].unique():
        with dot_map.subgraph(name=f'cluster_{division}') as c:
            c.attr(label=division, style='rounded', color='lightblue', fontname="Helvetica-Bold")
            nodes = df[df['Division'] == division]
            for _, row in nodes.iterrows():
                c.node(row['topic_code'], label=f"{row['Topic']}\n{row['status_label']}", fillcolor=colors[row['status_code']])
    dot_map.edges(edges)
    graph_filename_base = 'knowledge_graph_part'
    dot_map.render(graph_filename_base, format='png', cleanup=True)
    graph_filename_png = f'{graph_filename_base}.png'
    print(f"Successfully generated '{graph_filename_png}'")
except Exception as e:
    print(f"Failed to generate the knowledge graph part. Error: {e}")
    graph_filename_png = None


# --- Step 2: Generate the NEW aligned footer image ---

try:
    dot_footer = graphviz.Digraph('Footer_Part_Aligned')
    dot_footer.attr(rankdir='TB', ranksep='0.3', nodesep='0.2')

    # Row 1: Explanation (Diagram + Text on one line)
    with dot_footer.subgraph(name='explanation_row') as s:
        s.attr(rank='same') # Force all items in this subgraph to be on the same horizontal line
        s.node('node_A', 'Topic A', shape='box', style='rounded,filled', fillcolor='#E0E0E0', fontname="Helvetica")
        s.node('node_B', 'Topic B', shape='box', style='rounded,filled', fillcolor='#E0E0E0', fontname="Helvetica")
        s.node('explanation_text', '  Means: "Topic A" is a prerequisite for "Topic B"', shape='plaintext', fontsize='12', fontname="Helvetica")
        # Define the layout order for this row: A -> B, then the text
        s.edge('node_A', 'node_B')
        s.edge('node_B', 'explanation_text', style='invis', constraint='false') # Invisible edge for ordering

    # Row 2: Legend
    with dot_footer.subgraph(name='legend_row') as s:
        s.attr(rank='same') # Force all items onto a single horizontal line
        s.attr('node', shape='box', style='filled', fontsize='12', fontname="Helvetica")
        s.node('legend_mastered', 'Mastered', fillcolor=colors[4])
        s.node('legend_proficient', 'Proficient', fillcolor=colors[3])
        s.node('legend_review', 'Needs Review', fillcolor=colors[2])
        s.node('legend_not_started', 'Not Started', fillcolor=colors[1])
        s.edge('legend_mastered', 'legend_proficient', style='invis')
        s.edge('legend_proficient', 'legend_review', style='invis')
        s.edge('legend_review', 'legend_not_started', style='invis')

    # Add an invisible edge to stack the two rows vertically and ensure left-alignment
    dot_footer.edge('node_A', 'legend_mastered', style='invis')

    footer_filename_base = 'footer_part_aligned'
    dot_footer.render(footer_filename_base, format='png', cleanup=True)
    footer_filename_png = f'{footer_filename_base}.png'
    print(f"Successfully generated '{footer_filename_png}'")

except Exception as e:
    print(f"Failed to generate the footer part. Error: {e}")
    footer_filename_png = None



# --- Step 3: Stitch the two images together (MODIFIED FOR SPACING) ---

if graph_filename_png and footer_filename_png:
    try:
        img_graph = mpimg.imread(graph_filename_png)
        img_footer = mpimg.imread(footer_filename_png)
        h_graph, w_graph, _ = img_graph.shape
        h_footer, w_footer, _ = img_footer.shape

        # *** CHANGE IS HERE: Define the vertical space between images in pixels ***
        # You can change this value to increase or decrease the space.
        vertical_margin_pixels = 40

        # Calculate the new total dimensions, including the margin
        new_width = max(w_graph, w_footer)
        new_height = h_graph + h_footer + vertical_margin_pixels

        # Create the figure with the new calculated size
        fig = plt.figure(figsize=(new_width / 100, new_height / 100), dpi=100)

        # Convert all pixel heights to proportions of the new total height
        graph_height_prop = h_graph / new_height
        footer_height_prop = h_footer / new_height
        margin_height_prop = vertical_margin_pixels / new_height

        # Define the 'bottom' y-coordinate for each image as a proportion
        footer_bottom_prop = 0
        graph_bottom_prop = footer_height_prop + margin_height_prop

        # Calculate horizontal positions for centering
        graph_x_pos = (new_width - w_graph) / 2 / new_width
        footer_x_pos = (new_width - w_footer) / 2 / new_width
        
        # Place the graph image at the top
        ax_graph = fig.add_axes([graph_x_pos, graph_bottom_prop, w_graph/new_width, graph_height_prop])
        ax_graph.imshow(img_graph)
        ax_graph.axis('off')

        # Place the footer image at the bottom
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