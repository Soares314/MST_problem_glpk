import networkx as nx
from itertools import combinations

def find_connected_subgraphs(G):
    """
    Encontra todos os subgrafos conexos com mais de 2 vertices em um grafo G.
    G: Grafo NetworkX não direcionado
    Retorna: Lista de subgrafos conexos
    """
    def dfs_subset(start_node, nodes, visited, current_subgraph):
        """
        Função auxiliar DFS para gerar subgrafos conexos a partir de um conjunto de vertices
        """
        subgraphs = []
        # Criar subgrafo induzido pelos vertices no current_subgraph
        if len(current_subgraph) > 2:
            subgraph = G.subgraph(current_subgraph)
            if nx.is_connected(subgraph):  # Verifica se o subgrafo é conexo
                subgraphs.append(subgraph)
        
        # Explora vertices não visitados
        for node in nodes:
            if node not in visited:  # Evita duplicatas
                visited.add(node)
                # Adiciona nó ao subgrafo atual e continua DFS
                subgraphs.extend(dfs_subset(start_node, nodes, visited, current_subgraph | {node}))
                visited.remove(node)
        
        return subgraphs

    # Lista para armazenar todos os subgrafos conexos
    all_subgraphs = []
    nodes = list(G.nodes())

    # Para cada nó, tenta construir subgrafos conexos começando por ele
    for start_node in nodes:
        visited = {start_node}
        subgraphs = dfs_subset(start_node, nodes, visited, {start_node})
        all_subgraphs.extend(subgraphs)

    # Converte para tuplas
    unique_subgraphs = []
    seen = set()
    for sg in all_subgraphs:
        node_tuple = tuple(sorted(sg.nodes()))
        if node_tuple not in seen and len(node_tuple) > 2:
            seen.add(node_tuple)
            unique_subgraphs.append(sg)
    
    return unique_subgraphs

# Exemplo de uso
def main():
    # Criar um grafo de exemplo
    G = nx.Graph()
    arestas = [(1, 2), (2, 3), (3, 4), (4, 1), (2, 4), (3, 5)]  # Grafo com ciclo e um nó extra
    G.add_edges_from(arestas)

    # Encontrar subgrafos conexos
    subgraphs = find_connected_subgraphs(G)

    # Imprimir resultados
    print(f"Total de subgrafos conexos com mais de 2 vertices: {len(subgraphs)}")
    with open('restricoes.inc', 'w') as f:
        for i, sg in enumerate(subgraphs, 1):
            f.write(f"s.t. Aciclicidade_{i}: ")
            
            for i, edge in enumerate(sg.edges()):
                f.write(f"x[{edge[0]},{edge[1]}]")
                if i != len(sg.edges) - 1:
                    f.write(" + ")
                    
            f.write(f" <= {sg.number_of_nodes()};\n")
            print(f"Subgrafo {i}:")
            print(f"Vértices: {list(sg.nodes())}")
            print(f"Arestas: {list(sg.edges())}")
            print()

main()