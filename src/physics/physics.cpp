#include "physics.h"

const double GRAVITY = 9.8;
const double TIME_STEP = 0.016;
const double PI = 3.14159265358979323846;
double blockSpeed = 550;

Block::Block(double x, double y, double width, double height)
    : x(x), y(y), width(width), height(height), speed(blockSpeed) {}


void Block::updateFallSpeed() {
    speed = speed + GRAVITY * TIME_STEP; // Update speed based on gravity
    y += speed * TIME_STEP; // Update the position based on speed
}

void Block::setPerfect(bool perfect) { this->perfect = perfect; }

// //Check for collision between two blocks
bool Block::checkCollision(Block& fallingBlock, Block& towerBlock) {
    bool isCollidingX = fallingBlock.x < towerBlock.x + towerBlock.width && 
                        fallingBlock.x + fallingBlock.width > towerBlock.x;

    bool isCollidingY = fallingBlock.y + fallingBlock.height >= towerBlock.y && 
                        fallingBlock.y <= towerBlock.y + towerBlock.height;

    if (isCollidingX && isCollidingY) {
        // Adjust the y position of the falling block to sit directly on top of the tower block
        fallingBlock.y = towerBlock.y - fallingBlock.height;
        return true;
    }
    return false;
}

std::tuple<bool, std::string> Block::isBlockStable(Block& newBlock, const Block& topBlock) {
    // Calculate overlap between the new block and the top block
    double overlapLeft = std::max(newBlock.x, topBlock.x);
    double overlapRight = std::min(newBlock.x + newBlock.width, topBlock.x + topBlock.width);
    double overlapWidth = overlapRight - overlapLeft;

    // Set required overlap as a fraction of the new block’s width (e.g., 60%)
    double requiredOverlap = newBlock.width * 0.6;

    std::string direction;
    newBlock.x < topBlock.x ? direction = "left" : direction = "right";

    if (overlapWidth >= newBlock.width * 0.95) {
        newBlock.setPerfect(true);
    }

    return std::make_tuple(overlapWidth >= requiredOverlap, direction);
}


// Tower methods
Tower::Tower() {
    blocks.push_back(Block(190, 260, 200, 100));// y = 465
    height = 1;
    score = 0;
    blockSpeed = 550;
}
void Tower::addBlock(const Block& block) {
    blocks.push_back(block); // Add the block to the tower
    height++;
    block.perfect ? score+=50 : score+=25;
    blockSpeed += 12;
}

double Tower::getHeight() const {
    double maxHeight = 0;
    for (const auto& block : blocks) {
        double blockTop = block.y + block.height; // Calculate the top position of the block
        if (blockTop > maxHeight) {
            maxHeight = blockTop; // Update the maximum height
        }
    }
    return maxHeight; // Return the total height of the tower
}

Crane::Crane(double x, double y, double length)
    : x(x), y(y), length(length), angle(0), maxAngle(0.7), angularVelocity(2),
      carryingBlockPtr(nullptr), carrying(false) {}

void Crane::update(double deltaTime) {
    angle += angularVelocity * deltaTime;

    if (angle > maxAngle) {
        angle = maxAngle; 
        angularVelocity = -fabs(angularVelocity);
    } else if (angle < -maxAngle) {
        angle = -maxAngle; 
        angularVelocity = fabs(angularVelocity); 
    }

    x_hook = x + length * sin(angle);
    y_hook = y + length * cos(angle);

    if (carrying && carryingBlockPtr != nullptr) {
        updateBlockPosition(carryingBlockPtr);
    }
}

void Crane::modifyVelocityMaxAngle(double velocity, double maxAngle){
    if (this->angularVelocity > 0) this->angularVelocity += velocity;
    else this->angularVelocity -= velocity;
    this->maxAngle += maxAngle;
}


// Method to pick up a block with the crane
void Crane::pickUpBlock(Block* block) {
    if (!carrying) {
        carryingBlockPtr = block;
        carrying = true;
        std::random_device rd; // Seed for the random number generator
        std::mt19937 gen(rd()); // Mersenne Twister random number generator
        std::uniform_real_distribution<double> dis(-maxAngle, maxAngle); // Define the range
        angle = dis(gen);
        updateBlockPosition(block);
    }
}

// Method to drop the carried block
void Crane::dropBlock() {
    if (carrying) {
        carrying = false;
        carryingBlockPtr = nullptr;
        printf("Dropped block at (%f, %f)\n", x_hook, y_hook);
    }
}

// Function to calculate the angle in degrees between two points (x1, y1) and (x2, y2)
double Crane::calculateAngle() {
    // Calculate the differences
    double dx = x_hook - x;
    double dy = y_hook - y;

    // Calculate the angle in radians
    double angle_rad = atan2(dy, dx);

    // Convert radians to degrees
    double angle_deg = angle_rad * (180.0 / M_PI); // M_PI is a constant for π

    return angle_deg; // Return the angle in degrees
}

void Crane::updateBlockPosition(Block* block) {
    if (carrying && block != nullptr) {
        block->x = x_hook - block->width / 2; // Center the block on the hook
        block->y = y_hook; // Align the bottom of the block with the hook
    }
}

