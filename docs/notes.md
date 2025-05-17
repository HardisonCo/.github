I see a lot of threads pitting models against each other (or whole swarms of them) in the hope that "wisdom of crowds" will magically appear. After a stack of experiments of my own—and after watching the recent ASU/Microsoft-Research work [1].. I've landed on a simpler takeaway:
An LLM is a terrible verifier of another LLM. Subbarao Kambhampati's "(How) Do LLMs Reason/Plan?" talk shows o4-mini confidently producing provably wrong graph-coloring proofs until a symbolic SAT solver is introduced as the referee [1]. Stechly et al. quantify the problem: letting o4-mini critique its own answers *reduces* accuracy, whereas adding an external, sound verifier boosts it by ~30 pp across planning and puzzle tasks [2]. In other words, verification is *harder* than generation for today's autoregressive models, so you need a checker that actually reasons about the world (compiler, linter, SAT solver, ground-truth dataset, etc.).

Because of that asymmetry, stacking multiple LLMs rarely helps. The "LLM-Modulo" position paper argues that auto-regressive models simply can't do self-verification or long-horizon planning on their own and should instead be treated as high-recall idea generators wrapped by a single, sound verifier [3]. In my tests, replacing a five-model "debate" with one strong model + verifier gives equal or better answers with far less latency and orchestration overhead.

[1] https://www.youtube.com/watch?v=0u2hdSpNS2o - (How) Do LLMs Reason/Plan? (talk at Microsoft Research, 11 Apr 2025)

[2] https://arxiv.org/abs/2402.08115

[3] https://arxiv.org/abs/2402.01817 (related to the talk in #1)
0. teach agents about the codebase 
 -- Below is a step-by-step guide explaining how to understand a codebase by analyzing its code and using Git history. These instructions can help you quickly become productive and teach others how to navigate and contribute effectively.

first pass
    1. Gather High-Level Context
    Identify the Project’s Purpose

    Read the project’s README or documentation to understand goals, scope, and target users.

    Check for any design documents, wiki pages, or architecture diagrams if available.

    Discover Technology Stack

    Look at package manifests (e.g., package.json for Node.js, requirements.txt for Python, composer.json for PHP) to see which frameworks, libraries, and dependencies the code uses.

    Note the primary programming languages, frameworks, or architectural patterns involved.

    2. Examine Code Structure
    Directory Layout

    Observe the overall folder hierarchy (e.g., src/, app/, lib/, tests/) to see how code is organized.

    Look for domain-specific directories (e.g., models/, controllers/, services/, migrations/) that indicate architecture patterns (e.g., MVC, microservices).

    Identify Key Entry Points

    For web applications, locate the main server bootstrap file (e.g., index.js, app.js, server.py), or the framework-specific entry point (e.g., main.go in Go, manage.py in Django).

    For libraries/packages, look at the primary module file exported to users.

    Spot Cross-Cutting Concerns

    Examine configurations (e.g., .env, config/) to see environment variables and system settings.

    Check logging or instrumentation logic (often in a dedicated folder or utility file) to see where logs are generated.

    3. Use Git History to Understand Evolution
    Examine Commit Messages

    Look at commit messages in chronological order to see how the code evolved.

    Pay attention to commits that mention “refactor,” “fix,” “feature,” or “breaking change.” These indicate significant design shifts or areas that needed extra attention.

    Use git blame or Annotate Features

    git blame <file> shows which lines were changed by which commit and who authored them. This helps you see the rationale or context around specific lines.

    Useful for:

    Understanding why particular lines exist.

    Finding authors for deeper discussion or clarification.

    Review Pull/Merge Requests

    In platforms like GitHub, GitLab, or Bitbucket, each merge request typically includes a discussion thread.

    These threads might reveal design decisions, alternatives considered, or challenges faced during development.

    Searching closed pull requests by keywords (e.g., “authentication” or “performance”) can help you understand key features’ history.

    4. Learn by Tracking Significant Changes
    Identify Major Releases or Tags

    Look at Git tags or version numbers to find major releases.

    Review commit logs between releases to understand high-level changes (e.g., new features, architecture refactoring).

    Pinpoint “High-Risk” Areas

    Frequent bug fixes in certain files may indicate fragile or complex code.

    Many commits touching the same region can imply it’s a critical or evolving area of the code.

    Examine Architectural Overhauls

    If you see a commit or merge request that reorganizes large portions of code, it’s worth reading the discussion.

    Often there will be a design rationale explaining how the architecture changed, which is invaluable for new contributors.

    5. Synthesize Your Findings
    Build a Mental Model

    Combine knowledge from reading code structure, commit history, and documentation to form a conceptual map of how modules interact.

    Summarize your understanding: “Module A calls Module B to handle X feature. Module C is used for data persistence. Module D manages authentication.”

    Document Any Missing Explanations

    As you learn, note where the codebase lacks clarity.

    Contribute by adding comments, a new README.md in a subdirectory, or clarifying commit messages for the next person.

    Practice Small Fixes or Features

    Try minor contributions (e.g., refactor a small function, fix a bug).

    This helps you confirm your mental model of the system and gain confidence with the workflows.

    6. Teaching Others
    Host a Walk-Through

    Demonstrate how to read top-level files, point out important modules, and show how to navigate Git history.

    Answer questions about where to place new features or find existing functionalities.

    Provide Checklists

    Create a short cheat-sheet: “Steps to analyze a new module,” “Checklist before merging,” etc.

    Encourage new developers to follow these repeatable steps so they adopt best practices.

    Encourage Code Exploration via Git

    Show how to run git log --graph --oneline --decorate for a quick overview of branching and merging.

    Promote using git blame and PR reviews to understand context behind code lines and architectural decisions.

    Conclusion
    Analyzing a codebase involves reading high-level project documentation, understanding structure, and learning from the code itself.

    Using Git history provides insight into why the code looks the way it does, reveals architectural decisions, and indicates areas that are fragile or particularly important.

    A systematic approach—reviewing commits, reading PR/merge discussions, and referencing file histories—offers a deep and accurate understanding.

    Once you build a mental model, practice small contributions to solidify your knowledge and help others follow the same effective approach.

