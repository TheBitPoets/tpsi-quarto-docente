"""Check the teaching timeline and published GIF references without Pillow."""
import base64
import re
import html
import importlib.util
import json
from pathlib import Path
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("animations", ROOT / "scripts/build_course_animations.py")
animations = importlib.util.module_from_spec(spec)
spec.loader.exec_module(animations)


class AnimationTests(unittest.TestCase):
    def test_single_thread_defers_gui_and_clicks_until_io_finishes(self):
        waiting = animations.sequential_state(8)
        self.assertEqual(waiting["phase"], "send")
        self.assertEqual(waiting["latest"], 19)
        self.assertEqual(waiting["handled"], 0)
        self.assertEqual(waiting["pending"], 4)
        resumed = animations.sequential_state(9)
        self.assertEqual(resumed["latest"], 20)
        self.assertEqual(resumed["sampled"], 4)
        self.assertEqual(resumed["pending"], 0)
        self.assertEqual(resumed["handled"], 5)

    def test_gui_stays_live_with_full_queue_and_stalled_sensor(self):
        full = animations.concurrent_state(8)
        self.assertEqual(full["queue"], [21, 22, 23, 24])
        self.assertEqual(full["sending"], 20)
        self.assertEqual(full["latest"], 24)
        paused = animations.concurrent_state(13)
        self.assertTrue(paused["sensor_wait"])
        self.assertEqual(paused["latest"], 24)
        self.assertEqual(paused["sampled"], 8)
        self.assertGreater(paused["clicks"], full["clicks"])
        self.assertLess(len(paused["queue"]), len(full["queue"]))
        self.assertEqual(animations.concurrent_state(16)["latest"], 25)

    def test_fifo_never_duplicates_loses_or_overflows_measurements(self):
        for frame in range(animations.DURATION["concorrente"] * animations.FPS):
            t = frame / animations.FPS
            state = animations.concurrent_state(t)
            acquired = [v for when, v in animations.ARRIVALS if when <= t]
            outstanding = ([state["sending"]] if state["sending"] is not None else []) + state["queue"]
            self.assertEqual(state["delivered"] + outstanding, acquired)
            self.assertLessEqual(len(state["queue"]), 4)

    def test_offline_player_embeds_current_gifs_and_matches_template(self):
        page = (ROOT / "assets/tpsi4/01-io-animazioni.html").read_text(encoding="utf-8")
        match = re.search(r'<script type="application/json" id="animation-data">(.*?)</script>', page)
        self.assertIsNotNone(match)
        data = json.loads(match[1])
        self.assertEqual(set(data), set(animations.DURATION))
        for mode, duration in animations.DURATION.items():
            self.assertEqual(base64.b64decode(data[mode]["gif"]),
                             (ROOT / f"assets/tpsi4/01-io-{mode}-animazione.gif").read_bytes())
            poster = base64.b64decode(data[mode]["poster"].split(",", 1)[1])
            self.assertEqual(poster[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(struct.unpack(">II", poster[16:24]), animations.SIZE)
            self.assertEqual(data[mode]["duration"], duration)
        template = (ROOT / "assets/tpsi4/visual-system/io-player.template.html").read_text(encoding="utf-8")
        self.assertEqual(page, template.replace("{{ANIMATION_DATA}}", match[1]))

    def test_registered_gifs_are_linked_in_the_correct_subsections(self):
        items = json.loads((ROOT / "assets/tpsi4/visual-system/figure-index.json").read_text(encoding="utf-8"))["animations"]
        self.assertEqual(len(items), 2)
        for item in items:
            with self.subTest(animation=item["id"]):
                data = (ROOT / item["output"]).read_bytes()
                self.assertEqual(data[:6], b"GIF89a")
                self.assertEqual(struct.unpack("<HH", data[6:10]), (item["width"], item["height"]))
                self.assertIn(b"NETSCAPE2.0", data)
                self.assertEqual(data[-1:], b";")
                text = (ROOT / item["lesson"]).read_text(encoding="utf-8")
                section = text.split("### " + item["section"] + "\n", 1)[1].split("\n### ", 1)[0]
                self.assertIn("<!-- figure:" + item["id"] + " -->", section)
                self.assertIn('src="../../' + item["output"] + '"', section)
                self.assertIn('alt="' + html.escape(item["alt"], quote=True) + '"', section)
                self.assertIn(html.escape(item["caption"]), section)
                self.assertTrue((ROOT / item["generator"]).is_file())


if __name__ == "__main__":
    unittest.main()
