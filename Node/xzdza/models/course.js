const mongoose = require("mongoose")
const {Schema} = require("mongoose")
const coursesSchema = new Schema(
    {
        title: {
            type: String,
            required: true,
            unique: true
        },
        description: {
            type: String,
            required: true
        },
        maxStudents: {
            type: Number,
            default: 0,
            min: [0,"Course cannot have negative number of students"]
        },
        cost: {
            type: Number,
            default: 0,
            min: [0, "Course cannot have a negative cost"]
        }
    },
    {
        timestamps: true
    }
)

module.exports = mongoose.model("Course", coursesSchema)