second pass

customize 1st pass for code / stack and include output of 1st pass

third pass 

include context on projects role in abstract and projects role in the context of HMS and finally in the context of the greater goal e.g.: gov and domain overview knowledge

4th pass

include info about how dev process in general works, then how HMS does dev with HMS-DEV and how HMS does docs etc...

5th pass 

HITL / RLHF gym that trains on how well agent can operate in system context and as standalone entitiy etc.. + does its own docs etc... 
intro to issue system and intro to other agents + optimization of collaberation model w/ them

1. clean up each code base and get it started / working w/ specs and integrated
2. complete the docs and setup autodoc system
3. get all dev ops sorted out so we have commands and menu for that
4. make issue bot that uses code to fix all issues (bugs) for us so we can fire Maria
5. complete the entire issue fider -> codify -> ... flow












DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition
1. Introduction
We introduce DeepSeek-Prover-V2, an open-source large language model designed for formal theorem proving in Lean 4, with initialization data collected through a recursive theorem proving pipeline powered by DeepSeek-V3. The cold-start training procedure begins by prompting DeepSeek-V3 to decompose complex problems into a series of subgoals. The proofs of resolved subgoals are synthesized into a chain-of-thought process, combined with DeepSeek-V3's step-by-step reasoning, to create an initial cold start for reinforcement learning. This process enables us to integrate both informal and formal mathematical reasoning into a unified model.



2. Model Summary
Synthesize Cold-Start Reasoning Data through Recursive Proof Search

To construct the cold-start dataset, we develop a simple yet effective pipeline for recursive theorem proving, utilizing DeepSeek-V3 as a unified tool for both subgoal decomposition and formalization. We prompt DeepSeek-V3 to decompose theorems into high-level proof sketches while simultaneously formalizing these proof steps in Lean 4, resulting in a sequence of subgoals.

We use a smaller 7B model to handle the proof search for each subgoal, thereby reducing the associated computational burden. Once the decomposed steps of a challenging problem are resolved, we pair the complete step-by-step formal proof with the corresponding chain-of-thought from DeepSeek-V3 to create cold-start reasoning data.

