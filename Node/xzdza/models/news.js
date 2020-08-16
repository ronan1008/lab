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
        },
        type:{
            type: String,
            enum : ['最新消息','來年運勢','線上報名','成果發表展'],
            required: true,        
        },
        order: {
            type: Number,
            required: true,
        },
        mark: {
            type: Boolean,
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