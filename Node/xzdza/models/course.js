const mongoose = require("mongoose")
const {Schema} = require("mongoose")
const coursesSchema = new Schema(
    {
        grade: {
            type: String,
            required: true,
        },
        title: {
            type: String,
            required: true,
        },
        description: {
            type: String,
        },
/*
        registeredStudents: {
            type: Number,
            default: 0,
            min: [0,"Course cannot have negative number of students"]
        },
*/
        maxStudents: {
            type: Number,
            default: 0,
            min: [0,"Course cannot have negative number of students"]
        },
        startTime: {
            type: Date,
        },
        endTime: {
            type: Date,
        },
    },
    {
        timestamps: true
    }
)

userSchema.virtual("fullTitle").get( function (){
    return `${this.grade} ${this.title}`
})

module.exports = mongoose.model("Course", coursesSchema)