Reinforcement Learning with Synthetic Cold-Start Data

We curate a subset of challenging problems that remain unsolved by the 7B prover model in an end-to-end manner, but for which all decomposed subgoals have been successfully resolved. By composing the proofs of all subgoals, we construct a complete formal proof for the original problem. This proof is then appended to DeepSeek-V3's chain-of-thought, which outlines the corresponding lemma decomposition, thereby producing a cohesive synthesis of informal reasoning and subsequent formalization.

After fine-tuning the prover model on the synthetic cold-start data, we perform a reinforcement learning stage to further enhance its ability to bridge informal reasoning with formal proof construction. Following the standard training objective for reasoning models, we use binary correct-or-incorrect feedback as the primary form of reward supervision.

The resulting model, DeepSeek-Prover-V2-671B, achieves state-of-the-art performance in neural theorem proving, reaching 
88.9
% pass ratio on the MiniF2F-test and solving 49 out of 658 problems from PutnamBench. The proofs generated by DeepSeek-Prover-V2 for the miniF2F dataset are available for download as a ZIP archive.

3. ProverBench: Formalization of AIME and Textbook Problems
we introduce ProverBench, a benchmark dataset comprising 325 problems. Of these, 15 are formalized from number theory and algebra questions featured in the recent AIME competitions (AIME 24 and 25), offering authentic high-school competition-level challenges. The remaining 310 problems are drawn from curated textbook examples and educational tutorials, contributing a diverse and pedagogically grounded collection of formalized mathematical problems. This benchmark is designed to enable more comprehensive evaluation across both high-school competition problems and undergraduate-level mathematics.

Area	Count
AIME 24&25	15
Number Theory	40
Elementary Algebra	30
Linear Algebra	50
Abstract Algebra	40
Calculus	90
Real Analysis	30
Complex Analysis	10
Functional Analysis	10
Probability	10
Total	325
4. Model & Dataset Downloads
We release DeepSeek-Prover-V2 in two model sizes: 7B and 671B parameters. DeepSeek-Prover-V2-671B is trained on top of DeepSeek-V3-Base. DeepSeek-Prover-V2-7B is built upon DeepSeek-Prover-V1.5-Base and features an extended context length of up to 32K tokens.

Model	Download
DeepSeek-Prover-V2-7B	🤗 HuggingFace
DeepSeek-Prover-V2-671B	🤗 HuggingFace
Dataset	Download
DeepSeek-ProverBench	🤗 HuggingFace
5. Quick Start
You can directly use Huggingface's Transformers for model inference. DeepSeek-Prover-V2-671B shares the same architecture as DeepSeek-V3. For detailed information and supported features, please refer to the DeepSeek-V3 documentation on Hugging Face.

The following is a basic example of generating a proof for a problem from the miniF2F dataset:

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
torch.manual_seed(30)

model_id = "DeepSeek-Prover-V2-7B"  # or DeepSeek-Prover-V2-671B
tokenizer = AutoTokenizer.from_pretrained(model_id)

formal_statement = """
import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat

/-- What is the positive difference between $120\%$ of 30 and $130\%$ of 20? Show that it is 10.-/
theorem mathd_algebra_10 : abs ((120 : ℝ) / 100 * 30 - 130 / 100 * 20) = 10 := by
  sorry
""".strip()

prompt = """
Complete the following Lean 4 code:

```lean4
{}
```

Before producing the Lean 4 code to formally prove the given theorem, provide a detailed proof plan outlining the main proof steps and strategies.
The plan should highlight key ideas, intermediate lemmas, and proof structures that will guide the construction of the final formal proof.
""".strip()

chat = [
  {"role": "user", "content": prompt.format(formal_statement)},
]

model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True)
inputs = tokenizer.apply_chat_template(chat, tokenize=True, add_generation_prompt=True, return_tensors="pt").to(model.device)

import time
start = time.time()
outputs = model.generate(inputs, max_new_tokens=8192)
print(tokenizer.batch_decode(outputs))
print(time.time() - start)


use https://github.com/PhialsBasement/Chain-of-Recursive-Thoughts




