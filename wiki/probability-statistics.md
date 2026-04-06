# Probability and Statistics

This topic covers foundational probability theory for computer scientists, drawn from the Stanford CS109 course. It provides the mathematical underpinning for machine learning, Bayesian reasoning, and statistical modeling.

## Source

- `raw/02-cs109-probability-for-computer-scientists/Stanford CS109.md`
- Course playlist: https://www.youtube.com/playlist?list=PLoROMvodv4rOpr_A7B9SriE_iZmkanvUg
- Book: https://probabilityforcs.firebaseapp.com/book

## Foundations

### Sample Space and Events

- A **sample space** is the set of all possible outcomes of an experiment
- An **event** is a subset of the sample space
- **Probability** assigns a number in [0, 1] to each event

### Independence

Two events A and B are **independent** if knowing one gives no information about the other:
- P(A ∩ B) = P(A) · P(B)

**Example (two dice):**
- Let X₁ = first die, X₂ = second die, S = X₁ + X₂
- Events "X₁ = 1" and "S = 7" **are independent** (P(S=7|X₁=1) = 1/6 = P(S=7))
- Events "X₁ = 1" and "S = 5" **are NOT independent** (P(S=5|X₁=1) ≠ P(S=5))
- Therefore X₁ and S as **random variables** are **dependent** — independence must hold for all values

## Bayes' Theorem

Bayes' theorem updates a belief (prior) given new evidence:

```
P(H | E) = P(E | H) · P(H) / P(E)
```

- **P(H)** — prior: your belief before seeing evidence
- **P(E | H)** — likelihood: probability of evidence given hypothesis
- **P(H | E)** — posterior: updated belief after seeing evidence
- **P(E)** — normalizing constant (often hard to compute directly)

### Two Tricks for the Denominator

1. **Ratio formulation** — reformulate as a ratio problem to avoid computing P(E) directly
2. **Law of total probability** — expand P(E) = Σ P(E|Hᵢ)·P(Hᵢ) over all hypotheses

### Bayesian Updating

A **belief is not a single number — it is a distribution** over all possible values. As you observe evidence, you update this distribution:
- Prior distribution → observe evidence → posterior distribution
- If someone asks "what is your belief?" → give a distribution, not a point estimate

## Marginalization

Marginalization sums out a variable to get the **marginal probability**:
- P(A) = Σ P(A, B=b) over all values of B
- Historical note: called "marginal" because these totals were written in the margins of probability tables

## Conditional Probability

```
P(A | B) = P(A ∩ B) / P(B)
```

## Joint Distributions

A **joint distribution** P(X, Y) describes the probability of all combinations of two variables:
- From a joint distribution, you can derive marginals and conditionals
- Independence: P(X, Y) = P(X) · P(Y) for all values (plot looks like a rectangular grid)
- Dependence: the plot shows non-rectangular structure

## Random Variables

A random variable is a function from outcomes to numbers:
- **Discrete** random variable: finite or countably infinite range
- **Continuous** random variable: uncountably infinite range (described by a PDF)

## Expectation and Variance

- **Expected value (mean):** E[X] = Σ x · P(X = x)
- **Variance:** Var(X) = E[(X − E[X])²]

## Covariance

Covariance measures the linear relationship between two random variables X and Y:

```
Cov(X, Y) = E[(X − E[X])(Y − E[Y])]
```

- **Positive covariance:** when X is high, Y tends to be high (move together)
- **Negative covariance:** when X is high, Y tends to be low (move opposite)
- **Zero covariance:** no linear relationship

**Intuition:** for a data point above the mean in both X and Y, the product of deviations is positive → contributes positively to covariance.

## Logarithm Tricks in Probability

Working in log-space is common when:
- Products of many small probabilities underflow to zero
- Log turns products into sums: log(P(A)·P(B)) = log P(A) + log P(B)
- Log is monotone, so argmax is preserved

## Related Topics

- [[neural-networks]] — loss functions and cross-entropy use probability concepts
- [[mlops]] — evaluation metrics like precision/recall are based on probability
- [[optimization]] — gradient descent and stochastic methods have probabilistic interpretations
