const mongoose = require("mongoose")
const { Schema } = mongoose

var newsSchema = new Schema(
    {
        title:{
            type: String,
            required: true,
            trim: true
        },
        description: {
            type: String,
            required: true,
            lowercase: true,
            trim: true,
            unique: true
        },
        order: {
            type: Number,
            required: true,
        },
        startTime: {
            type: Date,
            required: true,
        },
        endTime: {
            type: Date,
            required: true,
        },
    },
    {
        timestamps: true
    }
)

module.exports = mongoose.model("News", newsSchema)