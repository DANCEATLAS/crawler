"""Offline checks for the lesson search of 24 November 2026 (crawler.py, rule 2): a video whose own title names the dance
and a lesson is a candidate even when few people watched it, and the dances that found nothing under the older rule are
looked for once more, a bounded number a day, those nearest the starting line first."""
import io
import json
import os
import sys
import unittest
import urllib.error
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import crawler  # noqa: E402  (the crawler lives at the repository's root)

from .common import jload  # noqa: E402
from .test_foundation import TemporaryProject  # noqa: E402


def video(vid, title, seconds=300, views=40, likes=1, comments=0, description="", category="26", embeddable=True, channel="A teacher"):
    return {"id": vid, "snippet": {"title": title, "description": description, "channelTitle": channel, "categoryId": category},
            "statistics": {"viewCount": str(views), "likeCount": str(likes), "commentCount": str(comments)},
            "contentDetails": {"duration": f"PT{seconds // 60}M{seconds % 60}S", "definition": "hd"}, "status": {"embeddable": embeddable}}


class LessonRuleTests(unittest.TestCase):
    DANCE = {"slug": "odzemek", "name": "Odzemek", "country": "Slovakia", "aliases": ["Odzemok"]}

    def find(self, items, said=None):
        with patch.object(crawler, "search_ids", return_value=[i["id"] for i in items]), patch.object(crawler, "_ytdlp_search", return_value=[]), \
                patch.object(crawler, "videos", return_value=items), patch.object(crawler, "comments", side_effect=lambda vid, keys, n=100: (said or {}).get(vid, [])):
            return crawler.lesson_eval(self.DANCE, None)

    def test_a_lesson_named_in_its_title_is_a_candidate_though_few_watched_and_nobody_commented(self):
        out = self.find([video("a", "Odzemek dance tutorial - basic steps")])
        self.assertEqual([(l["youtube_id"], l["lesson_status"], l["ratio"]) for l in out], [("a", "candidate", 0.25)])

    def test_comments_are_not_asked_for_when_the_video_has_none(self):
        asked = []
        items = [video("a", "Odzemek dance tutorial - basic steps"), video("b", "Odzemek dance tutorial for beginners", comments=7)]
        with patch.object(crawler, "search_ids", return_value=["a", "b"]), patch.object(crawler, "_ytdlp_search", return_value=[]), \
                patch.object(crawler, "videos", return_value=items), patch.object(crawler, "comments", side_effect=lambda vid, keys, n=100: asked.append(vid) or []):
            out = crawler.lesson_eval(self.DANCE, None)
        self.assertEqual(asked, ["b"])                                                     # "a" has no comments, or has them turned off
        self.assertEqual(sorted(l["youtube_id"] for l in out), ["a", "b"])                 # and is a candidate all the same

    def test_the_title_has_to_name_both_the_dance_and_a_lesson(self):
        self.assertEqual(self.find([video("a", "Folk dance tutorial", description="We learn the Odzemek today")]), [])      # the dance only in the description
        self.assertEqual(self.find([video("b", "Odzemek at the festival in Detva")]), [])                                    # no lesson in the title
        self.assertEqual(len(self.find([video("c", "Odzemok - how to dance, step by step")])), 1)                             # another name of the dance counts

    def test_music_films_clips_that_cannot_be_embedded_and_snippets_stay_out(self):
        for item in (video("a", "Odzemek tutorial", category="10"), video("b", "Odzemek tutorial (official video)"), video("c", "Odzemek tutorial - movie scene"),
                     video("d", "Odzemek tutorial", embeddable=False), video("e", "Odzemek tutorial", seconds=45), video("f", "Odzemek tutorial", seconds=2 * 3600),
                     video("g", "Odzemek tutorial", views=50000, likes=10)):                                               # widely watched and hardly liked
            self.assertEqual(self.find([item]), [], item["snippet"]["title"])

    def test_a_praised_lesson_comes_first_and_at_most_two_candidates_follow(self):
        praise = ["Finally clicked, thank you so much!", "Best teacher, so clear and easy to follow"]
        items = [video("small1", "Odzemek tutorial part 1"), video("small2", "Odzemek tutorial part 2"), video("small3", "Odzemek tutorial part 3"),
                 video("loved", "Learn the Odzemek", views=9000, likes=400, comments=30)]
        out = self.find(items, {"loved": praise})
        self.assertEqual([(l["youtube_id"], l["lesson_status"]) for l in out], [("loved", "in_review"), ("small1", "candidate"), ("small2", "candidate")])
        self.assertTrue(out[0]["ratio"] > out[1]["ratio"])

    def test_viewers_who_say_it_is_wrong_keep_a_small_candidate_out(self):
        self.assertEqual(self.find([video("a", "Odzemek tutorial", comments=3)], {"a": ["this is wrong", "confusing and too fast"]}), [])


