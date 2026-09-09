# Adaptive Algorithms

## Mastery (0–100)

**Inputs**: current Mastery, AnswerAttempt, consecutive_mistakes  
**Output**: updated Mastery (clamped)

Correct answer:
```
multiplier = {easy: 0.7, medium: 1.0, hard: 1.3}
diminishing = max(0.2, 1 - (score/100) * easy_penalty)
gain = base_gain * multiplier * diminishing
score += gain
```

Incorrect answer:
```
loss = base_loss * (1 + min(0.5, consecutive_mistakes * 0.1))
score -= loss
```

Defaults (configurable): base_gain=8, base_loss=5, easy_penalty=0.6

## Adaptive Difficulty

Mastery bands (configurable):
- < 40 % → Easy
- 40–75 % → Medium
- ≥ 75 % → Hard

Recent performance adjustment (last ≤ 5 attempts on the topic):
- ≥ 80 % correct → step difficulty up one level
- ≤ 30 % correct → step difficulty down one level

## Knowledge Diagnosis

A topic is considered weak when:
- mastery < threshold (default 50 %), or
- consecutive mistakes ≥ 2 even if mastery is higher

Priority = 0.7 * (100 − mastery)/100 + 0.3 * min(consecutive/5, 1)

## Recommendation

1. Rank weak topics by priority
2. Attach suggested difficulty from DifficultySelector
3. If no weak topics, pick the next curriculum topic still below goal mastery

## Learning Path

1. Collect all topics with mastery < goal (default 70 %)
2. Topological sort respecting prerequisites among those candidates
3. Prefer weak topics when multiple nodes have in-degree 0
4. Return ordered list (truncated)

## Question Selection

1. Determine target difficulty
2. Prefer questions of that difficulty not seen in the last 15 attempts
3. Fall back to any difficulty, still excluding recent
4. Last resort: allow repeats

## Mistake Analysis

- Increment total_mistakes and consecutive_mistakes on incorrect
- Reset consecutive on correct; set is_improving = True when a streak is broken
- Designed for future concept-tag level analysis
