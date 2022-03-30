"""Laplacian centrality measures."""

import networkx as nx

__all__ = ["laplacian_centrality"]

# @not_implemented_for("multigraph")


def laplacian_centrality(
    G, normalized=True, nbunch=None, directed_laplacian_matrix_args=None
):
    r"""Compute the Laplacian centrality for nodes in the graph `G`.

    The Laplacian Centrality of a node `i` is measured by the drop in the Laplacian Energy
    after deleting node `i` from the graph.

    Where the Laplacian Energy is the sum of the squared eigenvalues of graph `G`'s Laplacian matrix.

    .. math::

        C_L(u_i,G) = \frac{(\Delta E)_i}{E_L (G)} = \frac{E_L (G)-E_L (G_i)}{E_L (G)}

        E_L (G) = \sum_{i=0}^n \lambda_i^2

    Where $E_L (G)$ is the Laplacian energy of graph `G`,
    E_L (G_i) is the Laplacian energy of graph `G` after deleting node `i`
    and $\lambda_i$ are the eigenvalues of `G`'s Laplacian matrix.

    Parameters
    ----------

    G : graph
        A networkx graph

    normalized : bool (default = True)
        If True the centrality score is scaled so the sum over all nodes is 1. 
        If False the centrality score for each node is the drop in Laplacian 
        energy when that node is removed.

    nbunch : list (default = None)
        An nbunch is a single node, container of nodes or None (representing all nodes)

    directed_laplacian_matrix_args : dictionary (default = None)
        Parameters of the nx.directed_laplacian_matrix function.


    Returns
    -------
    nodes : dictionary
       Dictionary of nodes with Laplacian centrality as the value.

    Examples
    --------
    >>> nxg = nx.Graph()
    >>> nxg.add_weighted_edges_from([(0,1,4),(0,2,2),(2,1,1),(1,3,2),(1,4,2),(4,5,1)])
    >>> sorted((v, f"{c:0.2f}") for v, c in laplacian_centrality(nxg).items())
    [(0, '0.70'), (1, '0.90'), (2, '0.28'), (3, '0.22'), (4, '0.26'), (5, '0.04')]

    Notes
    -----
    The algorithm is implemented based on [1] with an extension to directed graphs using nx.directed_laplacian_matrix function.

    Raises
    ------
    NetworkXPointlessConcept
        If the graph `G` is the null graph.

    References
    ----------
    .. [1] Qi, X., Fuller, E., Wu, Q., Wu, Y., and Zhang, C.-Q. (2012).
    Laplacian centrality: A new centrality measure for weighted networks.
    Information Sciences, 194:240-253.
    https://math.wvu.edu/~cqzhang/Publication-files/my-paper/INS-2012-Laplacian-W.pdf

    """
    import numpy as np
    import scipy as sp
    import scipy.linalg  # call as sp.linalg
    import scipy.sparse  # call as sp.sparse

    if len(G) == 0:
        raise nx.NetworkXPointlessConcept(
            "cannot compute centrality for the null graph"
        )

    if G.is_directed():
        lap_matrix = sp.sparse.csr_matrix(
            nx.directed_laplacian_matrix(G, **directed_laplacian_matrix_args)
        )
    else:
        lap_matrix = nx.laplacian_matrix(G)

    if normalized:
        sum_of_full = np.power(
            sp.linalg.eigh(lap_matrix.toarray(), eigvals_only=True), 2
        ).sum()
    else:
        sum_of_full = 1

    laplace_centralities_dict = {}
    for i, node in enumerate(G.nbunch_iter(nbunch)):

        new_diag = lap_matrix.diagonal() - abs(lap_matrix.getcol(i).toarray().flatten())

        # remove row and col i from lap_matrix
        all_but_i = list(np.arange(lap_matrix.shape[0]))
        all_but_i.remove(i)
        A_2 = lap_matrix[all_but_i, :]
        A_2 = A_2[:, all_but_i]

        A_2.setdiag(np.r_[new_diag[:i], new_diag[i + 1 :]])

        sum_of_eigen_values_2 = np.power(
            sp.linalg.eigh(A_2.toarray(), eigvals_only=True), 2
        ).sum()

        if normalized:
            l_cent = 1 - (sum_of_eigen_values_2 / sum_of_full)
        else:
            l_cent = sum_of_eigen_values_2

        laplace_centralities_dict[node] = l_cent

    return laplace_centralities_dict
