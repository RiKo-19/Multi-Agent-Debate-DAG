# Multi-Agent Debate DAG using LangGraph

This project implements a **debate simulation system** using **LangGraph** where two AI agents — a **Scientist** and a **Philosopher** — engage in a structured debate on a user-provided topic. The system manages memory, enforces turn-taking, prevents repeated arguments, and ends with a **Judge node** that summarizes the debate and declares a winner.

---

## ⚙️ Features

* **Two Personas**: Scientist (logic/evidence) vs Philosopher (ethics/reasoning)
* **Structured 8-Round Debate**: Each agent gets 4 turns
* **MemoryNode**: Keeps a structured summary of debate progress
* **Validation**: Ensures correct turn-taking and no repeated arguments
* **JudgeNode**: Summarizes debate, declares winner with justification
* **CLI Interface**: Topic entered at runtime, results printed to console
* **Logging**: All debate steps recorded in `debate.log`
* **DAG Diagram**: Debate flow saved as a `.dot` file for visualization later create a `.png` file

---

## 🛠️  Installation & Setup

1. **Clone repository** or extract files from submission.

2. **Create virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   or manually install:

   ```bash
   pip install langgraph langchain-openai python-dotenv graphviz
   ```

4. **Set environment variables:**
   Create a `.env` file in the project root:

   ```ini
   OPENROUTER_API_KEY=your_api_key_here
   OPENAI_API_BASE=https://openrouter.ai/api/v1
   ```

---

## ▶️ Running the Program

Run the debate system via CLI:

```bash
python debate.py
```

You will be prompted:

```
Enter topic for debate: Should death be accepted as natural, or should humans pursue immortality?
```

The debate will run for **8 rounds** and end with a Judge’s summary and decision.

---

## 💻 Usage Example
```
Enter topic for debate: is space exploration worth the cost?
Starting debate between Scientist and Philosopher on: s space exploration worth the cost?

--- Round 1 ---
[Round 1] Scientist: Space exploration is worth the cost because it leads to technological advancements that benefit society as a whole, such as satellite technology, medical advancements, and environmental monitoring systems.
--- Round 2 ---
[Round 2] Philosopher: While addressing pressing issues on Earth is important, investing in space exploration has the potential to lead to long-term benefits and advancements that can ultimately benefit all of humanity, both on Earth and beyond. It is crucial to balance immediate needs with long-term goals for the betterment of society.
--- Round 3 ---
[Round 3] Scientist: Furthermore, the knowledge gained from space exploration can also lead to new scientific discoveries and innovations that can drive economic growth and create new industries, ultimately benefiting society in the long run.
--- Round 4 ---
[Round 4] Philosopher: While the potential benefits of space exploration are undeniable, the cost of such endeavors must also be weighed against the pressing needs of society, such as poverty, healthcare, education, and environmental sustainability. Prioritizing resources towards addressing these issues may have a more immediate and tangible impact on improving the lives of individuals on Earth.
--- Round 5 ---
[Round 5] Scientist: Space exploration has led to numerous technological advancements, such as satellite technology, GPS, and medical innovations, that have greatly benefited society. Investing in space exploration not only drives innovation but also inspires future generations to pursue careers in STEM fields, ultimately benefiting society in the long run.
--- Round 6 ---
[Round 6] Philosopher: As a philosopher, I believe that we must prioritize addressing pressing issues on Earth, such as poverty, healthcare, and environmental sustainability, before investing in space exploration. We must consider the ethical implications of allocating resources to space exploration when there are urgent needs that require attention here on Earth.
--- Round 7 ---
[Round 7] Scientist: As a Scientist, I believe that space exploration is worth the cost because it has led to numerous technological advancements that have benefited society in countless ways, from satellite technology to medical innovations. The knowledge gained from exploring space has also expanded our understanding of the universe and our place within it, sparking curiosity and inspiring future generations to pursue careers in science and technology.
--- Round 8 ---
[Round 8] Philosopher: As a Philosopher, I believe that the exploration of space can provide a unique perspective on the human experience and our place in the universe. However, we must also consider the opportunity cost of investing in space exploration when there are urgent needs to be addressed here on Earth.       

[Judge] Reviewing debate...
1. The debate centers around whether space exploration is worth the cost, with the Scientist arguing that the technological advancements and economic benefits justify the investment, while the Philosopher emphasizes the importance of addressing pressing issues on Earth before prioritizing space exploration.

2. Winner: Scientist

3. The Scientist makes a compelling argument by highlighting the tangible benefits of space exploration, such as technological advancements, economic growth, and inspiring future generations. They also emphasize the importance of gaining knowledge about the universe and our place within it. While the Philosopher raises valid points about the ethical implications and opportunity cost of investing in space exploration, the concrete benefits presented by the Scientist make a stronger case for the value of space exploration.

 DAG diagram saved as dag_diagram.dot
```

---

## 🧠 Example Topics to Test

* Should AI be regulated like medicine?
* Is space exploration worth the cost?
* Can machines ever be conscious?
* Should humans edit the genes of unborn children?
* Is morality objective or subjective?

---

## 🗺️ Diagram

<img width="376" height="673" alt="Image" src="https://github.com/user-attachments/assets/55e2d7a6-7efb-434c-8eff-f6c438760d94" />
