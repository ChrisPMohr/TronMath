## Overview
The Mono-Green Tron deck prioritizes being able to play turn three Tron above almost all else. To facilitate this, it plays a lot of ways to find lands. Players of the deck often wonder how likely it is they will be able to find turn 3 Tron. [The linked spreadsheet](https://docs.google.com/spreadsheets/d/1JImt0zkLeBXdWJi9_AiS9IxoUqZeljkZhHpeVQ_5qIU/edit?usp=sharing "The linked spreadsheet") shows those probabilities.

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
* A turn 2 Sylvan Scrying combined with a Chromatic Sphere or Chromatic Star (from here on in, just a "Chromatic"), guarantees turn 3 tron. We don't distinguish the two cards because it's irrelevant to these calculations.
* One Ancient Stirrings can be cast on turn 2 when combined with a Chromatic to dig 5 cards.
* Two Chromatics can be played and activated (one on turn 1, one on turn 2) to draw a card and possibly allow casting Sylvan Scrying or Ancient Stirrings.
* One copy of Once Upon a Time can be cast for free as the first spell of the game. Another copy can be cast on turn 2 when combined with a Chromatic.

There are several versions of spreadsheets to for different decklists containing different mixes of these cards.

There are several cards that are played in some versions on MonoG Tron that are not considered:
* This spreadsheet does not consider the effect of Relic of Progenitus on a hand. In general, the only way it results in turn 3 tron is if the hand has nothing else to play. A single chromatic could be played on turn 1 or 2.

It would be possible to update the spreadsheet to take this or other cards into account.

#### Which Hands?
The spreadsheet shows every combination of cards that can lead to a unique lines of play. For example, we don't distinguish `Tron XY + Map` from `Tron XY + Map + Chromatic`, because the extra Chromatic doesn't effect the line of play the player would take.

### Simulation Code
This simulation simulates both drawing hands, and playing those hands in order to get turn 3 tron. The general method is know as a [Monte Carlo Experiment](https://en.wikipedia.org/wiki/Monte_Carlo_method "Monte Carlo Experiment").

In short, the simulation code takes a starting deck with a certain number of copies of Tron lands, Chromatics, Maps, Scryings, Stirrings, Once Upon a Time, and other cards ("Blanks"). The deck is shuffled. Then the first 7 cards are examined in order to determine what hand was draw.

Next, the hand is played. This is done by executing a series of rules, which encode both the rules for playing each card and starting a new turn. The rules are ordered, and we continuously execute the highest priority rule until it's turn 3.

We repeat these trials many times in order to improve the accuracy of the estimates.

For the data currently in the spreadsheet, opening hands were simulated with 100 million trials.

#### Simulation Play Rules

1. If we've drawn all three Tron lands, we have Tron.
1. If it's Turn 3, we don't have Tron.
1. If it's Turn 1, and we have a Expedition Map in hand and an untapped mana, we will have Tron.
1. If we have {1G} and a Sylvan Scrying in hand, we will have Tron.
1. If we have a Once Upon a Time, and haven't cast one yet, cast it.
1. If we have a Chromatic in play and a free mana, crack it for a green.
1. If we have a Once Upon a Time, have cast one already, and have {1G} to cast it, cast it if we do not have a Chromatic and an Ancient Stirrings in hand.
1. If we have a Chromatic in hand and at least 2 mana, play a Chromatic.
1. If we have an Ancient Stirrings in hand and {G} to cast it, cast it.
1. If we have a Once Upon a Time, have cast one already, and have {1G} to cast it, cast it.
1. If we have a Chromatic in hand and at least 1 mana, play a Chromatic.
1. Finish the turn. Untap and draw a card.

#### Other Considerations
Some of the lines of play that are executed by the simulation are debatable from a strategy perspective, but optimize the chances of turn 3 tron. For example, with 2 Chromatics in hand, a player might not crack the second Chromatic on turn 2 when they would be unable to play a Sylvan Scrying if they drew it. Luckily, this doesn't effect the results too much because the chance of the extra card finding the tron land is low, so you can mostly choose not to take these questionable lines and the probabilities will still be roughly correct. Further, since the entire calculation for the probabilities are in the spreadsheet, it's easy to update that line of play.

#### Configuration
The simulation code can be configured in a number of ways.
The initial distribution of cards can be adjust to find probabilities for different decklists.
The simulation can switch between being on the play and on the draw.
The number of trials can be changed to adjust the tradeoff between accuracy and speed.

#### Debugging
The logging level of the simulation can be set to "DEBUG" in order to print messages for every rule execution when playing the hands. This is useful to verify that the rules are executing correctly. It's recommended to set the number of trials very low when doing this.

`simulated_hands` variable can be set to only play out a subset of all possible hands. This useful combined with setting the logging level to debug rules, or can be used to calculate the probability of turn 3 tron for just some hands, if that is desired.

### Spreadsheet

#### Chance to Draw a Hand
The spreadsheet shows the chance to draw a each possible hand. The order of preference for the hands is by chance to have turn 3 tron (described further below).

It's important to note that the chance to draw a hand is not the chance to have a hand that contains those cards, it's the chance to have a hand that contains those cards and doesn't also contain the cards for a better hand. This is necessary so that each hand of cards grouped in the hand has the same chance of having turn 3 tron.

One thing that is interesting to note is that, thanks to the London Mulligan rule, the chance of drawing a particular hand is not effected by the number of mulligans that have been taken, so long as you are allowed to keep enough cards in hand.

#### Chance to Improve hand after N mulligans
The chance to improve your hand after one mulligan is straightforward: it is the sum of the probability to draw any of the hands that have a better chance at hitting turn 3 Tron.

The chance of improving your hand after N mulligans is more accurately the chance that if you are willing to mulligan N times and stop whenever you draw a better hand, that you will succeed. Because the chances of improving your hand from your original is independent for each mulligan, the chance of improving your hand with `N` mulligans with a chance to improve it with one mulligan of `P` is `1 - (1 - P)^N`.

This becomes somewhat inaccurate after more than one mulligans, because there are hands that require 6, 5, or 4 cards, which obviously are impossible to draw after mulliganing more than once. The simulation could be updated to find the chance of drawing each hand, including only hands that require no more than 5, 4, or 3 cards, in order to have this probability exactly. Most of these hands requiring many cards are only possible in decks that include Once Upon a Time.

### Verifying the Simulation

Previously, this spreadsheet was calculated primary by hand, using a simulation only in a few cases where calculating the probabilities was challenging. This can be used to verify that the simulation is producing valid results for the chances to have turn 3 tron.

The previous spreadsheet is saved in the tab called "Probabilities (Old)". The description of how those probabilities were derived is below.

#### How are the Probabilities Calculated?
There are two different ways we can determine the probability of an event. We can calculate it exactly, in many cases by using the [hypergeometric distribution](https://en.wikipedia.org/wiki/Hypergeometric_distribution "hypergeometric distribution"). In the case we're drawing or looking at more than one card, we are looking at the chance to draw one or more copies of the relevant card. On this [calculator](https://stattrek.com/online-calculator/hypergeometric.aspx "calculator"), this is the `Cumulative Probability: P(X > 1)`.

We can use a Monte Carlo experiment to simulate random events. Older versions of this repository contains the code for running these simulations.

It's more straightforward to use the hypogeometric distribution, but it can only be used in certain circumstances: when the events being measured are mutually exclusive. In other cases, we will use simulations.

#### Chance to have Turn 3 Tron
Some hands have guaranteed turn 3 tron, but most will have to draw into it. In order to find the chance of turn 3 tron for a given starting hand. Whenever the player draws a card that could effect their play, we calculate the chance of each set of cards that would lead to a different line of play.

Occasionally, multiple cards will be drawn in a row such that there's no reason to change decisions after the first card is drawn. For example, if a Chromatic is played on turn 1, if in order to optimize the chance of a turn 3 tron, there's no reason not to crack it on turn 2 regardless of what was drawn. Calculating the probabilities of the draws together requirers fewer calculations, but may be more complicated. In particular, when drawing only a single card, all of the events are mutually exclusive, so it's easy to calculate the probabilities, but when calculating probabilities for drawing multiple cards at once, we need to use a simulation. In cases where the probability has been calculated with a simulation, the probability is marked with an asterisk (\*).

To organize these probabilities, we use a probability tree. The top of the tree represents the initial state. Each branching indicates drawing one or more cards. The branch is labeled with what card or cards were drawn and the chance of them being drawn. The box under the branch describes what play is made in the case that card was drawn. This may either lead to another branch, or may be the end, when no more plays can be made before turn 3.

Every box is labeled with the number of cards left in the deck after the plays leading to that point. This information can be derived from the description of cards played, but it makes it easier to verify the probabilities are calcuated correctly.

The final box for every branch either is guaranteed to have turn 3 tron, or lists the final draws or cards looked at (from Ancient Stirrings) after every decision is made by the player and the chance to find the missing tron piece in the cards seen here.

Based on this tree, we can determine the total chance to have turn 3 tron.

### Frequently Asked Questions
Your questions here!

### Future Work
* Calculate the probabilities for hands when keeping a smaller number of cards.
* Calculate probabilities for best hands without two tron lands.
* Figure out a calculation for keep/mulligan advice and add to the spreadsheet.
* Make simulation code nicer.