CoRT (Chain of Recursive Thoughts) 🧠🔄
TL;DR: I made my AI think harder by making it argue with itself repeatedly. It works stupidly well.
What is this?
CoRT makes AI models recursively think about their responses, generate alternatives, and pick the best one. It's like giving the AI the ability to doubt itself and try again... and again... and again.

Does it actually work?
YES. I tested it with Mistral 3.1 24B and it went from "meh" to "holy crap", especially for such a small model, at programming tasks.

How it works
AI generates initial response
AI decides how many "thinking rounds" it needs
For each round:
Generates 3 alternative responses
Evaluates all responses
Picks the best one
Final response is the survivor of this AI battle royale
How to use the Web UI(still early dev)
Open start_recthink.bat
wait for a bit as it installs dependencies
profit??
If running on linux:

pip install -r requirements.txt
cd frontend && npm install
cd ..
python ./recthink_web.py
(open a new shell)

cd frontend
npm start
Examples
Mistral 3.1 24B + CoRT rec

Mistral 3.1 24B non CoRT non-rec

Try it yourself
pip install -r requirements.txt
export OPENROUTER_API_KEY="your-key-here"
python recursive-thinking-ai.py
The Secret Sauce
The magic is in:

Self-evaluation
Competitive alternative generation
Iterative refinement
Dynamic thinking depth
Star History(THANK YOU SO MUCH)
Star History Chart
Contributing
Found a way to make it even better? PR's welcome!

License
MIT - Go wild with it

and 










I see a lot of threads pitting models against each other (or whole swarms of them) in the hope that "wisdom of crowds" will magically appear. After a stack of experiments of my own—and after watching the recent ASU/Microsoft-Research work [1].. I've landed on a simpler takeaway:
An LLM is a terrible verifier of another LLM. Subbarao Kambhampati's "(How) Do LLMs Reason/Plan?" talk shows o4-mini confidently producing provably wrong graph-coloring proofs until a symbolic SAT solver is introduced as the referee [1]. Stechly et al. quantify the problem: letting o4-mini critique its own answers *reduces* accuracy, whereas adding an external, sound verifier boosts it by ~30 pp across planning and puzzle tasks [2]. In other words, verification is *harder* than generation for today's autoregressive models, so you need a checker that actually reasons about the world (compiler, linter, SAT solver, ground-truth dataset, etc.).

Because of that asymmetry, stacking multiple LLMs rarely helps. The "LLM-Modulo" position paper argues that auto-regressive models simply can't do self-verification or long-horizon planning on their own and should instead be treated as high-recall idea generators wrapped by a single, sound verifier [3]. In my tests, replacing a five-model "debate" with one strong model + verifier gives equal or better answers with far less latency and orchestration overhead.

[1] https://www.youtube.com/watch?v=0u2hdSpNS2o - (How) Do LLMs Reason/Plan? (talk at Microsoft Research, 11 Apr 2025)

[2] https://arxiv.org/abs/2402.08115

[3] https://arxiv.org/abs/2402.01817 (related to the talk in #1)
0. teach agents about the codebase 
 -- Below is a step-by-step guide explaining how to understand a codebase by analyzing its code and using Git history. These instructions can help you quickly become productive and teach others how to navigate and contribute effectively.

