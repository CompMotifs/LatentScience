# Prompting LLMs to rephrase

## Goals
1. For paper in [paper1, paper2]
    - List every concept, method, and challenge used in the paper
        - Explain each one in detailed but simple terms for the following ideas:
            - how it works
            - the goal of its use
        - Rewrite each explanation above by replacing all terms with the most general way of saying it
2. For each category1, category2 above in [[concept, method, challenge] for each paper]
    - Is there overlap between the explanations in category1 with those in category2?
    

Prompts for the above
1. "I'm providing you with a scientific paper. Please identify every concept, method, and challenge present in the paper. For each item you identify, provide two explanations:

- A detailed but simple explanation focusing on how it works and the goal of its use.
- A rewritten version of that explanation, replacing all specific terms with the most general way of describing them."




To distill knowledge from research papers, we ask an LLM to identify the following concepts and reduce them into simplified language:
1. shared applied concept
2. methodological links
3. foundational philosophical links
4. cross-cutting themes and challenges
5. structural analogies (e.g., feedback loops, search spaces, fractal behavior)

## Approach 1: prompt each paper to distill core concepts
We will ask the LLM to reduce a single paper into the following ideas (this is basically the 'single' version of the 2-paper list above):
1. applied concept
2. methodologies
3. foundational philosophies
4. themes and challenges
5. structural challenges (e.g., feedback loops, search spaces, fractal behavior)

We want each LLM to list multiple for each of the above.

## Approach 2: use one prompt to reduce a single paper

Prompt: I am going to provide you with a scientific paper. My goal is to understand the core concepts, methods, and challenges presented in the most simple terms possible. I will feed you the paper's abstract, introduction, discussion and relevant sections. Give me a list of the concepts, methods, and challenges with very simple explanations.

Example: I tried the above onto the paper "A blueprint for a synthetic genetic feedback optimizer" (2023)



## Examples

### Output from "A blueprint for a synthetic genetic feedback optimizer"

#### Gemini
Here's a breakdown of the key concepts, methods, and challenges from the paper, explained in the simplest possible terms:

Concepts
Biomolecular Control / Biomanufacturing Factories: Think of cells as tiny factories. Biomolecular control is like giving these cell factories specific instructions using genetic tools so they can produce useful things like medicines or biofuels more efficiently.
Genetic Feedback Module (The Optimizer): This is the main invention of the paper. It's a special set of genetic instructions that acts like an automatic adjustment system inside a cell. Its job is to constantly "tune" the cell's performance to be the best it can be, even as things change around it.
Regulator Species: These are like little signal molecules inside the cell. The genetic optimizer adjusts how much of these signals are made and how quickly they disappear, which in turn influences the cell's performance.
Performance Metric: This is simply how we measure if the cell is doing a good job. It could be how much of a product it makes, how fast it grows, or how well it handles stress. The optimizer tries to maximize this "good job" score.
Mass Action Kinetics: This is a fancy way of saying how chemical reactions happen in a simple, predictable way based on how many molecules are involved. The paper uses this idea to model how the optimizer works inside the cell.
Implicit Reference Signal: Imagine trying to hit a moving target you can't quite see, but you know you're getting closer when your score goes up. In cells, the "best" performance often isn't a fixed number (explicit), but something that constantly shifts (implicit). The optimizer's cool trick is that it can find and follow this moving "best" performance without being told exactly where it is.
Methods
Genetic Engineering: This is the overall method of changing a cell's DNA to give it new abilities or instructions, like building the genetic feedback module itself.
Synthetic Biology: This is a field where scientists design and build new biological parts and systems (like the genetic optimizer) that don't exist in nature, or they redesign existing ones. It's like biological engineering.
Deterministic Simulations: This method involves using computer programs to predict how the genetic optimizer will behave in a perfectly predictable world, where there's no randomness. It helps test the basic idea.
Stochastic Simulations: This method also uses computer programs, but it includes randomness, like small unpredictable wiggles or bumps that naturally happen in biological systems. This makes the predictions more realistic and helps show if the optimizer works even with a bit of chaos.
Euler-Maruyama Scheme: This is a specific mathematical technique used in the stochastic simulations to help the computer model how things change over time with random influences.
Challenges
Context-Dependence: This means that a genetic module designed to work well in one type of cell or environment might behave completely differently, or even fail, when moved to another. It's like a special key that only works in one specific lock.
Metabolic Burden: Imagine a factory being asked to do too many jobs at once. Metabolic burden means that when cells are forced to express too many new proteins (like the ones from the genetic optimizer), it can slow down their normal growth and functions, making them less efficient.
Delay Between Regulator and Reporter: This is a potential limitation. If there's too much of a time lag between when the optimizer adjusts the "regulator" signals and when those changes actually affect the cell's "performance metric" (the reporter), the optimizer might not work as well.
Optimizer Speed Limitations: The optimizer can't respond to changes in the cell's environment that happen too quickly. It needs a bit of time to "think" and adjust, so it's best suited for situations where environmental shifts are slow, like over hours or days.