class VideoServiceTests(unittest.TestCase):
    """The crawl of 24 November 2026: a video with its comments turned off answers 403; read as a spent key, it retired every
    key in turn on that one video, the lesson search ended after two dances and the viral search found nothing."""

    @staticmethod
    def refused(reason, code=403):
        body = json.dumps({"error": {"code": code, "errors": [{"reason": reason}]}}).encode() if reason is not None else b"not json"
        return urllib.error.HTTPError("https://video.invalid/", code, "refused", None, io.BytesIO(body))

    def service(self, answers):
        """answers: key -> a reason for refusing, or a dict to answer with."""
        asked = []
        def urlopen(url, timeout=30):
            key = url.split("key=")[1].split("&")[0]; asked.append(key); a = answers[key]
            if isinstance(a, dict): return io.BytesIO(json.dumps(a).encode())
            raise self.refused(a)
        return patch.object(crawler.urllib.request, "urlopen", side_effect=urlopen), asked

    def test_comments_turned_off_is_an_answer_about_the_video_and_no_key_is_retired(self):
        for reason in ("commentsDisabled", "forbidden", None):                             # None: a refusal that cannot be read
            keys = crawler.Keys(["k1", "k2"]); net, asked = self.service({"k1": reason, "k2": reason})
            with net:
                with self.assertRaises(LookupError):
                    crawler.api("commentThreads", {"videoId": "x"}, keys)
                self.assertEqual(crawler.comments("x", keys), [])
            self.assertEqual((asked, keys.dead, keys.cur()), (["k1", "k1"], set(), "k1"), reason)

    def test_a_spent_key_is_retired_and_the_next_one_is_asked(self):
        keys = crawler.Keys(["k1", "k2"]); net, asked = self.service({"k1": "quotaExceeded", "k2": {"items": [{"id": "v"}]}})
        with net:
            self.assertEqual(crawler.videos(["v"], keys), [{"id": "v"}])
            self.assertEqual(crawler.api("commentThreads", {"videoId": "v"}, keys), {"items": [{"id": "v"}]})
        self.assertEqual((asked, keys.dead, keys.cur()), (["k1", "k2", "k2"], {0}, "k2"))

    def test_when_every_key_is_spent_the_run_is_told_so(self):
        keys = crawler.Keys(["k1", "k2"]); net, asked = self.service({"k1": "quotaExceeded", "k2": "dailyLimitExceeded"})
        with net, self.assertRaises(RuntimeError):
            crawler.videos(["v"], keys)
        self.assertEqual((asked, keys.cur()), (["k1", "k2"], None))
        keys = crawler.Keys(["k1"]); net, asked = self.service({"k1": "quotaExceeded"})   # a spent key is a spent key on the comments question too
        with net, self.assertRaises(RuntimeError):
            crawler.api("commentThreads", {"videoId": "x"}, keys)