first pass
    1. Gather High-Level Context
    Identify the Project’s Purpose

    Read the project’s README or documentation to understand goals, scope, and target users.

    Check for any design documents, wiki pages, or architecture diagrams if available.

    Discover Technology Stack

    Look at package manifests (e.g., package.json for Node.js, requirements.txt for Python, composer.json for PHP) to see which frameworks, libraries, and dependencies the code uses.

    Note the primary programming languages, frameworks, or architectural patterns involved.

    2. Examine Code Structure
    Directory Layout

    Observe the overall folder hierarchy (e.g., src/, app/, lib/, tests/) to see how code is organized.

    Look for domain-specific directories (e.g., models/, controllers/, services/, migrations/) that indicate architecture patterns (e.g., MVC, microservices).

    Identify Key Entry Points

    For web applications, locate the main server bootstrap file (e.g., index.js, app.js, server.py), or the framework-specific entry point (e.g., main.go in Go, manage.py in Django).

    For libraries/packages, look at the primary module file exported to users.

    Spot Cross-Cutting Concerns

    Examine configurations (e.g., .env, config/) to see environment variables and system settings.

    Check logging or instrumentation logic (often in a dedicated folder or utility file) to see where logs are generated.

    3. Use Git History to Understand Evolution
    Examine Commit Messages

    Look at commit messages in chronological order to see how the code evolved.

    Pay attention to commits that mention “refactor,” “fix,” “feature,” or “breaking change.” These indicate significant design shifts or areas that needed extra attention.

    Use git blame or Annotate Features

    git blame <file> shows which lines were changed by which commit and who authored them. This helps you see the rationale or context around specific lines.

    Useful for:

    Understanding why particular lines exist.

    Finding authors for deeper discussion or clarification.

    Review Pull/Merge Requests

    In platforms like GitHub, GitLab, or Bitbucket, each merge request typically includes a discussion thread.

    These threads might reveal design decisions, alternatives considered, or challenges faced during development.

    Searching closed pull requests by keywords (e.g., “authentication” or “performance”) can help you understand key features’ history.

    4. Learn by Tracking Significant Changes
    Identify Major Releases or Tags

    Look at Git tags or version numbers to find major releases.

    Review commit logs between releases to understand high-level changes (e.g., new features, architecture refactoring).

    Pinpoint “High-Risk” Areas

    Frequent bug fixes in certain files may indicate fragile or complex code.

    Many commits touching the same region can imply it’s a critical or evolving area of the code.

    Examine Architectural Overhauls

    If you see a commit or merge request that reorganizes large portions of code, it’s worth reading the discussion.

    Often there will be a design rationale explaining how the architecture changed, which is invaluable for new contributors.

    5. Synthesize Your Findings
    Build a Mental Model

    Combine knowledge from reading code structure, commit history, and documentation to form a conceptual map of how modules interact.

    Summarize your understanding: “Module A calls Module B to handle X feature. Module C is used for data persistence. Module D manages authentication.”

    Document Any Missing Explanations

    As you learn, note where the codebase lacks clarity.

    Contribute by adding comments, a new README.md in a subdirectory, or clarifying commit messages for the next person.

    Practice Small Fixes or Features

    Try minor contributions (e.g., refactor a small function, fix a bug).

    This helps you confirm your mental model of the system and gain confidence with the workflows.

    6. Teaching Others
    Host a Walk-Through

    Demonstrate how to read top-level files, point out important modules, and show how to navigate Git history.

    Answer questions about where to place new features or find existing functionalities.

    Provide Checklists

    Create a short cheat-sheet: “Steps to analyze a new module,” “Checklist before merging,” etc.

    Encourage new developers to follow these repeatable steps so they adopt best practices.

    Encourage Code Exploration via Git

    Show how to run git log --graph --oneline --decorate for a quick overview of branching and merging.

    Promote using git blame and PR reviews to understand context behind code lines and architectural decisions.

    Conclusion
    Analyzing a codebase involves reading high-level project documentation, understanding structure, and learning from the code itself.

    Using Git history provides insight into why the code looks the way it does, reveals architectural decisions, and indicates areas that are fragile or particularly important.

    A systematic approach—reviewing commits, reading PR/merge discussions, and referencing file histories—offers a deep and accurate understanding.

    Once you build a mental model, practice small contributions to solidify your knowledge and help others follow the same effective approach.

second pass

customize 1st pass for code / stack and include output of 1st pass

third pass 

include context on projects role in abstract and projects role in the context of HMS and finally in the context of the greater goal e.g.: gov and domain overview knowledge

4th pass

include info about how dev process in general works, then how HMS does dev with HMS-DEV and how HMS does docs etc...

5th pass 

HITL / RLHF gym that trains on how well agent can operate in system context and as standalone entitiy etc.. + does its own docs etc... 
intro to issue system and intro to other agents + optimization of collaberation model w/ them





- verify

- should be able to pair with agents - 
  1 agent is researcher
  1 agent is coder
  1 agent is doing specs 



