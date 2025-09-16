class TestBasicTake(unittest.TestCase):
    def test_returns_not_found_for_unmapped_path(self):
        request = FakeRequest(path="/missing")
        take = BasicTake()
        response = take.act(request)
        assert_that(response.status(), equal_to(404))
