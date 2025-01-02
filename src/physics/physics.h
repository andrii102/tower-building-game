#ifndef PHYSICS_H
#define PHYSICS_H
#define _USE_MATH_DEFINES

#include <string>
#include <tuple>
#include <vector>
#include <cmath>
#include <random>

class Block {
public:
    double x;       
    double y;       
    double width;   
    double height;  
    double speed;   // Falling speed of the block
    bool perfect = false;

    Block(double x, double y, double width, double height);
    void updateFallSpeed();

    // Static methods for collision and placement
    static bool checkCollision(Block& fallingBlock, Block& towerBlock);
    std::tuple<bool, std::string> isBlockStable(Block& newBlock, const Block& topBlock);
    void setPerfect(bool perfect);
};

class Tower {
public:
    Tower();

    std::vector<Block> blocks;
    int height;
    int score;
    void addBlock(const Block& block);
    double getHeight() const; 
};

class Crane {
public:
    double x;
    double y;          
    double x_hook;
    double y_hook;
    double length;
    double angle;  // Current angle in radians
    double maxAngle;
    double angularVelocity;  // Current angular velocity
    Block* carryingBlockPtr = nullptr; // Pointer to the block being carried
    bool carrying = false;

    Crane(double x, double y, double length);
    void update(double deltaTime); // Update crane position
    void pickUpBlock(Block* block);
    void dropBlock();
    double calculateAngle();
    void updateBlockPosition(Block* block);
    void modifyVelocityMaxAngle(double velocity, double maxAngle);
};

#endif
