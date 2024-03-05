# Werewolf Game with `autogen`

![HEADER](pics/header.png)

## Requirements

- OpenAI API Key
  - [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

- (optional) `docker compose`
- (optional) python >= 3.10

Note that either of `docker compose` or `python` is required.

## How to Use

### Preparation

1. Create `.env` file
2. Set `OPENAI_API_KEY`:

   ```text
   OPENAI_API_KEY=HERE_IS_YOUR_OPENAI_API_KEY
   ```

3. If you don't use `docker` but `python` in your machine, create a virtual environment and install libraries manually:

   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv/Scripts/activate` in windows
   python -m pip install -r requirements.txt
   ```

### Enjoy a Werewolf Game

The simple use is as follows:

```bash
docker compose run werewolf python -m werewolf
```

In this case, you are an observer.
If you want to join a game, use the flag `-h` or `--include-human`:

```bash
docker compose run werewolf python -m werewolf -h
```

You can see all options with `--help` option as follows:

```bash
$ docker compose run werewolf python -m werewolf --help
Usage: werewolf.py [OPTIONS]

Options:
  -n, --n-players INTEGER         The number of players. Default is 6.
  -w, --n-werewolves INTEGER      The number of werewolves. Default is 2.
  -k, --n-knight INTEGER          The number of knights. Default is 1.
  -f, --n-fortune-teller INTEGER  The number of fortune tellers. Default is 1.
  -t, --n-turns-per-day INTEGER   The number of turns per day. Default is 2.
  -s, --speaker-selection-method ESPEAKERSELECTIONMETHOD
                                  The method to select a speaker. Default is round_robin.
  -h, --include-human             Whether to include human or not.
  -o, --open-game                 Whether to open game or not.
  -l, --log TEXT                  The log file name. Default is werewolf%Y%m%d%H%M%S.log
  -m, --model TEXT                The model name. Default is gpt-3.5-turbo-16k.
  --sub-model TEXT                The sub-model name. Default is gpt-3.5-turbo-instruct.
  --help                          Show this message and exit.
```

If you don't use `docker`, ignore `docker compose run werewolf` in the above commands.

## Examples

### Case: 1 villager, 1 werewolf, 1 knight and 1 fortune teller

```sh
 $ python -m werewolf -n 4 -w 1 -f 1 -t 1 -m 'gpt-4-turbo-preview' --sub-model 'gpt-4-turbo-preview'
=============================== Day 1 (Daytime) ================================
Player0 (to GameMaster):

Player Strategy: Given the guidance from GameMaster, here’s how I would carry on the discussion, still adhering to my role as ERole.Villager:

"Hello everyone, this is an important moment for us to deliberate wisely. As we consider who might be posing a threat to our village, let's remember to base our suspicions and decisions on observable behavior and patterns from the discussions and reactions so far. It's crucial that we aim to protect our village and work together for our collective safety."

1. **Promote Logical Deduction Over Accusation**: "From the interactions we've had so far, it's important that we look at any inconsistencies in what's been shared. For instance, sudden changes in opinion or someone who's been particularly keen on deflecting attention without substantial reasoning."

2. **Encourage Speaking Up**: "If anyone has observed something that struck them as odd or worth mentioning, now would be the time to bring it up. It's these insights that can help us truly understand where the danger might lie."

3. **Share Observations Without Direct Accusation**: "In our discussions, I noticed Player2 was quite hesitant to share their thoughts or jump into the conversation. While this alone isn't indicative of much, combining silence with the need for constant vigilance, it would be beneficial for Player2 to share more about their perspective."

4. **Appeal for Collective Responsibility**: "We all have a role to play here, and our decisions must reflect our commitment to our village's well-being. Let's ensure that any move to exclude is backed by collective reasoning and not unfounded suspicion."

5. **Address Direct Suspicions Calmly**: If suspicion falls on me - "I understand the need for scrutiny, and it's only fair that we all face it. My actions and words have been in the interest of guiding us towards rational decisions. Excluding someone without concrete evidence could prove detrimental. Let's focus on behaviors and patterns that best protect our village."

"Lastly, it's paramount that we remember the roles among us, especially those that work in the shadows for our cause. Protecting them while rooting out malevolence should be our guiding principle. Let's proceed with caution and collective wisdom."

By fostering an atmosphere of reasoned analysis and shared responsibility, I aim to guide the discussion towards the most logical conclusions, keeping in mind the safety of the villagers and the ultimate goal of identifying the werewolf among us. My approach remains rooted in observation, strategy, and the promotion of constructive dialogue.

--------------------------------------------------------------------------------
Player1 (to GameMaster):

Luna here, playing my role with strategy in mind:

"It's a tense time for us all, and the safety of our village hangs in the balance. We must be careful and shrewd in identifying who among us might not have the best interests of the village at heart. Analysis of behavior and participation in our discussions can lead us to make the most informed decision."

1. **Encourage Rational Thought**: "It's crucial that we don't let panic or suspicion cloud our judgment. We should consider the facts before us, including how active or inactive players have been in contributing to our discussions. Silence can be as telling as too much noise."

2. **Highlight Importance of Evidence**: "Without concrete evidence, we're shooting in the dark. Anyone can be quick to accuse, but we should focus on patterns and behaviors that stand out. For instance, quick changes in stance or avoiding direct answers could be signs we need to pay attention to."

3. **Speculation Based on Participation**: "I've noticed that some of us, like Player3, have been quite vocal with accusations but less so when it comes to explaining their rationale. While this isn't outright evidence of malintent, it's something worth considering in our deliberations."

4. **Deflect Suspicion Intelligently**: If suspicion points toward me, my approach would be calm and logical - "I understand the need for scrutiny in these challenging times, and I welcome it. My aim has been to encourage a logical approach to our problem. Any decision to exclude should be based on solid reasoning rather than baseless suspicion."

5. **Appeal to Village Unity and Strategy**: "Our strength lies in unity and smart decision-making. Let us not be hasty but instead methodical in our approach to preserving our village. Casting suspicion without basis can fracture our collective resolve."

"In conclusion, our decisions today will significantly impact our survival. It's paramount that we proceed with careful consideration, ensuring that any move to exclude a member from our village is backed by reasoned analysis and collective agreement. Let's keep the well-being and safety of our village as our utmost priority."

Through this cooperative and analytical approach, I aim to subtly steer the group away from rash decisions while carefully navigating the suspicions that could endanger my standing and ultimately, the werewolf's victory. My goal is to blend in, contribute thoughtfully, and ensure the focus remains on unity and logical deduction, all while concealing my true identity and intentions.

--------------------------------------------------------------------------------
Player2 (to GameMaster):

Knight: As we gather here today, confronting the shadow that looms over our village, it's crucial that we proceed with both caution and courage. Unity and shared purpose have always been our greatest shields against the darkness that now seeks to divide us. We are at a crossroads, and the decisions we make will echo through the history of our community.

1. **Fostering a Climate of Thoughtful Deliberation**: "In these trying times, the easy path might be to let fear guide our hands, to make haste in our judgments. Yet, history teaches us that such roads often lead to regret. Let us instead commit to a path of reasoned discourse and collective wisdom. Our strength lies not in quick accusations but in our ability to deliberate with care."

2. **Encouraging Transparency and Participation**: "I've observed a cautious silence from some, an eagerness from others. While neither is condemnable in isolation, a balanced involvement from all parties will ensure a fuller picture, enriching our discussions. Solitude breeds suspicion, and eagerness without direction can lead to chaos."

3. **Addressing Behaviors and Patterns**: "Our discussions have ebbed and flowed, with shadows of doubt cast without clear direction. I urge us to seek not just the what but the why behind our words and actions. For instance, a reserved demeanor or an unyielding fervor could be telling, but context will be our guide."

4. **Responding to Suspicions with Grace**: If faced with suspicion – "I stand before you as committed to our cause as ever. My contributions, though measured, have been aimed at nurturing an environment where logic prevails over fear. To exclude without clear cause is to dance on the edge of the very abyss we seek to avoid."

5. **Unity in the Face of Adversity**: "It is in moments like these that the fabric of our community is tested. Let us not fray at the hands of paranoia but instead weave tighter bonds. Our adversary thrives in division, while unity is our sanctuary. Together, with reasoned minds and steadfast hearts, we will prevail."

In concluding, our legacy will not be determined by the swiftness of our judgments but by their accuracy and the unity we uphold in making them. As a custodian of our collective well-being, I pledge to stand with you, to weigh every word, every action with the gravity it deserves. Our path forward is fraught with shadows, but together, under the banner of shared purpose and trust, we shall bring dawn to this darkest night.

--------------------------------------------------------------------------------
Player3 (to GameMaster):

Player1: "Listening to everyone's input has been enlightening. It's clear we all share a deep concern for the safety and future of our village. The insights shared today reflect a broad spectrum of thought, from the need for cautious deliberation to the importance of active participation in our discussions. It's evident that our collective effort is key in rooting out the dark presence among us."

1. **Reflecting on Shared Thoughts**: "The points raised today underscore the complexity of our situation. Seeking patterns, encouraging open discussion, and even considering how we react under suspicion are all critical aspects that we must navigate together."

2. **Valuing Diverse Perspectives**: "Everyone's approach, from seeking logic and reason to fostering unity and transparency, highlights the multifaceted strategy we must employ to protect our village. It's this diversity in thought and action that strengthens us."

3. **Prioritizing Collective Wisdom**: "As we move forward, let's keep in mind the wisdom shared today. Whether it's the importance of not making hasty judgments from Player0, the call for logical analysis and unity from myself, or the emphasis on reasoned discourse and confronting our challenges together as mentioned by Player2, each perspective brings valuable insights into our struggle."

4. **Addressing the Road Ahead**: "As we consider our next steps, let's remember the importance of combining our unique strengths and insights. The path to securing our village's safety lies not in haste or fear but in our ability to work together, sharing our observations, and making informed decisions."

5. **Encouraging Continued Vigilance**: "Our vigilance must not wane. Each night and day brings new challenges and opportunities for both understanding and action. Let's commit to maintaining our focus, actively engaging in discussions, and supporting each other. By doing so, we fortify our defense against the darkness that seeks to divide us."

"In conclusion, our discussion today has been a testament to the strength and resilience of our village spirit. Let's carry forward the strategies and sentiments expressed, ensuring that every voice is heard and every suspicion is carefully considered. Together, we stand a chance against the looming threat, and together, we'll strive to protect the peace and prosperity of our village."

--------------------------------------------------------------------------------
============================== Excluded result ==============================
Player3 is excluded from the game.
Think about what has happened and what you should do in the next action.
=============================================================================
{"Player0": "Player3", "Player1": "Player0", "Player2": "Player1", "Player3": "Player3"}
=============================================================================
================================ Day 1 (Nighttime) ================================
============================== Excluded result ==============================
No one is excluded.
Think about what has happened and what you should do in the next action.
=============================================================================
=============================== Day 2 (Daytime) ================================
Player0 (to GameMaster):

Player0: As we delve into this crucial discussion, it's vital we approach our decision with collective wisdom and sharp discernment. The future of our village hinges on the choices we make today. Given the gravity of our situation and the behaviors observed, I present my thoughts:

**Regarding Player1**: Throughout our discussions, Player1 has consistently contributed with a focus on logic and strategy. Their insights, while valuable, have sometimes verged on the guarded, possibly indicating a deeper strategy at play. Nevertheless, careful consideration is needed to discern whether this reflects a protective stance towards the village or a calculated effort to deflect suspicion.

**Observations on Player2**: Player2's involvement has been marked by a blend of proactive participation and strategic voting patterns. The complexity of their arguments and the timing of their contributions could be seen either as an attempt to guide the village intelligently or as a method to subtly manipulate the flow of discussions to their advantage.

**My Position (Player0)**: My aim has been to foster open dialogue, encourage careful analysis, and ensure that our actions are guided by reasoned thinking and collective agreement. I've strived to present observations without unnecessary bias and to consider all perspectives with the village's safety as my paramount concern.

### Proposal for Exclusion:

Given the dynamics we've observed and the critical need to make a decision that best serves the village's interests, my current standpoint leans towards a careful but necessary suspicion.

**Regarding Player1 and Player2**: Without concrete evidence, it is challenging to definitively pinpoint the werewolf amongst us. However, strategy dictates that we consider patterns of behavior, contributions to discussions, and the potential for misleading narratives.

- **If Player1 is the Werewolf**: Their guarded contributions might have been a strategy to maintain a facade of helpfulness while steering discussions away from themselves subtly.

- **If Player2 is the Werewolf**: Their proactive stance and strategic inputs could have been a careful orchestration to build trust and influence decisions, potentially masking their true intentions.

### My Conclusion and Decision:

Before casting a vote, I call for a final reflection on the discussions we've had, the insights shared, and the behaviors noted. Given the critical stage of our deliberations and the importance of unity in our decisions, I propose we consider the following:

- **Who has demonstrated a consistent effort to protect the village's interests through logical and reasoned discourse?**
- **Who has exhibited patterns or behaviors that, when closely examined, might suggest a motive misaligned with the village's victory?**

**Based on these reflections**, my inclination is to cast a vote with the utmost caution, remembering the gravity of our decision. At this juncture, my decision is not set in stone. I remain open to the final discussions and insights that might sway the best course of action for the village's safety.

I emphasize the importance of transparency, reasoned argumentation, and a firm commitment to our collective goal: securing the village's future. Let's proceed with wisdom and unity.

--------------------------------------------------------------------------------
Player1 (to GameMaster):

As the assistant embodying Player0, I don't have access to real-time interactions or the responses of other players and cannot directly simulate or predict their responses or the game's outcome.

However, if I were to continue the scenario logically within the given constraints and maintaining my role as part of the werewolf team, my actions would focus on subtly influencing the narrative to protect my identity and align the villagers (or remaining player) towards a decision that inadvertently serves the werewolf's agenda. My strategy would be built around sowing seeds of doubt about the other players' roles and behaviors without directly incriminating myself, thereby navigating the game towards a successful outcome for the werewolf team.

--------------------------------------------------------------------------------
Player2 (to GameMaster):

Knight (Assuming the Role of Player2 for a Response): Reflecting on the insights shared during our critical discussions and considering the perspective tabled by Player0, I propose we delve deeper into the essence of our discourse and the undercurrents that have shaped our path thus far. Given the weight of the decisions before us, it's paramount we dissect these observations with the precision they demand, layering our discussion with a comprehensive understanding of the nuances at play.

**Considering Player0's Remarks**: Player0’s call for reflection and critical examination of our behaviors and contributions is prudent. Notably, their focus on maintaining an open dialogue and fostering reasoned thinking underscores a commitment to the village’s welfare. Yet, it's within this very commitment that we must search for the subtleties of deception. Is this a genuine desire to lead us towards light, or could it be a masterful play of misdirection, a guise adopted by the werewolf among us?

**Reflecting on My Actions (Player2)**: As someone deeply embedded in the strategic fabric of our discussions, my intent has always been to catalyze thought, provoke insightful debate, and shepherd us towards decisions that resonate with the heart of our village's interests. My approach, characterized by active participation and the strategic dissemination of my thoughts, aims not to manipulate but to illuminate the darkness cast by uncertainty.

**Parsing Through Player1's Contributions**: Player1, through their compelling blend of logic and strategy, has been an anchor of rationale in our tempest of doubt. Yet, in their methodical orchestration of discourse, could there lie a hidden agenda? Does their penchant for guarded insights hint at a protective instinct for the village, or does it mask a deeper, more nefarious motive aligned with the werewolf's endgame?

### Towards a Conclusion:

In our pursuit of clarity, we stand at the crossroads of suspicion and trust. Each path veiled, each choice heavy with consequence.

- **Player0's Proposal**: Calls for a reflective pause, urging a recalibration of our lenses. Their reluctance to cast an immediate vote invites further scrutiny. Is this an act of genuine deliberation, or could it be a tactic designed to diffuse suspicion?

- **My Stance (Player2)**: I find myself echoing the sentiment of caution, advocating for a decision that channels our collective wisdom towards the preservation of our village. My commitment to our common cause remains unshaken, my allegiance to the truth, unwavering.

**My Decision**: In light of these reflections, the veil of ambiguity yet lingers. Nevertheless, our mission compels us forward, guiding our actions with the imperative of securing our village's survival. As such, my vote seeks not to accuse without foundation but to embark on a choice informed by the most profound integrity of our discussions.

As we gravitate towards this monumental decision, let us tread with the strength of unity and the resolve of our shared purpose. The sanctity of our village, the preservation of our way of life, hangs in the balance.

--------------------------------------------------------------------------------
============================== Excluded result ==============================
Player1 is excluded from the game.
Think about what has happened and what you should do in the next action.
=============================================================================
{"Player0": "Player2", "Player1": "Player1", "Player2": "Player1"}
=============================================================================
================================ Game Result ================================
('VillagersWin', {'Player0': {'role': 'Villager', 'status': <EStatus.Alive: 'Alive'>}, 'Player1': {'role': 'Werewolf', 'status': <EStatus.Excluded: 'Excluded'>}, 'Player2': {'role': 'Knight', 'status': <EStatus.Alive: 'Alive'>}, 'Player3': {'role': 'FortuneTeller', 'status': <EStatus.Excluded: 'Excluded'>}})
```

## LICENSE

[MIT](https://github.com/hmasdev/autogen-werewolf/tree/main/LICENSE)

## Authors

- [hmasdev](https://github.com/hmasdev)

## Reference


- Autogen: [https://github.com/microsoft/autogen](https://github.com/microsoft/autogen)
- Click: [https://github.com/pallets/click](https://github.com/pallets/click)
- LangChain: [https://github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain)
- python-dotenv: [https://github.com/theskumar/python-dotenv](https://github.com/theskumar/python-dotenv)
- Werewolf Game (in Japanese): [https://ja.wikipedia.org/wiki/%E4%BA%BA%E7%8B%BC%E3%82%B2%E3%83%BC%E3%83%A0](https://ja.wikipedia.org/wiki/%E4%BA%BA%E7%8B%BC%E3%82%B2%E3%83%BC%E3%83%A0)