1. clean up each code base and get it started / working w/ specs and integrated
2. complete the docs and setup autodoc system
3. get all dev ops sorted out so we have commands and menu for that
4. make issue bot that uses code to fix all issues (bugs) for us so we can fire Maria
5. complete the entire issue fider -> codify -> ... flow












DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition
1. Introduction
We introduce DeepSeek-Prover-V2, an open-source large language model designed for formal theorem proving in Lean 4, with initialization data collected through a recursive theorem proving pipeline powered by DeepSeek-V3. The cold-start training procedure begins by prompting DeepSeek-V3 to decompose complex problems into a series of subgoals. The proofs of resolved subgoals are synthesized into a chain-of-thought process, combined with DeepSeek-V3's step-by-step reasoning, to create an initial cold start for reinforcement learning. This process enables us to integrate both informal and formal mathematical reasoning into a unified model.



2. Model Summary
Synthesize Cold-Start Reasoning Data through Recursive Proof Search

To construct the cold-start dataset, we develop a simple yet effective pipeline for recursive theorem proving, utilizing DeepSeek-V3 as a unified tool for both subgoal decomposition and formalization. We prompt DeepSeek-V3 to decompose theorems into high-level proof sketches while simultaneously formalizing these proof steps in Lean 4, resulting in a sequence of subgoals.

We use a smaller 7B model to handle the proof search for each subgoal, thereby reducing the associated computational burden. Once the decomposed steps of a challenging problem are resolved, we pair the complete step-by-step formal proof with the corresponding chain-of-thought from DeepSeek-V3 to create cold-start reasoning data.

Reinforcement Learning with Synthetic Cold-Start Data

We curate a subset of challenging problems that remain unsolved by the 7B prover model in an end-to-end manner, but for which all decomposed subgoals have been successfully resolved. By composing the proofs of all subgoals, we construct a complete formal proof for the original problem. This proof is then appended to DeepSeek-V3's chain-of-thought, which outlines the corresponding lemma decomposition, thereby producing a cohesive synthesis of informal reasoning and subsequent formalization.

After fine-tuning the prover model on the synthetic cold-start data, we perform a reinforcement learning stage to further enhance its ability to bridge informal reasoning with formal proof construction. Following the standard training objective for reasoning models, we use binary correct-or-incorrect feedback as the primary form of reward supervision.

The resulting model, DeepSeek-Prover-V2-671B, achieves state-of-the-art performance in neural theorem proving, reaching 
88.9
% pass ratio on the MiniF2F-test and solving 49 out of 658 problems from PutnamBench. The proofs generated by DeepSeek-Prover-V2 for the miniF2F dataset are available for download as a ZIP archive.

3. ProverBench: Formalization of AIME and Textbook Problems
we introduce ProverBench, a benchmark dataset comprising 325 problems. Of these, 15 are formalized from number theory and algebra questions featured in the recent AIME competitions (AIME 24 and 25), offering authentic high-school competition-level challenges. The remaining 310 problems are drawn from curated textbook examples and educational tutorials, contributing a diverse and pedagogically grounded collection of formalized mathematical problems. This benchmark is designed to enable more comprehensive evaluation across both high-school competition problems and undergraduate-level mathematics.

Area	Count
AIME 24&25	15
Number Theory	40
Elementary Algebra	30
Linear Algebra	50
Abstract Algebra	40
Calculus	90
Real Analysis	30
Complex Analysis	10
Functional Analysis	10
Probability	10
Total	325
4. Model & Dataset Downloads
We release DeepSeek-Prover-V2 in two model sizes: 7B and 671B parameters. DeepSeek-Prover-V2-671B is trained on top of DeepSeek-V3-Base. DeepSeek-Prover-V2-7B is built upon DeepSeek-Prover-V1.5-Base and features an extended context length of up to 32K tokens.

Model	Download
DeepSeek-Prover-V2-7B	🤗 HuggingFace
DeepSeek-Prover-V2-671B	🤗 HuggingFace
Dataset	Download
DeepSeek-ProverBench	🤗 HuggingFace
5. Quick Start
You can directly use Huggingface's Transformers for model inference. DeepSeek-Prover-V2-671B shares the same architecture as DeepSeek-V3. For detailed information and supported features, please refer to the DeepSeek-V3 documentation on Hugging Face.

