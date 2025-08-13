import pandas as pd
import graphviz

# --- 数据准备 (与之前相同) ---
df = pd.read_csv('mapping.csv')
initial_status = {
    'misa': 3, 'complex': 2, 'trig': 3, 'function': 2, 'log': 4, 'exp': 4,
    'equation': 3, 'poly': 3, 'seq': 2, 'stats': 3, 'circle': 2, 'angle': 3,
    'coor': 3, 'length': 2, '3d': 1, 'area': 2, 'sim': 2, 'base': 1,
    'mod': 1, 'factor': 2, 'div': 2, 'lcm': 3, 'digit': 1, 'Markov': 1,
    'Recursion': 1, 'logic': 3, 'uniform': 2, 'geom': 1, 'game': 1,
    'Expectation': 1, 'count': 2, 'prob': 2
}
status_after_foundation = {k: 3 if v <= 2 else v for k, v in initial_status.items()}
df['status_code'] = df['topic_code'].map(status_after_foundation)
status_map = {
    4: '已掌握', 3: '表现不错', 2: '需要复习', 1: '还未开始'
}
df['status_label'] = df['status_code'].map(status_map)

# --- 可视化设计 (优化版) ---

# 使用'dot'引擎，更适合层级关系。fontname设为您参考网站中的'Inter'字体。
dot = graphviz.Digraph('AMC10_Knowledge_Map_Enhanced', comment='Enhanced AMC10 Learning Path')
dot.attr(layout='dot', rankdir='TB', splines='ortho', label='AMC10 知识图谱 (增强版)', labelloc='t', fontsize='20', fontname='Inter')
dot.attr('node', shape='record', style='rounded,filled', fontname='Inter', color='#B0BEC5')
dot.attr('edge', color='#546E7A', arrowhead='normal', penwidth='1.5')


# 定义状态颜色
colors = {
    4: '#A5D6A7', # Mastered (柔和绿)
    3: '#FFF59D', # Proficient (柔和黄)
    2: '#EF9A9A', # Needs Review (柔和红)
    1: '#ECEFF1'  # Not Started (高级灰)
}

# 按Division创建子图
for division in df['Division'].unique():
    with dot.subgraph(name=f'cluster_{division}') as c:
        c.attr(label=division, style='rounded', color='#78909C', fontname='Inter', fontcolor='#37474F')
        nodes = df[df['Division'] == division]
        for _, row in nodes.iterrows():
            # 使用 record shape, 可以创建更复杂的节点布局
            label = f"{{ {row['Topic']} | <status> {row['status_label']} }}"
            c.node(
                row['topic_code'],
                label=label,
                fillcolor=colors[row['status_code']]
            )

# --- 核心优化：增加更丰富的知识点依赖关系 ---
enhanced_edges = [
    # Algebra
    ('equation', 'poly'), ('poly', 'function'), ('exp', 'log'), ('seq', 'function'),
    # Number Theory
    ('div', 'factor'), ('div', 'lcm'), ('factor', 'mod'), ('div', 'base'), ('div', 'digit'),
    # Geometry
    ('angle', 'trig'), ('length', 'area'), ('area', '3d'), ('sim', 'length'), ('sim', 'area'),
    # Counting
    ('count', 'prob'), ('prob', 'uniform'), ('prob', 'Expectation'), ('count', 'Recursion'),
    ('prob', 'Markov'), ('logic', 'game'),
    # Cross-Disciplinary
    ('equation', 'coor'), ('trig', 'coor'), ('circle', 'coor'),
    ('area', 'geom'), ('count', 'geom'), ('trig', 'complex')
]
dot.edges(enhanced_edges)

# 保存并渲染图像
try:
    output_filename = 'student_knowledge_map_enhanced'
    dot.render(output_filename, format='png', cleanup=True)
    print(f"\n已成功生成优化后的知识图谱可视化文件: {output_filename}.png")
except Exception as e:
    print(f"\n生成图像失败，请确保您已安装Graphviz软件并将其添加至系统路径。错误信息: {e}")
    print("代码已准备好，您可以在配置正确的环境中运行它。")