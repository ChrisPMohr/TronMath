## Overview
The Mono-Green Tron deck prioritizes being able to play turn three Tron above almost all else. To faciltate this, it plays a lot of ways to find lands. Players of the deck often wonder how likely it is they will be able to find turn 3 Tron. [The linked spreadsheet](https://docs.google.com/spreadsheets/d/1JImt0zkLeBXdWJi9_AiS9IxoUqZeljkZhHpeVQ_5qIU/edit?usp=sharing "The linked spreadsheet") shows those probabilities.

### Goals
The two things that need to be determined for this spreadsheet are
1. The chance of a given hand being drawn
2. The chance of a given hand having three different tron lands untapped on turn 3 (from here on called "having turn 3 tron")

From there, we'd like to determine the chance that your hand will get better from taking one or more mulligans.

### Hands
One of the first things that needs to be determined is what hands should even be considered. A few principles were used here:

#### Only Two Land Hands
General wisdom among Tron players is that only hands with two different tron lands should be kept.  They are certainly more likely to have turn 3 tron than most other hands. For these reasons, this sheet only considers hands with two different tron lands, but could be extended to consider one land hands, which are certainly capable of having turn 3 tron.

It doesn't matter which two tron lands are in hand, so we just call them lands X and Y, with the third land being Z.

#### Which Cards?
There aren't too many cards that can be cast on turns 1 and 2 in a traditional MonoG Tron list that effect the chance of a turn 3 tron.
* A turn 1 Expedition Map guarantees turn 3 tron, but on turn 2 it does nothing.
* A turn 2 Sylvan Scrying combined with a Chromatic Sphere or Chromatic Star (from here on in, just a "Chromatic"), guarnatees turn 3 tron. We don't distinguish the two cards because it's irrelevant to these calculations.
* One Ancient Stirrings can be cast on turn 2 when combined with a Chromatic to dig 5 cards.
* Two Chromatics can be played and activated (one on turn 1, one on turn 2) to draw a card and possibly allow casting Slyvan Scrying or Ancient Stirrings.

There are several cards that are played in some versions on MonoG Tron that are not considered:
* This spreadsheet does not consider the effect of Relic of Progenitus on a hand. In general, the only way it results in turn 3 tron is if the hand has nothing else to play. A single chromatic could be played on turn 1 or 2.
* This spreadsheet does not consider the recently printed Once Upon A Time.

It would be possible to update the spreadsheet to take one or both of these cards into account.

#### Which Hands?
The spreadsheet shows every combination of cards that can lead to a unique lines of play. For example, we don't distinguish `Tron XY + Map` from `Tron XY + Map + Chromatic`, because the extra Chromatic doesn't effect the line of play the player would take.

### How are the Probabilities Calculated?
#### Methods
There are two different ways we can determine the probability of an event. We can calculate it exactly, in many cases by using the [hypergeometric distribution](https://en.wikipedia.org/wiki/Hypergeometric_distribution "hypergeometric distribution"). In the case we're drawing or looking at more than one card, we are looking at the chance to draw one or more copies of the relevant card. On this [calculator](https://stattrek.com/online-calculator/hypergeometric.aspx "calculator"), this is the `Cumulative Probability: P(X > 1)`.

We can also simulate the random variables (in this case, the drawing of cards) and measure how often the event occurs. This is called a [Monte Carlo Experiment](https://en.wikipedia.org/wiki/Monte_Carlo_method "Monte Carlo Experiment"). This repository contains the code for running these simulations.

It's more straightforward to use the hypogeometric distribution, but it can only be used in certain circumstances: when the events being measured are mutually exclusive. In other cases, we will use simulations.

#### Simulation Code
In short, the simulation code takes a starting deck with a certain number of copies of Tron lands, Chromatics, Maps, Scryings, Stirrings, and other cards ("Blanks"). The deck is shuffled, then the first N cards are examined. We evaluate whether each of the events we care about has happened. It is important to know which event is preferable in the case they overlap.

We repeat these trials many times in order to improve the accuracy of the estimates.

For the data currently in the spreadsheet, opening hands were simulated with 100 million trials, and draws within a hand were simulated with 10 million trials.

#### Chance to Draw a Hand
The events of drawing each of the hands are not mutually exclusive, so we will use a simulation. The order of preference for the hands is by chance to have turn 3 tron (described further below).

It's important to note that the chance to draw a hand is not the chance to have a hand that contains those cards, it's the chance to have a hand that contains those cards and doesn't also contain the cards for a better hand. This is necessary to allow the hand to fully describe what lines of play are possible.

One thing that is interesting to note is that, thanks to the London Mulligan rule, the chance of drawing a particular hand is not effected by the number of mulligans that have been taken, so long as you are allowed to keep enough cards in hand.

#### Chance to Improve hand after N mulligans
The chance to improve your hand after one mulligan is straightforward: it is the sum of the probability to draw any of the hands that have a better chance at hitting turn 3 Tron.

The chance of improving your hand after N mulligans is more accurately the chance that if you are willing to mulligan N times and stop whenever you draw a better hand, that you will succeed. Because the chances of improving your hand from your original is independent for each mulligan, the chance of improving your hand with `N` mulligans with a chance to improve it with one mulligan of `P` is `1 - (1 - P)^N`.

This becomes somewhat inaccurate after 2 mulligans, because there are hands that require 5 cards, which obviously are impossible to draw. The difference from the number on the sheet is pretty small for 3 mulligans, because there's only a single 5 card hand, `Tron XY + Chromatic + Chromatic + Stirrings`, which has a similar chance to have turn 3 Tron as `Tron XY + Chromatic + Stirrings`. For 4 mulligans, this is more probamatic, because there are a lot of 4 card hands. Calculating the chances to have these hands would require running the simulation again for different hand sizes.

#### Chance to have Turn 3 Tron
Some hands have guaranteed turn 3 tron, but most will have to draw into it. In order to find the chance of turn 3 tron for a given starting hand. Whenever the player draws a card that could effect their play, we calculate the chance of each set of cards that would lead to a different line of play.

Occasionally, multiple cards will be drawn in a row such that there's no reason to change decisions after the first card is drawn. For example, if a Chromatic is played on turn 1, if in order to optimize the chance of a turn 3 tron, there's no reason not to crack it on turn 2 regardless of what was drawn. Calculating the probabilities of the draws together requirers fewer calculations, but may be more complicated. In particular, when drawing only a single card, all of the events are mutually exclusive, so it's easy to calculate the probabilities, but when calculating probabilities for drawing multiple cards at once, we need to use a simulation. In cases where the probability has been calculated with a simulation, the probability is marked with an asterisk (\*).

To organize these probabilities, we use a probability tree. The top of the tree represents the initial state. Each branching indicates drawing one or more cards. The branch is labeled with what card or cards were drawn and the chance of them being drawn. The box under the branch describes what play is made in the case that card was drawn. This may either lead to another branch, or may be the end, when no more plays can be made before turn 3.

Every box is labeled with the number of cards left in the deck after the plays leading to that point. This information can be derived from the description of cards played, but it makes it easier to verify the probabilities are calcuated correctly.

The final box for every branch either is guaranteed to have turn 3 tron, or lists the final draws or cards looked at (from Ancient Stirrings) after every decision is made by the player and the chance to find the missing tron piece in the cards seen here.

Based on this tree, we can determine the total chance to have turn 3 tron.

#### Other Considerations
Some of the lines of play included are debatable from a strategy perspective, but optimize the chances of turn 3 tron. For example, with 2 Chromatics in hand, a player might not crack the second Chromatic on turn 2 when they would be unable to play a Sylvan Scrying if they drew it. Luckily, this doesn't effect the results too much because the chance of the extra card finding the tron land is low, so you can mostly choose not to take these questionable lines and the probabilities will still be roughly correct. Further, since the entire calculation for the probabilities are in the spreadsheet, it's easy to update that line of play.

The probabilities to have turn 3 tron are the chance on a 7 card hand. The chance is slightly higher after one or mulligans, because the cards sent to the bottom are guaranteed to be "blanks", so effectively all future draws are out of a smaller library. There's a couple ways this could be resolved, either by 

### Frequently Asked Questions
Your questions here!

### Future Work
* Try calculating probabilities entirely by simulation.
* Calculate probabilities for best hands without two tron lands.
* Calculate probabilities for decks with Once Upon a Time.
* Figure out a calculation for keep/mulligan advice and add to the spreadsheet.
* Make simulation code nicer.