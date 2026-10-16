# Use Teacher Workbench with OpenAI

Complete [installation](openai-install.md). Use ChatGPT Work for tasks needing finished files or several preparation steps, subject to your account's capabilities. See [Use ChatGPT](https://learn.chatgpt.com/docs/use-chatgpt).

In ChatGPT, select Teacher Workbench with `@`; in Codex use `$tw-orchestrator`. For a file-based session, say: “Read the attached Teacher Workbench instructions and apply the available workflows to this task.”

## Prepare and revise a lesson

> Use Teacher Workbench. Read this grade 5 mathematics lesson and prepare a 35-minute version in our attached template. Preserve the objective. Include a worked example, guided practice, extension, language supports, and a three-question exit ticket with a separate key. Create an editable teacher plan and separate student handout.

Inspect the files, then continue:

> Students understand equal groups but confuse numerator and denominator. Adjust the example and first practice question to expose that confusion. Explain what I should look for in their responses.

Request review:

> Use tw-pedagogical-review on the revised files. Check content, keys, timing, alignment, and accessibility. Correct material errors and identify anything I still need to verify.

## Rehearse a teaching move

> Use tw-lesson-rehearsal with this lesson. Let me practice explaining the worked example. Present one plausible misconception at a time, wait for my response, and give specific feedback tied to the lesson. Label the dialogue as a simulation.

## Check the calculator with synthetic data

> Use tw-grade-calculations. Quizzes are 40%: 8/10, 18/20, and one missing assignment worth 10 points. The project is 60%: 45/50. Pool points within each category. Calculate the grade excluding the missing assignment, then counting it as zero. Run the bundled calculator if available, show the policy and arithmetic, and say whether you executed it.

Expected results: **88.67%** when excluded and **80.00%** when zero. This checks arithmetic; it does not recommend a grading policy.

## Keep the workflow useful

Supply actual constraints and correct drafts in ordinary language. Request the resource you need. Ask the assistant to distinguish sources opened from unavailable references, and code executed from calculations described.

The host supplies file production, browsing, connections, and scheduling. Verify the delivered file or link. Use deidentified evidence, keep consequential decisions with the teacher, and review before sharing. The [teacher guide](../USER_GUIDE.pdf) has more examples.