The following is a basic example of generating a proof for a problem from the miniF2F dataset:

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
torch.manual_seed(30)

model_id = "DeepSeek-Prover-V2-7B"  # or DeepSeek-Prover-V2-671B
tokenizer = AutoTokenizer.from_pretrained(model_id)

formal_statement = """
import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat

/-- What is the positive difference between $120\%$ of 30 and $130\%$ of 20? Show that it is 10.-/
theorem mathd_algebra_10 : abs ((120 : ℝ) / 100 * 30 - 130 / 100 * 20) = 10 := by
  sorry
""".strip()

prompt = """
Complete the following Lean 4 code:

```lean4
{}
```

Before producing the Lean 4 code to formally prove the given theorem, provide a detailed proof plan outlining the main proof steps and strategies.
The plan should highlight key ideas, intermediate lemmas, and proof structures that will guide the construction of the final formal proof.
""".strip()

chat = [
  {"role": "user", "content": prompt.format(formal_statement)},
]

model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True)
inputs = tokenizer.apply_chat_template(chat, tokenize=True, add_generation_prompt=True, return_tensors="pt").to(model.device)

import time
start = time.time()
outputs = model.generate(inputs, max_new_tokens=8192)
print(tokenizer.batch_decode(outputs))
print(time.time() - start)


use https://github.com/PhialsBasement/Chain-of-Recursive-Thoughts




CoRT (Chain of Recursive Thoughts) 🧠🔄
TL;DR: I made my AI think harder by making it argue with itself repeatedly. It works stupidly well.
What is this?
CoRT makes AI models recursively think about their responses, generate alternatives, and pick the best one. It's like giving the AI the ability to doubt itself and try again... and again... and again.

Does it actually work?
YES. I tested it with Mistral 3.1 24B and it went from "meh" to "holy crap", especially for such a small model, at programming tasks.

How it works
AI generates initial response
AI decides how many "thinking rounds" it needs
For each round:
Generates 3 alternative responses
Evaluates all responses
Picks the best one
Final response is the survivor of this AI battle royale
How to use the Web UI(still early dev)
Open start_recthink.bat
wait for a bit as it installs dependencies
profit??
If running on linux:

pip install -r requirements.txt
cd frontend && npm install
cd ..
python ./recthink_web.py
(open a new shell)

cd frontend
npm start
Examples
Mistral 3.1 24B + CoRT rec

Mistral 3.1 24B non CoRT non-rec

Try it yourself
pip install -r requirements.txt
export OPENROUTER_API_KEY="your-key-here"
python recursive-thinking-ai.py
The Secret Sauce
The magic is in:

Self-evaluation
Competitive alternative generation
Iterative refinement
Dynamic thinking depth
Star History(THANK YOU SO MUCH)
Star History Chart
Contributing
Found a way to make it even better? PR's welcome!

License
MIT - Go wild with it

and 















use trivia and gamify if/how agent can contriute to codebase, we need to determine if understand 
goal
code
etc..
before they commit and we run dev prompt checks 








blaX.ai is like hacker news for black people and its the ibd.today writer view 
because we publish our manifesto changes there as white papers and updates etc..
also allows me to do my own show hn but to a non bias audience of specialized agent experts
the 1st step in changing a community is to raise the level of discourse in said ]
community so instead of what you see on x we have blaX.ai
- allows us to subtily introduce gov-ai and ai-gov
- justin scott
- cornesll west

- weave in gov and other products that make network real
- use - https://news.ycombinator.com/item?id=43835445 for discussion model that is recursive 
- add hn agent 
- make ai agent talent agency only avaliable via command line 
- weave in media refs like last week tonight
- weave in trascropt of helalthcare doc
- make weave func that lets us weave in X to docs 
- politians lie so do we, but we will fix if you find error e.g.: docs not aligned with real func

DETERMINE HOW THE USE CASES CAN BE SATISFIED BY THE MFE DOCUMENTATION AND COMPONENTS - THEN TRAIN AI ON THAT
FOR MAKING / CUSTOMIZING MFE FOR USER/PROGRAM