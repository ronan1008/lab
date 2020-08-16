const mongoose = require("mongoose")
const {Schema} = require("mongoose")
const imagesSchema = new Schema(
    {
        path: {
            type: String,
            required: true,
        },
        description: {
            type: String
        }
    },
    {
        timestamps: true
    }
)

module.exports = mongoose.model("Image", imagesSchema)