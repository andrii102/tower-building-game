# 🏗️ Tower Building Game

A simple Tower Building game implemented in **C++** with a **Python interface** using **Pybind11**. This project demonstrates how to connect performant C++ game logic with the flexibility of Python using Pybind11.

## 🕹️ Gameplay

In this game, players aim to stack blocks as precisely as possible to build the tallest tower. Each block moves horizontally, and the player must drop it at the right moment to align it with the previous one. Poor alignment causes parts of the block to fall off, making the next block smaller and increasing the challenge. The game ends when no more blocks can be stacked.

Try to reach the highest score by perfectly timing your drops!

## 🔧 Features

- Core game mechanics written in C++
- Exposed to Python using Pybind11
- Easy to extend and integrate with Python UI
- Lightweight and fast

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- CMake
- C++ compiler
- Pybind11

### Build Instructions

To create the module:

```bash
mkdir build
cd build
cmake ..
cmake --build .
```

Move the `assets` directory to the `build` folder:

```bash
mv ../assets .
```

You're set! 🎮
