import discord
from discord.ext import commands
import os
import requests
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DOBBY_API_KEY = os.getenv("DOBBY_API_KEY")
DOBBY_API_URL = os.getenv("DOBBY_API_URL")

if not DOBBY_API_KEY or DOBBY_API_KEY == "YOUR_API_KEY_HERE":
    raise Exception("Please set your DOBBY_API_KEY in the .env file!")

# Discord intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# User scores
scores = {}

# Supported quiz topics
TOPICS = ["Python", "Blockchain", "Cybersecurity"]

# Function to call Fireworks API and generate quiz
def generate_quiz(topic):
    headers = {
        "Authorization": f"Bearer {DOBBY_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = (
        f"Generate a single multiple-choice quiz question about {topic}.\n"
        "Rules:\n"
        "1. Only provide the question and 4 options labeled A, B, C, D.\n"
        "2. Provide the correct answer at the end in the format 'Answer: <letter>'.\n"
        "3. Do NOT include explanations, commentary, or placeholders.\n"
        "4. Ensure the question is fully complete and readable.\n"
        "Output ONLY the quiz question, options, and answer."
    )

    data = {
        "model": "accounts/fireworks/models/gpt-oss-20b",
        "prompt": prompt,
        "max_tokens": 200
    }

    try:
        response = requests.post(DOBBY_API_URL, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()["choices"][0]["text"].strip()

            # Remove extra instruction lines if API returns them
            lines = result.splitlines()
            clean_lines = [line for line in lines if not line.lower().startswith("rules") and not line.lower().startswith("the user")]
            question_text = "\n".join(clean_lines)

            if "Answer:" not in question_text:
                question_text = fallback_question(topic)

            return question_text
        else:
            return f"API error {response.status_code}: {response.text}"
    except Exception as e:
        return f"API error: {str(e)}"

# Fallback questions if API fails
def fallback_question(topic):
    if topic == "Python":
        return (
            "Question: Which of the following is the correct way to open a file in Python for reading, ensuring the file is automatically closed after processing?\n"
            "A. file = open('data.txt', 'r'); data = file.read(); file.close()\n"
            "B. with open('data.txt', 'r') as file: data = file.read()\n"
            "C. file = open('data.txt', 'r'); data = file.read();\n"
            "D. with open('data.txt') as file: data = file.read()\n"
            "Answer: B"
        )
    elif topic == "Blockchain":
        return (
            "Question: What is the primary purpose of a hash function in a blockchain?\n"
            "A. To increase the value of coins\n"
            "B. To provide proof of work for miners\n"
            "C. To create a digital fingerprint for each block\n"
            "D. To allow anonymous transactions\n"
            "Answer: C"
        )
    elif topic == "Cybersecurity":
        return (
            "Question: Which of the following is a common type of phishing attack?\n"
            "A. Spear phishing\n"
            "B. Firewall bypass\n"
            "C. SQL injection\n"
            "D. Packet sniffing\n"
            "Answer: A"
        )
    else:
        return "No quiz available for this topic."

# Bot ready
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user} (ID: {bot.user.id})")

# !quiz command
@bot.command(name="quiz")
async def quiz(ctx, *, topic=None):
    if topic is None:
        topic = random.choice(TOPICS)
    elif topic not in TOPICS:
        await ctx.send(f"Invalid topic. Choose one of: {', '.join(TOPICS)}")
        return

    await ctx.send(f"Generating a quiz question about {topic}...")
    question = generate_quiz(topic)
    await ctx.send(f"**Quiz ({topic})**\n{question}")

# !score command
@bot.command(name="score")
async def score(ctx):
    user = str(ctx.author)
    user_score = scores.get(user, 0)
    await ctx.send(f"{ctx.author.mention}, your current score is {user_score}.")

# !answer command
@bot.command(name="answer")
async def answer(ctx, choice: str):
    user = str(ctx.author)
    # Random correctness placeholder; replace later with real answer checking
    if random.choice([True, False]):
        scores[user] = scores.get(user, 0) + 1
        await ctx.send(f"Correct! {ctx.author.mention}, your new score is {scores[user]}.")
    else:
        await ctx.send(f"Incorrect. {ctx.author.mention}, try the next question.")

# Run the bot
bot.run(TOKEN)
