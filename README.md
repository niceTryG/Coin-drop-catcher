🛒 Wagon Catcher

A 2D arcade-style catching game made with Python and Kivy

Wagon Catcher is a simple yet addictive game where you control a wagon to catch falling food before it hits the ground.
As levels progress, the speed, challenge, and number of falling items increase — testing your focus and reflexes.

🎯 Gameplay

Use the arrow keys to move the wagon left and right.

Catch falling food items to earn points.

Every 20 catches, the game advances to the next level.

Each new level increases:

Falling speed

Number of food items

Allowed misses before Game Over

When you exceed the allowed missed limit, the game ends.

⚙️ Game Mechanics
Element	Description
🎮 Controls	Left / Right Arrow Keys
🍎 Goal	Catch as many food items as possible
💥 Misses	3 misses in Level 1, +1 per level
🧭 Progression	Level increases every 20 catches
🧠 Logic	Miss count resets when a new level starts
🧩 Features

Dynamic difficulty scaling

Smooth player movement

Real-time score, level, and miss tracking

Automatic level progression

Visually appealing grass and background alignment

Fully built with Python (Kivy)

💡 Highlights

Each level feels faster and more challenging

The wagon always stays within the ground zone for realism

Misses reset at level-up, keeping gameplay balanced

Designed for learning game loops, object motion, and collision detection

🧠 What I Learned

Working with Kivy’s Canvas and Clock

Building a game with class-based architecture

Handling keyboard input and movement

Managing UI elements (Labels, Score, Levels, Misses)

Implementing collision detection and physics-like logic

🛠️ Technologies

Python 3

Kivy Framework

▶️ How to Play

Clone or download this repository:

git clone https://github.com/niceTryG/wagon-catcher.git


Install dependencies:

pip install kivy


Run the game:

python main.py
