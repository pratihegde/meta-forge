# MetaForge Demo Script

## 1. Introduction & Architecture (0:00 - 0:45)
**[Visual: Show the MetaForge Landing Page (Dark Theme)]**

**Speaker:**
"Hi everyone. Today I'm demonstrating MetaForge, an AI-powered application builder that transforms natural language into working web apps in minutes."

**[Visual: Briefly show the Architecture Diagram or the 'agents/orchestrator.py' file]**

**Speaker:**
"Under the hood, MetaForge uses a sophisticated multi-agent architecture powered by the Google Agent Development Kit (ADK).
It's not just one AI model; it's a team of specialized agents working together:
- First, a **Planner Agent** analyzes your request and creates a detailed technical specification.
- Then, **Frontend and Backend Agents** work in parallel to write the actual code—React for the UI and Python for the server.
- Finally, a **Self-Healing mechanism** validates the code and automatically fixes any errors before showing you the result."

## 2. End-to-End Scenario: Tic Tac Toe (0:45 - 1:15)
**[Visual: MetaForge Landing Page input box]**

**Speaker:**
"Let's see it in action. I'll ask it to build a classic: 'Create a modern, dark-themed Tic Tac Toe game with a score counter.'"

**[Action: Type the prompt and click 'Generate']**

**Speaker:**
"As soon as I click generate, the orchestration begins."

## 3. Under the Hood: The Loading Process (1:15 - 2:00)
**[Visual: The Workspace View with the Progress Panel/Spinner active]**

**Speaker:**
"While the app is loading, here is exactly what is happening in the background:
1.  **Analysis Phase:** The Planner Agent is breaking down 'Tic Tac Toe' into requirements: a 3x3 grid, click handlers, state management for X and O, and a win checking algorithm.
2.  **Code Generation:** The Orchestrator now spins up the Coding Agents. You can see the logs here [point to logs]—the Frontend Agent is generating the React components and CSS for that 'dark theme' I requested.
3.  **Validation:** Once the code is written, MetaForge runs a syntax check. If there's a missing bracket or an import error, the Self-Healing loop kicks in to fix it without me even knowing.
4.  **Deployment:** Finally, the files are written to a local directory and a hot-reloading preview server starts up."

## 4. Result & Refinement (2:00 - End)
**[Visual: The Tic Tac Toe game appears in the Live Preview iframe]**

**Speaker:**
"And there it is. A fully functional Tic Tac Toe game generated from scratch."

**[Action: Play a few moves to show it works]**

**Speaker:**
"But MetaForge isn't done. I can continue the conversation. Let's say I want to restart the game."

**[Action: Type 'Add a Reset Game button' in the chat box]**

**Speaker:**
"The Refinement Agent takes the existing code, understands the context, and injects just the new functionality. This makes iterative development incredibly fast."

**Speaker:**
"This is MetaForge: turning ideas into software with the power of multi-agent orchestration. Thanks for watching."

---

## Appendix: Alternative Demo Prompts

Since you want the demo to be **fun and interactive**, here are the best "Game" prompts. These are visually engaging and great for showing off real-time interaction:

### Option A: The Classic (Snake Game)
**Why it works:** Everyone knows how it should work, so if it works, it's instantly impressive. It shows off the AI's ability to handle game loops and keyboard events.
- **Initial Prompt:** "Create a classic Snake game using HTML5 Canvas. The snake should move automatically and grow when it eats the red food. Use arrow keys for controls. Display the current score."
- **Refinement:** "Make the game speed up slightly every time the snake eats food to make it harder."

### Option B: The "Brainy" Game (Memory Match)
**Why it works:** Flipping cards is a very satisfying interaction. It demonstrates complex state management (remembering which cards are flipped, checking for matches, resetting if wrong).
- **Initial Prompt:** "Build a Memory Match card game. Create a 4x4 grid of cards. When clicked, cards should flip to reveal an emoji. If two flipped cards match, keep them face up. If not, flip them back after 1 second."
- **Refinement:** "Add a 'Moves Counter' to track how many attempts I've made."

### Option C: The Action Game (Whack-a-Mole)
**Why it works:** Fast-paced and colorful. It proves the app is responsive and not lagging.
- **Initial Prompt:** "Create a Whack-a-Mole style game. Display a 3x3 grid of holes. Every second, a 'mole' (use a brown circle or emoji) should appear in a random hole for a short time. Clicking the mole increases the score."
- **Refinement:** "Add a 30-second countdown timer. Show a 'Game Over' screen with the final score when time runs out."

### Option D: The Skill Test (Typing Racer)
**Why it works:** It requires real-time validation of every keystroke, which makes the "Self-Healing" code validation story even more compelling if it works perfectly.
- **Initial Prompt:** "Create a Typing Speed Test app. Display a random sentence for me to type. Highlight correct characters in green and incorrect ones in red as I type. Show my WPM (Words Per Minute) in real-time."
- **Refinement:** "Add a 'New Sentence' button to generate a different random sentence."
