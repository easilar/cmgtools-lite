import unittest
from tau import Tau

class TestTau(unittest.TestCase):

    def test_1(self):
        tau = Tau()
        self.assertEqual(tau.pt(), 0)
        tau.foo()
        tau.bar()
        self.assertSetEqual(Tau.not_implemented,
                            set(['pt','foo','bar']))

if __name__ == '__main__':
    unittest.main()
