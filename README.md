# Introduction

Shroom Rush is a relaxing platformer game where players control Finley, a mushroom character, navigating through challenges, collecting coins, and discovering new story elements. Built with Pygame, this game is an escape from reality, providing a cute and fun experience in each level.

# Inspiration

In today’s fast-paced world, people need a light-hearted escape from stress. We created Shroom Rush as a simple, enjoyable game that helps users unwind, with a cute main character, an engaging story, and gentle gameplay designed to provide a mental break from the everyday.

# Features

- **Character Control:** Move left, right, and jump to navigate Finley’s world.
- **Dynamic Obstacle Avoidance:** Time jumps and movements to dodge slimy obstacles.
- **Coin Collection:** Collect coins to boost your score and unlock achievements.
- **Limited Lives & Level Progression:** Start with three lives and reach the end portal to progress.
- **Background Music:** Added immersive background music for enhanced gameplay.
- **Unique Character Dialogues:** Engaging dialogues generated with OpenAI’s API at each level’s end.
- **Custom Maps & Assets:** Designed maps with Tiled and graphics using Adobe Express.
- **High Score Tracking:** Scores stored in MongoDB for future replayability and competition.

# How to run

- **Clone the Repository:**

```python
git clone [<repo_url>](https://github.com/tvirat/NewHacks.git)
```

- **Install Dependencies:**

```python
pip install -r requirements.txt
```

- **Run the Game:**

```python
python game.py
```

# Technical Details

- **Game Engine:** Pygame for core mechanics and character control.
- **Map Design:** Custom levels built using Tiled and loaded with PyTMX.
- **Database:** MongoDB for tracking high scores and storing user data.
- **Dialogues & Story Expansion:** OpenAI’s API for unique in-game character dialogues.
- **Design Tools:** Adobe Express for creating game assets and graphics.

# Future Prospects

- **Web App Deployment:** We plan to host Shroom Rush as a web app on platforms like Vercel, allowing easier access with a public domain.
- **Additional Levels & Story:** Expanding Finley’s journey with more levels and richer story elements.
- **Enhanced User Experience:** User authentication for personalized score tracking and leaderboard integration.
- **Social Features:** Adding leaderboard and community challenges to increase replayability.
