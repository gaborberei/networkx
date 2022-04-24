"""
testing 
"""
import pytest
import networkx as nx
from networkx.algorithms.centrality.laplacian import laplacian_centrality

np = pytest.importorskip("numpy")
sp = pytest.importorskip("scipy")


class TestLaplacianCentrality:
    def setup_method(self):

        self.K = nx.krackhardt_kite_graph()
        self.P3 = nx.path_graph(3)
        self.K5 = nx.complete_graph(5)

        E = nx.Graph()
        E.add_weighted_edges_from(
            [(0, 1, 4), (4, 5, 1), (0, 2, 2), (2, 1, 1), (1, 3, 2), (1, 4, 2)]
        )
        self.E = E

        self.KC = nx.karate_club_graph()

        self.FF = nx.florentine_families_graph()

        DG = nx.DiGraph()
        DG.add_edge(0, 5)
        DG.add_edge(1, 5)
        DG.add_edge(2, 5)
        DG.add_edge(3, 5)
        DG.add_edge(4, 5)
        DG.add_edge(5, 6)
        DG.add_edge(5, 7)
        DG.add_edge(5, 8)
        self.DG = DG

    def test_laplacian_centrality_E(self):
        d = laplacian_centrality(self.E)
        exact = {
            0: 0.700000,
            1: 0.900000,
            2: 0.280000,
            3: 0.220000,
            4: 0.260000,
            5: 0.040000,
        }

        for n, dc in d.items():
            assert exact[n] == pytest.approx(dc, abs=1e-7)

    def test_laplacian_centrality_KC(self):

        d = laplacian_centrality(self.KC)
        exact = {
            0: 0.2543593,
            1: 0.1724524,
            2: 0.2166053,
            3: 0.0964646,
            4: 0.0350344,
            5: 0.0571109,
            6: 0.0540713,
            7: 0.0788674,
            8: 0.1222204,
            9: 0.0217565,
            10: 0.0308751,
            11: 0.0215965,
            12: 0.0174372,
            13: 0.118861,
            14: 0.0366341,
            15: 0.0548712,
            16: 0.0172772,
            17: 0.0191969,
            18: 0.0225564,
            19: 0.0331147,
            20: 0.0279955,
            21: 0.0246361,
            22: 0.0382339,
            23: 0.1294193,
            24: 0.0227164,
            25: 0.0644697,
            26: 0.0281555,
            27: 0.075188,
            28: 0.0364742,
            29: 0.0707087,
            30: 0.0708687,
            31: 0.131019,
            32: 0.2370821,
            33: 0.3066709,
        }
        for n, dc in d.items():
            assert exact[n] == pytest.approx(dc, abs=1e-7)

    def test_laplacian_centrality_K(self):

        d = laplacian_centrality(self.K)
        exact = {
            0: 0.3010753,
            1: 0.3010753,
            2: 0.2258065,
            3: 0.483871,
            4: 0.2258065,
            5: 0.3870968,
            6: 0.3870968,
            7: 0.1935484,
            8: 0.0752688,
            9: 0.0322581,
        }
        for n, dc in d.items():
            assert exact[n] == pytest.approx(dc, abs=1e-7)

    def test_laplacian_centrality_P3(self):
        d = laplacian_centrality(self.P3)
        exact = {0: 0.6, 1: 1.0, 2: 0.6}
        for n, dc in d.items():
            assert exact[n] == pytest.approx(dc, abs=1e-7)

    def test_laplacian_centrality_K5(self):
        d = laplacian_centrality(self.K5)
        exact = {0: 0.52, 1: 0.52, 2: 0.52, 3: 0.52, 4: 0.52}
        for n, dc in d.items():
            assert exact[n] == pytest.approx(dc, abs=1e-7)

    def test_laplacian_centrality_FF(self):
        d = laplacian_centrality(self.FF)
        exact = {
            "Acciaiuoli": 0.0804598,
            "Medici": 0.4022989,
            "Castellani": 0.1724138,
            "Peruzzi": 0.183908,
            "Strozzi": 0.2528736,
            "Barbadori": 0.137931,
            "Ridolfi": 0.2183908,
            "Tornabuoni": 0.2183908,
            "Albizzi": 0.1954023,
            "Salviati": 0.1149425,
            "Pazzi": 0.0344828,
            "Bischeri": 0.1954023,
            "Guadagni": 0.2298851,
            "Ginori": 0.045977,
            "Lamberteschi": 0.0574713,
        }
        for n, dc in d.items():
            assert exact[n] == pytest.approx(dc, abs=1e-7)

    def test_laplacian_centrality_DG(self):
        d = laplacian_centrality(self.DG)
        exact = {
            0: 0.2123352,
            5: 0.515391,
            1: 0.2123352,
            2: 0.2123352,
            3: 0.2123352,
            4: 0.2123352,
            6: 0.2952031,
            7: 0.2952031,
            8: 0.2952031,
        }
        for n, dc in d.items():
            assert exact[n] == pytest.approx(dc, abs=1e-7)
