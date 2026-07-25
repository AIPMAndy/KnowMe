import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import analyze  # noqa: E402
import collect  # noqa: E402


class FeishuCollectionTests(unittest.TestCase):
    def test_parse_lark_cli_payload_preserves_speakers(self):
        payload = {
            "ok": True,
            "data": {
                "messages": [
                    {
                        "message_id": "om_1",
                        "msg_type": "text",
                        "create_time": "2026-07-25T10:00:00+08:00",
                        "sender": {"id": "ou_manager", "name": "林总"},
                        "content": "先给我数据和结论，再讨论方案。",
                    },
                    {
                        "message_id": "om_2",
                        "msg_type": "text",
                        "sender": {"id": "ou_andy", "name": "Andy"},
                        "content": "收到。",
                    },
                ],
                "has_more": False,
            },
        }

        messages, has_more, page_token = collect.parse_feishu_payload(payload)

        self.assertEqual([message["speaker"] for message in messages], ["林总", "Andy"])
        self.assertEqual(messages[0]["speaker_id"], "ou_manager")
        self.assertFalse(has_more)
        self.assertIsNone(page_token)

    def test_parse_copied_feishu_text(self):
        messages = collect.parse_feishu_text(
            "林总 10:30\n先看数据。\n再给两个方案。\nAndy: 好的，我下午发。"
        )

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["speaker"], "林总")
        self.assertIn("再给两个方案", messages[0]["content"])
        self.assertEqual(messages[1]["speaker"], "Andy")

    def test_mark_subject_does_not_mix_participants(self):
        messages = [
            {"role": "participant", "speaker": "林总", "content": "数据优先"},
            {"role": "participant", "speaker": "Andy", "content": "收到"},
        ]

        count = collect.mark_subject(messages, "林总")

        self.assertEqual(count, 1)
        self.assertEqual(messages[0]["role"], "subject")
        self.assertEqual(messages[1]["role"], "participant")


class PipelineTests(unittest.TestCase):
    def test_self_analysis_and_advice_remain_compatible(self):
        messages = []
        for index in range(24):
            messages.append({
                "role": "subject",
                "speaker": "self",
                "content": f"第{index + 1}项先看数据和逻辑，因为我想按计划确定下一步。",
                "source": "text",
            })
        data = {
            "source": "text",
            "analysis": {"mode": "self", "target": "self"},
            "messages": messages,
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            data_path = temp_path / "data.json"
            report_path = temp_path / "report.md"
            advice_path = temp_path / "advice.md"
            data_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

            analyze_result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "analyze.py"),
                    "--input", str(data_path),
                    "--output", str(report_path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(analyze_result.returncode, 0, analyze_result.stderr)

            advise_result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "advise.py"),
                    "--report", str(report_path),
                    "--output", str(advice_path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(advise_result.returncode, 0, advise_result.stderr)
            self.assertIn("Your MBTI Type", report_path.read_text(encoding="utf-8"))
            self.assertIn("based on 24 messages", advice_path.read_text(encoding="utf-8"))

    def test_other_person_pipeline_generates_targeted_report(self):
        manager_lines = []
        for index in range(24):
            manager_lines.append(
                f"林总: 第{index + 1}项先看具体数据和证据，因为要按计划确定下一步，再给两个方案。"
            )
            manager_lines.append(f"Andy: 收到第{index + 1}项，我整理后回复。")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            chat_path = temp_path / "feishu.txt"
            data_path = temp_path / "data.json"
            report_path = temp_path / "report.md"
            chat_path.write_text("\n".join(manager_lines), encoding="utf-8")

            collect_result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "collect.py"),
                    "--source", "feishu",
                    "--file", str(chat_path),
                    "--mode", "other",
                    "--target", "林总",
                    "--self-name", "Andy",
                    "--relationship", "boss",
                    "--output", str(data_path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(collect_result.returncode, 0, collect_result.stderr)

            data = json.loads(data_path.read_text(encoding="utf-8"))
            self.assertEqual(data["subject_messages"], 24)
            self.assertEqual(
                {message["speaker"] for message in data["messages"] if message["role"] == "subject"},
                {"林总"},
            )

            analyze_result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "analyze.py"),
                    "--input", str(data_path),
                    "--output", str(report_path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(analyze_result.returncode, 0, analyze_result.stderr)

            report = report_path.read_text(encoding="utf-8")
            self.assertIn("Analyzed subject: **林总**", report)
            self.assertIn("Analysis mode: **other**", report)
            self.assertIn("Relationship context: **boss**", report)
            self.assertIn("How to Communicate With This Person", report)
            self.assertIn("24 messages from the subject", report)
            self.assertNotIn("Analyzed subject: **Andy**", report)

    def test_small_sample_is_low_confidence(self):
        detector = analyze.SignalDetector()
        for _ in range(5):
            detector.analyze_message("具体数据和计划已经确定。")

        results = detector.get_results()

        self.assertEqual(results["overall_confidence"], "low")


if __name__ == "__main__":
    unittest.main()
