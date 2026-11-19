# Positive and negative examples

These examples come from real decks and the feedback after presenting them. Use them as references when deciding whether to split a concept and how to present it. Learn the reason each one worked or failed; do not copy its look (a grey code box, a particular callout text) onto slides where that reason does not apply.

## Positive: needs step-by-step guidance, so splitting is far better than one slide

The opening has to make the audience understand why a robot needs a video demonstration.

1. Show only a familiar language-model one-shot prompt: a grey monospace box with two Q&A pairs. The first pair is the example; the answer to the second pair (the model's output) is in green, with a small grey caption "green = model output" below. The rest of the slide is empty, so the audience first understands something familiar.
2. Add a red callout below the prompt box: "Can we do this for robot manipulation in the physical world?" A red curved arrow sweeps from the lower-left of the prompt box to the callout. Pose the question and let the audience think first.
3. Replace the callout: put a red frame around the first Q&A pair (the two lines that are the example), and a light grey-blue solid arrow points down from the frame to a callout below: "This is the example! So the physical world needs some kind of example too." This names the principle: the model learns the task from the example in its context.
4. On the right half, add the subheading "Embodied model: one-shot physical prompt" and the paper's demonstration video (a person demonstrates pouring bolts with handheld grippers). Remove the frame and the arrow; the callout becomes the conclusion: "In the physical world, the example is a video demonstration." The physical demonstration is introduced as the robot counterpart of In-Context Learning.

These four steps form one path of thought: familiar example → question → principle → new mechanism. Shown all at once, the audience sees the answer and skips the thinking; split, every step has something to think about and to say (each step over 20 seconds).

## Positive: a relationship understood at a glance, so do not split

One slide on "compositional generalization" whose point is "A + B = the ability to do A and then continue with B". On the left, a video of demonstration A (unzipping a pencil pouch); a "+"; a video of demonstration B (taking money out of the pouch); a "⇒"; on the far right, a video of the model chaining A and B into one continuous behaviour. Each video has a one-line grey caption, and one line of key message runs below: "two independent demos become one continuous behaviour". The three videos sit side by side and play at the same time, so the audience sees at once that "the two on the left = the one on the right".

The concept needs no detailed explanation; the point is the relationship itself. Showing only A, or A + B, leaves nothing to say (one sentence per step), and splitting breaks the equation. **When the layout itself is the explanation, use one slide.**

## Negative: a parallel list split too far

A slide "validated on 8 real platforms and 5 robot bodies" was split into 8 slides, each showing one robot or one condition with a single sentence of script (5–15 seconds). The audience did not need to see the platforms in sequence, and the constant page-turning lost them. Fix: one slide of about 1–1.5 minutes with all five robot photos in a row and the test conditions below.

## Negative → positive: a poll whose answer the talk already gives

A talk titled "RoboTTT: Context Scaling for Robot Policies" opened with a pre-test / post-test opinion poll: "Can one-shot learning extend to long-horizon, high-precision work?" (already ... soon ... many years ... never), and later asked "As pre-training context grows from 128 to 8K steps, real-robot performance will: keep rising / saturate / rise then fall / not change". The first repeated the event description; the second was answered by the talk's title. Neither reveal taught anything.

Replaced with:

1. Right after the slide showing that the robot cannot tell which stage it is at from one frame: "Add one past frame to the model's input. On the Pup Go Car task, the completion score becomes: clearly better / about the same / worse". Most people pick "better"; the answer is worse (39.5% vs 57% without history). The reveal is the first step of the next slide ("three ways to remember the past"), and it motivates why memory must be learned rather than appended.
2. Before the scaling curve: "The best short-context baseline scores 45.6. How long must RoboTTT's pre-training context be before it beats it? about 4 s (128 steps) / about 17 s (512) / about 1 min (2K) / 4.5 min (8K)". The answer (about 1 minute; at 1K it still loses, 43.9) shows that long memory only pays off once it is long enough, which is the real content of the scaling claim.

Both have a sourced answer, a likely wrong guess, nothing given away beforehand, and a reveal that opens the next point.

## Negative → positive: sentences on slides

The slide text should be the keyword skeleton of the script. Before and after from a real deck (Traditional Chinese originals):

| Before (sentence on the slide) | After (keywords; the sentence moves to the notes) |
|---|---|
| "In-Context Learning (ICL): without changing the weights, it learns a new task only from examples placed in its context, just like giving a language model one worked example." | "In-Context Learning (ICL): weights fixed, learns from examples" |
| "But the update rule is a hand-designed linear rule, and the authors argue it cannot extract the structure of long, repetitive streams." | "but hand-designed linear update, no gradient descent" |
| "DAgger: when the robot errs a human takes over and demonstrates the fix, then the fixes are used for training." | "DAgger: human fixes errors, robot trains on them" |
| "'Latency does not grow' comes from the architecture; the main text reports no measured latency." | "Latency: no measured numbers" |
| A poll slide with two lines of set-up before the question | "Add 1 past frame: Pup Go Car score?" (set-up spoken) |

Running `scripts/audit_text.py` on the first draft flagged 38 sentence-like lines; after the rewrite only the author list and source credits remained.
