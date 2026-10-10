import unittest,random
from controller import allocate,DEFAULT_LOADS,metrics
class Tests(unittest.TestCase):
    def test_slide(self):
        rows=allocate(DEFAULT_LOADS,70)
        self.assertEqual([r['allocated_kw'] for r in rows],[25,20,25,0,0])
    def test_zero_and_full(self):
        self.assertEqual(metrics(allocate(DEFAULT_LOADS,0),0)['served_kw'],0)
        self.assertEqual(metrics(allocate(DEFAULT_LOADS,150),150)['served_kw'],100)
    def test_budget_and_switching(self):
        rng=random.Random(10)
        for _ in range(1000):
            power=rng.uniform(0,160)
            rows=allocate(DEFAULT_LOADS,power)
            self.assertLessEqual(sum(r['allocated_kw'] for r in rows),power+1e-9)
            for r in rows:
                self.assertTrue(0<=r['allocated_kw']<=r['demand_kw'])
                if not r['controllable']:self.assertIn(r['allocated_kw'],[0,r['demand_kw']])
    def test_invalid(self):
        for p in [-1,float('nan'),float('inf')]:
            with self.assertRaises(ValueError):allocate(DEFAULT_LOADS,p)
        with self.assertRaises(ValueError):allocate(DEFAULT_LOADS,70,(0,0,0))
if __name__=='__main__':unittest.main()
