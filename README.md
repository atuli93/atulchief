# Quiz Bot

A Discord Quiz Bot that generates multiple-choice questions on topics like Python, Blockchain, Cybersecurity, and more. Track your score and challenge yourself or friends!

---

## Features
- Generate quizzes on Python, Blockchain, Cybersecurity, etc.
- Multiple-choice questions with four options (A–D)
- Track your score in real-time
- Easy to extend with new topics
- Simple human-friendly responses

---

## Setup

1. **Clone the repository**
```bash
git clone https://github.com/atuli93/atulchief.git
cd atulchief
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create ```.env``` file in project root:**
```bash
DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN
DOBBY_API_KEY=YOUR_API_KEY_HERE
DOBBY_API_URL=https://api.fireworks.ai/inference/dobby-70b
```

5. **Run the Bot**
```bash
python bot.py
```

# Commands

```!quiz <topic>``` → Generates a quiz question for the given topic
Example: ```!quiz Python```

```!answer <option>``` → Answer the current quiz question
Example: ```!answer B```

```!score``` → Check your current score


# Example
## Bot asking a question:
```bash
Quiz (Python)
Question: Which built-in Python function is used to convert a string to lowercase?
A) uppercase()
B) lower()
C) casefold()
D) toLower()
Answer: B
```

## Contributing
**Feel free to add new topics or improve question handling.**

# License
## MIT License
