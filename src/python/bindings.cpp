#include <pybind11/pybind11.h>
#include <pybind11/stl.h> // For STL support
#include "physics.h"

namespace py = pybind11;

PYBIND11_MODULE(physics, m) {
    py::class_<Block>(m, "Block")
        .def(py::init<double, double, double, double>(), // Constructor
             py::arg("x"), py::arg("y"), py::arg("width"), py::arg("height"))
        .def("updateFallSpeed", &Block::updateFallSpeed) // Update fall speed
        .def_readwrite("x", &Block::x) // Expose x
        .def_readwrite("y", &Block::y) // Expose y
        .def_readwrite("width", &Block::width) // Expose width
        .def_readwrite("height", &Block::height) // Expose height
        .def_readwrite("speed", &Block::speed) // Expose speed
        .def_readonly("perfect", &Block::perfect) // Expose perfect
        .def_static("checkCollision", &Block::checkCollision) // Static collision check
        .def("isBlockStable", &Block::isBlockStable);

    py::class_<Tower>(m, "Tower")
        .def(py::init<>()) // Constructor
        .def_readonly("blocks", &Tower::blocks) // Expose blocks
        .def_readonly("height", &Tower::height) // Expose height
        .def_readonly("score", &Tower::score) // Expose score
        .def("addBlock", &Tower::addBlock, py::arg("block")) // Add a block to the tower
        .def("getHeight", &Tower::getHeight); // Get the height of the tower

    py::class_<Crane>(m, "Crane")
        .def(py::init<double ,double, double>(), // Constructor
            py::arg("x"), py::arg("y"), py::arg("length"))
        .def_readwrite("x", &Crane::x) // Expose x
        .def_readwrite("y", &Crane::y) // Expose y
        .def_readwrite("x_hook", &Crane::x_hook) // Expose x_hook
        .def_readwrite("y_hook", &Crane::y_hook) // Expose y_hook
        .def_readwrite("angle", &Crane::angle) // Expose angle
        .def_readwrite("maxAngle", &Crane::maxAngle) // Expose max angle
        .def_readwrite("angularVelocity", &Crane::angularVelocity) // Expose angular velocity
        .def_readwrite("length", &Crane::length) // Expose length
        .def_readwrite("carrying", &Crane::carrying) // Expose carrying
        .def("update", &Crane::update, py::arg("deltaTime")) // Update the crane state
        .def("pickUpBlock", &Crane::pickUpBlock)
        .def("dropBlock", &Crane::dropBlock)
        .def("calculateAngle", &Crane::calculateAngle)
        .def("updateBlockPosition", &Crane::updateBlockPosition, py::arg("block"))
        .def("modifyVelocityMaxAngle", &Crane::modifyVelocityMaxAngle, py::arg("velocity"), py::arg("maxAngle"));
}
