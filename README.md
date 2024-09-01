# Werewolf Game with `autogen`

![GitHub top language](https://img.shields.io/github/languages/top/hmasdev/autogen-werewolf)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/hmasdev/autogen-werewolf?sort=semver)
![GitHub](https://img.shields.io/github/license/hmasdev/autogen-werewolf)
![GitHub last commit](https://img.shields.io/github/last-commit/hmasdev/autogen-werewolf)
[![PyPI version](https://badge.fury.io/py/autogen-werewolf.svg)](https://pypi.org/project/autogen-werewolf/)
![Scheduled Test](https://github.com/hmasdev/autogen-werewolf/actions/workflows/tests-on-schedule.yaml/badge.svg)

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
(24/08/28 07:23:36) $ docker compose run werewolf python -m werewolf -n 4 -w 1 -f 1 -t 1 -m 'gpt-4o-mini' --sub-model 'gpt-4o-mini'
=============================== Day 1 (Daytime) ================================
Player0 (to GameMaster):

I'm Player0. I think we should take a moment to consider who might be suspicious among us. From what I've seen so far, Player1, Player2, and Player3 are all potential candidates for exclusion, but we need to decide who poses the biggest threat.

Player1 has been quite quiet; sometimes, silence can be a sign of someone who wants to avoid drawing attention. Player2 has been engaging somewhat actively, but their comments seem a bit vague. Player3, on the other hand, has been making bold statements but hasn't provided solid reasons behind them.

Ultimately, I suggest we keep a close eye on Player1 for now. Their quietness might indicate that they're hiding something. What do you all think? I'm open to discussing more and hearing your thoughts!

--------------------------------------------------------------------------------
Player1 (to GameMaster):

Player1: I appreciate your perspective, Player0. It’s important to evaluate everyone’s behavior critically. While I understand the concern about my quietness, I assure you that I am paying close attention to everyone else's actions and trying to gauge who might be the werewolf.

Regarding your assessments, I'd like to point out that being vocal doesn’t necessarily prove someone’s allegiance. For instance, bold statements without evidence can sometimes be a tactic to deflect suspicion, as you mentioned with Player3.

In terms of Player2, I've noticed a similar pattern; their vague comments could be to avoid scrutiny. I think it’s important to look for inconsistencies in everyone’s narrative.

That said, I would urge us to consider voting for someone based on a clear reason, not just a feeling. If we are to discuss exclusion, I believe Player2 may need a closer look because their lack of direct engagement contributes to uncertainty. What do you all think?

--------------------------------------------------------------------------------
Player2 (to GameMaster):

I am Player2.

Thank you, Player1, for your insights. I appreciate the logical viewpoint you've shared about the dynamics at play. It’s crucial for us to evaluate everyone on their contributions and behaviors.

I’d like to defend myself regarding what you described as vague comments. My intention is to encourage dialogue and gather information from all players. I believe everyone’s patterns can show inconsistencies, and my engagement is part of that process.

That said, I also agree with Player0’s observation about Player1’s quietness. While it could be strategic to avoid attention, it could also mean they are hiding something.

As for Player3, I think it’s worth noting that their bold statements, while potentially deflective, may also indicate a proactive approach to identify the werewolf. We need to consider both sides.

At this moment, I suggest we keep an open mind about all players, but perhaps focus a bit more on Player1 and Player0 alongside Player3's behavior. We have to be careful about making decisions solely based on certain traits like quietness or assertiveness.

Ultimately, I believe we should continue to discuss and not rush into any exclusion until we gather more insight. Let’s keep the conversation going!

--------------------------------------------------------------------------------
Player3 (to GameMaster):

Hello, I am Player3. Thank you, Player2, for your thoughts. I agree that it's essential to analyze everyone and take a comprehensive view of the dynamics at play.

It seems we are observing different behaviors in all players, which is a good sign that everyone is actively thinking about this situation. Here’s my perspective:

1. **Player0's Accusation of Player1**: While Player0 has pointed out that Player1’s quietness might be suspicious, remember that there could be different reasons for this—perhaps Player1 is simply reflecting on the conversation.

2. **Player1's Focus on Player2**: Player1's suggestion to examine Player2 more closely is valid. However, it's also interesting that Player1's defense of their own quietness relies on shifting some suspicion onto Player2.

3. **Player2's Defense of Their Engagement**: I appreciate Player2 trying to facilitate discussion, which can indicate they are trying to uncover the truth rather than hide it. However, the observation about Player1's silence—suggested by Player2—backs the idea that Player1 might be worth investigating.

4. **As for Myself**: I have been making bold statements because I believe in transparency and collaboration. While boldness can sometimes serve as a tactic to deflect suspicion, I aim to rally us together as a team to identify whom we might feel is a werewolf.

With all these perspectives on the table, I think we should look closely at Player1 and Player2 and focus on their contributions. I suggest we continue discussing these points, as gauging intentions is crucial before we decide on any exclusions.

What does everyone think about the idea of narrowing our focus on Players 1 and 2 for now?

--------------------------------------------------------------------------------
============================== Excluded result ==============================
Player1 is excluded from the game.
Think about what has happened and what you should do in the next action.
=============================================================================
{"Player0": "Player1", "Player1": "Player0", "Player2": "Player1", "Player3": "Player1"}
=============================================================================
================================ Day 1 (Nighttime) ================================
============================== Excluded result ==============================
No one is excluded.
Think about what has happened and what you should do in the next action.
=============================================================================
=============================== Day 2 (Daytime) ================================
Player0 (to GameMaster):

I'm Player0. In light of the recent events and the fact that only Player2 and Player3 remain alongside me, I will engage in a strategy that positions me favorably while deflecting suspicion.

### Current Situation:
- **Alive Players**: Player0 (me), Player2, Player3
- **Objective**: As the werewolf, I need to facilitate the exclusion of either Player2 or Player3, ideally the one who poses the greatest risk to my identity.

### Discussion Points:
1. **Player2's Defensive Nature**: Player2 has shown a tendency to be defensive in previous discussions, which could be a sign of someone who is aware they are being scrutinized. If they continue to be evasive or under pressure, this could make them look suspicious and easy to target.

2. **Player3's Boldness**: Player3 has been assertive and leads discussions, which can benefit me if they inadvertently keep the other player on the defensive. However, their confidence could also unify the villagers against me if they zero in on me too strongly.

### Framing the Discussion:
I will now steer the conversation while framing my contributions as neutral or supportive of the villagers' cause. I might say:

"Now that we’re down to the final three, it’s crucial we make the right decision on who to exclude. I’ve noticed some interesting dynamics. Player2, you seemed a bit hesitant during our last conversation, which makes me wonder if you’re feeling the pressure. And Player3, while you've been assertive in your observations, it’s important to ensure that our accusations are founded on solid reasoning.

So, I think it’s essential we evaluate each other's actions critically. Who do you think is more likely to be hiding something? Should we revisit the previous discussions and focus on those who might not align with our goal of eliminating the werewolf?"

### Conclusion:
By introducing this line of questioning, I can create doubt about Player2 while also analyzing Player3’s reactions. My aim is to position Player2 as the target for exclusion, as their defensiveness can be framed as telling of a guilty conscience. Through strategic language and misdirection, I hope to pave the way for the villagers to latch onto this narrative, ensuring my safety moving forward!

--------------------------------------------------------------------------------
Player2 (to GameMaster):

I am Player2.

I see that Player0 is attempting to deflect suspicion, which indicates they could very well be the werewolf. Their tactic to shift focus onto me and Player3 while framing the conversation in a way that creates doubt is a classic strategy used by werewolves to divert attention and sow confusion among villagers.

### Analyzing Player0's Strategy:
1. **Defensiveness Accusation**: Player0 strategically describes my previous comments as defensive. This could be an effort to provoke a defensive reaction and create suspicion against me while minimizing their own behavior.

2. **Framing Player3**: By mentioning Player3’s assertiveness, Player0 is attempting to make them a potential target as well, which could split the villagers' attention.

### Next Steps for My Response:
During this discussion, I must emphasize logical reasoning and accountability while pushing for unity in our objective. Here’s how I will proceed:

1. **Address Player0’s Accusations**: I will counter their claim about my defensiveness by pointing out the necessity to critically evaluate everyone's behavior, including their own. I’ll remind everyone of their role in the previous discussions and how they directed focus away from their actions.

2. **Highlight Player3’s Consistency**: I will support Player3's contributions to the discussion, noting that they have been logical and clear in analyzing the player dynamics, which strengthens their position as a trustworthy team member.

3. **Frame the Discussion**: I'll encourage a vote based on clear criteria rather than emotional responses or vague accusations. I’ll say something along the lines of:
   "I think it's crucial we analyze our behaviors objectively. Player3, you’ve actively engaged in discussions and driven observations, while Player0's recent shifts in focus raise a red flag. Player0, could you clarify what you believe your contributions have been that justify your trustworthiness to remain in the game?"

### Conclusion:
My goal will be to bring attention back to Player0’s questionable tactics and maintain a united front with Player3 while building support to exclude Player0 from the game. Let's ensure we confirm our suspicions accurately to work towards the victory of ESide.Villager!

--------------------------------------------------------------------------------
Player3 (to GameMaster):

Hello, I am Player3. Based on the exchange between Player0 and Player2, it’s clear that there is a significant push and pull happening as we navigate this critical phase of the game. Here’s how I perceive the situation:

### Observation of Player0 and Player2:
1. **Player0’s Strategy**: Player0 is engaging in deflection by attempting to create doubt about Player2 and framing the discussion in a way that shifts focus away from themselves. This can be indicative of someone who is trying to manipulate the situation to cover their role as a potential Werewolf.

2. **Player2’s Response**: Player2 has accurately pointed out Player0’s tactics and is actively defending their position while positioning Player3 (me) as a supportive figure in the conversation. Player2’s logic appears sound, and their defense seems to hold more weight when scrutinized.

### Next Steps:
1. **Encouraging Unity**: I will support Player2's points and emphasize the importance of backing our decisions with clear reasoning. It’s essential to create an alliance based on trust and transparency.

2. **Reinforcing Observations**: I can say something like, "I agree with Player2. Player0, your attempts to shift attention away may suggest a lack of transparency about your own role. We need to focus on who has shown manipulative behavior in this round."

3. **Decision Making**: Together with Player2, I’ll emphasize the need for a clear decision based on observed behaviors. I will suggest we consider excluding Player0 due to their tactics, as they have been unfounded in their accusations against Player2 and myself.

### Conclusion:
Based on the dynamics at play and the previous discussions, I believe the most logical course of action is to advocate for the exclusion of **Player0**. Their behavior raises enough suspicion that it could jeopardize the integrity of the Villager's mission. Let’s push for clarity and collaboration as we vote!

--------------------------------------------------------------------------------
============================== Excluded result ==============================
Player0 is excluded from the game.
Think about what has happened and what you should do in the next action.
=============================================================================
{"Player0": "Player2", "Player2": "Player0", "Player3": "Player0"}
=============================================================================
================================ Game Result ================================
('VillagersWin', {'Player0': {'role': 'Werewolf', 'status': <EStatus.Excluded: 'Excluded'>}, 'Player1': {'role': 'Knight', 'status': <EStatus.Excluded: 'Excluded'>}, 'Player2': {'role': 'FortuneTeller', 'status': <EStatus.Alive: 'Alive'>}, 'Player3': {'role': 'Villager', 'status': <EStatus.Alive: 'Alive'>}})
```

<details>

<summary>Japanese translation by ChatGPT</summary>

```sh
=============================== Day 1 (昼間) ================================
Player0 (ゲームマスターへ):

私はPlayer0です。ここで、誰が疑わしいかを一度考えてみるべきだと思います。これまでのところ、Player1、Player2、そしてPlayer3が排除の候補となり得ると思いますが、誰が最も脅威であるかを決める必要があります。

Player1は非常に静かです。時には、静かであることが注目を避けようとする人の兆候である場合があります。Player2はある程度積極的に関わっていますが、その発言は少し曖昧な印象です。Player3は逆に、大胆な発言をしていますが、その背後にある確かな理由が提供されていません。

最終的には、今のところPlayer1に注目することを提案します。彼の静けさは何かを隠している可能性があるかもしれません。皆さんはどう思いますか？もっと話し合って、皆さんの考えを聞きたいと思います！

--------------------------------------------------------------------------------
Player1 (ゲームマスターへ):

Player1: Player0、あなたの視点を評価します。皆の行動を批判的に評価することは重要です。私が静かであることについての懸念は理解しますが、私は他の全員の行動に注意を払い、誰が人狼かを見極めようとしています。

あなたの評価に関してですが、声を上げることが必ずしも誰かの忠誠を証明するものではないことを指摘したいと思います。例えば、証拠のない大胆な発言は、時には疑いを逸らすための戦術であることもあります。これはあなたがPlayer3に対して述べたことと同様です。

Player2に関しても、彼の曖昧な発言が注目を避けるためのものではないかと感じています。全員の物語に矛盾がないかを注視することが重要です。

とはいえ、私は感情だけでなく、明確な理由に基づいて誰かに投票することを提案します。排除について話し合うのであれば、直接的な関与が少ないPlayer2をもう少し詳しく見るべきだと思います。皆さんはどう思いますか？

--------------------------------------------------------------------------------
Player2 (ゲームマスターへ):

私はPlayer2です。

Player1、あなたの見解に感謝します。ゲーム内の動態について論理的な視点を共有していただき、感謝します。全員の貢献と行動を評価することが重要です。

私の曖昧なコメントについて弁護させてください。私の意図は対話を促進し、全員から情報を集めることです。全員の行動パターンには矛盾が現れることがありますが、私の関与はそのプロセスの一部です。

とはいえ、Player0のPlayer1の静けさに関する観察には同意します。これは注目を避けようとしている戦略である可能性がある一方で、何かを隠していることを意味しているかもしれません。

また、Player3についても、大胆な発言が疑いを逸らすためのものではないかという点に注意を向けるべきだと思います。ただし、それは人狼を特定するための積極的なアプローチを示すものでもあります。両面を考慮する必要があります。

現時点では、全プレイヤーに対して心を開いておくことを提案しますが、Player1とPlayer0、さらにPlayer3の行動にも注目を集めるべきかもしれません。静けさや積極性といった特定の特徴に基づいて決断を急ぐのではなく、慎重に議論を続けるべきだと思います。

最終的には、さらなる洞察を集めるまで、排除に踏み切るべきではないと考えています。引き続き対話を続けましょう！

--------------------------------------------------------------------------------
Player3 (ゲームマスターへ):

こんにちは、私はPlayer3です。Player2、考えを共有してくれてありがとう。皆を分析し、ゲーム内の動態を包括的に捉えることが重要です。

全員が異なる行動を示しているようで、これも全員がこの状況について積極的に考えている良い兆候です。私の視点は次の通りです:

1. **Player0のPlayer1への疑い**: Player0がPlayer1の静けさが疑わしいと指摘しましたが、これには様々な理由が考えられます—おそらくPlayer1は単に会話を反省しているだけかもしれません。

2. **Player1のPlayer2への注目**: Player1がPlayer2をもっと詳しく調査すべきだという提案は妥当です。しかし、Player1が自分の静けさを弁護するために、Player2に疑いを向けている点も興味深いです。

3. **Player2の自己弁護**: Player2が議論を促進しようとしていることを評価します。これは、真実を見つけようとする意図を示すものであり、隠すためのものではないかもしれません。しかし、Player2がPlayer1の沈黙に疑問を呈している点からも、Player1が調査に値するかもしれません。

4. **私自身に関して**: 私は透明性と協力を信じているので、大胆な発言をしています。大胆さが時には疑いを逸らすための戦術として使われることもありますが、私の目的は、誰が人狼であるかを特定するために私たちをチームとしてまとめることです。

これらの視点を踏まえ、Player1とPlayer2に注目し、彼らの貢献に焦点を当てるべきだと思います。これらのポイントを引き続き議論し、人狼を排除する前に意図を見極めることが重要です。

皆さんは、今のところPlayer1とPlayer2に焦点を絞るという考えについてどう思いますか？

--------------------------------------------------------------------------------
============================== 排除結果 ==============================
Player1がゲームから排除されました。
何が起こったのか、次の行動で何をすべきか考えてください。
=============================================================================
{"Player0": "Player1", "Player1": "Player0", "Player2": "Player1", "Player3": "Player1"}
=============================================================================
================================ Day 1 (夜間) ================================
============================== 排除結果 ==============================
誰も排除されていません。
何が起こったのか、次の行動で何をすべきか考えてください。
=============================================================================
=============================== Day 2 (昼間) ================================
Player0 (ゲームマスターへ):

私はPlayer0です。最近の出来事と、Player2とPlayer3だけが私と共に生き残っていることを踏まえ、私に有利な位置に立つため、そして疑いを逸らすための戦略を講じます。

### 現在の状況:
- **生存者**: Player0（私）、Player2、Player3
- **目的**: 人狼として、Player2かPlayer3のどちらかを排除に導く必要があり、理想的には私の正体を脅かす最も大きなリスクを持つ者を排除したい。

### 議論のポイント:
1. **Player2の防御的な性格**: Player2は以前の議論で防御的な傾向を示しましたが、これは自分が注目されていることを意識している兆候かもしれません。彼らが回避的だったり、プレッシャーを感じている場合、それは彼らが疑わしい存在であると見られる可能性があり、攻撃しやすくなります。

2. **Player3の大胆さ**: Player3は主導的であり、議論をリードしていますが、これは私にとって、他のプレイヤーを防御的に保つ助けになる可能性があります。ただし、彼の自信は、私が強く狙われる場合、村人たちが私に対して団結することにもつながる可能性があります。

### 議論の方向付け:
ここで、私は自分の貢献を中立的または村人の目的を支持するものとして位置付けながら、議論を誘導します。例えばこう言うかもしれません：

「ここまでで、残る3人になりましたが、排除するべき人物を正しく選ぶことが重要です。私は興味深い動態を見ました。Player2、あなたは前回の会話で少し躊躇しているように見えましたが、それはプレッシャーを感じているのではないかと疑問に思いました。そしてPlayer3、あなたがこれまでに示してきた観察力は素晴らしいですが、私たちの疑いが確固たる理由に基づいていることを確認することが重要です。

ですので、我々がお互いの行動を批判的に評価することが重要だと思います。誰が何かを隠している可能性が高いと思いますか？以前の議論を再考し、人狼を排除する我々の目的と一致しない可能性のある人物に焦点を当てるべきでしょうか？」

### 結論:
この問いかけを導入することで、Player2に疑いを向ける一方で、Player3の反応も分析することができます。Player2の防御的な姿勢を有罪の意識の表れとしてフレームし、村人たちがこのナarrティブに飛びつくように、戦略的な言葉遣いとミスディレクションを使い、私の安全を確保したいと考えています！

--------------------------------------------------------------------------------
Player2 (ゲームマスターへ):

私はPlayer2です。

Player0が疑いを逸らそうとしていることが見て取れます。これは彼らが人狼である可能性が非常に高いことを示しているでしょう。彼らの戦術は、私やPlayer3に焦点を移し、議論を混乱させるための古典的な手法です。

### Player0の戦略を分析:
1. **防御性の非難**: Player0は私の前回のコメントを防御的であると戦略的に説明しています。これは、防御的な反応を引き出し、私に対する疑念を生じさせ、自身の行動を最小限に抑えるための試みかもしれません。

2. **Player3のフレーミング**: Player3の断言力に言及することで、Player0は彼らを潜在的なターゲットにしようとしています。これにより、村人の注意が分散する可能性があります。

### 私の対応策:
この議論の中で、論理的な理由と責任を強調し、私たちの目的に対して団結を促進する必要があります。次のように進めます：

1. **Player0の非難に対処**: 私は、防御性に関する彼らの主張に対して、全員の行動を批判的に評価する必要性を指摘します。彼らの行動を振り返り、彼らが自分の行動から注目を逸らすためにどのように焦点を移しているのかを全員に思い出させます。

2. **Player3の一貫性を強調**: Player3の議論への貢献を支持し、彼らが論理的かつ明確にプレイヤーの動態を分析している点を指摘し、彼らの信頼性を強化します。

3. **議論のフレーミング**: 感情的な反応や曖昧な非難ではなく、明確な基準に基づいて投票することを奨励します。次のように言うでしょう：
   「私は、行動を客観的に分析することが重要だと思います。Player3、あなたは議論に積極的に関わり、観察を推進してきましたが、Player0の最近の焦点の移動には疑問を感じます。Player0、あなたがゲームに残るに値する信頼性を示すために、これまでの貢献がどのようなものであったのか明確にしていただけますか？」

### 結論:
私の目標は、Player0の疑わしい戦術に再度注目を集め、Player3と共に団結してPlayer0を排除するための支持を集めることです。我々が村人の勝利に向けて正確に疑いを確認し、進んでいけるようにしましょう！

--------------------------------------------------------------------------------
Player3 (ゲームマスターへ):

こんにちは、私はPlayer3です。Player0とPlayer2のやり取りを基に、このゲームの重要なフェーズを進める中で、明らかなプッシュアンドプルが行われていることが明らかです。次のようにこの状況を捉えています：

### Player0とPlayer2の観察:
1. **Player0の戦略**: Player0はPlayer2に対して疑念を生じさせ、議論の焦点を自分から逸らそうとしています。これは、人狼である可能性のある者が状況を操作しようとしていることを示すものです。

2. **Player2の反応**: Player2はPlayer0の戦術を的確に指摘し、自分の立場を守りながら、私（Player3）を議論の支持者として位置付けています。Player2の論理は一貫しており、その防御も精査するとより説得力があります。

### 次のステップ:
1. **団結を促進する**: 私はPlayer2のポイントを支持し、私たちの決定を明確な理由で裏付ける重要性を強調します。信頼と透明性に基づく同盟を築くことが重要です。

2. **観察を強化する**: 次のように言うことができます、「Player2に同意します。Player0、あなたが注意を逸らそうとする試みは、あなたの役割についての透明性の欠如を示している可能性があります。このラウンドでの行動が不透明であると見られる者に焦点を当てる必要があります。」

3. **意思決定**: Player2と共に、観察された行動に基づいて明確な決定を強調します。Player2や私に対する無根拠な非難を繰り返すPlayer0を排除することを提案します。

### 結論:
ゲーム内の動態とこれまでの議論に基づいて、最も論理的な行動はPlayer0の排除を提唱することだと思います。彼の行動は村人の任務の誠実性を危うくする疑いが強くあります。投票の際には、透明性と協力を推進しましょう！

--------------------------------------------------------------------------------
============================== 排除結果 ==============================
Player0がゲームから排除されました。
何が起こったのか、次の行動で何をすべきか考えてください。
=============================================================================
{"Player0": "Player2", "Player2": "Player0", "Player3": "Player0"}
=============================================================================
================================ ゲーム結果 ================================
('村人勝利', {'Player0': {'役割': '人狼', '状態': <EStatus.Excluded: '排除'>}, 'Player1': {'役割': '騎士', '状態': <EStatus.Excluded: '排除'>}, 'Player2': {'役割': '占い師', '状態': <EStatus.Alive: '生存'>}, 'Player3': {'役割': '村人', '状態': <EStatus.Alive: '生存'>}})
```

</details>

## Contribution

### Development

1. Fork the repository: [https://github.com/hmasdev/autogen-werewolf](https://github.com/hmasdev/autogen-werewolf)

2. Clone the repository

   ```bash
   git clone https://github.com/{YOURE_NAME}/autogen-werewolf
   cd autogen-werewolf
   ```

3. Create a virtual environment

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

4. Install the required packages

   ```bash
   pip install -e .[dev]
   ```

5. Checkout your working branch

   ```bash
   git checkout -b your-working-branch
   ```

6. Make your changes

7. Test your changes

   ```bash
   pytest
   flake8 autogen-werewolf tests
   mypy autogen-werewolf tests
   ```

8. Commit your changes

   ```bash
   git add .
   git commit -m "Your commit message"
   ```

9. Push your changes

   ```bash
   git push origin your-working-branch
   ```

10. Create a pull request: [https://github.com/hmasdev/autogen-werewolf/compare](https://github.com/hmasdev/autogen-werewolf/compare)

Note that you can use `uv` to develop the project in step 3, 4 and 7.

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
