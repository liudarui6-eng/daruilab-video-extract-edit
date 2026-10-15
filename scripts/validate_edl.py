#!/usr/bin/env python3
"""Validate a single-source, normal-speed hard-cut EDL without modifying files."""
import argparse
import json
import math
import sys


def number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(label + " must be a finite number")
    return float(value)


def validate(data):
    if not isinstance(data, dict):
        raise ValueError("EDL must be an object")
    duration = number(data.get("source_duration"), "source_duration")
    if duration <= 0:
        raise ValueError("source_duration must be positive")
    allowed = data.get("allowed_source_range", [0, duration])
    if not isinstance(allowed, list) or len(allowed) != 2:
        raise ValueError("allowed_source_range must contain two numbers")
    low, high = [number(x, "allowed_source_range") for x in allowed]
    if not 0 <= low < high <= duration:
        raise ValueError("allowed_source_range is outside source duration")
    clips = data.get("clips")
    if not isinstance(clips, list) or not clips:
        raise ValueError("clips must be a nonempty list")
    result, ids = [], set()
    for clip in clips:
        if not isinstance(clip, dict):
            raise ValueError("each clip must be an object")
        cid = clip.get("id")
        if not isinstance(cid, str) or not cid.strip() or cid in ids:
            raise ValueError("clip id must be a unique nonempty string")
        ids.add(cid)
        target = number(clip.get("target_seconds"), cid + " target_seconds")
        tolerance = number(clip.get("tolerance_seconds", 0), cid + " tolerance_seconds")
        if target <= 0 or tolerance < 0:
            raise ValueError(cid + " invalid target or tolerance")
        segments = clip.get("segments")
        if not isinstance(segments, list) or not segments:
            raise ValueError(cid + " requires segments")
        cursor, mapping = 0.0, []
        for segment in segments:
            if not isinstance(segment, dict) or set(segment) != {"start", "end"}:
                raise ValueError(cid + " segments support only start/end (no speed or transitions)")
            start = number(segment["start"], cid + " start")
            end = number(segment["end"], cid + " end")
            if not low <= start < end <= high:
                raise ValueError(cid + " source interval is invalid or outside allowed range")
            output_end = cursor + end - start
            mapping.append({"source": [start, end], "output": [cursor, output_end]})
            cursor = output_end
        if abs(cursor - target) > tolerance + 1e-6:
            raise ValueError(cid + " duration %.3f outside target %.3f ± %.3f" % (cursor, target, tolerance))
        result.append({"id": cid, "duration": cursor, "mapping": mapping})
    return {"valid": True, "clip_count": len(result), "clips": result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("edl", help="Path to EDL JSON")
    args = parser.parse_args()
    try:
        with open(args.edl, encoding="utf-8") as stream:
            result = validate(json.load(stream))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
