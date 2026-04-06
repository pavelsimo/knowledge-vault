# Human-Centered AI

Human-centered AI asks not only whether a model can perceive, predict, or act, but whether it does so in ways that respect human values, limitations, preferences, safety, and privacy. In the CS231N framing, the goal shifts from building AI that merely sees the world to building AI that helps people.

## Source

- [[raw/00-clippings/(824) Stanford CS231N Deep Learning for Computer Vision  Spring 2025  Lecture 18 Human-Centered AI - YouTube.md|raw/00-clippings/(824) Stanford CS231N Deep Learning for Computer Vision  Spring 2025  Lecture 18 Human-Centered AI - YouTube.md]]

## Three Framing Questions

The lecture organizes the space into three goals:

1. Build AI to see **what humans see**
2. Build AI to see **what humans do not see**
3. Build AI to see **what humans would like to see**

The first goal produced classical computer vision benchmarks like object recognition. The second highlights superhuman pattern recognition in medicine, fine-grained perception, or large-scale monitoring. The third asks the harder systems question: what should AI optimize for, and for whom?

## Human Perception Is Powerful but Limited

Humans are excellent at visual understanding, but not perfect:
- **Attention is limited** — we miss events under fatigue or overload
- **Change blindness** shows that large scene changes can go unnoticed
- **Cognitive bias** shapes what we expect to see
- **Social and historical bias** affects how we interpret people and situations

That matters because AI is often evaluated against human performance. "Better than a person on average" is not enough if the failures are systematic, unfair, or occur in high-stakes situations.

## Where AI Can Help

AI is useful when it augments human perception rather than pretending humans are unnecessary:
- Monitoring repetitive or fatiguing environments
- Detecting subtle visual patterns humans miss
- Extending coverage where there are not enough trained workers
- Supporting care, accessibility, and safety workflows

Healthcare is a strong example. Hospitals, patient rooms, and elder care settings have too few human eyes and too much repetition. In those settings, vision systems can improve consistency and coverage.

## Bias, Safety, and Privacy

Human-centered AI treats model quality as more than raw accuracy.

Key risks:
- **Bias** — performance differs across groups or contexts
- **Safety** — errors can cause real-world harm in driving, medicine, or robotics
- **Privacy** — helpful monitoring can still become invasive
- **Labor impact** — systems can replace, deskill, or reshape work rather than simply assist it

A useful design rule is: if a system scales human bias, inattention, or surveillance, it is not enough to say that the model is technically impressive.

## Augmentation Over Replacement

One of the clearest takeaways from the lecture is that AI should often be framed as **augmentation**:
- Help clinicians, rather than simply "replace doctors"
- Help caregivers, rather than ignore labor shortages
- Help people in tasks they want help with, not tasks they value doing themselves

That last point matters in robotics too. People often want help with dirty, repetitive, or exhausting chores, but not with socially meaningful or emotionally important activities. Human preference should shape the task distribution.

## Human Preferences as a Design Signal

For embodied AI and robotics, a human-centered approach means asking:
- Which tasks do people actually want automated?
- Which tasks require trust, dignity, or social judgment?
- Which tasks are acceptable only with strong privacy guarantees?

This is why benchmark design matters. A benchmark that optimizes only task completion can miss whether the task itself is worth automating.

## Practical Takeaway

Human-centered AI broadens the objective:

```
good model != accurate model only
good model = accurate + fair + safe + privacy-aware + aligned with human preferences
```

That broader definition becomes more important as computer vision moves into healthcare, robotics, public infrastructure, and multimodal assistants.

## Related Topics

- [[computer-vision]] — the technical foundations of visual perception
- [[multimodal-models]] — image captioning, grounding, and multimodal hallucination
- [[robot-learning]] — task selection, embodiment, and human preferences in automation
- [[mlops]] — monitoring, failure analysis, and production safeguards
