import unittest

from app.wait_time.sourcing_data import POIPool
from datetime import datetime, timezone, timedelta


class TestPOIPool(unittest.TestCase):
    @classmethod
    def setUp(self):
        sample_iso_timestamp1 = (
            datetime.now(timezone.utc) - timedelta(seconds=400)
        ).isoformat()
        sample_iso_timestamp2 = (
            datetime.now(timezone.utc) - timedelta(seconds=1900)
        ).isoformat()
        self.sample_pool_dict = {
            "current_average_wait_time": 8,
            "pool": {
                "test@sample.com": {
                    "start_time": datetime.now(timezone.utc) - timedelta(seconds=300),
                    "last_seen": datetime.now(timezone.utc) - timedelta(seconds=100),
                }
            },
            "recent_wait_times": {sample_iso_timestamp1: 6, sample_iso_timestamp2: 9},
        }
        self.sample_pool = POIPool(
            "tim_hortons_musc",
            pool_data=self.sample_pool_dict["pool"],
            recent_wait_times=self.sample_pool_dict["recent_wait_times"],
            current_average_wait_time=self.sample_pool_dict[
                "current_average_wait_time"
            ],
        )

    def test_to_from_dict(self):
        self.assertEqual(
            self.sample_pool,
            POIPool.from_dict("tim_hortons_musc", self.sample_pool_dict),
        )

    def test_update_user_in_pool(self):
        self.sample_pool.update_user_in_pool("test@sample.com")
        self.assertEqual(len(self.sample_pool.pool_data), 1)
        self.sample_pool.update_user_in_pool("newuser@sample.com")
        self.assertEqual(len(self.sample_pool.pool_data), 2)

    def test_is_user_in_pool(self):
        self.assertTrue(self.sample_pool.is_user_in_pool("test@sample.com"))
        self.assertFalse(self.sample_pool.is_user_in_pool("nonexistent@sample.com"))

    def test_remove_user_from_pool(self):
        old_wait_time = self.sample_pool.current_average_wait_time
        self.sample_pool.remove_user_from_pool("test@sample.com")
        self.assertEqual(len(self.sample_pool.pool_data), 0)
        # This user has a wait time of about 300 seconds, so new average wait time should be less than before
        self.assertLess(self.sample_pool.current_average_wait_time, old_wait_time)
        # Check that outgoing wait time has been added to recent wait times
        self.assertEqual(len(self.sample_pool.recent_wait_times), 3)
        # Check that user has been removed from pool
        self.assertFalse(self.sample_pool.is_user_in_pool("test@sample.com"))

    def test_clear_stale_wait_times(self):
        self.sample_pool.clear_stale_wait_times()
        self.assertEqual(len(self.sample_pool.recent_wait_times), 1)
        self.sample_pool.clear_stale_wait_times(ttl=300)
        self.assertEqual(len(self.sample_pool.recent_wait_times), 0)

    def test_clear_stale_pool_users(self):
        self.sample_pool.clear_stale_pool_users()  # should do nothing
        self.assertTrue(self.sample_pool.is_user_in_pool("test@sample.com"))
        self.sample_pool.clear_stale_pool_users(ttl=100)
        self.assertFalse(self.sample_pool.is_user_in_pool("test@sample.com"))