class LookedForAgainTests(TemporaryProject):
    def crawl(self, dances, cache, results, env=None, found=None, line=None):
        self.save("dance_list.json", [dict({"publish": True, "wikipedia": "https://en.wikipedia.org/wiki/X"}, slug=s, name=s) for s in dances])
        self.save("tutorial_cache.json", cache)
        self.save("tutorial_results.json", results)
        if line:
            self.save("pipeline_state/active_ready.json", {"profiles": line})
        tried = []

        def lesson_eval(d, keys):
            tried.append(d["slug"])
            answer = (found or {}).get(d["slug"], [])
            if isinstance(answer, Exception):
                raise answer
            return answer
        with patch.object(crawler, "YT_KEYS", ["k"]), patch.object(crawler, "MODE", "tutorial"), patch.object(crawler, "lesson_eval", side_effect=lesson_eval), \
                patch.dict("os.environ", env or {}), patch("builtins.print"):
            crawler.main()
        return tried, jload("tutorial_cache.json"), jload("tutorial_results.json")

    def test_a_dance_that_found_nothing_under_the_older_rule_is_looked_for_once_more(self):
        today = crawler.time.strftime("%Y-%m-%d")
        lesson = [{"youtube_id": "v", "lesson_status": "candidate"}]
        tried, cache, results = self.crawl(["has", "empty-old", "empty-new", "never"],
                                           {"has": {"n": 1}, "empty-old": {"n": 0, "at": today}, "empty-new": {"n": 0, "at": today, "v": crawler.TUT_RULE}},
                                           {"has": {"lessons": lesson, "status": "in_review"}}, found={"empty-old": lesson})
        self.assertEqual(tried, ["never", "empty-old"])                                   # never tried first; not the one that has a lesson, not the one this rule already tried
        self.assertEqual((cache["empty-old"]["n"], cache["empty-old"]["v"], cache["never"]["v"]), (1, crawler.TUT_RULE, crawler.TUT_RULE))
        self.assertEqual(sorted(results), ["empty-old", "has"])

    def test_a_bounded_number_a_day_and_the_dances_nearest_the_line_first(self):
        old = {s: {"n": 0, "at": "2026-11-20"} for s in ("far", "near", "nearest", "unknown")}
        line = {"far": {"state": "building", "missing": ["footwork_counts", "mistakes", "posture", "arms"]}, "near": {"state": "building", "missing": ["footwork_counts", "mistakes"]},
                "nearest": {"state": "building", "missing": ["footwork_counts"]}}
        tried, cache, _ = self.crawl(["far", "near", "nearest", "unknown"], old, {}, env={"TUT_WAVE": "2"}, line=line)
        self.assertEqual(tried, ["nearest", "near"])
        self.assertEqual([cache[s].get("v") for s in ("nearest", "near", "far", "unknown")], [crawler.TUT_RULE, crawler.TUT_RULE, None, None])

    def test_a_search_that_broke_is_not_written_down_as_no_lesson(self):
        tried, cache, _ = self.crawl(["a", "b"], {}, {}, found={"a": ValueError("the video service answered with an error")})
        self.assertEqual((tried, sorted(cache)), (["a", "b"], ["b"]))                     # "a" is looked for again tomorrow

    def test_searches_that_gave_no_video_at_all_are_not_no_lesson_and_five_in_a_row_stop_the_day(self):
        with patch.object(crawler, "search_ids", return_value=[]), patch.object(crawler, "_ytdlp_search", return_value=[]), patch.object(crawler, "videos", return_value=[]):
            with self.assertRaises(LookupError):                                          # blocked, timed out or over the day's cap: nothing was looked at
                crawler.lesson_eval({"slug": "x", "name": "Xdance"}, ["k"])
        silent = LookupError("no search gave any video")
        names = ["d%d" % i for i in range(8)]
        tried, cache, _ = self.crawl(names, {}, {}, found={n: silent for n in names})
        self.assertEqual((len(tried), cache), (5, {}))                                    # the day stops after five; nothing is written down, all are looked for again
        tried, cache, _ = self.crawl(names, {}, {}, found={n: silent for n in names[:4]})
        self.assertEqual((len(tried), sorted(cache)), (8, names[4:]))                     # four broke, then the search answered: the day goes on

    def test_the_crawl_writes_down_what_it_did_and_every_part_that_ended_early(self):
        lesson = [{"youtube_id": "v", "lesson_status": "candidate"}]
        self.crawl(["a", "b", "c"], {"c": {"n": 0, "at": "2026-01-01"}}, {}, found={"a": lesson})
        report = jload("pipeline_state/crawl_report.json")
        self.assertEqual((report["lessons"], report["stops"], report["mode"]), ({"due": 3, "looked_at": 3, "found": 1, "second_looks": 1}, [], "tutorial"))
        self.assertRegex(report["at"], r"^20\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ$")
        self.crawl(["a", "b", "c"], {}, {}, found={"b": RuntimeError("all keys exhausted (quota)")})
        report = jload("pipeline_state/crawl_report.json")                                 # the crawl of 24 November 2026, as it would have been written
        self.assertEqual((report["lessons"]["looked_at"], report["stops"]), (1, ["tut stop: all keys exhausted (quota)"]))


if __name__ == "__main__":
    unittest.main()
