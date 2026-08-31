# Four building blocks

<p class="axioval-kicker">Picture tour: page 2 of 3</p>

Axioval uses four building blocks. Think of them as a dictionary, a recipe, a filled card, and a bundle.

<div class="diagram-frame" markdown>

<picture class="responsive-diagram">
  <source media="(max-width: 44rem)" srcset="../../assets/images/building-blocks-mobile.svg">
  <img src="../../assets/images/building-blocks.svg" alt="A dictionary, recipe, filled card, and bundle">
</picture>

</div>

## 1. Dictionary

The dictionary gives important things stable names. It can name an object such as a wall, a fact such as load bearing, or a known place where that fact may be stored.

Define a name once, then use it in many checks.

## 2. Recipe

A recipe describes a kind of check without choosing the final values. For example:

> Find a yes or no fact and compare it with the expected answer.

Many real checks can reuse that recipe.

## 3. Filled card

A filled card turns the recipe into one real check:

> Find the fact called Load bearing. The expected answer is yes.

It also says which objects should be inspected.

## 4. Bundle

The bundle keeps the dictionary, recipes, and filled cards together. It also carries a label that identifies the bundle and its version.

Before a bundle is used, every name and value is checked. Missing, unclear, or conflicting parts stop the process.

## The wall example

| Building block | In our example |
| --- | --- |
| Dictionary | Wall, Load bearing, External |
| Recipe | Compare a yes or no fact with an expected answer |
| Filled cards | Wall is required, Load bearing is yes, External is yes |
| Bundle | The complete cost group 331 example |

??? info "Show the technical names"
    The dictionary contains reusable definitions. A recipe is a rule definition.
    A filled card is a rule instance. The bundle is a ruleset package with a
    manifest and definition files.

!!! tip "Why separate the parts?"
    A shared dictionary avoids duplicate meanings. A shared recipe avoids
    repeating the same kind of check. Filled cards stay short and easy to review.

[Follow the wall example](../tutorials/din-276-331.md){ .md-button .md-button--primary }
