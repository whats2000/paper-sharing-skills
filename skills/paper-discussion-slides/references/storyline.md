# Storyline: examples of moving the audience's question

These come from a semester of robotics lectures by an experienced lecturer and from one of our own paper talks. They show ways to carry the audience from one slide to the next. Learn what each does for the audience; do not copy its look.

## The core problem: every slide fine, the deck fragmented

A paper talk had a clear point on every slide, yet felt disjointed. The slides that flowed were the poll slides: "add one past frame: better or worse?" left the room with a question, the reveal ("worse") raised the next one ("so how should memory work?"), and the core idea answered it. Everywhere else the deck changed topic cold:

- after the core idea, the next slide started "one dual-arm robot, three assembly tasks" with no question in between. A bridge such as "does this notebook actually help? test it on the longest task" turns the experiment into the answer to something;
- three result slides each made their own point. One question ("besides a higher score, what does remembering longer buy?") turns them into three answers to the same question;
- a closing "limitations" slide showed four unrelated cards. Each limitation could point back to the result it qualifies, so the audience knows which earlier claim to discount.

The fix is not better single slides; it is designing the hand-over between them.

## Keep the thread visible

- **A map that returns.** A lecture on visual SLAM showed its concept map (five boxes: rotations, reference frames, camera model, depth unprojection, point cloud alignment) at the start and again at each section boundary, five times in all, each time with the coming part highlighted. A manipulation lecture did the same four times, and its speaker notes on every map slide held the same line: the core question of the whole lecture. In a 30–45 minute talk, two or three returns are enough.
- **A pipeline with the current stage lit.** A research talk explained its three-stage data pipeline on three slides with the same strip at the top: the current stage in colour, the other two greyed.
- **A key-idea slide that grows.** "Key idea: camera ⟺ 3D coordinate system?" opened a section; when it returned later it had one more line: "how do we obtain the corresponding origin?", which opened the next section.
- **Bookends.** A talk opened and closed on the same definition of the field (with key words highlighted) and the same early robot photo; a lecture opened and closed on its learning outcomes.

## Let questions drive

- **A question chain.** An imitation-learning lecture went: challenges of behaviour cloning → a fix (collecting expert corrections) → "can we tackle the problem differently?" → "why do we fail to capture the expert?" → "can we use historical information?" → recurrent models → "what else?" → multimodal behaviour → diffusion models. Every answer exposed the next problem, so the audience always knew why the next slide existed.
- **An agenda of questions.** "How to build a dataset? Lots of decisions." followed by slides titled "Where?", "Who collects the data?", "How large?", "Who annotates?".
- **Sub-problems as plain questions.** A hanging-objects talk drew the two technical issues, then labelled them "Where to hang?" and "How to hang?".
- **A hook line.** A red line at the bottom of a slide: "Sounds great. Any other reason?", "Can we represent the reference frame differently?", "What would it take to build such a model?". It appears on the last click, after the slide's own point has been made; shown from the start it would give the next slide away. The next slide answers it.
- **The core question as a gap.** Top row: custom robot → expert programming → special-purpose behaviour. Bottom row: general-purpose robot → **?** → general-purpose behaviour. The `?` in the empty slot is the question the whole course answers; the same slide returns with "Can the advances in AI close the gap?".

## Make each step graspable

- **Everyday analogy.** Active perception explained by shaking a bottle to guess what is inside; adapting to physical properties shown by a person eating ice cream with a plastic spoon and then a metal one; the sense-plan-act loop introduced by asking the room how they would put a toy into a box before naming the three stages.
- **One diagram built up.** Changing reference frames was taught on one grid across seven slides: two frames, then a point, then its two coordinates, then the notation, then translation, then rotation.
- **Observation → insight → payoff.** Keypoints on different objects move alike when hung on the same hook → one trajectory works for any object → N × M planning problems become N × 1.

## Show the evidence

- **Demos that accumulate.** One hanging demo, then four, then sixteen, then a wall of a hundred small clips with "Success rate: 92% (92/100)" laid over it. The volume is the argument.
- **Same scene, with and without.** The same bowl and food: without guidance it spills, with guidance it does not; then "a 3 mm average deviation is enough to spill".
- **Breadth.** A grid of unseen foods (spheres, cubes, tubes, mixtures, liquid), then varying amounts and spreads.

## Focus inside a set

- **Move the highlight.** "Why do we need this technology? Autonomy / Comfort / Financiality" stayed in place on three slides; the frame moved to the next word and the picture changed to match it.
- **Quote, then highlight.** A definition appeared plain, then again with its key words highlighted. A paragraph of six principles appeared whole, then with all but one faded.

## Bring people in

- **Personal experience and humour.** "Who collects the data? Me? NO. We hired an 'expert' driver." "Am I done? Nightmare is coming… I spent a whole week watching videos." A 1990s household robot video ending with "Operated by a human ;-)".
- **The people behind the work.** Photos of the researchers behind a dataset or a talk, the lab, the team.

## Speaker notes in these decks

Few slides had notes; the slides carried the picture and the speaker explained live. Where notes existed they held what the slide did not show: the why, the everyday analogy, the numbers (the bottle-shaking analogy; N × M becoming N × 1), or simply the core question to keep the speaker on the thread.
