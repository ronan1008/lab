const mongoose = require("mongoose")
const {Schema} = require("mongoose")
const imagesSchema = new Schema(
    {
        path: {
            type: String,
            required: true,
        },
        thumb_path: {
            type: String
        },
        description: {
            type: String
        }
    },
    {
        timestamps: true
    }
)

module.exports = mongoose.model("Course", imagesSchema)